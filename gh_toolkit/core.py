"""
gh_toolkit.core - Core GH_IO binary and XML parsing engine for Grasshopper definitions.

Zero external dependencies: uses Python standard library zlib, struct, xml.etree, uuid.
"""

import os
import sys
import zlib
import struct
import uuid
import base64
import json
import xml.etree.ElementTree as ET
from typing import List, Dict, Any, Optional, Tuple, Union

# ==============================================================================
# GH_IO Type System Constants
# ==============================================================================

TYPE_MAP = {
    0: ("unset", None),
    1: ("gh_bool", "bool"),
    2: ("gh_byte", "byte"),
    3: ("gh_int32", "int32"),
    4: ("gh_int64", "int64"),
    5: ("gh_single", "single"),
    6: ("gh_double", "double"),
    7: ("gh_decimal", "decimal"),
    8: ("gh_date", "date"),
    9: ("gh_guid", "guid"),
    10: ("gh_string", "string"),
    20: ("gh_bytearray", "bytearray"),
    21: ("gh_doublearray", "doublearray"),
    30: ("gh_drawing_point", "point"),
    31: ("gh_drawing_pointf", "pointf"),
    32: ("gh_drawing_size", "size"),
    33: ("gh_drawing_sizef", "sizef"),
    34: ("gh_drawing_rectangle", "rect"),
    35: ("gh_drawing_rectanglef", "rectf"),
    36: ("gh_drawing_color", "color"),
    37: ("gh_drawing_bitmap", "bitmap"),
    50: ("gh_point2d", "pt2d"),
    51: ("gh_point3d", "pt3d"),
    52: ("gh_point4d", "pt4d"),
    60: ("gh_interval1d", "interval1d"),
    61: ("gh_interval2d", "interval2d"),
    70: ("gh_line", "line"),
    71: ("gh_boundingbox", "box"),
    72: ("gh_plane", "plane"),
    80: ("gh_version", "version"),
}

NAME_TO_TYPE = {v[0]: k for k, v in TYPE_MAP.items()}


# ==============================================================================
# Data Models: GHItem & GHChunk
# ==============================================================================

