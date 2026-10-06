---
name: grasshopper
description: >-
  High-performance suite for inspecting, decompiling, converting, modifying, and synthesizing Rhino Grasshopper definitions (.gh, .ghx, and JSON Graph IR). Zero external dependencies. Features native DEFLATE binary decompressor, 152-component Heteroptera catalog, 8 architectural pillars synthesized from 193 production definitions, and programmatic DAG builder.
---

# Grasshopper Engineering & Synthesis Skill

Zero-dependency engine to **read, decompile, inspect, modify, and synthesize** Rhino Grasshopper definitions (`.gh` binary and `.ghx` XML).

---

## 1. Fast Action Matrix

| User Goal | Tool / Action | Reference |
|---|---|---|
| **Inspect definition / components** | `python3 <skill_dir>/scripts/gh_toolkit.py info <file.gh>` | Section 3 |
| **Convert `.gh` <-> `.ghx` <-> JSON** | `python3 <skill_dir>/scripts/gh_toolkit.py to-ghx <in> <out>` | Section 3 |
| **Batch extract Python & C# scripts** | `python3 <skill_dir>/scripts/gh_toolkit.py extract-scripts <dir>` | `references/SCRIPT_LIBRARY.md` |
| **Space Syntax floorplan analysis** | `Topology Of Adjacencies` -> `Reconstruct Topology` -> `Space Syntax` | `references/ARCHITECTURAL_RECIPES.md` |
| **Parametric masonry / brick bonds** | `Weighted Allocator` + `Careless Range` + `Instance Manager` | `references/ARCHITECTURAL_RECIPES.md` |
| **Facade framing & section slicing** | `CurvePlane` slicing + `IntervalsUnion` | `references/SCRIPT_LIBRARY.md` |
| **Programmatic graph generation** | Use Python `GHBuilder` API | Section 4 |
| **Lookup component GUIDs / ports** | Check compact index or `gh_toolkit heteroptera --info` | `references/COMPONENT_INDEX.md` |

---

## 2. Core Technical Invariants

1. **Native Binary Decompression**: Binary `.gh` archives are raw DEFLATE streams. Process directly with `zlib.decompress(data, -15)`. No Rhino COM/.NET GUI required.
2. **Wire Mechanism**: Input parameters connect upstream by setting item `Source` (`type_code=9`, GUID of upstream output parameter) and incrementing `SourceCount` (`type_code=3`).
3. **Data Access Modes**: `0` = Item, `1` = List, `2` = Tree.
4. **Canvas Layout Geometry**: Horizontal spacing: `+220` to `+280` px on X axis; Vertical spacing: `+80` to `+120` px on Y axis.
5. **Topological Reconstruction Invariant**: Always pipe `Topology Of Adjacencies.Cell→Cell` through `Reconstruct Topology` before feeding `Space Syntax.Node→Node` to avoid boundary edge indexing faults.
6. **Multilingual Annotation Invariant**: Pass Persian/Arabic strings through `ToolsUnicode` before baking to prevent inverted glyphs.

---

## 3. Toolkit CLI Cheatsheet

```bash
# 1. Inspect definition metadata & canvas components
python3 <skill_dir>/scripts/gh_toolkit.py info path/to/definition.gh

# 2. Lossless bidirectional conversion
python3 <skill_dir>/scripts/gh_toolkit.py to-ghx input.gh output.ghx
python3 <skill_dir>/scripts/gh_toolkit.py to-gh input.ghx output.gh
python3 <skill_dir>/scripts/gh_toolkit.py to-json input.gh graph.json

# 3. Batch extract embedded GhPython & C# scripts
python3 <skill_dir>/scripts/gh_toolkit.py extract-scripts ./definitions --out ./scripts

# 4. Query Heteroptera component schemas
python3 <skill_dir>/scripts/gh_toolkit.py heteroptera --info "Space Syntax"
python3 <skill_dir>/scripts/gh_toolkit.py heteroptera --list networks
```

---

## 4. Programmatic Graph Synthesis (`GHBuilder`)

```python
from gh_toolkit import GHBuilder

builder = GHBuilder(name="ParametricWorkflow")

# Add Sliders
s_cnt = builder.add_slider("s_cnt", "Count", min_val=1, max_val=50, current_val=10, pivot=(100, 100))
s_gap = builder.add_slider("s_gap", "Gap", min_val=0.1, max_val=5.0, current_val=1.2, pivot=(100, 180))

# Add GhPython component
code = "import Rhino.Geometry as rg\npts = [rg.Point3d(i * gap, 0, 0) for i in range(int(count))]"
py_comp = builder.add_python_script("py_masonry", code, inputs=["count", "gap"], outputs=["pts"], pivot=(350, 120))

# Connect Wires: <alias>.<output_name> -> <alias>.<input_name>
builder.connect("s_cnt.out", "py_masonry.count")
builder.connect("s_gap.out", "py_masonry.gap")

# Save as native Rhino definition
builder.save_gh("ParametricWorkflow.gh")
builder.save_ghx("ParametricWorkflow.ghx")
```

---

## 5. Modular Knowledge Base

* [Architectural Recipes](references/ARCHITECTURAL_RECIPES.md): The 8 architectural pillars learned from 193 definitions (Masonry, Space Syntax, Facades, Kangaroo, GIS, Tessellations, Product Catalogs).
* [Curated Script Library](references/SCRIPT_LIBRARY.md): Idiomatic GhPython & C# scripts (DataTree helpers, hex genome codecs, curve slicing, viewport conduits).
* [Component & GUID Index](references/COMPONENT_INDEX.md): Compact lookup table of core Grasshopper and Heteroptera components.
* [Compact Schema Index](resources/compact_index.json): Lightweight 46 KB lookup index for programmatic queries.
