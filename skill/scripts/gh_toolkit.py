#!/usr/bin/env python3
"""
gh_toolkit.py - Comprehensive Grasshopper Definition Engine

A zero-external-dependency library and CLI tool for:
1. Decompressing and compressing binary Grasshopper files (.gh)
2. Parsing and writing XML Grasshopper files (.ghx)
3. Bidirectional conversion: .gh <-> .ghx <-> JSON Graph IR
4. Inspecting canvas topologies, components, parameters, and wires
5. Extracting embedded C# and GhPython scripts
6. Programmatic graph synthesis (GHBuilder API)
"""

import os
import sys
import time
import zlib
import struct
import uuid
import base64
import json
import argparse
import subprocess
import shutil
import xml.etree.ElementTree as ET
from typing import List, Dict, Any, Optional, Tuple, Union


# ==============================================================================
# 1. GH_IO Type System Constants
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
# 2. Data Models (GHItem & GHChunk)
# ==============================================================================

class GHItem:
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
    def __init__(self, name: str, index: int = -1):
        self.name = name
        self.index = index
        self.items: List[GHItem] = []
        self.chunks: List["GHChunk"] = []

    def add_item(self, name: str, type_code: int, value: Any, index: int = -1) -> GHItem:
        item = GHItem(name, type_code, value, index)
        self.items.append(item)
        return item

    def create_chunk(self, name: str, index: int = -1) -> "GHChunk":
        chunk = GHChunk(name, index)
        self.chunks.append(chunk)
        return chunk

    def find_chunk(self, name: str) -> Optional["GHChunk"]:
        for c in self.chunks:
            if c.name == name:
                return c
        return None

    def find_chunks(self, name: str) -> List["GHChunk"]:
        return [c for c in self.chunks if c.name == name]

    def find_item(self, name: str) -> Optional[GHItem]:
        for it in self.items:
            if it.name == name:
                return it
        return None

    def get_value(self, name: str, default: Any = None) -> Any:
        it = self.find_item(name)
        return it.value if it else default

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "index": self.index,
            "items": [it.to_dict() for it in self.items],
            "chunks": [ch.to_dict() for ch in self.chunks],
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "GHChunk":
        chunk = cls(d["name"], d.get("index", -1))
        for it_d in d.get("items", []):
            chunk.items.append(GHItem.from_dict(it_d))
        for ch_d in d.get("chunks", []):
            chunk.chunks.append(cls.from_dict(ch_d))
        return chunk


class GHArchive:
    def __init__(self, root: Optional[GHChunk] = None):
        self.root = root or GHChunk("Root")

    def to_dict(self) -> Dict[str, Any]:
        return self.root.to_dict()

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "GHArchive":
        return cls(GHChunk.from_dict(d))


# ==============================================================================
# 3. Binary Parser & Serializer (Raw Deflate GH_IO)
# ==============================================================================

def _read_7bit_int(data: bytes, pos: int) -> Tuple[int, int]:
    val = 0
    shift = 0
    while True:
        b = data[pos]
        pos += 1
        val |= (b & 0x7F) << shift
        if (b & 0x80) == 0:
            break
        shift += 7
    return val, pos


def _write_7bit_int(val: int) -> bytes:
    buf = bytearray()
    while val >= 0x80:
        buf.append((val & 0x7F) | 0x80)
        val >>= 7
    buf.append(val & 0x7F)
    return bytes(buf)


def _read_string(data: bytes, pos: int) -> Tuple[str, int]:
    length, pos = _read_7bit_int(data, pos)
    s = data[pos : pos + length].decode("utf-8", errors="replace")
    pos += length
    return s, pos


def _write_string(s: str) -> bytes:
    raw = s.encode("utf-8")
    return _write_7bit_int(len(raw)) + raw


def read_gh_binary(data_or_path: Union[bytes, str]) -> GHArchive:
    if isinstance(data_or_path, str):
        with open(data_or_path, "rb") as f:
            raw = f.read()
    else:
        raw = data_or_path

    try:
        data = zlib.decompress(raw, -zlib.MAX_WBITS)
    except Exception:
        data = raw

    pos = 0

    def read_item() -> GHItem:
        nonlocal pos
        name, pos = _read_string(data, pos)
        idx = struct.unpack_from("<i", data, pos)[0]
        pos += 4
        type_code = struct.unpack_from("<i", data, pos)[0]
        pos += 4

        val: Any = None
        if type_code == 0:
            val = None
        elif type_code == 1:
            val = bool(data[pos])
            pos += 1
        elif type_code == 2:
            val = data[pos]
            pos += 1
        elif type_code == 3:
            val = struct.unpack_from("<i", data, pos)[0]
            pos += 4
        elif type_code == 4:
            val = struct.unpack_from("<q", data, pos)[0]
            pos += 8
        elif type_code == 5:
            val = struct.unpack_from("<f", data, pos)[0]
            pos += 4
        elif type_code == 6:
            val = struct.unpack_from("<d", data, pos)[0]
            pos += 8
        elif type_code == 7:
            val = list(struct.unpack_from("<4i", data, pos))
            pos += 16
        elif type_code == 8:
            val = struct.unpack_from("<q", data, pos)[0]
            pos += 8
        elif type_code == 9:
            val = str(uuid.UUID(bytes_le=data[pos : pos + 16]))
            pos += 16
        elif type_code == 10:
            val, pos = _read_string(data, pos)
        elif type_code == 20:
            cnt = struct.unpack_from("<i", data, pos)[0]
            pos += 4
            val = data[pos : pos + cnt]
            pos += cnt
        elif type_code == 21:
            cnt = struct.unpack_from("<i", data, pos)[0]
            pos += 4
            val = list(struct.unpack_from(f"<{cnt}d", data, pos))
            pos += cnt * 8
        elif type_code in (30, 32):
            val = list(struct.unpack_from("<ii", data, pos))
            pos += 8
        elif type_code in (31, 33):
            val = list(struct.unpack_from("<ff", data, pos))
            pos += 8
        elif type_code == 34:
            val = list(struct.unpack_from("<iiii", data, pos))
            pos += 16
        elif type_code == 35:
            val = list(struct.unpack_from("<ffff", data, pos))
            pos += 16
        elif type_code == 36:
            b, g, r, a = struct.unpack_from("<BBBB", data, pos)
            pos += 4
            val = [a, r, g, b]
        elif type_code == 37:
            cnt = struct.unpack_from("<i", data, pos)[0]
            pos += 4
            val = data[pos : pos + cnt]
            pos += cnt
        elif type_code == 50:
            val = list(struct.unpack_from("<dd", data, pos))
            pos += 16
        elif type_code == 51:
            val = list(struct.unpack_from("<ddd", data, pos))
            pos += 24
        elif type_code == 52:
            val = list(struct.unpack_from("<dddd", data, pos))
            pos += 32
        elif type_code == 60:
            val = list(struct.unpack_from("<dd", data, pos))
            pos += 16
        elif type_code == 61:
            val = list(struct.unpack_from("<dddd", data, pos))
            pos += 32
        elif type_code in (70, 71):
            val = list(struct.unpack_from("<dddddd", data, pos))
            pos += 48
        elif type_code == 72:
            val = list(struct.unpack_from("<9d", data, pos))
            pos += 72
        elif type_code == 80:
            val = list(struct.unpack_from("<iii", data, pos))
            pos += 12
        else:
            raise ValueError(f"Unknown type_code: {type_code} at pos {pos}")

        return GHItem(name, type_code, val, idx)

    def read_chunk() -> GHChunk:
        nonlocal pos
        name, pos = _read_string(data, pos)
        idx = struct.unpack_from("<i", data, pos)[0]
        pos += 4
        item_count = struct.unpack_from("<i", data, pos)[0]
        pos += 4
        chunk_count = struct.unpack_from("<i", data, pos)[0]
        pos += 4

        chunk = GHChunk(name, idx)
        for _ in range(item_count):
            chunk.items.append(read_item())
        for _ in range(chunk_count):
            chunk.chunks.append(read_chunk())
        return chunk

    root = read_chunk()
    return GHArchive(root)


def write_gh_binary(archive: GHArchive, out_path: Optional[str] = None, compress: bool = True) -> bytes:
    buf = bytearray()

    def write_item(item: GHItem):
        buf.extend(_write_string(item.name))
        buf.extend(struct.pack("<i", item.index))
        buf.extend(struct.pack("<i", item.type_code))

        tc = item.type_code
        v = item.value

        if tc == 0:
            pass
        elif tc == 1:
            buf.append(1 if v else 0)
        elif tc == 2:
            buf.append(int(v) & 0xFF)
        elif tc == 3:
            buf.extend(struct.pack("<i", int(v)))
        elif tc == 4:
            buf.extend(struct.pack("<q", int(v)))
        elif tc == 5:
            buf.extend(struct.pack("<f", float(v)))
        elif tc == 6:
            buf.extend(struct.pack("<d", float(v)))
        elif tc == 7:
            if isinstance(v, (list, tuple)):
                buf.extend(struct.pack("<4i", *[int(x) for x in v]))
            else:
                buf.extend(struct.pack("<4i", int(v), 0, 0, 0))
        elif tc == 8:
            buf.extend(struct.pack("<q", int(v)))
        elif tc == 9:
            u = uuid.UUID(str(v))
            buf.extend(u.bytes_le)
        elif tc == 10:
            buf.extend(_write_string(str(v or "")))
        elif tc == 20:
            raw = v if isinstance(v, bytes) else v.encode("utf-8")
            buf.extend(struct.pack("<i", len(raw)))
            buf.extend(raw)
        elif tc == 21:
            buf.extend(struct.pack("<i", len(v)))
            buf.extend(struct.pack(f"<{len(v)}d", *v))
        elif tc in (30, 32):
            buf.extend(struct.pack("<ii", int(v[0]), int(v[1])))
        elif tc in (31, 33):
            buf.extend(struct.pack("<ff", float(v[0]), float(v[1])))
        elif tc == 34:
            buf.extend(struct.pack("<iiii", *[int(x) for x in v]))
        elif tc == 35:
            buf.extend(struct.pack("<ffff", *[float(x) for x in v]))
        elif tc == 36:
            a, r, g, b = [int(x) for x in v]
            buf.extend(struct.pack("<BBBB", b, g, r, a))
        elif tc == 37:
            raw = v if isinstance(v, bytes) else base64.b64decode(v)
            buf.extend(struct.pack("<i", len(raw)))
            buf.extend(raw)
        elif tc == 50:
            buf.extend(struct.pack("<dd", float(v[0]), float(v[1])))
        elif tc == 51:
            buf.extend(struct.pack("<ddd", float(v[0]), float(v[1]), float(v[2])))
        elif tc == 52:
            buf.extend(struct.pack("<dddd", *[float(x) for x in v]))
        elif tc == 60:
            buf.extend(struct.pack("<dd", float(v[0]), float(v[1])))
        elif tc == 61:
            buf.extend(struct.pack("<dddd", *[float(x) for x in v]))
        elif tc in (70, 71):
            buf.extend(struct.pack("<6d", *[float(x) for x in v]))
        elif tc == 72:
            buf.extend(struct.pack("<9d", *[float(x) for x in v]))
        elif tc == 80:
            buf.extend(struct.pack("<iii", int(v[0]), int(v[1]), int(v[2])))
        else:
            raise ValueError(f"Unsupported write type_code: {tc}")

    def write_chunk(chunk: GHChunk):
        buf.extend(_write_string(chunk.name))
        buf.extend(struct.pack("<i", chunk.index))
        buf.extend(struct.pack("<i", len(chunk.items)))
        buf.extend(struct.pack("<i", len(chunk.chunks)))
        for it in chunk.items:
            write_item(it)
        for ch in chunk.chunks:
            write_chunk(ch)

    write_chunk(archive.root)
    uncompressed = bytes(buf)

    if compress:
        compressor = zlib.compressobj(level=zlib.Z_DEFAULT_COMPRESSION, method=zlib.DEFLATED, wbits=-zlib.MAX_WBITS)
        final_data = compressor.compress(uncompressed) + compressor.flush()
    else:
        final_data = uncompressed

    if out_path:
        with open(out_path, "wb") as f:
            f.write(final_data)

    return final_data


# ==============================================================================
# 4. XML Parser & Serializer (.ghx)
# ==============================================================================

def read_ghx(xml_path_or_str: str) -> GHArchive:
    if os.path.isfile(xml_path_or_str):
        tree = ET.parse(xml_path_or_str)
        root_elem = tree.getroot()
    else:
        root_elem = ET.fromstring(xml_path_or_str)

    def parse_item(elem: ET.Element) -> GHItem:
        name = elem.attrib.get("name", "")
        tc = int(elem.attrib.get("type_code", "0"))
        idx = int(elem.attrib.get("index", "-1"))
        text = elem.text.strip() if elem.text else ""

        val: Any = None
        if tc == 0:
            val = None
        elif tc == 1:
            val = text.lower() in ("true", "1")
        elif tc in (2, 3):
            val = int(text) if text else 0
        elif tc in (4, 8):
            val = int(text) if text else 0
        elif tc in (5, 6):
            val = float(text) if text else 0.0
        elif tc == 7:
            cleaned = text.replace(",", " ").replace("[", "").replace("]", "").strip()
            val = [int(x) for x in cleaned.split()] if cleaned else [0, 0, 0, 0]
        elif tc == 9:
            val = text
        elif tc == 10:
            val = elem.text or ""
        elif tc in (20, 37):
            b_tag = elem.find("bitmap")
            raw_b64 = (b_tag.text if b_tag is not None and b_tag.text else text).strip()
            val = base64.b64decode(raw_b64) if raw_b64 else b""
        elif tc == 21:
            val = [float(x) for x in text.split()]
        elif tc in (30, 31):
            val = [float(elem.findtext("X", "0")), float(elem.findtext("Y", "0"))]
        elif tc in (32, 33):
            val = [float(elem.findtext("W", "0")), float(elem.findtext("H", "0"))]
        elif tc in (34, 35):
            val = [
                float(elem.findtext("X", "0")),
                float(elem.findtext("Y", "0")),
                float(elem.findtext("W", "0")),
                float(elem.findtext("H", "0")),
            ]
        elif tc == 36:
            argb = elem.findtext("ARGB", "0;0;0;0").split(";")
            val = [int(x) for x in argb]
        elif tc == 50:
            val = [float(elem.findtext("X", "0")), float(elem.findtext("Y", "0"))]
        elif tc == 51:
            val = [float(elem.findtext("X", "0")), float(elem.findtext("Y", "0")), float(elem.findtext("Z", "0"))]
        elif tc == 52:
            val = [
                float(elem.findtext("X", "0")),
                float(elem.findtext("Y", "0")),
                float(elem.findtext("Z", "0")),
                float(elem.findtext("W", "0")),
            ]
        elif tc == 60:
            val = [float(elem.findtext("T0", "0")), float(elem.findtext("T1", "0"))]
        elif tc == 61:
            val = [
                float(elem.findtext("Au", "0")),
                float(elem.findtext("Bu", "0")),
                float(elem.findtext("Av", "0")),
                float(elem.findtext("Bv", "0")),
            ]
        elif tc in (70, 71):
            val = [
                float(elem.findtext("Ax", "0")),
                float(elem.findtext("Ay", "0")),
                float(elem.findtext("Az", "0")),
                float(elem.findtext("Bx", "0")),
                float(elem.findtext("By", "0")),
                float(elem.findtext("Bz", "0")),
            ]
        elif tc == 72:
            val = [
                float(elem.findtext("Ox", "0")),
                float(elem.findtext("Oy", "0")),
                float(elem.findtext("Oz", "0")),
                float(elem.findtext("Xx", "1")),
                float(elem.findtext("Xy", "0")),
                float(elem.findtext("Xz", "0")),
                float(elem.findtext("Yx", "0")),
                float(elem.findtext("Yy", "1")),
                float(elem.findtext("Yz", "0")),
            ]
        elif tc == 80:
            val = [
                int(elem.findtext("Major", "0")),
                int(elem.findtext("Minor", "0")),
                int(elem.findtext("Revision", "0")),
            ]
        else:
            val = text

        return GHItem(name, tc, val, idx)

    def parse_chunk(elem: ET.Element) -> GHChunk:
        name = elem.attrib.get("name", "")
        idx = int(elem.attrib.get("index", "-1"))
        chunk = GHChunk(name, idx)

        items_elem = elem.find("items")
        if items_elem is not None:
            for it_elem in items_elem.findall("item"):
                chunk.items.append(parse_item(it_elem))

        chunks_elem = elem.find("chunks")
        if chunks_elem is not None:
            for ch_elem in chunks_elem.findall("chunk"):
                chunk.chunks.append(parse_chunk(ch_elem))

        return chunk

    root_chunk = parse_chunk(root_elem)
    return GHArchive(root_chunk)