class GHItem:
    """Represents a strongly-typed data item in a Grasshopper archive."""

    def __init__(self, name: str, type_code: int, value: Any, index: int = -1):
        self.name = name
        self.type_code = type_code
        self.type_name = TYPE_MAP.get(type_code, ("unknown", None))[0]
        self.value = value
        self.index = index

    def to_dict(self) -> Dict[str, Any]:
        val = self.value
        if isinstance(val, bytes):
            val = base64.b64encode(val).decode("ascii")
        return {
            "name": self.name,
            "type_code": self.type_code,
            "type_name": self.type_name,
            "index": self.index,
            "value": val,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "GHItem":
        tc = d["type_code"]
        val = d["value"]
        if tc in (20, 37) and isinstance(val, str):
            val = base64.b64decode(val)
        return cls(d["name"], tc, val, d.get("index", -1))


class GHChunk:
    """Represents a hierarchical node (chunk) containing items and child chunks."""

    def __init__(self, name: str, index: int = -1):
        self.name = name
        self.index = index
        self.items: List[GHItem] = []
        self.chunks: List["GHChunk"] = []

    def add_item(self, name: str, type_code: int, value: Any, index: int = -1) -> GHItem:
        item = GHItem(name, type_code, value, index)
        self.items.append(item)
        return item

    def find_item(self, name: str) -> Optional[GHItem]:
        for it in self.items:
            if it.name == name:
                return it
        return None

    def get_value(self, name: str, default: Any = None) -> Any:
        it = self.find_item(name)
        return it.value if it else default

    def add_chunk(self, chunk: "GHChunk") -> "GHChunk":
        self.chunks.append(chunk)
        return chunk

    def create_chunk(self, name: str, index: int = -1) -> "GHChunk":
        c = GHChunk(name, index)
        self.chunks.append(c)
        return c

    def find_chunk(self, name: str) -> Optional["GHChunk"]:
        for ch in self.chunks:
            if ch.name == name:
                return ch
        return None

    def find_chunks(self, name: str) -> List["GHChunk"]:
        return [ch for ch in self.chunks if ch.name == name]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "index": self.index,
            "items": [it.to_dict() for it in self.items],
            "chunks": [ch.to_dict() for ch in self.chunks],
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "GHChunk":
        c = cls(d["name"], d.get("index", -1))
        for it in d.get("items", []):
            c.items.append(GHItem.from_dict(it))
        for ch in d.get("chunks", []):
            c.chunks.append(cls.from_dict(ch))
        return c


class GHArchive:
    """Root container for a serialized Grasshopper document."""

    def __init__(self):
        self.root = GHChunk("Root")

    def to_dict(self) -> Dict[str, Any]:
        return {"Archive": self.root.to_dict()}

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "GHArchive":
        a = cls()
        a.root = GHChunk.from_dict(d["Archive"])
        return a


# ==============================================================================
# Binary Serialization & Decompression Engine
# ==============================================================================

class BinaryBuffer:
    def __init__(self, data: bytes):
        self.data = data
        self.pos = 0

    def read_bytes(self, n: int) -> bytes:
        if self.pos + n > len(self.data):
            raise EOFError("Unexpected end of binary stream")
        res = self.data[self.pos : self.pos + n]
        self.pos += n
        return res

    def read_int32(self) -> int:
        return struct.unpack("<i", self.read_bytes(4))[0]

    def read_int64(self) -> int:
        return struct.unpack("<q", self.read_bytes(8))[0]

    def read_single(self) -> float:
        return struct.unpack("<f", self.read_bytes(4))[0]

    def read_double(self) -> float:
        return struct.unpack("<d", self.read_bytes(8))[0]

    def read_bool(self) -> bool:
        return bool(self.read_bytes(1)[0])

    def read_byte(self) -> int:
        return self.read_bytes(1)[0]

    def read_7bit_encoded_int(self) -> int:
        res = 0
        shift = 0
        while True:
            b = self.read_byte()
            res |= (b & 0x7F) << shift
            if not (b & 0x80):
                break
            shift += 7
        return res

    def read_string(self) -> str:
        length = self.read_7bit_encoded_int()
        if length == 0:
            return ""
        raw = self.read_bytes(length)
        return raw.decode("utf-8", errors="replace")

    def read_guid(self) -> str:
        raw = self.read_bytes(16)
        return str(uuid.UUID(bytes_le=raw))


def write_7bit_encoded_int(val: int) -> bytes:
    buf = bytearray()
    while val >= 0x80:
        buf.append((val & 0x7F) | 0x80)
        val >>= 7
    buf.append(val & 0x7F)
    return bytes(buf)


def write_string(val: str) -> bytes:
    encoded = val.encode("utf-8")
    return write_7bit_encoded_int(len(encoded)) + encoded


def read_item_value(buf: BinaryBuffer, type_code: int) -> Any:
    if type_code == 1:
        return buf.read_bool()
    elif type_code == 2:
        return buf.read_byte()
    elif type_code == 3:
        return buf.read_int32()
    elif type_code == 4:
        return buf.read_int64()
    elif type_code == 5:
        return buf.read_single()
    elif type_code == 6:
        return buf.read_double()
    elif type_code == 7:
        raw = buf.read_bytes(16)
        return raw.hex()
    elif type_code == 8:
        return buf.read_int64()
    elif type_code == 9:
        return buf.read_guid()
    elif type_code == 10:
        return buf.read_string()
    elif type_code in (20, 37):
        length = buf.read_int32()
        return buf.read_bytes(length)
    elif type_code == 21:
        count = buf.read_int32()
        return [buf.read_double() for _ in range(count)]
    elif type_code == 30:
        return (buf.read_int32(), buf.read_int32())
    elif type_code == 31:
        return (buf.read_single(), buf.read_single())
    elif type_code == 32:
        return (buf.read_int32(), buf.read_int32())
    elif type_code == 33:
        return (buf.read_single(), buf.read_single())
    elif type_code == 34:
        return (buf.read_int32(), buf.read_int32(), buf.read_int32(), buf.read_int32())
    elif type_code == 35:
        return (buf.read_single(), buf.read_single(), buf.read_single(), buf.read_single())
    elif type_code == 36:
        return (buf.read_byte(), buf.read_byte(), buf.read_byte(), buf.read_byte())
    elif type_code == 50:
        return (buf.read_double(), buf.read_double())
    elif type_code == 51:
        return (buf.read_double(), buf.read_double(), buf.read_double())
    elif type_code == 52:
        return (buf.read_double(), buf.read_double(), buf.read_double(), buf.read_double())
    elif type_code == 60:
        return (buf.read_double(), buf.read_double())
    elif type_code == 61:
        return (buf.read_double(), buf.read_double(), buf.read_double(), buf.read_double())
    elif type_code == 70:
        return (
            (buf.read_double(), buf.read_double(), buf.read_double()),
            (buf.read_double(), buf.read_double(), buf.read_double()),
        )
    elif type_code == 71:
        return (
            (buf.read_double(), buf.read_double()),
            (buf.read_double(), buf.read_double()),
            (buf.read_double(), buf.read_double()),
        )
    elif type_code == 72:
        return {
            "origin": (buf.read_double(), buf.read_double(), buf.read_double()),
            "xaxis": (buf.read_double(), buf.read_double(), buf.read_double()),
            "yaxis": (buf.read_double(), buf.read_double(), buf.read_double()),
            "zaxis": (buf.read_double(), buf.read_double(), buf.read_double()),
        }
    elif type_code == 80:
        return (buf.read_int32(), buf.read_int32(), buf.read_int32())
    else:
        raise ValueError(f"Unknown GH_IO type code: {type_code}")


def serialize_item_value(type_code: int, value: Any) -> bytes:
    if type_code == 1:
        return struct.pack("<?", bool(value))
    elif type_code == 2:
        return struct.pack("<B", int(value))
    elif type_code == 3:
        return struct.pack("<i", int(value))
    elif type_code == 4:
        return struct.pack("<q", int(value))
    elif type_code == 5:
        return struct.pack("<f", float(value))
    elif type_code == 6:
        return struct.pack("<d", float(value))
    elif type_code == 7:
        if isinstance(value, str):
            return bytes.fromhex(value)
        return b"\x00" * 16
    elif type_code == 8:
        return struct.pack("<q", int(value))
    elif type_code == 9:
        u = uuid.UUID(value) if isinstance(value, str) else value
        return u.bytes_le
    elif type_code == 10:
        return write_string(str(value))
    elif type_code in (20, 37):
        raw = value if isinstance(value, (bytes, bytearray)) else b""
        return struct.pack("<i", len(raw)) + raw
    elif type_code == 21:
        return struct.pack("<i", len(value)) + b"".join(struct.pack("<d", float(v)) for v in value)
    elif type_code in (30, 32):
        return struct.pack("<ii", int(value[0]), int(value[1]))
    elif type_code in (31, 33):
        return struct.pack("<ff", float(value[0]), float(value[1]))
    elif type_code == 34:
        return struct.pack("<iiii", int(value[0]), int(value[1]), int(value[2]), int(value[3]))
    elif type_code == 35:
        return struct.pack("<ffff", float(value[0]), float(value[1]), float(value[2]), float(value[3]))
    elif type_code == 36:
        return struct.pack("<BBBB", int(value[0]), int(value[1]), int(value[2]), int(value[3]))
    elif type_code == 50:
        return struct.pack("<dd", float(value[0]), float(value[1]))
    elif type_code == 51:
        return struct.pack("<ddd", float(value[0]), float(value[1]), float(value[2]))
    elif type_code == 52:
        return struct.pack("<dddd", float(value[0]), float(value[1]), float(value[2]), float(value[3]))
    elif type_code == 60:
        return struct.pack("<dd", float(value[0]), float(value[1]))
    elif type_code == 61:
        return struct.pack("<dddd", float(value[0]), float(value[1]), float(value[2]), float(value[3]))
    elif type_code == 70:
        return struct.pack("<dddddd", float(value[0][0]), float(value[0][1]), float(value[0][2]),
                           float(value[1][0]), float(value[1][1]), float(value[1][2]))
    elif type_code == 71:
        return struct.pack("<dddddd", float(value[0][0]), float(value[0][1]), float(value[1][0]),
                           float(value[1][1]), float(value[2][0]), float(value[2][1]))
    elif type_code == 72:
        o = value["origin"]
        x = value["xaxis"]
        y = value["yaxis"]
        z = value["zaxis"]
        return struct.pack("<dddddddddddd", float(o[0]), float(o[1]), float(o[2]),
                           float(x[0]), float(x[1]), float(x[2]),
                           float(y[0]), float(y[1]), float(y[2]),
                           float(z[0]), float(z[1]), float(z[2]))
    elif type_code == 80:
        return struct.pack("<iii", int(value[0]), int(value[1]), int(value[2]))
    else:
        raise ValueError(f"Unsupported serialization type code: {type_code}")


def read_chunk_binary(buf: BinaryBuffer) -> GHChunk:
    name = buf.read_string()
    index = buf.read_int32()
    item_count = buf.read_int32()
    chunk_count = buf.read_int32()

    chunk = GHChunk(name, index)

    for _ in range(item_count):
        it_name = buf.read_string()
        it_index = buf.read_int32()
        it_type = buf.read_int32()
        it_val = read_item_value(buf, it_type)
        chunk.add_item(it_name, it_type, it_val, it_index)

    for _ in range(chunk_count):
        child = read_chunk_binary(buf)
        chunk.add_chunk(child)

    return chunk


def serialize_chunk_binary(chunk: GHChunk) -> bytes:
    out = bytearray()
    out.extend(write_string(chunk.name))
    out.extend(struct.pack("<i", chunk.index))
    out.extend(struct.pack("<i", len(chunk.items)))
    out.extend(struct.pack("<i", len(chunk.chunks)))

    for item in chunk.items:
        out.extend(write_string(item.name))
        out.extend(struct.pack("<i", item.index))
        out.extend(struct.pack("<i", item.type_code))
        out.extend(serialize_item_value(item.type_code, item.value))

    for child in chunk.chunks:
        out.extend(serialize_chunk_binary(child))

    return bytes(out)


def read_gh_binary(path_or_data: Union[str, bytes]) -> GHArchive:
    """Read binary .gh Grasshopper file using zero-external-dependency raw DEFLATE."""
    if isinstance(path_or_data, str):
        with open(path_or_data, "rb") as f:
            raw = f.read()
    else:
        raw = path_or_data

    try:
        decompressed = zlib.decompress(raw, -15)
    except Exception:
        decompressed = raw

    buf = BinaryBuffer(decompressed)
    archive = GHArchive()
    archive.root = read_chunk_binary(buf)
    return archive


def write_gh_binary(archive: GHArchive, path: str, compress: bool = True):
    """Write binary .gh Grasshopper file using standard raw DEFLATE compression."""
    serialized = serialize_chunk_binary(archive.root)
    if compress:
        comp = zlib.compressobj(level=9, method=zlib.DEFLATED, wbits=-15)
        out_data = comp.compress(serialized) + comp.flush()
    else:
        out_data = serialized

    with open(path, "wb") as f:
        f.write(out_data)


# ==============================================================================
# XML (.ghx) Parser & Serializer
# ==============================================================================

def parse_xml_item(elem: ET.Element) -> GHItem:
    name = elem.get("name", "")
    type_code = int(elem.get("type_code", "0"))
    idx = int(elem.get("index", "-1"))
    text = (elem.text or "").strip()

    if type_code == 1:
        val = text.lower() == "true"
    elif type_code in (2, 3, 4):
        val = int(text) if text else 0
    elif type_code in (5, 6):
        val = float(text) if text else 0.0
    elif type_code == 9:
        val = text
    elif type_code == 10:
        val = elem.text or ""
    elif type_code in (20, 37):
        val = base64.b64decode(text) if text else b""
    elif type_code == 30 or type_code == 31:
        x_el = elem.find("X")
        y_el = elem.find("Y")
        val = (float(x_el.text) if x_el is not None else 0.0, float(y_el.text) if y_el is not None else 0.0)
    elif type_code == 34 or type_code == 35:
        x_el = elem.find("X")
        y_el = elem.find("Y")
        w_el = elem.find("W")
        h_el = elem.find("H")
        val = (
            float(x_el.text) if x_el is not None else 0.0,
            float(y_el.text) if y_el is not None else 0.0,
            float(w_el.text) if w_el is not None else 0.0,
            float(h_el.text) if h_el is not None else 0.0,
        )
    elif type_code == 36:
        argb_el = elem.find("ARGB")
        if argb_el is not None and argb_el.text:
            parts = [int(p) for p in argb_el.text.split(";")]
            val = tuple(parts)
        else:
            val = (255, 0, 0, 0)
    elif type_code == 80:
        maj = int(elem.find("Major").text) if elem.find("Major") is not None else 0
        min_v = int(elem.find("Minor").text) if elem.find("Minor") is not None else 0
        rev = int(elem.find("Revision").text) if elem.find("Revision") is not None else 0
        val = (maj, min_v, rev)
    else:
        val = text

    return GHItem(name, type_code, val, idx)


def parse_xml_chunk(elem: ET.Element) -> GHChunk:
    name = elem.get("name", "")
    idx = int(elem.get("index", "-1"))
    chunk = GHChunk(name, idx)

    items_container = elem.find("items")
    if items_container is not None:
        for it_el in items_container.findall("item"):
            chunk.items.append(parse_xml_item(it_el))

    chunks_container = elem.find("chunks")
    if chunks_container is not None:
        for ch_el in chunks_container.findall("chunk"):
            chunk.chunks.append(parse_xml_chunk(ch_el))

    return chunk


def read_ghx(path_or_xml: str) -> GHArchive:
    """Read XML-based .ghx Grasshopper file."""
    if os.path.exists(path_or_xml):
        tree = ET.parse(path_or_xml)
        root_el = tree.getroot()
    else:
        root_el = ET.fromstring(path_or_xml)

    archive = GHArchive()
    if root_el.tag == "Archive":
        archive.root.name = root_el.get("name", "Root")
        items_c = root_el.find("items")
        if items_c is not None:
            for it in items_c.findall("item"):
                archive.root.items.append(parse_xml_item(it))
        chunks_c = root_el.find("chunks")
        if chunks_c is not None:
            for ch in chunks_c.findall("chunk"):
                archive.root.chunks.append(parse_xml_chunk(ch))
    return archive


def chunk_to_xml_elem(chunk: GHChunk, tag_name: str = "chunk") -> ET.Element:
    el = ET.Element(tag_name)
    el.set("name", chunk.name)
    if chunk.index >= 0:
        el.set("index", str(chunk.index))

    if chunk.items:
        items_el = ET.SubElement(el, "items")
        items_el.set("count", str(len(chunk.items)))
        for it in chunk.items:
            it_el = ET.SubElement(items_el, "item")
            it_el.set("name", it.name)
            it_el.set("type_name", it.type_name)
            it_el.set("type_code", str(it.type_code))
            if it.index >= 0:
                it_el.set("index", str(it.index))

            if it.type_code == 1:
                it_el.text = "true" if it.value else "false"
            elif it.type_code in (2, 3, 4, 5, 6, 8, 9, 10):
                it_el.text = str(it.value)
            elif it.type_code in (20, 37):
                it_el.text = base64.b64encode(it.value).decode("ascii") if isinstance(it.value, bytes) else ""
            elif it.type_code in (30, 31):
                ET.SubElement(it_el, "X").text = str(it.value[0])
                ET.SubElement(it_el, "Y").text = str(it.value[1])
            elif it.type_code in (34, 35):
                ET.SubElement(it_el, "X").text = str(it.value[0])
                ET.SubElement(it_el, "Y").text = str(it.value[1])
                ET.SubElement(it_el, "W").text = str(it.value[2])
                ET.SubElement(it_el, "H").text = str(it.value[3])
            elif it.type_code == 36:
                argb = it_el.makeelement("ARGB", {})
                argb.text = f"{it.value[0]};{it.value[1]};{it.value[2]};{it.value[3]}"
                it_el.append(argb)
            elif it.type_code == 80:
                ET.SubElement(it_el, "Major").text = str(it.value[0])
                ET.SubElement(it_el, "Minor").text = str(it.value[1])
                ET.SubElement(it_el, "Revision").text = str(it.value[2])
            else:
                it_el.text = str(it.value)

    if chunk.chunks:
        chunks_el = ET.SubElement(el, "chunks")
        chunks_el.set("count", str(len(chunk.chunks)))
        for ch in chunk.chunks:
            chunks_el.append(chunk_to_xml_elem(ch, "chunk"))

    return el


def write_ghx(archive: GHArchive, path: str):
    """Write XML-based .ghx Grasshopper file."""
    root_el = chunk_to_xml_elem(archive.root, "Archive")
    tree = ET.ElementTree(root_el)
    ET.indent(tree, space="  ", level=0)
    with open(path, "wb") as f:
        f.write(b'<?xml version="1.0" encoding="utf-8" standalone="yes"?>\n')
        tree.write(f, encoding="utf-8", xml_declaration=False)


# ==============================================================================
# Graph Intermediate Representation (GHGraph)
# ==============================================================================

class GHComponent:
    def __init__(self, name: str, nickname: str, comp_id: str, guid: str = ""):
        self.name = name
        self.nickname = nickname
        self.comp_id = comp_id
        self.guid = guid
        self.pivot = (0.0, 0.0)
        self.inputs: List[Dict[str, Any]] = []
        self.outputs: List[Dict[str, Any]] = []
        self.script_source: Optional[str] = None
        self.properties: Dict[str, Any] = {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "nickname": self.nickname,
            "id": self.comp_id,
            "guid": self.guid,
            "pivot": self.pivot,
            "inputs": self.inputs,
            "outputs": self.outputs,
            "script_source": self.script_source,
            "properties": self.properties,
        }


class GHGraph:
    def __init__(self, name: str = "GrasshopperGraph"):
        self.name = name
        self.components: List[GHComponent] = []
        self.wires: List[Dict[str, str]] = []

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(
            {
                "name": self.name,
                "components": [c.to_dict() for c in self.components],
                "wires": self.wires,
            },
            indent=indent,
        )

    @classmethod
    def from_archive(cls, archive: GHArchive) -> "GHGraph":
        graph = cls()
        defn = archive.root.find_chunk("Definition")
        if not defn:
            return graph

        props = defn.find_chunk("DefinitionProperties")
        if props:
            graph.name = props.get_value("Name", "Untitled")

        objects = defn.find_chunk("DefinitionObjects")
        if not objects:
            return graph

        param_map = {}

        for obj in objects.chunks:
            guid = obj.get_value("GUID", "")
            name = obj.get_value("Name", "Unknown")
            cont = obj.find_chunk("Container")
            if not cont:
                continue

            inst_guid = cont.get_value("InstanceGuid", str(uuid.uuid4()))
            nickname = cont.get_value("NickName", "")
            comp_id = f"c_{inst_guid[:8]}"

            comp = GHComponent(name, nickname, comp_id, guid=guid)

            attr = cont.find_chunk("Attributes")
            if attr:
                pivot = attr.get_value("Pivot", (0.0, 0.0))
                comp.pivot = pivot

            pdata = cont.find_chunk("ParameterData")
            containers = [cont]
            if pdata:
                containers.append(pdata)

            for c_node in containers:
                for p_chunk in c_node.chunks:
                    p_name = p_chunk.name
                    if p_name.startswith("param_input") or p_name.startswith("InputParam"):
                        p_guid = p_chunk.get_value("InstanceGuid")
                        p_label = p_chunk.get_value("Name", "in")
                        sources = [it.value for it in p_chunk.items if it.name == "Source"]
                        comp.inputs.append({
                            "guid": p_guid,
                            "name": p_label,
                            "nickname": p_chunk.get_value("NickName", ""),
                            "sources": sources,
                        })
                    elif p_name.startswith("param_output") or p_name.startswith("OutputParam"):
                        p_guid = p_chunk.get_value("InstanceGuid")
                        p_label = p_chunk.get_value("Name", "out")
                        comp.outputs.append({
                            "guid": p_guid,
                            "name": p_label,
                            "nickname": p_chunk.get_value("NickName", ""),
                        })
                        if p_guid:
                            param_map[p_guid] = (comp_id, p_label, comp.name)

            for key in ("ScriptSource", "CodeInput"):
                code = cont.get_value(key)
                if code:
                    comp.script_source = code
                    break

            for key in ("UserText", "Slider", "Value"):
                val = cont.get_value(key)
                if val:
                    comp.properties[key] = val

            graph.components.append(comp)

        for comp in graph.components:
            for p_in in comp.inputs:
                for src_guid in p_in.get("sources", []):
                    if src_guid in param_map:
                        src_comp_id, src_param_name, _ = param_map[src_guid]
                        graph.wires.append({
                            "from": f"{src_comp_id}.{src_param_name}",
                            "to": f"{comp.comp_id}.{p_in['name']}",
                        })

        return graph
