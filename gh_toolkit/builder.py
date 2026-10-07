"""
gh_toolkit.builder - Programmatic synthesis and canvas layout for Grasshopper definitions.
"""

import uuid
from typing import Tuple, Optional, Dict, Any, List

from .core import GHArchive, write_gh_binary, write_ghx
from .heteroptera import find_heteroptera_component
from .native import find_native_component


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
        props.add_item("Description", 10, "Synthesized by Antigravity Grasshopper Toolkit")
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

    def add_slider(
        self,
        alias: str,
        nickname: str,
        min_val: float,
        max_val: float,
        current_val: float,
        pivot: Tuple[float, float],
    ) -> str:
        """Add a native Number Slider component to the canvas."""
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
        """Add a native Panel component for text / notes."""
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
        """Add a native GhPython Script Component to the canvas."""
        comp_guid = "410755b1-224a-4c1e-a407-bf32fb45ea7e"
        inst_guid = str(uuid.uuid4())

        obj = self.objects_chunk.create_chunk("Object", self.object_count)
        self.object_count += 1
        obj.add_item("GUID", 9, comp_guid)
        obj.add_item("Name", 10, "GhPython Script")

        cont = obj.create_chunk("Container")
        cont.add_item("Description", 10, "GhPython script component")
        cont.add_item("InstanceGuid", 9, inst_guid)
        cont.add_item("Name", 10, "GhPython Script")
        cont.add_item("NickName", 10, "Python")
        cont.add_item("ScriptSource", 10, code)

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

    def add_heteroptera_component(
        self,
        name_or_guid: str,
        alias: str,
        pivot: Tuple[float, float],
        nickname: Optional[str] = None,
    ) -> str:
        """Instantiate any of the 152 Heteroptera plugin components by name or GUID."""
        comp_info = find_heteroptera_component(name_or_guid)
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
        """Instantiate any of the 211 verified native Grasshopper components by name or GUID."""
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

    def add_component(
        self,
        name_or_guid: str,
        alias: str,
        pivot: Tuple[float, float],
        nickname: Optional[str] = None,
    ) -> str:
        """Instantiate any component (checking Heteroptera first, then Native catalog)."""
        comp_het = find_heteroptera_component(name_or_guid)
        if comp_het:
            return self.add_heteroptera_component(name_or_guid, alias, pivot, nickname)
        comp_nat = find_native_component(name_or_guid)
        if comp_nat:
            return self.add_native_component(name_or_guid, alias, pivot, nickname)
        raise KeyError(f"Component '{name_or_guid}' not found in Heteroptera or Native catalogs.")

    def add_space_syntax_pipeline(self, start_pivot: Tuple[float, float] = (100, 100)) -> Dict[str, str]:
        """Synthesize the canonical Heteroptera Space Syntax analysis pipeline."""
        x, y = start_pivot
        ids = {}
        ids["center"] = self.add_heteroptera_component("Center", "center", (x + 220, y))
        ids["adj"] = self.add_heteroptera_component("Topology Of Adjacencies", "adj", (x + 220, y + 140))
        ids["recon"] = self.add_heteroptera_component("Reconstruct Topology", "recon", (x + 460, y + 70))
        ids["s_src"] = self.add_slider("s_src", "SourceNode", 0, 20, 0, (x + 460, y + 210))
        ids["s_depth"] = self.add_slider("s_depth", "Depth", 1, 15, 6, (x + 460, y + 270))
        ids["ss"] = self.add_heteroptera_component("Space Syntax", "ss", (x + 700, y + 100))
        ids["norm"] = self.add_heteroptera_component("Normalizer", "norm", (x + 940, y + 100))

        self.connect("adj.Cell→Cell", "recon.Node→Node")
        self.connect("center.Center", "recon.Points (Optional)")
        self.connect("recon.Node→Node", "ss.Node→Node")
        self.connect("s_src.out", "ss.Source")
        self.connect("s_depth.out", "ss.Depth")
        self.connect("ss.Node SpaceSyntax", "norm.Numbers")
        return ids

    def connect(self, src_port: str, dest_port: str):
        """Topologically connect an output port to an input port."""
        src_guid = self.param_lut.get(src_port)
        dest_guid = self.param_lut.get(dest_port)
        if not src_guid or not dest_guid:
            raise KeyError(f"Cannot connect: unknown port '{src_port}' or '{dest_port}'")

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

    def save_gh(self, path: str):
        """Save as compressed binary .gh file."""
        write_gh_binary(self.archive, path, compress=True)

    def save_ghx(self, path: str):
        """Save as clean XML .ghx file."""
        write_ghx(self.archive, path)