def write_ghx(archive: GHArchive, out_path: Optional[str] = None) -> str:
    root_elem = ET.Element("Archive", {"name": archive.root.name})

    def format_item(parent: ET.Element, item: GHItem):
        attribs = {
            "name": item.name,
            "type_name": item.type_name,
            "type_code": str(item.type_code),
        }
        if item.index != -1:
            attribs["index"] = str(item.index)

        it_elem = ET.SubElement(parent, "item", attribs)
        tc = item.type_code
        v = item.value

        if tc == 1:
            it_elem.text = "true" if v else "false"
        elif tc in (2, 3, 4, 8):
            it_elem.text = str(v)
        elif tc in (5, 6):
            it_elem.text = f"{float(v):g}"
        elif tc == 7:
            it_elem.text = " ".join(str(x) for x in v) if isinstance(v, (list, tuple)) else str(v)
        elif tc in (9, 10):
            it_elem.text = str(v or "")
        elif tc == 36:
            argb = ET.SubElement(it_elem, "ARGB")
            argb.text = f"{int(v[0])};{int(v[1])};{int(v[2])};{int(v[3])}"
        elif tc in (30, 31, 50):
            ET.SubElement(it_elem, "X").text = str(v[0])
            ET.SubElement(it_elem, "Y").text = str(v[1])
        elif tc in (34, 35):
            ET.SubElement(it_elem, "X").text = str(v[0])
            ET.SubElement(it_elem, "Y").text = str(v[1])
            ET.SubElement(it_elem, "W").text = str(v[2])
            ET.SubElement(it_elem, "H").text = str(v[3])
        elif tc == 37:
            b_tag = ET.SubElement(it_elem, "bitmap")
            b_tag.text = base64.b64encode(v).decode("ascii") if isinstance(v, bytes) else str(v)
        elif tc == 51:
            ET.SubElement(it_elem, "X").text = str(v[0])
            ET.SubElement(it_elem, "Y").text = str(v[1])
            ET.SubElement(it_elem, "Z").text = str(v[2])
        elif tc == 61:
            ET.SubElement(it_elem, "Au").text = str(v[0])
            ET.SubElement(it_elem, "Bu").text = str(v[1])
            ET.SubElement(it_elem, "Av").text = str(v[2])
            ET.SubElement(it_elem, "Bv").text = str(v[3])
        elif tc == 72:
            ET.SubElement(it_elem, "Ox").text = str(v[0])
            ET.SubElement(it_elem, "Oy").text = str(v[1])
            ET.SubElement(it_elem, "Oz").text = str(v[2])
            ET.SubElement(it_elem, "Xx").text = str(v[3])
            ET.SubElement(it_elem, "Xy").text = str(v[4])
            ET.SubElement(it_elem, "Xz").text = str(v[5])
            ET.SubElement(it_elem, "Yx").text = str(v[6])
            ET.SubElement(it_elem, "Yy").text = str(v[7])
            ET.SubElement(it_elem, "Yz").text = str(v[8])
        elif tc == 80:
            ET.SubElement(it_elem, "Major").text = str(v[0])
            ET.SubElement(it_elem, "Minor").text = str(v[1])
            ET.SubElement(it_elem, "Revision").text = str(v[2])
        else:
            if isinstance(v, bytes):
                it_elem.text = base64.b64encode(v).decode("ascii")
            else:
                it_elem.text = str(v if v is not None else "")

    def format_chunk(parent: ET.Element, chunk: GHChunk):
        attribs = {"name": chunk.name}
        if chunk.index != -1:
            attribs["index"] = str(chunk.index)
        ch_elem = ET.SubElement(parent, "chunk", attribs)

        if chunk.items:
            items_elem = ET.SubElement(ch_elem, "items", {"count": str(len(chunk.items))})
            for it in chunk.items:
                format_item(items_elem, it)

        if chunk.chunks:
            chunks_elem = ET.SubElement(ch_elem, "chunks", {"count": str(len(chunk.chunks))})
            for ch in chunk.chunks:
                format_chunk(chunks_elem, ch)

    if archive.root.items:
        items_elem = ET.SubElement(root_elem, "items", {"count": str(len(archive.root.items))})
        for it in archive.root.items:
            format_item(items_elem, it)

    if archive.root.chunks:
        chunks_elem = ET.SubElement(root_elem, "chunks", {"count": str(len(archive.root.chunks))})
        for ch in archive.root.chunks:
            format_chunk(chunks_elem, ch)

    ET.indent(root_elem, space="  ")
    xml_str = '<?xml version="1.0" encoding="utf-8" standalone="yes"?>\n' + ET.tostring(root_elem, encoding="utf-8").decode("utf-8")

    if out_path:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(xml_str)

    return xml_str


# ==============================================================================
# 5. Graph IR (Intermediate Representation)
# ==============================================================================

class GHGraphComponent:
    def __init__(self, comp_id: str, name: str, nickname: str = "", guid: str = "", pivot: Tuple[float, float] = (0, 0)):
        self.comp_id = comp_id
        self.name = name
        self.nickname = nickname or name
        self.guid = guid
        self.pivot = list(pivot)
        self.inputs: List[Dict[str, Any]] = []
        self.outputs: List[Dict[str, Any]] = []
        self.properties: Dict[str, Any] = {}
        self.script_source: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        d = {
            "id": self.comp_id,
            "name": self.name,
            "nickname": self.nickname,
            "guid": self.guid,
            "pivot": self.pivot,
            "inputs": self.inputs,
            "outputs": self.outputs,
            "properties": self.properties,
        }
        if self.script_source is not None:
            d["script_source"] = self.script_source
        return d


class GHGraph:
    def __init__(self, name: str = "GrasshopperDefinition"):
        self.name = name
        self.components: List[GHGraphComponent] = []
        self.wires: List[Dict[str, str]] = []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "component_count": len(self.components),
            "wire_count": len(self.wires),
            "components": [c.to_dict() for c in self.components],
            "wires": self.wires,
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)

    @classmethod
    def from_archive(cls, archive: GHArchive) -> "GHGraph":
        graph = cls()
        defn = archive.root.find_chunk("Definition")
        if not defn:
            return graph

        props = defn.find_chunk("DefinitionProperties")
        if props:
            graph.name = props.get_value("Name", "Untitled")

        objs_chunk = defn.find_chunk("DefinitionObjects")
        if not objs_chunk:
            return graph

        param_map: Dict[str, Tuple[str, str, bool]] = {}

        for obj_chunk in objs_chunk.find_chunks("Object"):
            guid = obj_chunk.get_value("GUID", "")
            name = obj_chunk.get_value("Name", "Unknown")
            container = obj_chunk.find_chunk("Container")
            if not container:
                continue

            inst_guid = container.get_value("InstanceGuid", str(uuid.uuid4()))
            nick = container.get_value("NickName", name)
            comp_id = f"c_{inst_guid[:8]}"

            attr = container.find_chunk("Attributes")
            pivot = [0.0, 0.0]
            if attr:
                p_val = attr.get_value("Pivot", [0.0, 0.0])
                pivot = [float(p_val[0]), float(p_val[1])]

            comp = GHGraphComponent(comp_id, name, nick, guid, (pivot[0], pivot[1]))

            # Locate all input/output chunks across container, ParameterData, ParameterManager
            search_containers = [container]
            for sub in ("ParameterData", "ParameterManager"):
                ch = container.find_chunk(sub)
                if ch:
                    search_containers.append(ch)

            for cnt in search_containers:
                for p_chunk in cnt.chunks:
                    cname = p_chunk.name.lower()
                    if "input" in cname or cname == "param_input":
                        p_name = p_chunk.get_value("Name", p_chunk.get_value("NickName", "in"))
                        p_guid = p_chunk.get_value("InstanceGuid", "")
                        sources = [str(it.value) for it in p_chunk.items if it.name == "Source"]
                        comp.inputs.append({
                            "name": p_name,
                            "guid": p_guid,
                            "sources": sources,
                        })
                        if p_guid:
                            param_map[p_guid] = (comp_id, p_name, True)

                    elif "output" in cname or cname == "param_output":
                        p_name = p_chunk.get_value("Name", p_chunk.get_value("NickName", "out"))
                        p_guid = p_chunk.get_value("InstanceGuid", "")
                        comp.outputs.append({
                            "name": p_name,
                            "guid": p_guid,
                        })
                        if p_guid:
                            param_map[p_guid] = (comp_id, p_name, False)

            # Check if container itself has input wire (e.g. Panel receiving input)
            direct_sources = [str(it.value) for it in container.items if it.name == "Source"]
            if direct_sources:
                comp.inputs.append({
                    "name": "in",
                    "guid": inst_guid,
                    "sources": direct_sources,
                })
                param_map[inst_guid] = (comp_id, "in", True)

            # Embedded scripts (GhPython or C#)
            code_input = container.get_value("CodeInput")
            script_src = container.get_value("ScriptSource")
            using_src = container.get_value("UsingSource")
            add_src = container.get_value("AdditionalSource")

            if code_input:
                comp.script_source = code_input
            elif script_src or add_src:
                full_cs = ""
                if using_src:
                    full_cs += f"// Using Source\n{using_src}\n\n"
                if add_src:
                    full_cs += f"// Additional Source / Members\n{add_src}\n\n"
                if script_src:
                    full_cs += f"// RunScript Source\n{script_src}\n"
                comp.script_source = full_cs

            # Panel content
            panel_text = container.get_value("UserText")
            if panel_text:
                comp.properties["text"] = panel_text

            # Slider properties
            slider = container.find_chunk("Slider")
            if slider:
                comp.properties["slider"] = {
                    "min": slider.get_value("Min"),
                    "max": slider.get_value("Max"),
                    "val": slider.get_value("Value"),
                }

            graph.components.append(comp)

        # Reconstruct wires
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


# ==============================================================================
# 6. High-Level Graph Builder API
# ==============================================================================


def load_heteroptera_catalog() -> Dict[str, Any]:
    """Load the 152-component Heteroptera catalog from local resources or tools."""
    candidates = [
        os.path.join(os.path.dirname(__file__), "..", "resources", "heteroptera_catalog.json"),
        os.path.join(os.path.dirname(__file__), "heteroptera_catalog.json"),
        os.path.join(os.path.dirname(__file__), "..", "..", "gh_toolkit", "data", "heteroptera_catalog.json"),
        os.path.join(os.getcwd(), "gh_toolkit", "data", "heteroptera_catalog.json"),
        os.path.join(os.getcwd(), "tools", "heteroptera_catalog.json"),
        os.path.join(os.getcwd(), "heteroptera_catalog.json"),
    ]
    for p in candidates:
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
    return {"by_guid": {}, "by_name": {}, "subcategories": {}}


def load_native_catalog() -> Dict[str, Any]:
    """Load the verified native Grasshopper component catalog (211 components)."""
    candidates = [
        os.path.join(os.path.dirname(__file__), "..", "resources", "native_catalog.json"),
        os.path.join(os.path.dirname(__file__), "native_catalog.json"),
        os.path.join(os.path.dirname(__file__), "..", "..", "gh_toolkit", "data", "native_catalog.json"),
        os.path.join(os.getcwd(), "gh_toolkit", "data", "native_catalog.json"),
        os.path.join(os.getcwd(), "skill", "resources", "native_catalog.json"),
    ]
    for p in candidates:
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
    return {"by_guid": {}, "by_name": {}, "categories": {}}


def find_native_component(name_or_guid: str) -> Optional[Dict[str, Any]]:
    """Look up a native Grasshopper component by GUID, Name, or Nickname."""
    catalog = load_native_catalog()
    query = name_or_guid.lower().strip()
    if query in catalog.get("by_guid", {}):
        return catalog["by_guid"][query]
    if name_or_guid in catalog.get("by_name", {}):
        return catalog["by_name"][name_or_guid]
    for k, v in catalog.get("by_name", {}).items():
        if k.lower() == query:
            return v
        if v.get("nickname") and v["nickname"].lower() == query:
            return v
    return None


def list_native_components(category: Optional[str] = None) -> List[Dict[str, Any]]:
    """List native components, optionally filtered by category."""
    catalog = load_native_catalog()
    cats = catalog.get("categories", {})
    results = []
    for cat, names in cats.items():
        if category and category.lower() not in (cat.lower(), "all"):
            continue
        for n in names:
            comp = catalog.get("by_name", {}).get(n)
            if comp:
                results.append(comp)
    return results


_CACHED_LEGOPOD_CATALOG: Optional[Dict[str, Any]] = None


def load_legopod_catalog() -> Dict[str, Any]:
    """Load the verified LegoPod component catalog (42 components)."""
    global _CACHED_LEGOPOD_CATALOG
    if _CACHED_LEGOPOD_CATALOG is not None:
        return _CACHED_LEGOPOD_CATALOG

    candidates = [
        os.path.join(os.path.dirname(__file__), "..", "resources", "legopod_catalog.json"),
        os.path.join(os.path.dirname(__file__), "legopod_catalog.json"),
        os.path.join(os.path.dirname(__file__), "..", "..", "gh_toolkit", "data", "legopod_catalog.json"),
        os.path.join(os.getcwd(), "gh_toolkit", "data", "legopod_catalog.json"),
        os.path.join(os.getcwd(), "skill", "resources", "legopod_catalog.json"),
    ]

    for p in candidates:
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    _CACHED_LEGOPOD_CATALOG = json.load(f)
                    return _CACHED_LEGOPOD_CATALOG
            except Exception:
                pass

    return {"by_guid": {}, "by_name": {}, "subcategories": {}, "total_components": 0}


def find_legopod_component(name_or_guid: str) -> Optional[Dict[str, Any]]:
    """Look up a LegoPod component by GUID, Name, or Nickname."""
    catalog = load_legopod_catalog()
    query = name_or_guid.lower().strip()

    if query in catalog.get("by_guid", {}):
        return catalog["by_guid"][query]
    if name_or_guid in catalog.get("by_name", {}):
        return catalog["by_name"][name_or_guid]
    for k, v in catalog.get("by_name", {}).items():
        if k.lower() == query:
            return v
        if v.get("nickname") and v["nickname"].lower() == query:
            return v
    return None


def list_legopod_components(subcategory: Optional[str] = None) -> List[Dict[str, Any]]:
    """List LegoPod components, optionally filtered by subcategory."""
    catalog = load_legopod_catalog()
    subcats = catalog.get("subcategories", {})
    results = []
    for sub, names in subcats.items():
        if subcategory and subcategory.lower() not in (sub.lower(), "all"):
            continue
        for n in names:
            comp = catalog.get("by_name", {}).get(n)
            if comp:
                results.append(comp)
    return results


_CACHED_MAGPIE_CATALOG: Optional[Dict[str, Any]] = None


def load_magpie_catalog() -> Dict[str, Any]:
    """Load the verified Magpie component catalog (14 components)."""
    global _CACHED_MAGPIE_CATALOG
    if _CACHED_MAGPIE_CATALOG is not None:
        return _CACHED_MAGPIE_CATALOG

    candidates = [
        os.path.join(os.path.dirname(__file__), "..", "resources", "magpie_catalog.json"),
        os.path.join(os.path.dirname(__file__), "magpie_catalog.json"),
        os.path.join(os.path.dirname(__file__), "..", "..", "gh_toolkit", "data", "magpie_catalog.json"),
        os.path.join(os.getcwd(), "gh_toolkit", "data", "magpie_catalog.json"),
        os.path.join(os.getcwd(), "skill", "resources", "magpie_catalog.json"),
    ]

    for p in candidates:
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    _CACHED_MAGPIE_CATALOG = json.load(f)
                    return _CACHED_MAGPIE_CATALOG
            except Exception:
                pass

    return {"by_guid": {}, "by_name": {}, "subcategories": {}, "total_components": 0}


def find_magpie_component(name_or_guid: str) -> Optional[Dict[str, Any]]:
    """Look up a Magpie component by GUID, Name, or Nickname."""
    catalog = load_magpie_catalog()
    query = name_or_guid.lower().strip()

    if query in catalog.get("by_guid", {}):
        return catalog["by_guid"][query]
    if name_or_guid in catalog.get("by_name", {}):
        return catalog["by_name"][name_or_guid]
    for k, v in catalog.get("by_name", {}).items():
        if k.lower() == query:
            return v
        if v.get("nickname") and v["nickname"].lower() == query:
            return v
    return None


def list_magpie_components(subcategory: Optional[str] = None) -> List[Dict[str, Any]]:
    """List Magpie components, optionally filtered by subcategory."""
    catalog = load_magpie_catalog()
    subcats = catalog.get("subcategories", {})
    results = []
    for sub, names in subcats.items():
        if subcategory and subcategory.lower() not in (sub.lower(), "all"):
            continue
        for n in names:
            comp = catalog.get("by_name", {}).get(n)
            if comp:
                results.append(comp)
    return results


def find_yak() -> Optional[str]:
    """Locate McNeel Yak package manager executable."""
    import shutil
    candidates = [
        shutil.which("yak"),
        "/Applications/Rhino 8.app/Contents/Resources/bin/yak",
        "/Applications/Rhino 7.app/Contents/Resources/bin/yak",
        os.path.expanduser("~/Library/Application Support/McNeel/Rhinoceros/8.0/yak"),
        r"C:\Program Files\Rhino 8\System\yak.exe",
        r"C:\Program Files\Rhino 7\System\yak.exe",
    ]
    for c in candidates:
        if c and os.path.exists(c):
            return c
    return None


def get_heteroptera_status() -> Dict[str, Any]:
    """Check Heteroptera installation status in Rhino."""
    import subprocess
    import re
    yak_bin = find_yak()
    status = {
        "yak_found": yak_bin is not None,
        "yak_path": yak_bin,
        "installed": False,
        "installed_version": None,
        "latest_version": None,
        "is_latest": False,
        "packages_dir": None,
    }
    mac_pkg = os.path.expanduser("~/Library/Application Support/McNeel/Rhinoceros/packages/8.0/Heteroptera")
    if os.path.exists(mac_pkg):
        status["packages_dir"] = mac_pkg
        try:
            vers = [d for d in os.listdir(mac_pkg) if os.path.isdir(os.path.join(mac_pkg, d)) and not d.startswith(".")]
            if vers:
                def v_key(v): return [int(x) if x.isdigit() else 0 for x in re.findall(r"\d+", v)]
                vers.sort(key=v_key, reverse=True)
                status["installed"] = True
                status["installed_version"] = vers[0]
        except Exception:
            pass
    if not yak_bin:
        return status
    try:
        res = subprocess.run([yak_bin, "list"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=10)
        if res.returncode == 0:
            m = re.search(r"Heteroptera\s+\(([\d\.]+)\)", res.stdout, re.IGNORECASE)
            if m:
                status["installed"] = True
                status["installed_version"] = m.group(1)
    except Exception:
        pass
    try:
        res = subprocess.run([yak_bin, "search", "heteroptera"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=15)
        if res.returncode == 0:
            m = re.search(r"Heteroptera\s+\(([\d\.]+)\)", res.stdout, re.IGNORECASE)
            if m:
                status["latest_version"] = m.group(1)
    except Exception:
        pass
    if status["installed_version"] and status["latest_version"]:
        status["is_latest"] = (status["installed_version"] == status["latest_version"])
    elif status["installed"] and not status["latest_version"]:
        status["is_latest"] = True
    return status


def install_heteroptera(force: bool = False) -> Tuple[bool, str]:
    """Install or upgrade Heteroptera via Yak."""
    import subprocess
    yak_bin = find_yak()
    if not yak_bin:
        return False, "Yak package manager not found."
    status = get_heteroptera_status()
    if status["installed"] and status["is_latest"] and not force:
        return True, f"Heteroptera is already up to date ({status['installed_version']})."
    try:
        res = subprocess.run([yak_bin, "install", "Heteroptera"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=60)
        if res.returncode == 0:
            new_stat = get_heteroptera_status()
            return True, f"Successfully installed Heteroptera ({new_stat.get('installed_version', 'latest')})."
        return False, f"Yak install failed: {res.stderr.strip() or res.stdout.strip()}"
    except Exception as e:
        return False, f"Error: {e}"



class GHBuilder:
    """Convenience builder to synthesize new valid Grasshopper definitions."""

    def __init__(self, name: str = "GeneratedDefinition"):
        self.archive = GHArchive()
        self.name = name

        self.archive.root.add_item("ArchiveVersion", 80, [0, 2, 2])
        self.defn = self.archive.root.create_chunk("Definition")
        self.defn.add_item("plugin_version", 80, [1, 0, 7])

        doc_header = self.defn.create_chunk("DocumentHeader")
        doc_header.add_item("DocumentID", 9, str(uuid.uuid4()))
        doc_header.add_item("Preview", 10, "Shaded")
        doc_header.add_item("PreviewMeshType", 3, 1)
        doc_header.add_item("PreviewNormal", 36, [100, 150, 0, 0])
        doc_header.add_item("PreviewSelected", 36, [100, 0, 150, 0])

        props = self.defn.create_chunk("DefinitionProperties")
        props.add_item("Date", 8, 638295068918890330)
        props.add_item("Description", 10, "Synthesized by Antigravity GH Toolkit")
        props.add_item("Name", 10, name)
        props.create_chunk("Revisions").add_item("RevisionCount", 3, 0)
        proj = props.create_chunk("Projection")
        proj.add_item("Target", 30, [100, 100])
        proj.add_item("Zoom", 5, 1.0)
        props.create_chunk("Views").add_item("ViewCount", 3, 0)

        self.objects_chunk = self.defn.create_chunk("DefinitionObjects")
        self.object_count = 0

        thumb = self.archive.root.create_chunk("Thumbnail")
        thumb.add_item("Thumbnail", 37, b"")

        self.param_lut: Dict[str, str] = {}

    def add_slider(self, alias: str, nickname: str, min_val: float, max_val: float, current_val: float, pivot: Tuple[float, float]) -> str:
        comp_guid = "57da07bd-ecab-415d-9d86-af36d7073abc"
        inst_guid = str(uuid.uuid4())
        out_param_guid = str(uuid.uuid4())

        obj = self.objects_chunk.create_chunk("Object", self.object_count)
        self.object_count += 1
        obj.add_item("GUID", 9, comp_guid)
        obj.add_item("Lib", 9, "d45600cd-4e6d-4548-a006-880026e13470")
        obj.add_item("Name", 10, "Number Slider")

        cont = obj.create_chunk("Container")
        cont.add_item("Description", 10, "A slider for numeric values")
        cont.add_item("InstanceGuid", 9, inst_guid)
        cont.add_item("Name", 10, "Number Slider")
        cont.add_item("NickName", 10, nickname)

        attr = cont.create_chunk("Attributes")
        attr.add_item("Bounds", 35, [pivot[0], pivot[1], 150.0, 20.0])
        attr.add_item("Pivot", 31, [pivot[0] + 75.0, pivot[1] + 10.0])

        slider = cont.create_chunk("Slider")
        slider.add_item("Digits", 3, 2)
        slider.add_item("Interval", 3, 1)
        slider.add_item("Max", 6, float(max_val))
        slider.add_item("Min", 6, float(min_val))
        slider.add_item("Value", 6, float(current_val))

        p_out = cont.create_chunk("param_output", 0)
        p_out.add_item("InstanceGuid", 9, out_param_guid)
        p_out.add_item("Name", 10, "Output")
        p_out.add_item("NickName", 10, nickname)

        self.param_lut[f"{alias}.out"] = out_param_guid
        self.param_lut[f"{alias}.Output"] = out_param_guid
        self.param_lut[f"{alias}"] = out_param_guid
        return inst_guid

    def add_panel(self, alias: str, text: str, pivot: Tuple[float, float]) -> str:
        comp_guid = "ca916113-d820-437b-9994-6ab08216173b"
        inst_guid = str(uuid.uuid4())
        out_param_guid = str(uuid.uuid4())

        obj = self.objects_chunk.create_chunk("Object", self.object_count)
        self.object_count += 1
        obj.add_item("GUID", 9, comp_guid)
        obj.add_item("Name", 10, "Panel")

        cont = obj.create_chunk("Container")
        cont.add_item("Description", 10, "Panel for notes and text")
        cont.add_item("InstanceGuid", 9, inst_guid)
        cont.add_item("Name", 10, "Panel")
        cont.add_item("NickName", 10, "")
        cont.add_item("UserText", 10, text)

        attr = cont.create_chunk("Attributes")
        attr.add_item("Bounds", 35, [pivot[0], pivot[1], 160.0, 60.0])
        attr.add_item("Pivot", 31, [pivot[0], pivot[1]])

        p_out = cont.create_chunk("param_output", 0)
        p_out.add_item("InstanceGuid", 9, out_param_guid)
        p_out.add_item("Name", 10, "out")

        self.param_lut[f"{alias}.out"] = out_param_guid
        self.param_lut[f"{alias}"] = out_param_guid
        return inst_guid

    def add_python_script(
        self,
        alias: str,
        code: str,
        inputs: List[str],
        outputs: List[str],
        pivot: Tuple[float, float],
    ) -> str:
        comp_guid = "410755b1-224a-4c1e-a407-bf32fb45ea7e"
        inst_guid = str(uuid.uuid4())

        obj = self.objects_chunk.create_chunk("Object", self.object_count)
        self.object_count += 1
        obj.add_item("GUID", 9, comp_guid)
        obj.add_item("Name", 10, "GhPython Script")

        cont = obj.create_chunk("Container")
        cont.add_item("Description", 10, "GhPython provides a Python script component")
        cont.add_item("InstanceGuid", 9, inst_guid)
        cont.add_item("Name", 10, "Python Script")
        cont.add_item("NickName", 10, "Py")
        cont.add_item("CodeInput", 10, code)

        attr = cont.create_chunk("Attributes")
        attr.add_item("Bounds", 35, [pivot[0], pivot[1], 80.0, 60.0])
        attr.add_item("Pivot", 31, [pivot[0] + 40.0, pivot[1] + 30.0])

        pdata = cont.create_chunk("ParameterData")
        pdata.add_item("InputCount", 3, len(inputs))
        pdata.add_item("OutputCount", 3, len(outputs))

        for idx, in_name in enumerate(inputs):
            p_in = pdata.create_chunk("InputParam", idx)
            p_guid = str(uuid.uuid4())
            p_in.add_item("InstanceGuid", 9, p_guid)
            p_in.add_item("Name", 10, in_name)
            p_in.add_item("NickName", 10, in_name)
            p_in.add_item("Optional", 1, True)
            self.param_lut[f"{alias}.{in_name}"] = p_guid

        for idx, out_name in enumerate(outputs):
            p_out = pdata.create_chunk("OutputParam", idx)
            p_guid = str(uuid.uuid4())
            p_out.add_item("InstanceGuid", 9, p_guid)
            p_out.add_item("Name", 10, out_name)
            p_out.add_item("NickName", 10, out_name)
            self.param_lut[f"{alias}.{out_name}"] = p_guid

        return inst_guid

    def connect(self, src_port: str, dest_port: str):
        src_guid = self.param_lut.get(src_port)
        dest_guid = self.param_lut.get(dest_port)
        if not src_guid or not dest_guid:
            raise KeyError(f"Cannot connect: unknown port '{src_port}' or '{dest_port}'")

        # Search in objects for dest param
        for obj in self.objects_chunk.chunks:
            cont = obj.find_chunk("Container")
            if not cont:
                continue
            search_containers = [cont]
            pdata = cont.find_chunk("ParameterData")
            if pdata:
                search_containers.append(pdata)

            for sc in search_containers:
                for p_chunk in sc.chunks:
                    if p_chunk.get_value("InstanceGuid") == dest_guid:
                        p_chunk.add_item("Source", 9, src_guid)
                        cnt = p_chunk.get_value("SourceCount", 0)
                        sc_item = p_chunk.find_item("SourceCount")
                        if sc_item:
                            sc_item.value = cnt + 1
                        else:
                            p_chunk.add_item("SourceCount", 3, 1)
                        return


    def add_heteroptera_component(
        self,
        name_or_guid: str,
        alias: str,
        pivot: Tuple[float, float],
        nickname: Optional[str] = None
    ) -> str:
        """Instantiate any of the 152 Heteroptera plugin components by name or GUID."""
        catalog = load_heteroptera_catalog()
        comp_info = None
        ng_lower = name_or_guid.lower()
        if ng_lower in catalog.get("by_guid", {}):
            comp_info = catalog["by_guid"][ng_lower]
        elif name_or_guid in catalog.get("by_name", {}):
            comp_info = catalog["by_name"][name_or_guid]
        else:
            for k, v in catalog.get("by_name", {}).items():
                if k.lower() == ng_lower:
                    comp_info = v
                    break

        if not comp_info:
            raise KeyError(f"Heteroptera component '{name_or_guid}' not found in catalog.")

        comp_guid = comp_info["guid"]
        comp_name = comp_info["name"]
        nick = nickname or comp_info.get("nickname") or comp_name
        inst_guid = str(uuid.uuid4())

        obj = self.objects_chunk.create_chunk("Object", self.object_count)
        self.object_count += 1
        obj.add_item("GUID", 9, comp_guid)
        obj.add_item("Lib", 9, "08bdcae0-d034-48dd-a145-24a9fcf3d3ff")
        obj.add_item("Name", 10, comp_name)

        cont = obj.create_chunk("Container")
        cont.add_item("Description", 10, comp_info.get("description", ""))
        cont.add_item("InstanceGuid", 9, inst_guid)
        cont.add_item("Name", 10, comp_name)
        cont.add_item("NickName", 10, nick)

        inputs = comp_info.get("inputs", [])
        outputs = comp_info.get("outputs", [])
        h = max(40.0, max(len(inputs), len(outputs)) * 24.0 + 20.0)
        w = 90.0

        attr = cont.create_chunk("Attributes")
        attr.add_item("Bounds", 35, [pivot[0], pivot[1], w, h])
        attr.add_item("Pivot", 31, [pivot[0] + w / 2.0, pivot[1] + h / 2.0])

        for idx, inp in enumerate(inputs):
            p_in = cont.create_chunk("param_input", idx)
            p_guid = str(uuid.uuid4())
            p_in.add_item("InstanceGuid", 9, p_guid)
            p_in.add_item("Name", 10, inp["name"])
            p_in.add_item("NickName", 10, inp.get("nickname", inp["name"]))
            p_in.add_item("Description", 10, inp.get("description", ""))
            p_in.add_item("Optional", 1, True)
            acc_str = inp.get("access", "item").lower()
            acc_val = 2 if acc_str == "tree" else (1 if acc_str == "list" else 0)
            p_in.add_item("Access", 3, acc_val)

            self.param_lut[f"{alias}.{inp['name']}"] = p_guid
            if inp.get("nickname"):
                self.param_lut[f"{alias}.{inp['nickname']}"] = p_guid

        for idx, outp in enumerate(outputs):
            p_out = cont.create_chunk("param_output", idx)
            p_guid = str(uuid.uuid4())
            p_out.add_item("InstanceGuid", 9, p_guid)
            p_out.add_item("Name", 10, outp["name"])
            p_out.add_item("NickName", 10, outp.get("nickname", outp["name"]))
            p_out.add_item("Description", 10, outp.get("description", ""))

            self.param_lut[f"{alias}.{outp['name']}"] = p_guid
            if outp.get("nickname"):
                self.param_lut[f"{alias}.{outp['nickname']}"] = p_guid
            if idx == 0:
                self.param_lut[f"{alias}.out"] = p_guid
                self.param_lut[f"{alias}"] = p_guid

        return inst_guid

    def add_native_component(
        self,
        name_or_guid: str,
        alias: str,
        pivot: Tuple[float, float],
        nickname: Optional[str] = None,
    ) -> str:
        """Instantiate any native Grasshopper component by name or GUID."""
        comp_info = find_native_component(name_or_guid)
        if not comp_info:
            raise KeyError(f"Native component '{name_or_guid}' not found in catalog.")

        comp_guid = comp_info["guid"]
        comp_name = comp_info["name"]
        nick = nickname or comp_info.get("nickname") or comp_name
        inst_guid = str(uuid.uuid4())

        obj = self.objects_chunk.create_chunk("Object", self.object_count)
        self.object_count += 1
        obj.add_item("GUID", 9, comp_guid)
        obj.add_item("Lib", 9, "d45600cd-4e6d-4548-a006-880026e13470")
        obj.add_item("Name", 10, comp_name)

        cont = obj.create_chunk("Container")
        cont.add_item("Description", 10, comp_info.get("behavior", ""))
        cont.add_item("InstanceGuid", 9, inst_guid)
        cont.add_item("Name", 10, comp_name)
        cont.add_item("NickName", 10, nick)

        inputs = comp_info.get("inputs", [])
        outputs = comp_info.get("outputs", [])
        h = max(40.0, max(len(inputs), len(outputs)) * 24.0 + 20.0)
        w = 90.0

        attr = cont.create_chunk("Attributes")
        attr.add_item("Bounds", 35, [pivot[0], pivot[1], w, h])
        attr.add_item("Pivot", 31, [pivot[0] + w / 2.0, pivot[1] + h / 2.0])

        for idx, inp in enumerate(inputs):
            p_in = cont.create_chunk("param_input", idx)
            p_guid = str(uuid.uuid4())
            p_in.add_item("InstanceGuid", 9, p_guid)
            p_in.add_item("Name", 10, inp["name"])
            p_in.add_item("NickName", 10, inp.get("nickname", inp["name"]))
            p_in.add_item("Optional", 1, True)
            self.param_lut[f"{alias}.{inp['name']}"] = p_guid
            for al in inp.get("aliases", []):
                self.param_lut[f"{alias}.{al}"] = p_guid
            if inp.get("nickname"):
                self.param_lut[f"{alias}.{inp['nickname']}"] = p_guid

        for idx, outp in enumerate(outputs):
            p_out = cont.create_chunk("param_output", idx)
            p_guid = str(uuid.uuid4())
            p_out.add_item("InstanceGuid", 9, p_guid)
            p_out.add_item("Name", 10, outp["name"])
            p_out.add_item("NickName", 10, outp.get("nickname", outp["name"]))
            self.param_lut[f"{alias}.{outp['name']}"] = p_guid
            for al in outp.get("aliases", []):
                self.param_lut[f"{alias}.{al}"] = p_guid
            if outp.get("nickname"):
                self.param_lut[f"{alias}.{outp['nickname']}"] = p_guid
            if idx == 0:
                self.param_lut[f"{alias}.out"] = p_guid
                self.param_lut[f"{alias}"] = p_guid

        return inst_guid

    def add_legopod_component(
        self,
        name_or_guid: str,
        alias: str,
        pivot: Tuple[float, float],
        nickname: Optional[str] = None,
    ) -> str:
        """Instantiate any of the 42 LegoPod plugin components by name or GUID."""
        comp_info = find_legopod_component(name_or_guid)
        if not comp_info:
            raise KeyError(f"LegoPod component '{name_or_guid}' not found in catalog.")

        comp_guid = comp_info["guid"]
        comp_name = comp_info["name"]
        nick = nickname or comp_info.get("nickname") or comp_name
        inst_guid = str(uuid.uuid4())

        obj = self.objects_chunk.create_chunk("Object", self.object_count)
        self.object_count += 1
        obj.add_item("GUID", 9, comp_guid)
        obj.add_item("Name", 10, comp_name)

        cont = obj.create_chunk("Container")
        cont.add_item("Description", 10, comp_info.get("description", ""))
        cont.add_item("InstanceGuid", 9, inst_guid)
        cont.add_item("Name", 10, comp_name)
        cont.add_item("NickName", 10, nick)

        inputs = comp_info.get("inputs", [])
        outputs = comp_info.get("outputs", [])
        h = max(40.0, max(len(inputs), len(outputs)) * 24.0 + 20.0)
        w = 90.0

        attr = cont.create_chunk("Attributes")
        attr.add_item("Bounds", 35, [pivot[0], pivot[1], w, h])
        attr.add_item("Pivot", 31, [pivot[0] + w / 2.0, pivot[1] + h / 2.0])

        for idx, inp in enumerate(inputs):
            p_in = cont.create_chunk("param_input", idx)
            p_guid = str(uuid.uuid4())
            p_in.add_item("InstanceGuid", 9, p_guid)
            p_in.add_item("Name", 10, inp["name"])
            p_in.add_item("NickName", 10, inp.get("nickname", inp["name"]))
            p_in.add_item("Description", 10, inp.get("description", ""))
            p_in.add_item("Optional", 1, True)
            acc_str = inp.get("access", "item").lower()
            acc_val = 2 if acc_str == "tree" else (1 if acc_str == "list" else 0)
            p_in.add_item("Access", 3, acc_val)

            self.param_lut[f"{alias}.{inp['name']}"] = p_guid
            if inp.get("nickname"):
                self.param_lut[f"{alias}.{inp['nickname']}"] = p_guid

        for idx, outp in enumerate(outputs):
            p_out = cont.create_chunk("param_output", idx)
            p_guid = str(uuid.uuid4())
            p_out.add_item("InstanceGuid", 9, p_guid)
            p_out.add_item("Name", 10, outp["name"])
            p_out.add_item("NickName", 10, outp.get("nickname", outp["name"]))
            p_out.add_item("Description", 10, outp.get("description", ""))

            self.param_lut[f"{alias}.{outp['name']}"] = p_guid
            if outp.get("nickname"):
                self.param_lut[f"{alias}.{outp['nickname']}"] = p_guid
            if idx == 0:
                self.param_lut[f"{alias}.out"] = p_guid
                self.param_lut[f"{alias}"] = p_guid

        return inst_guid

    def add_magpie_component(
        self,
        name_or_guid: str,
        alias: str,
        pivot: Tuple[float, float],
        nickname: Optional[str] = None,
    ) -> str:
        """Instantiate any of the 14 Magpie machine-learning components by name or GUID."""
        comp_info = find_magpie_component(name_or_guid)
        if not comp_info:
            raise KeyError(f"Magpie component '{name_or_guid}' not found in catalog.")

        comp_guid = comp_info["guid"]
        comp_name = comp_info["name"]
        nick = nickname or comp_info.get("nickname") or comp_name
        inst_guid = str(uuid.uuid4())

        obj = self.objects_chunk.create_chunk("Object", self.object_count)
        self.object_count += 1
        obj.add_item("GUID", 9, comp_guid)
        obj.add_item("Name", 10, comp_name)

        cont = obj.create_chunk("Container")
        cont.add_item("Description", 10, comp_info.get("description", ""))
        cont.add_item("InstanceGuid", 9, inst_guid)
        cont.add_item("Name", 10, comp_name)
        cont.add_item("NickName", 10, nick)

        inputs = comp_info.get("inputs", [])
        outputs = comp_info.get("outputs", [])
        h = max(40.0, max(len(inputs), len(outputs)) * 24.0 + 20.0)
        w = 90.0

        attr = cont.create_chunk("Attributes")
        attr.add_item("Bounds", 35, [pivot[0], pivot[1], w, h])
        attr.add_item("Pivot", 31, [pivot[0] + w / 2.0, pivot[1] + h / 2.0])

        for idx, inp in enumerate(inputs):
            p_in = cont.create_chunk("param_input", idx)
            p_guid = str(uuid.uuid4())
            p_in.add_item("InstanceGuid", 9, p_guid)
            p_in.add_item("Name", 10, inp["name"])
            p_in.add_item("NickName", 10, inp.get("nickname", inp["name"]))
            p_in.add_item("Description", 10, inp.get("description", ""))
            p_in.add_item("Optional", 1, True)
            acc_str = inp.get("access", "item").lower()
            acc_val = 2 if acc_str == "tree" else (1 if acc_str == "list" else 0)
            p_in.add_item("Access", 3, acc_val)

            self.param_lut[f"{alias}.{inp['name']}"] = p_guid
            if inp.get("nickname"):
                self.param_lut[f"{alias}.{inp['nickname']}"] = p_guid

        for idx, outp in enumerate(outputs):
            p_out = cont.create_chunk("param_output", idx)
            p_guid = str(uuid.uuid4())
            p_out.add_item("InstanceGuid", 9, p_guid)
            p_out.add_item("Name", 10, outp["name"])
            p_out.add_item("NickName", 10, outp.get("nickname", outp["name"]))
            p_out.add_item("Description", 10, outp.get("description", ""))

            self.param_lut[f"{alias}.{outp['name']}"] = p_guid
            if outp.get("nickname"):
                self.param_lut[f"{alias}.{outp['nickname']}"] = p_guid
            if idx == 0:
                self.param_lut[f"{alias}.out"] = p_guid
                self.param_lut[f"{alias}"] = p_guid

        return inst_guid

    def add_component(
        self,
        name_or_guid: str,
        alias: str,
        pivot: Tuple[float, float],
        nickname: Optional[str] = None,
    ) -> str:
        """Instantiate any component (searching Native, Heteroptera, LegoPod, or Magpie)."""
        comp_nat = find_native_component(name_or_guid)
        if comp_nat:
            return self.add_native_component(name_or_guid, alias, pivot, nickname)
        comp_het = find_heteroptera_component(name_or_guid)
        if comp_het:
            return self.add_heteroptera_component(name_or_guid, alias, pivot, nickname)
        comp_lego = find_legopod_component(name_or_guid)
        if comp_lego:
            return self.add_legopod_component(name_or_guid, alias, pivot, nickname)
        comp_mag = find_magpie_component(name_or_guid)
        if comp_mag:
            return self.add_magpie_component(name_or_guid, alias, pivot, nickname)
        raise KeyError(
            f"Component '{name_or_guid}' not found in Native, Heteroptera, LegoPod, or Magpie catalogs."
        )

    def add_space_syntax_pipeline(self, start_pivot: Tuple[float, float] = (100, 100)) -> Dict[str, str]:
        """Synthesizes the standard Heteroptera Space Syntax analysis pipeline."""
        x, y = start_pivot
        ids = {}
        ids["center"] = self.add_heteroptera_component("Center", "center", (x + 200, y))
        ids["adj"] = self.add_heteroptera_component("Topology Of Adjacencies", "adj", (x + 200, y + 120))
        ids["recon"] = self.add_heteroptera_component("Reconstruct Topology", "recon", (x + 420, y + 60))
        ids["s_src"] = self.add_slider("s_src", "SourceNode", 0, 20, 0, (x + 420, y + 200))
        ids["s_depth"] = self.add_slider("s_depth", "Depth", 1, 15, 6, (x + 420, y + 260))
        ids["ss"] = self.add_heteroptera_component("Space Syntax", "ss", (x + 640, y + 100))
        ids["norm"] = self.add_heteroptera_component("Normalizer", "norm", (x + 860, y + 100))

        self.connect("adj.Cell→Cell", "recon.Node→Node")
        self.connect("center.Center", "recon.Points (Optional)")
        self.connect("recon.Node→Node", "ss.Node→Node")
        self.connect("s_src.out", "ss.Source")
        self.connect("s_depth.out", "ss.Depth")
        self.connect("ss.Node SpaceSyntax", "norm.Numbers")
        return ids

    def add_spatial_ml_metadata_pipeline(
        self,
        start_pivot: Tuple[float, float] = (100, 100),
        cluster_count: int = 4,
        source_node: int = 0,
        depth: int = 6,
    ) -> Dict[str, str]:
        """Synthesize a complete Tri-Plugin pipeline fusing:
        1. Heteroptera: Spatial adjacency network + Space Syntax integration + Normalizer
        2. Magpie: Clustering Machine (unsupervised spatial classification)
        3. LegoPod: User-Dictionary packaging with cluster tags + Custom Attribute definition
        """
        x, y = start_pivot
        ids = {}

        # --- Phase 1: Heteroptera Topological Analysis ---
        ids["center"] = self.add_heteroptera_component("Center", "center", (x + 220, y))
        ids["adj"] = self.add_heteroptera_component("Topology Of Adjacencies", "adj", (x + 220, y + 140))
        ids["recon"] = self.add_heteroptera_component("Reconstruct Topology", "recon", (x + 460, y + 70))
        ids["s_src"] = self.add_slider("s_src", "SourceNode", 0, 20, source_node, (x + 460, y + 210))
        ids["s_depth"] = self.add_slider("s_depth", "Depth", 1, 15, depth, (x + 460, y + 270))
        ids["ss"] = self.add_heteroptera_component("Space Syntax", "ss", (x + 700, y + 100))
        ids["norm"] = self.add_heteroptera_component("Normalizer", "norm", (x + 940, y + 100))

        # --- Phase 2: Magpie Unsupervised Machine Learning ---
        ids["s_clusters"] = self.add_slider("s_clusters", "ClusterCount", 2, 10, cluster_count, (x + 940, y + 210))
        ids["cluster"] = self.add_magpie_component("Clustering Machine", "cluster", (x + 1180, y + 100))
        ids["pca"] = self.add_magpie_component("PCA Machine", "pca", (x + 1180, y + 240))

        # --- Phase 3: LegoPod BIM Metadata & Object Packaging ---
        ids["dict"] = self.add_legopod_component("User Dictionary", "dict", (x + 1420, y + 100))
        ids["att"] = self.add_legopod_component("Build Attribute", "att", (x + 1660, y + 100))

        # --- Wire Topology ---
        # Heteroptera wiring
        self.connect("adj.Cell→Cell", "recon.Node→Node")
        self.connect("center.Center", "recon.Points (Optional)")
        self.connect("recon.Node→Node", "ss.Node→Node")
        self.connect("s_src.out", "ss.Source")
        self.connect("s_depth.out", "ss.Depth")
        self.connect("ss.Node SpaceSyntax", "norm.Numbers")

        # Heteroptera -> Magpie wiring
        self.connect("norm.Numbers", "cluster.Inputs")
        self.connect("s_clusters.out", "cluster.Clusters")
        self.connect("norm.Numbers", "pca.Data")

        # Magpie -> LegoPod wiring
        self.connect("cluster.ClusterNumber", "dict.Values")
        self.connect("dict.Dictionary", "att.Dictionary")

        return ids

    def add_generative_field_block_pipeline(
        self,
        start_pivot: Tuple[float, float] = (100, 100),
    ) -> Dict[str, str]:
        """Synthesize a Generative Morphogenesis Tri-Plugin pipeline:
        1. Heteroptera: Field Booster + Curvature Field dynamics
        2. Magpie: PCA Machine dimensionality reduction on field deformation
        3. LegoPod: Define Block + Custom Attribute instantiation
        """
        x, y = start_pivot
        ids = {}

        # Heteroptera Vector Fields
        ids["curv_field"] = self.add_heteroptera_component("Curvature Field", "curv_field", (x + 220, y))
        ids["booster"] = self.add_heteroptera_component("Field Booster", "booster", (x + 460, y))
        ids["s_boost"] = self.add_slider("s_boost", "BoostFactor", 0.1, 5.0, 1.5, (x + 220, y + 140))

        # Magpie Analysis
        ids["pca"] = self.add_magpie_component("PCA Machine", "pca", (x + 700, y))
        ids["corr"] = self.add_magpie_component("Correlation Matrix", "corr", (x + 700, y + 140))

        # LegoPod Modular Block Packaging
        ids["att"] = self.add_legopod_component("Build Attribute", "att", (x + 940, y))
        ids["def_block"] = self.add_legopod_component("Define Block", "def_block", (x + 1180, y))

        # Wiring
        self.connect("curv_field.Field", "booster.Field")
        self.connect("s_boost.out", "booster.Boost")
        self.connect("att.Attribute", "def_block.Attributes (Optional)")

        return ids

    def save_gh(self, path: str):
        write_gh_binary(self.archive, path, compress=True)

    def save_ghx(self, path: str):
        write_ghx(self.archive, path)


# ==============================================================================
# 6.5 Live Rhino 8 & Grasshopper Bridge
# ==============================================================================

def find_rhinocode() -> Optional[str]:
    """Locate the rhinocode CLI on macOS or in PATH."""
    standard_mac_path = "/Applications/Rhino 8.app/Contents/Resources/bin/rhinocode"
    if os.path.isfile(standard_mac_path) and os.access(standard_mac_path, os.X_OK):
        return standard_mac_path
    which_path = shutil.which("rhinocode")
    if which_path:
        return which_path
    return None


def get_rhino_env() -> Dict[str, str]:
    """Prepare environment variables with .NET roll forward enabled for Rhino 8."""
    env = os.environ.copy()
    env["DOTNET_ROLL_FORWARD"] = "LatestMajor"
    return env


def get_bridge_tmp_dir() -> str:
    """Get a persistent user-level directory for script exchange."""
    bridge_dir = os.path.expanduser("~/.gh_toolkit/bridge")
    os.makedirs(bridge_dir, exist_ok=True)
    return bridge_dir


def is_rhino_running() -> bool:
    """Check if any Rhino 8 instance is running with an active script server."""
    instances = get_rhino_instances()
    return len(instances) > 0


def get_rhino_instances() -> List[Dict[str, Any]]:
    """List running Rhino instances via rhinocode list."""
    rhinocode_bin = find_rhinocode()
    if not rhinocode_bin:
        return []

    try:
        res = subprocess.run(
            [rhinocode_bin, "list"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=get_rhino_env(),
            timeout=5,
        )
        if res.returncode != 0:
            return []

        lines = res.stdout.strip().splitlines()
        instances = []
        for line in lines[1:]:
            parts = line.strip().split()
            if len(parts) >= 2 and parts[0].isdigit():
                instances.append({
                    "pid": int(parts[0]),
                    "pipe_id": parts[1],
                    "doc": parts[2] if len(parts) > 2 else None,
                    "path": parts[3] if len(parts) > 3 else None,
                })
        return instances
    except Exception:
        return []


def find_rhino_bridge() -> Optional[str]:
    """Locate the native rhino_bridge helper binary."""
    # Look next to package or in ~/.gh_toolkit/bin or PATH
    local_bin = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "gh_toolkit", "bin", "rhino_bridge")
    if os.path.isfile(local_bin) and os.access(local_bin, os.X_OK):
        return local_bin
    which_path = shutil.which("rhino_bridge")
    if which_path:
        return which_path
    return None


def run_in_rhino(python_code: str, instance_id: Optional[str] = None, timeout: int = 15) -> Dict[str, Any]:
    """Execute a Python snippet inside running Rhino 8 instance via rhino_bridge or rhinocode."""
    bridge_bin = find_rhino_bridge()
    rhinocode_bin = find_rhinocode()
    if not bridge_bin and not rhinocode_bin:
        return {
            "success": False,
            "error": "Neither rhino_bridge nor rhinocode CLI found. Ensure Rhino 8 is installed."
        }

    instances = get_rhino_instances()
    target_pipe = instance_id
    if not target_pipe and instances:
        target_pipe = instances[0]["pipe_id"]

    bridge_dir = get_bridge_tmp_dir()
    temp_id = uuid.uuid4().hex[:8]
    script_path = os.path.join(bridge_dir, f"cmd_{temp_id}.py")
    result_path = os.path.join(bridge_dir, f"res_{temp_id}.json")

    wrapper = f"""# -*- coding: utf-8 -*-
import sys
import os
import json
import traceback

__RESULT_PATH__ = {repr(result_path)}
__TMP_PATH__ = {repr(result_path + ".tmp")}

try:
    __str_types = (str, unicode)
except NameError:
    __str_types = (str,)

def __clean(val):
    if val is None:
        return None
    if isinstance(val, (int, float, bool) + __str_types):
        return val
    if isinstance(val, dict):
        return {{str(k): __clean(v) for k, v in val.items()}}
    if isinstance(val, (list, tuple)):
        return [__clean(x) for x in val]
    return str(val)

def __execute():
{chr(10).join('    ' + line for line in python_code.strip().splitlines())}

try:
    __res = __execute()
    with open(__TMP_PATH__, 'w') as __f:
        json.dump({{'success': True, 'result': __clean(__res)}}, __f, indent=2)
    if os.path.exists(__RESULT_PATH__):
        try:
            os.remove(__RESULT_PATH__)
        except Exception:
            pass
    os.rename(__TMP_PATH__, __RESULT_PATH__)
except Exception as __e:
    with open(__TMP_PATH__, 'w') as __f:
        json.dump({{'success': False, 'error': str(__e), 'traceback': traceback.format_exc()}}, __f, indent=2)
    if os.path.exists(__RESULT_PATH__):
        try:
            os.remove(__RESULT_PATH__)
        except Exception:
            pass
    os.rename(__TMP_PATH__, __RESULT_PATH__)
"""

    with open(script_path, "w", encoding="utf-8") as f:
        f.write(wrapper)

    if bridge_bin:
        cmd = [bridge_bin, script_path]
        if target_pipe:
            cmd.append(target_pipe)
    else:
        cmd = [rhinocode_bin]
        if target_pipe:
            cmd.extend(["-r", target_pipe])
        cmd.extend(["script", script_path])

    try:
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=get_rhino_env(),
            timeout=timeout,
        )

        # Wait for result payload (Rhino executes asynchronously on main loop, typically 50-150ms)
        start_t = time.time()
        data = None
        while time.time() - start_t < timeout:
            if os.path.exists(result_path):
                try:
                    with open(result_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    break
                except (ValueError, json.JSONDecodeError):
                    # File may be mid-write or partially flushed
                    time.sleep(0.05)
                    continue
            time.sleep(0.05)

        if data is None:
            hint = "Ensure 'StartScriptServer' is running in Rhino 8."
            err_msg = proc.stderr.strip() or proc.stdout.strip()
            return {
                "success": False,
                "error": f"Rhino script produced no valid result payload. {err_msg} ({hint})",
                "stderr": proc.stderr,
                "stdout": proc.stdout,
            }

        return data

    except subprocess.TimeoutExpired:
        return {"success": False, "error": f"Execution timed out after {timeout} seconds"}
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        for path_to_clean in (script_path, result_path, result_path + ".tmp"):
            if os.path.exists(path_to_clean):
                try:
                    os.remove(path_to_clean)
                except Exception:
                    pass


def live_status() -> Dict[str, Any]:
    """Get status of running Rhino, Grasshopper canvas, and active document."""
    instances = get_rhino_instances()
    if not instances:
        return {
            "rhino_running": False,
            "error": "Rhino 8 is not running or script server is not active. Run 'StartScriptServer' in Rhino 8 command line."
        }

    script = """
import Rhino
import Grasshopper

canvas = Grasshopper.Instances.ActiveCanvas
doc_server = Grasshopper.Instances.DocumentServer
active_doc = canvas.Document if canvas else None

docs = []
if doc_server:
    for d in doc_server:
        docs.append({
            'name': str(d.DisplayName),
            'file_path': str(d.FilePath) if d.FilePath else None,
            'object_count': d.ObjectCount,
            'modified': d.Modified
        })

active_info = None
if active_doc:
    active_info = {
        'name': str(active_doc.DisplayName),
        'file_path': str(active_doc.FilePath) if active_doc.FilePath else None,
        'object_count': active_doc.ObjectCount,
        'modified': active_doc.Modified
    }

return {
    'rhino_version': str(Rhino.RhinoApp.Version),
    'rhino_doc': Rhino.RhinoDoc.ActiveDoc.Name if Rhino.RhinoDoc.ActiveDoc else None,
    'canvas_available': canvas is not None,
    'documents_count': len(docs),
    'documents': docs,
    'active_document': active_info
}
"""
    res = run_in_rhino(script)
    if res.get("success"):
        res_data = res.get("result", {})
        res_data["rhino_running"] = True
        res_data["instances"] = instances
        return res_data
    return {"rhino_running": True, "instances": instances, "error": res.get("error")}


def live_list_objects() -> Dict[str, Any]:
    """List all components and parameters on the active Grasshopper canvas with their pins and wires."""
    script = """
import Rhino
import Grasshopper
import Grasshopper.Kernel as gh_kernel

canvas = Grasshopper.Instances.ActiveCanvas
doc = canvas.Document if canvas else None

if not doc:
    return {'error': 'No active Grasshopper document found on canvas'}

objects = []
for obj in doc.Objects:
    pivot = obj.Attributes.Pivot
    info = {
        'instance_guid': str(obj.InstanceGuid),
        'component_guid': str(obj.ComponentGuid),
        'name': str(obj.Name),
        'nickname': str(obj.NickName),
        'category': str(obj.Category),
        'subcategory': str(obj.SubCategory),
        'type': type(obj).__name__,
        'pivot': [round(pivot.X, 1), round(pivot.Y, 1)],
        'locked': obj.Locked,
        'hidden': getattr(obj, 'Hidden', False)
    }

    if isinstance(obj, gh_kernel.IGH_Component):
        inputs = []
        for p in obj.Params.Input:
            sources = [str(s.InstanceGuid) for s in p.Sources]
            inputs.append({
                'name': str(p.Name),
                'nickname': str(p.NickName),
                'instance_guid': str(p.InstanceGuid),
                'sources': sources,
                'type_name': str(p.TypeName)
            })
        outputs = []
        for p in obj.Params.Output:
            recipients = [str(r.InstanceGuid) for r in p.Recipients]
            outputs.append({
                'name': str(p.Name),
                'nickname': str(p.NickName),
                'instance_guid': str(p.InstanceGuid),
                'recipients': recipients,
                'type_name': str(p.TypeName)
            })
        info['inputs'] = inputs
        info['outputs'] = outputs
    elif isinstance(obj, gh_kernel.IGH_Param):
        sources = [str(s.InstanceGuid) for s in obj.Sources]
        recipients = [str(r.InstanceGuid) for r in obj.Recipients]
        info['sources'] = sources
        info['recipients'] = recipients
        info['type_name'] = str(obj.TypeName)

    tname = type(obj).__name__
    if 'Slider' in tname or hasattr(obj, 'Slider'):
        try:
            info['value'] = float(obj.Slider.Value)
            info['min'] = float(obj.Slider.Minimum)
            info['max'] = float(obj.Slider.Maximum)
        except Exception:
            pass
    elif 'Panel' in tname or hasattr(obj, 'UserText'):
        try:
            info['value'] = str(obj.UserText)
        except Exception:
            pass
    elif 'BooleanToggle' in tname or hasattr(obj, 'Value'):
        try:
            info['value'] = bool(obj.Value)
        except Exception:
            pass

    objects.append(info)

return {
    'doc_name': str(doc.DisplayName),
    'total_objects': len(objects),
    'objects': objects
}
"""
    res = run_in_rhino(script)
    if res.get("success"):
        return res.get("result", {})
    return {"error": res.get("error")}


def live_add_component(name_or_guid: str, x: float = 100.0, y: float = 100.0, nickname: Optional[str] = None) -> Dict[str, Any]:
    """Add a component or parameter to active Grasshopper document."""
    script = f"""
import System
from System.Drawing import PointF
import Rhino
import Grasshopper
import Grasshopper.Kernel as gh_kernel

canvas = Grasshopper.Instances.ActiveCanvas
doc = canvas.Document if canvas else None

if not doc:
    doc = gh_kernel.GH_Document()
    Grasshopper.Instances.DocumentServer.AddDocument(doc)
    if canvas:
        canvas.Document = doc

target_str = {repr(name_or_guid)}
comp_server = Grasshopper.Instances.ComponentServer

proxy = None
try:
    guid = System.Guid(target_str)
    proxy = comp_server.EmitObjectProxy(guid)
except Exception:
    pass

if not proxy:
    proxy = comp_server.FindObjectByName(target_str, True, True)

if not proxy:
    return {{'success': False, 'error': "Component '{{}}' not found in ComponentServer.".format(target_str)}}

instance = proxy.CreateInstance()
if not instance:
    return {{'success': False, 'error': "Failed to instantiate component '{{}}'.".format(target_str)}}

instance.CreateAttributes()
instance.Attributes.Pivot = PointF(float({x}), float({y}))

custom_nick = {repr(nickname)}
if custom_nick:
    instance.NickName = custom_nick

doc.AddObject(instance, False)
doc.NewSolution(False)
if canvas:
    canvas.Refresh()

return {{
    'success': True,
    'instance_guid': str(instance.InstanceGuid),
    'component_guid': str(instance.ComponentGuid),
    'name': str(instance.Name),
    'nickname': str(instance.NickName),
    'category': str(instance.Category),
    'pivot': [float({x}), float({y})]
}}
"""
    res = run_in_rhino(script)
    if res.get("success"):
        return res.get("result", {})
    return {"success": False, "error": res.get("error")}


def live_remove_object(target_id_or_name: str) -> Dict[str, Any]:
    """Remove a component from active canvas by instance GUID, name, or nickname."""
    script = f"""
import Grasshopper

canvas = Grasshopper.Instances.ActiveCanvas
doc = canvas.Document if canvas else None

if not doc:
    return {{'success': False, 'error': 'No active Grasshopper document'}}

target = {repr(str(target_id_or_name).lower())}
to_remove = []

for obj in doc.Objects:
    iguid = str(obj.InstanceGuid).lower()
    cguid = str(obj.ComponentGuid).lower()
    name = str(obj.Name).lower()
    nick = str(obj.NickName).lower()
    if target in (iguid, cguid, name, nick):
        to_remove.append(obj)

if not to_remove:
    return {{'success': False, 'error': "No object matching '{{}}' found on canvas".format(target)}}

removed = []
for obj in to_remove:
    doc.RemoveObject(obj, False)
    removed.append(str(obj.InstanceGuid))

doc.NewSolution(False)
if canvas:
    canvas.Refresh()

return {{'success': True, 'removed_count': len(removed), 'removed_guids': removed}}
"""
    res = run_in_rhino(script)
    if res.get("success"):
        return res.get("result", {})
    return {"success": False, "error": res.get("error")}


def live_wire(source_id_or_name: str, target_id_or_name: str, source_pin: Union[int, str] = 0, target_pin: Union[int, str] = 0) -> Dict[str, Any]:
    """Connect an output pin of source component to an input pin of target component."""
    script = f"""
import Grasshopper
import Grasshopper.Kernel as gh_kernel

canvas = Grasshopper.Instances.ActiveCanvas
doc = canvas.Document if canvas else None

if not doc:
    return {{'success': False, 'error': 'No active Grasshopper document'}}

src_target = {repr(str(source_id_or_name).lower())}
dst_target = {repr(str(target_id_or_name).lower())}

src_obj = None
dst_obj = None

for obj in doc.Objects:
    iguid = str(obj.InstanceGuid).lower()
    name = str(obj.Name).lower()
    nick = str(obj.NickName).lower()
    if not src_obj and src_target in (iguid, name, nick):
        src_obj = obj
    if not dst_obj and dst_target in (iguid, name, nick):
        dst_obj = obj

if not src_obj:
    return {{'success': False, 'error': "Source object '{{}}' not found".format(src_target)}}
if not dst_obj:
    return {{'success': False, 'error': "Target object '{{}}' not found".format(dst_target)}}

src_param = None
if isinstance(src_obj, gh_kernel.IGH_Component):
    outputs = src_obj.Params.Output
    s_pin = {repr(source_pin)}
    if isinstance(s_pin, int) and 0 <= s_pin < outputs.Count:
        src_param = outputs[s_pin]
    else:
        s_pin_str = str(s_pin).lower()
        for p in outputs:
            if p.Name.lower() == s_pin_str or p.NickName.lower() == s_pin_str:
                src_param = p
                break
elif isinstance(src_obj, gh_kernel.IGH_Param):
    src_param = src_obj

if not src_param:
    return {{'success': False, 'error': "Could not resolve output pin '{{}}' on source object".format({repr(source_pin)})}}

dst_param = None
if isinstance(dst_obj, gh_kernel.IGH_Component):
    inputs = dst_obj.Params.Input
    d_pin = {repr(target_pin)}
    if isinstance(d_pin, int) and 0 <= d_pin < inputs.Count:
        dst_param = inputs[d_pin]
    else:
        d_pin_str = str(d_pin).lower()
        for p in inputs:
            if p.Name.lower() == d_pin_str or p.NickName.lower() == d_pin_str:
                dst_param = p
                break
elif isinstance(dst_obj, gh_kernel.IGH_Param):
    dst_param = dst_obj

if not dst_param:
    return {{'success': False, 'error': "Could not resolve input pin '{{}}' on target object".format({repr(target_pin)})}}

dst_param.AddSource(src_param)
doc.NewSolution(False)
if canvas:
    canvas.Refresh()

return {{
    'success': True,
    'source': {{'name': str(src_obj.Name), 'instance_guid': str(src_obj.InstanceGuid), 'output': str(src_param.Name)}},
    'target': {{'name': str(dst_obj.Name), 'instance_guid': str(dst_obj.InstanceGuid), 'input': str(dst_param.Name)}}
}}
"""
    res = run_in_rhino(script)
    if res.get("success"):
        return res.get("result", {})
    return {"success": False, "error": res.get("error")}


def live_unwire(target_id_or_name: str, target_pin: Union[int, str] = 0, source_id_or_name: Optional[str] = None) -> Dict[str, Any]:
    """Disconnect wire(s) leading into target input pin."""
    script = f"""
import Grasshopper
import Grasshopper.Kernel as gh_kernel

canvas = Grasshopper.Instances.ActiveCanvas
doc = canvas.Document if canvas else None

if not doc:
    return {{'success': False, 'error': 'No active Grasshopper document'}}

dst_target = {repr(str(target_id_or_name).lower())}
dst_obj = None

for obj in doc.Objects:
    iguid = str(obj.InstanceGuid).lower()
    name = str(obj.Name).lower()
    nick = str(obj.NickName).lower()
    if dst_target in (iguid, name, nick):
        dst_obj = obj
        break

if not dst_obj:
    return {{'success': False, 'error': "Target object '{{}}' not found".format(dst_target)}}

dst_param = None
if isinstance(dst_obj, gh_kernel.IGH_Component):
    inputs = dst_obj.Params.Input
    d_pin = {repr(target_pin)}
    if isinstance(d_pin, int) and 0 <= d_pin < inputs.Count:
        dst_param = inputs[d_pin]
    else:
        d_pin_str = str(d_pin).lower()
        for p in inputs:
            if p.Name.lower() == d_pin_str or p.NickName.lower() == d_pin_str:
                dst_param = p
                break
elif isinstance(dst_obj, gh_kernel.IGH_Param):
    dst_param = dst_obj

if not dst_param:
    return {{'success': False, 'error': "Could not resolve input pin '{{}}' on target object".format({repr(target_pin)})}}

src_target = {repr(str(source_id_or_name).lower() if source_id_or_name else None)}
disconnected = 0

if src_target:
    to_remove = []
    for s in dst_param.Sources:
        parent_obj = s.Attributes.GetTopLevel.DocObject
        if src_target in (str(s.InstanceGuid).lower(), str(parent_obj.Name).lower(), str(parent_obj.NickName).lower()):
            to_remove.append(s)
    for s in to_remove:
        dst_param.RemoveSource(s)
        disconnected += 1
else:
    disconnected = dst_param.Sources.Count
    dst_param.Sources.Clear()

doc.NewSolution(False)
if canvas:
    canvas.Refresh()

return {{
    'success': True,
    'disconnected_count': disconnected,
    'target': str(dst_obj.Name),
    'input': str(dst_param.Name)
}}
"""
    res = run_in_rhino(script)
    if res.get("success"):
        return res.get("result", {})
    return {"success": False, "error": res.get("error")}


def live_set_value(target_id_or_name: str, value: Any) -> Dict[str, Any]:
    """Set the value of a Number Slider, Panel text, or Boolean Toggle on canvas."""
    script = f"""
import sys
import System
import Grasshopper

canvas = Grasshopper.Instances.ActiveCanvas
doc = canvas.Document if canvas else None

if not doc:
    return {{'success': False, 'error': 'No active Grasshopper document'}}

target = {repr(str(target_id_or_name).lower())}
target_obj = None

for obj in doc.Objects:
    iguid = str(obj.InstanceGuid).lower()
    name = str(obj.Name).lower()
    nick = str(obj.NickName).lower()
    if target in (iguid, name, nick):
        target_obj = obj
        break

if not target_obj:
    return {{'success': False, 'error': "Object '{{}}' not found on canvas".format(target)}}

val = {repr(value)}
tname = type(target_obj).__name__
updated_type = None

if 'Slider' in tname or hasattr(target_obj, 'Slider'):
    try:
        target_obj.Slider.Value = System.Decimal(float(val))
    except Exception:
        target_obj.Slider.Value = float(val)
    target_obj.ExpireSolution(False)
    updated_type = 'Slider'
elif 'Panel' in tname or hasattr(target_obj, 'UserText'):
    target_obj.UserText = str(val)
    target_obj.ExpireSolution(False)
    updated_type = 'Panel'
elif 'BooleanToggle' in tname or hasattr(target_obj, 'Value'):
    target_obj.Value = bool(val if isinstance(val, bool) else (str(val).lower() in ('true', '1', 'yes')))
    target_obj.ExpireSolution(False)
    updated_type = 'BooleanToggle'
else:
    return {{'success': False, 'error': "Object type '{{}}' does not support live value mutation".format(tname)}}

doc.NewSolution(False)
if canvas:
    canvas.Refresh()

return {{
    'success': True,
    'object': str(target_obj.Name),
    'instance_guid': str(target_obj.InstanceGuid),
    'type': updated_type,
    'new_value': val
}}
"""
    res = run_in_rhino(script)
    if res.get("success"):
        return res.get("result", {})
    return {"success": False, "error": res.get("error")}


def live_solve() -> Dict[str, Any]:
    """Force recomputation of the active Grasshopper document and refresh canvas."""
    script = """
import Grasshopper

canvas = Grasshopper.Instances.ActiveCanvas
doc = canvas.Document if canvas else None

if not doc:
    return {'success': False, 'error': 'No active Grasshopper document'}

doc.NewSolution(False)
if canvas:
    canvas.Refresh()

return {
    'success': True,
    'doc_name': str(doc.DisplayName),
    'objects_count': doc.ObjectCount
}
"""
    res = run_in_rhino(script)
    if res.get("success"):
        return res.get("result", {})
    return {"success": False, "error": res.get("error")}


def live_save(filepath: Optional[str] = None) -> Dict[str, Any]:
    """Save the active Grasshopper document quietly without prompting."""
    script = f"""
import Grasshopper
import Grasshopper.Kernel as gh_kernel

canvas = Grasshopper.Instances.ActiveCanvas
doc = canvas.Document if canvas else None

if not doc:
    return {{'success': False, 'error': 'No active Grasshopper document'}}

path = {repr(filepath)} or doc.FilePath
if not path:
    return {{'success': False, 'error': 'No target file path specified and document has no existing FilePath'}}

doc_io = gh_kernel.GH_DocumentIO(doc)
saved = doc_io.SaveQuiet(path)

return {{
    'success': bool(saved),
    'file_path': str(path),
    'objects_count': doc.ObjectCount
}}
"""
    res = run_in_rhino(script)
    if res.get("success"):
        return res.get("result", {})
    return {"success": False, "error": res.get("error")}


def live_open(filepath: str) -> Dict[str, Any]:
    """Open a .gh or .ghx file directly into the active Grasshopper canvas."""
    abs_path = os.path.abspath(filepath)
    if not os.path.exists(abs_path):
        return {"success": False, "error": f"File does not exist: {abs_path}"}

    script = f"""
import Grasshopper
import Grasshopper.Kernel as gh_kernel

target = {repr(abs_path)}
canvas = Grasshopper.Instances.ActiveCanvas
doc_server = Grasshopper.Instances.DocumentServer

doc_io = gh_kernel.GH_DocumentIO()
opened = doc_io.Open(target)

if not opened or not doc_io.Document:
    return {{'success': False, 'error': "Failed to open definition from {{}}".format(target)}}

new_doc = doc_io.Document
if doc_server:
    doc_server.AddDocument(new_doc)
if canvas:
    canvas.Document = new_doc
    canvas.Refresh()

return {{
    'success': True,
    'file_path': str(target),
    'doc_name': str(new_doc.DisplayName),
    'objects_count': new_doc.ObjectCount
}}
"""
    res = run_in_rhino(script)
    if res.get("success"):
        return res.get("result", {})
    return {"success": False, "error": res.get("error")}


# ==============================================================================
# 7. CLI Utilities
# ==============================================================================


def main():
    parser = argparse.ArgumentParser(description="Grasshopper Definition Toolkit CLI")
    subparsers = parser.add_subparsers(dest="cmd", help="Sub-command")

    p_info = subparsers.add_parser("info", help="Inspect file metadata and components")
    p_info.add_argument("file", help="Path to .gh or .ghx file")

    p_to_ghx = subparsers.add_parser("to-ghx", help="Convert .gh binary to .ghx XML")
    p_to_ghx.add_argument("input", help="Input .gh file")
    p_to_ghx.add_argument("output", help="Output .ghx file")

    p_to_gh = subparsers.add_parser("to-gh", help="Convert .ghx XML to .gh binary")
    p_to_gh.add_argument("input", help="Input .ghx file")
    p_to_gh.add_argument("output", help="Output .gh file")

    p_to_json = subparsers.add_parser("to-json", help="Convert .gh/.ghx to JSON Graph IR")
    p_to_json.add_argument("input", help="Input file")
    p_to_json.add_argument("output", help="Output .json file")

    p_scripts = subparsers.add_parser("extract-scripts", help="Extract embedded Python/C# scripts")
    p_scripts.add_argument("target", help="File or directory of .gh/.ghx files")
    p_scripts.add_argument("--out", "-o", default="./extracted_scripts", help="Output directory")


    p_het = subparsers.add_parser("heteroptera", help="Inspect and audit Heteroptera components and pipelines")
    p_het.add_argument("--list", nargs="?", const="all", help="List Heteroptera components (optional subcategory filter)")
    p_het.add_argument("--info", help="Get detailed input/output schema for a component name or GUID")
    p_het.add_argument("--audit", help="Audit a .gh/.ghx file for Heteroptera components and pipelines")
    p_het.add_argument("--recipes", action="store_true", help="Display canonical Heteroptera wiring recipes")
    p_het.add_argument("--status", action="store_true", help="Check Heteroptera installation status & latest version")
    p_het.add_argument("--install", action="store_true", help="Install or upgrade Heteroptera to latest release via Yak")
    p_het.add_argument("--force", action="store_true", help="Force reinstall even if up to date")

    p_nat = subparsers.add_parser("native", help="Inspect verified native Grasshopper components (211 cataloged)")
    p_nat.add_argument("--list", nargs="?", const="all", help="List native components (optional category filter, e.g. Curve, Surface, Vector, Sets)")
    p_nat.add_argument("--info", help="Get input/output schema for a component name or GUID")

    p_lego = subparsers.add_parser("legopod", help="Inspect verified LegoPod plugin components (42 cataloged)")
    p_lego.add_argument("--list", nargs="?", const="all", help="List LegoPod components (optional subcategory filter)")
    p_lego.add_argument("--info", help="Get input/output schema for a LegoPod component name or GUID")

    p_mag = subparsers.add_parser("magpie", help="Inspect verified Magpie machine-learning components (14 cataloged)")
    p_mag.add_argument("--list", nargs="?", const="all", help="List Magpie components (optional subcategory filter)")
    p_mag.add_argument("--info", help="Get input/output schema for a Magpie component name or GUID")

    p_audit = subparsers.add_parser("audit", help="Audit a .gh/.ghx file across Native, Heteroptera, LegoPod, and Magpie with optimization advice")
    p_audit.add_argument("file", help="Path to .gh or .ghx file")

    p_synth = subparsers.add_parser("synthesize", help="Synthesize ready-to-run canonical definitions and tri-plugin pipelines")
    p_synth.add_argument("template", choices=["spatial-ml", "field-blocks", "space-syntax"], help="Template pipeline to synthesize")
    p_synth.add_argument("--out", "-o", required=True, help="Output path (.gh or .ghx)")
    p_synth.add_argument("--clusters", type=int, default=4, help="Number of clusters for spatial-ml (default: 4)")
    p_synth.add_argument("--source", type=int, default=0, help="Source node index for space syntax (default: 0)")
    p_synth.add_argument("--depth", type=int, default=6, help="Topological search depth for space syntax (default: 6)")

    # Live Rhino / Grasshopper Canvas Integration
    p_live = subparsers.add_parser("live", help="Interact directly with running Rhino 8 and active Grasshopper canvas")
    live_subs = p_live.add_subparsers(dest="live_cmd", help="Live action to execute")

    p_ls = live_subs.add_parser("status", help="Inspect connection to Rhino 8 and active Grasshopper document")

    p_ll = live_subs.add_parser("list", help="List all components, pins, and coordinates on active canvas")
    p_ll.add_argument("--json", action="store_true", help="Output full JSON DAG")

    p_la = live_subs.add_parser("add", help="Add component to active canvas")
    p_la.add_argument("name", help="Component Name or GUID")
    p_la.add_argument("--x", type=float, default=100.0, help="Canvas X coordinate (default: 100)")
    p_la.add_argument("--y", type=float, default=100.0, help="Canvas Y coordinate (default: 100)")
    p_la.add_argument("--name", "-n", dest="nickname", help="Custom NickName")

    p_lr = live_subs.add_parser("remove", help="Remove component from active canvas")
    p_lr.add_argument("target", help="Component Instance GUID, NickName, or Name")

    p_lw = live_subs.add_parser("wire", help="Connect source component output to target component input")
    p_lw.add_argument("source", help="Source component (GUID, NickName, or Name)")
    p_lw.add_argument("target", help="Target component (GUID, NickName, or Name)")
    p_lw.add_argument("--source-pin", "-s", default=0, help="Source output pin (index or name, default: 0)")
    p_lw.add_argument("--target-pin", "-t", default=0, help="Target input pin (index or name, default: 0)")

    p_lu = live_subs.add_parser("unwire", help="Disconnect input wires from target component")
    p_lu.add_argument("target", help="Target component (GUID, NickName, or Name)")
    p_lu.add_argument("--target-pin", "-t", default=0, help="Target input pin (index or name, default: 0)")
    p_lu.add_argument("--source", "-s", help="Optional specific source to disconnect")

    p_lset = live_subs.add_parser("set", help="Set value of Number Slider, Panel, or Boolean Toggle")
    p_lset.add_argument("target", help="Component (GUID, NickName, or Name)")
    p_lset.add_argument("value", help="Value to set")

    p_lsol = live_subs.add_parser("solve", help="Force recomputation of active Grasshopper document and refresh canvas")

    p_lsave = live_subs.add_parser("save", help="Save active Grasshopper document quietly")
    p_lsave.add_argument("path", nargs="?", help="Destination file path (.gh or .ghx)")

    p_lopen = live_subs.add_parser("open", help="Open definition into active Grasshopper canvas")
    p_lopen.add_argument("file", help="Path to .gh or .ghx file")

    args = parser.parse_args()


    if not args.cmd:
        parser.print_help()
        sys.exit(1)

    if args.cmd == "info":
        ext = os.path.splitext(args.file)[1].lower()
        archive = read_ghx(args.file) if ext == ".ghx" else read_gh_binary(args.file)
        graph = GHGraph.from_archive(archive)
        print(f"File: {args.file}")
        print(f"Definition Name: {graph.name}")
        print(f"Total Components: {len(graph.components)}")
        print(f"Total Wires: {len(graph.wires)}")
        print("\nComponents Sample:")
        for c in graph.components[:15]:
            print(f"  [{c.comp_id}] {c.name} ('{c.nickname}') - {len(c.inputs)} in, {len(c.outputs)} out")
            if c.script_source:
                print(f"      [Has Embedded Script: {len(c.script_source)} chars]")

    elif args.cmd == "to-ghx":
        archive = read_gh_binary(args.input)
        write_ghx(archive, args.output)
        print(f"Wrote XML Grasshopper definition to: {args.output}")

    elif args.cmd == "to-gh":
        archive = read_ghx(args.input)
        write_gh_binary(archive, args.output, compress=True)
        print(f"Wrote binary Grasshopper definition to: {args.output}")

    elif args.cmd == "to-json":
        ext = os.path.splitext(args.input)[1].lower()
        archive = read_ghx(args.input) if ext == ".ghx" else read_gh_binary(args.input)
        graph = GHGraph.from_archive(archive)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(graph.to_json())
        print(f"Wrote JSON Graph IR to: {args.output}")

    elif args.cmd == "extract-scripts":
        os.makedirs(args.out, exist_ok=True)
        files = []
        if os.path.isdir(args.target):
            for root, _, fnames in os.walk(args.target):
                for fn in fnames:
                    if fn.lower().endswith((".gh", ".ghx")):
                        files.append(os.path.join(root, fn))
        else:
            files.append(args.target)

        count = 0
        for fpath in files:
            try:
                ext = os.path.splitext(fpath)[1].lower()
                archive = read_ghx(fpath) if ext == ".ghx" else read_gh_binary(fpath)
                graph = GHGraph.from_archive(archive)
                base = os.path.splitext(os.path.basename(fpath))[0]
                for idx, c in enumerate(graph.components):
                    if c.script_source:
                        script_ext = ".cs" if "using " in c.script_source or "public class" in c.script_source else ".py"
                        out_name = f"{base}_{c.nickname or c.name}_{idx}{script_ext}"
                        out_name = "".join(ch if ch.isalnum() or ch in "._- " else "_" for ch in out_name)
                        out_path = os.path.join(args.out, out_name)
                        with open(out_path, "w", encoding="utf-8") as sf:
                            sf.write(c.script_source)
                        count += 1
                        print(f"Extracted: {out_name}")
            except Exception as e:
                print(f"Error reading {fpath}: {e}")
        print(f"Done! Extracted {count} script(s) to {args.out}")



    elif args.cmd == "heteroptera":
        if args.status:
            stat = get_heteroptera_status()
            print("=== Heteroptera Plugin Installation Status ===")
            print(f"Yak Package Manager: {'Found (' + str(stat['yak_path']) + ')' if stat['yak_found'] else 'Not Found'}")
            print(f"Installed in Rhino:  {'Yes (version ' + str(stat['installed_version']) + ')' if stat['installed'] else 'No'}")
            print(f"Latest on Yak:       {stat['latest_version'] or 'Unknown / Network error'}")
            print(f"Status:              {'Up to date' if stat['is_latest'] else ('Update Available' if stat['installed'] else 'Missing')}")
            if stat.get("packages_dir"):
                print(f"Package Directory:   {stat['packages_dir']}")
            return

        if args.install:
            print("Checking and installing Heteroptera via McNeel Yak...")
            ok, msg = install_heteroptera(force=args.force)
            print(msg)
            if not ok:
                sys.exit(1)
            return

        catalog = load_heteroptera_catalog()
        if not catalog.get("by_name"):
            print("Error: Heteroptera catalog not found. Please ensure heteroptera_catalog.json exists.")
            sys.exit(1)

        if args.recipes:
            recipes_text = (
                "=== Canonical Heteroptera Wiring Recipes ===\n\n"
                "1. Space Syntax Architectural Plan Analysis:\n"
                "   Floorplan Polylines -> Heteroptera: Center (Centroids)\n"
                "   Floorplan Polylines -> Heteroptera: Topology Of Adjacencies (Cell→Cell)\n"
                "   Cell→Cell + Centroids -> Heteroptera: Reconstruct Topology (Node→Node)\n"
                "   Node→Node + Source Node Slider -> Heteroptera: Space Syntax (Node SpaceSyntax)\n"
                "   Node SpaceSyntax -> Heteroptera: Normalizer -> Color Gradient -> Visual Plan\n\n"
                "2. Shortest Route Navigation on Proximity Network:\n"
                "   Spatial Points -> Heteroptera: Proximity Network (Node→Node)\n"
                "   Node→Node + Start + End -> Heteroptera: Shortest Route (Route)\n"
                "   Route + Points -> Heteroptera: Topology Embody -> Shortest Path Curve\n\n"
                "3. Stochastic Facade / Brick Allocation:\n"
                "   Grid Points -> Attractor -> Heteroptera: Careless Range / Weighted Allocator\n"
                "   Weights -> Heteroptera: Slingshot Allocator -> Brick rotation / offset index\n"
            )
            print(recipes_text)

        elif args.info:
            target = args.info.lower()
            comp = catalog.get("by_guid", {}).get(target)
            if not comp:
                for k, v in catalog.get("by_name", {}).items():
                    if k.lower() == target:
                        comp = v
                        break
            if not comp:
                print(f"Component '{args.info}' not found in Heteroptera catalog.")
                sys.exit(1)
            print(f"Component:    {comp['name']} [{comp.get('nickname', '')}]")
            print(f"GUID:         {comp['guid']}")
            print(f"Subcategory:  {comp.get('subcategory', 'General')}")
            print(f"Type Name:    {comp.get('type_name', '')}")
            print(f"Description:  {comp.get('description', '')}")
            print("\nInputs:")
            for inp in comp.get("inputs", []):
                print(f"  - {inp['name']} ({inp.get('nickname', '')}): {inp.get('type', '')} [{inp.get('access', 'item')}] - {inp.get('description', '')}")
            print("\nOutputs:")
            for outp in comp.get("outputs", []):
                print(f"  - {outp['name']} ({outp.get('nickname', '')}): {outp.get('type', '')} - {outp.get('description', '')}")

        elif args.audit:
            ext = os.path.splitext(args.audit)[1].lower()
            archive = read_ghx(args.audit) if ext == ".ghx" else read_gh_binary(args.audit)
            graph = GHGraph.from_archive(archive)
            guids = {c['guid'].lower(): c for c in catalog.get("by_guid", {}).values()}
            found_het = []
            for c in graph.components:
                cid = c.guid.lower()
                if cid in guids:
                    found_het.append((c, guids[cid]))
            print(f"Audit Results for: {args.audit}")
            print(f"Total Definition Components: {len(graph.components)}")
            print(f"Heteroptera Components:     {len(found_het)}")
            if found_het:
                by_sub = {}
                for c, meta in found_het:
                    by_sub.setdefault(meta.get('subcategory', 'General'), []).append(c.name)
                for sub, names in sorted(by_sub.items()):
                    print(f"  [{sub}] ({len(names)}): {', '.join(names[:6])}{'...' if len(names) > 6 else ''}")

        elif args.list:
            subcats = catalog.get("subcategories", {})
            filt = args.list.lower()
            print(f"Heteroptera Plugin Catalog ({catalog.get('total_components', 0)} components):\n")
            for sub, names in sorted(subcats.items()):
                if filt != "all" and filt != sub.lower():
                    continue
                print(f"=== {sub} ({len(names)} components) ===")
                for n in sorted(names):
                    meta = catalog.get("by_name", {}).get(n, {})
                    print(f"  * {n} [{meta.get('nickname', '')}] - GUID: {meta.get('guid', '')}")
                print()

    elif args.cmd == "native":
        catalog = load_native_catalog()
        if not catalog.get("by_name"):
            print("Error: Native catalog not found. Please ensure native_catalog.json exists.")
            sys.exit(1)

        if args.info:
            comp = find_native_component(args.info)
            if not comp:
                print(f"Component '{args.info}' not found in native catalog.")
                sys.exit(1)
            print(f"Component:    {comp['name']} [{comp.get('nickname', '')}]")
            print(f"GUID:         {comp['guid']}")
            print(f"Tab:          {comp.get('tab', 'Core')}")
            print(f"Category:     {comp.get('category', 'General')}")
            print(f"Behavior:     {comp.get('behavior', '')}")
            if comp.get("provenance"):
                print(f"Provenance:   {comp['provenance']}")
            print("\nInputs:")
            for inp in comp.get("inputs", []):
                print(f"  - {inp['name']}")
            print("\nOutputs:")
            for outp in comp.get("outputs", []):
                print(f"  - {outp['name']}")

        elif args.list:
            cats = catalog.get("categories", {})
            filt = args.list.lower() if args.list else "all"
            print(f"Native Grasshopper Catalog ({len(catalog.get('by_name', {}))} components):\n")
            for cat, names in sorted(cats.items()):
                if filt != "all" and filt != cat.lower():
                    continue
                print(f"=== {cat} ({len(names)} components) ===")
                for n in sorted(names):
                    meta = catalog.get("by_name", {}).get(n, {})
                    print(f"  * {n} [{meta.get('nickname', '')}] - GUID: {meta.get('guid', '')}")
                print()

    elif args.cmd == "legopod":
        catalog = load_legopod_catalog()
        if not catalog.get("by_name"):
            print("Error: LegoPod catalog not found. Please ensure legopod_catalog.json exists.")
            sys.exit(1)

        if args.info:
            comp = find_legopod_component(args.info)
            if not comp:
                print(f"Component '{args.info}' not found in LegoPod catalog.")
                sys.exit(1)
            print(f"Component:    {comp['name']} [{comp.get('nickname', '')}]")
            print(f"GUID:         {comp['guid']}")
            print(f"Category:     {comp.get('category', 'LegoPod')}")
            print(f"Subcategory:  {comp.get('subcategory', 'General')}")
            print(f"Description:  {comp.get('description', '')}")
            print("\nInputs:")
            for inp in comp.get("inputs", []):
                pdesc = f" - {inp['description']}" if inp.get("description") else ""
                print(f"  - {inp['name']} ({inp.get('nickname', '')}): {inp.get('type', 'Generic')} [{inp.get('access', 'item')}]{pdesc}")
            print("\nOutputs:")
            for outp in comp.get("outputs", []):
                pdesc = f" - {outp['description']}" if outp.get("description") else ""
                print(f"  - {outp['name']} ({outp.get('nickname', '')}): {outp.get('type', 'Generic')} [{outp.get('access', 'item')}]{pdesc}")

        elif args.list:
            subcats = catalog.get("subcategories", {})
            filt = args.list.lower() if args.list else "all"
            print(f"LegoPod Plugin Catalog ({catalog.get('total_components', 0)} components):\n")
            for sub, names in sorted(subcats.items()):
                if filt != "all" and filt != sub.lower():
                    continue
                print(f"=== {sub} ({len(names)} components) ===")
                for n in sorted(names):
                    meta = catalog.get("by_name", {}).get(n, {})
                    print(f"  * {n} [{meta.get('nickname', '')}] - GUID: {meta.get('guid', '')}")
                print()

    elif args.cmd == "magpie":
        catalog = load_magpie_catalog()
        if not catalog.get("by_name"):
            print("Error: Magpie catalog not found. Please ensure magpie_catalog.json exists.")
            sys.exit(1)

        if args.info:
            comp = find_magpie_component(args.info)
            if not comp:
                print(f"Component '{args.info}' not found in Magpie catalog.")
                sys.exit(1)
            print(f"Component:    {comp['name']} [{comp.get('nickname', '')}]")
            print(f"GUID:         {comp['guid']}")
            print(f"Category:     {comp.get('category', 'Magpie')}")
            print(f"Subcategory:  {comp.get('subcategory', 'General')}")
            print(f"Description:  {comp.get('description', '')}")
            print("\nInputs:")
            for inp in comp.get("inputs", []):
                pdesc = f" - {inp['description']}" if inp.get("description") else ""
                print(f"  - {inp['name']} ({inp.get('nickname', '')}): {inp.get('type', 'Generic')} [{inp.get('access', 'item')}]{pdesc}")
            print("\nOutputs:")
            for outp in comp.get("outputs", []):
                pdesc = f" - {outp['description']}" if outp.get("description") else ""
                print(f"  - {outp['name']} ({outp.get('nickname', '')}): {outp.get('type', 'Generic')} [{outp.get('access', 'item')}]{pdesc}")

        elif args.list:
            subcats = catalog.get("subcategories", {})
            filt = args.list.lower() if args.list else "all"
            print(f"Magpie Plugin Catalog ({catalog.get('total_components', 0)} components):\n")
            for sub, names in sorted(subcats.items()):
                if filt != "all" and filt != sub.lower():
                    continue
                print(f"=== {sub} ({len(names)} components) ===")
                for n in sorted(names):
                    meta = catalog.get("by_name", {}).get(n, {})
                    print(f"  * {n} [{meta.get('nickname', '')}] - GUID: {meta.get('guid', '')}")
                print()

    elif args.cmd == "audit":
        ext = os.path.splitext(args.file)[1].lower()
        archive = read_ghx(args.file) if ext == ".ghx" else read_gh_binary(args.file)
        graph = GHGraph.from_archive(archive)

        nat_cat = load_native_catalog()
        het_cat = load_heteroptera_catalog()
        lego_cat = load_legopod_catalog()
        mag_cat = load_magpie_catalog()

        nat_guids = {c["guid"].lower(): c for c in nat_cat.get("by_guid", {}).values()}
        het_guids = {c["guid"].lower(): c for c in het_cat.get("by_guid", {}).values()}
        lego_guids = {c["guid"].lower(): c for c in lego_cat.get("by_guid", {}).values()}
        mag_guids = {c["guid"].lower(): c for c in mag_cat.get("by_guid", {}).values()}

        found_nat = []
        found_het = []
        found_lego = []
        found_mag = []
        found_other = []

        for c in graph.components:
            cid = c.guid.lower()
            if cid in nat_guids:
                found_nat.append((c, nat_guids[cid]))
            elif cid in het_guids:
                found_het.append((c, het_guids[cid]))
            elif cid in lego_guids:
                found_lego.append((c, lego_guids[cid]))
            elif cid in mag_guids:
                found_mag.append((c, mag_guids[cid]))
            else:
                found_other.append(c)

        print(f"===============================================================")
        print(f"Comprehensive Audit Report: {os.path.basename(args.file)}")
        print(f"===============================================================")
        print(f"Total Components:           {len(graph.components)}")
        print(f"Total Wires:                {len(graph.wires)}")
        print(f"Embedded Script Components: {sum(1 for c in graph.components if c.script_source)}")
        print(f"\nComponent Ecosystem Breakdown:")
        print(f"  * Native Grasshopper:     {len(found_nat):3d} components")
        print(f"  * Heteroptera:            {len(found_het):3d} components")
        print(f"  * LegoPod:                {len(found_lego):3d} components")
        print(f"  * Magpie ML:              {len(found_mag):3d} components")
        print(f"  * Third-Party / Unknown:  {len(found_other):3d} components")

        if found_het:
            print("\nHeteroptera Components Present:")
            for c, m in found_het:
                print(f"  - {m['name']} ({m.get('subcategory', 'General')})")

        if found_lego:
            print("\nLegoPod Components Present:")
            for c, m in found_lego:
                print(f"  - {m['name']} ({m.get('subcategory', 'General')})")

        if found_mag:
            print("\nMagpie Machine Learning Components Present:")
            for c, m in found_mag:
                print(f"  - {m['name']} ({m.get('subcategory', 'General')})")

        print("\nOptimization & Architectural Advice:")
        advice_count = 0
        names = [c.name.lower() for c in graph.components]

        # Heteroptera advice
        if "distance" in names and not any("adjacen" in n or "topology" in n for n in names):
            print("  [!] Distance-matrix network detected: Consider replacing bulky native Distance/SmallerThan chains with Heteroptera 'Topology Of Adjacencies' + 'Reconstruct Topology'.")
            advice_count += 1
        if any("space syntax" in n for n in names) and not any("normaliz" in n for n in names):
            print("  [!] Space Syntax detected without Normalizer: Pipe Space Syntax scores through Heteroptera 'Normalizer' [0.0, 1.0] before color gradients or scaling.")
            advice_count += 1

        # LegoPod advice
        if len(graph.components) > 10 and not found_lego:
            print("  [!] No LegoPod metadata packaging detected: Consider using LegoPod 'User Dictionary' and 'Build Attribute' to attach analytical results to Rhino geometry.")
            advice_count += 1

        # Magpie advice
        if any(c.script_source and ("cluster" in c.script_source.lower() or "pca" in c.script_source.lower() or "kmeans" in c.script_source.lower()) for c in graph.components):
            print("  [!] Custom script clustering detected: Consider replacing custom Python scripts with Magpie 'Clustering Machine' or 'PCA Machine' for zero-dependency native execution.")
            advice_count += 1

        if advice_count == 0:
            print("  [+] Graph structure adheres to clean architectural and algorithmic invariants.")
        print()

    elif args.cmd == "synthesize":
        builder = GHBuilder(name=f"Synthesized_{args.template.title().replace('-', '')}")
        if args.template == "spatial-ml":
            builder.add_spatial_ml_metadata_pipeline(
                cluster_count=args.clusters,
                source_node=args.source,
                depth=args.depth
            )
        elif args.template == "field-blocks":
            builder.add_generative_field_block_pipeline()
        elif args.template == "space-syntax":
            builder.add_space_syntax_pipeline()

        out_ext = os.path.splitext(args.out)[1].lower()
        if out_ext == ".gh":
            builder.save_gh(args.out)
        else:
            builder.save_ghx(args.out)
        print(f"Synthesized '{args.template}' definition with {builder.object_count} components -> {args.out}")

    elif args.cmd == "live":
        if not args.live_cmd:
            print("Usage: gh-toolkit live {status,list,add,remove,wire,unwire,set,solve,save,open} ...")
            sys.exit(1)

        if args.live_cmd == "status":
            st = live_status()
            if not st.get("rhino_running"):
                print("❌ Rhino 8 is NOT connected.")
                print(f"   Reason: {st.get('error', 'Unknown error')}")
                print("   Tip: In Rhino 8 command line, run 'StartScriptServer' to enable external scripting.")
                sys.exit(1)
            print("⚡ Rhino 8 Live Connection Active:")
            print(f"   Rhino Version:     {st.get('rhino_version')}")
            print(f"   Rhino Active Doc:  {st.get('rhino_doc')}")
            act = st.get("active_document")
            if act:
                print(f"   Grasshopper Doc:   {act.get('name')} ({'Modified' if act.get('modified') else 'Clean'})")
                print(f"   Object Count:      {act.get('object_count')} canvas objects")
                if act.get('file_path'):
                    print(f"   Saved Path:        {act.get('file_path')}")
            else:
                print("   Grasshopper Doc:   No document open on canvas.")

        elif args.live_cmd == "list":
            res = live_list_objects()
            if "error" in res:
                print(f"❌ Error: {res['error']}")
                sys.exit(1)
            if getattr(args, "json", False):
                import json
                print(json.dumps(res, indent=2))
            else:
                print(f"📋 Live Canvas: {res.get('doc_name')} ({res.get('total_objects')} objects)\n")
                print(f"{'GUID (Prefix)':<16} {'Name':<24} {'NickName':<14} {'Pivot (X, Y)':<18} {'Inputs':<8} {'Outputs':<8}")
                print("-" * 90)
                for o in res.get("objects", []):
                    short_id = o['instance_guid'][:8]
                    inputs_count = len(o.get('inputs', []))
                    outputs_count = len(o.get('outputs', []))
                    pivot_str = f"({o['pivot'][0]}, {o['pivot'][1]})"
                    print(f"{short_id:<16} {o['name'][:23]:<24} {o['nickname'][:13]:<14} {pivot_str:<18} {inputs_count:<8} {outputs_count:<8}")
                    if "value" in o:
                        print(f"    ↳ Value: {o['value']}")

        elif args.live_cmd == "add":
            res = live_add_component(args.name, x=args.x, y=args.y, nickname=args.nickname)
            if not res.get("success"):
                print(f"❌ Failed to add component: {res.get('error')}")
                sys.exit(1)
            print(f"✅ Added '{res.get('name')}' to canvas at ({args.x}, {args.y})")
            print(f"   Instance GUID: {res.get('instance_guid')}")

        elif args.live_cmd == "remove":
            res = live_remove_object(args.target)
            if not res.get("success"):
                print(f"❌ Failed to remove component: {res.get('error')}")
                sys.exit(1)
            print(f"✅ Removed {res.get('removed_count')} component(s) from canvas.")

        elif args.live_cmd == "wire":
            s_pin = int(args.source_pin) if str(args.source_pin).isdigit() else args.source_pin
            t_pin = int(args.target_pin) if str(args.target_pin).isdigit() else args.target_pin
            res = live_wire(args.source, args.target, source_pin=s_pin, target_pin=t_pin)
            if not res.get("success"):
                print(f"❌ Failed to connect wire: {res.get('error')}")
                sys.exit(1)
            src = res.get("source", {})
            dst = res.get("target", {})
            print(f"✅ Connected: {src.get('name')}[{src.get('output')}] ──▶ {dst.get('name')}[{dst.get('input')}]")

        elif args.live_cmd == "unwire":
            t_pin = int(args.target_pin) if str(args.target_pin).isdigit() else args.target_pin
            res = live_unwire(args.target, target_pin=t_pin, source_id_or_name=args.source)
            if not res.get("success"):
                print(f"❌ Failed to disconnect wire: {res.get('error')}")
                sys.exit(1)
            print(f"✅ Disconnected {res.get('disconnected_count')} wire(s) from {res.get('target')}[{res.get('input')}].")

        elif args.live_cmd == "set":
            res = live_set_value(args.target, args.value)
            if not res.get("success"):
                print(f"❌ Failed to set value: {res.get('error')}")
                sys.exit(1)
            print(f"✅ Updated {res.get('type')} '{res.get('object')}' value to: {res.get('new_value')}")

        elif args.live_cmd == "solve":
            res = live_solve()
            if not res.get("success"):
                print(f"❌ Failed to solve canvas: {res.get('error')}")
                sys.exit(1)
            print(f"✅ Solved document '{res.get('doc_name')}' ({res.get('objects_count')} objects) and refreshed canvas.")

        elif args.live_cmd == "save":
            res = live_save(filepath=args.path)
            if not res.get("success"):
                print(f"❌ Failed to save document: {res.get('error')}")
                sys.exit(1)
            print(f"✅ Saved live Grasshopper definition to: {res.get('file_path')}")

        elif args.live_cmd == "open":
            res = live_open(args.file)
            if not res.get("success"):
                print(f"❌ Failed to open document: {res.get('error')}")
                sys.exit(1)
            print(f"✅ Opened '{res.get('doc_name')}' ({res.get('objects_count')} objects) on live canvas.")


if __name__ == "__main__":
    main()

