---
name: grasshopper
description: >-
  Comprehensive suite for inspecting, analyzing, converting, editing, and generating Rhino Grasshopper definitions (.gh, .ghx, and JSON Graph IR). Features native DEFLATE binary decompressor/compressor, XML schema generator, 630+ component GUID directory, wiring rule validation, data tree management (item, list, tree), embedded script authoring (GhPython & C#), and parametric architectural recipes (masonry, facades, attractors, space syntax).
---

# Grasshopper Definition Engineering & Generation Skill

This skill equips Antigravity to **read, decompile, inspect, modify, and synthesize** native Rhino Grasshopper definitions (`.gh` binary and `.ghx` XML) with zero external runtime dependencies.

---

## 1. Anatomy of Grasshopper Definitions

Grasshopper documents are hierarchical **Directed Acyclic Graphs (DAGs)** represented as nested **Chunks** and typed **Items**:
- **Root Chunk**: Contains `ArchiveVersion` (usually `0.2.2`), `Definition`, and optional `Thumbnail`.
- **Definition Chunk**: Contains `DocumentHeader`, `DefinitionProperties` (name, author, zoom), and `DefinitionObjects`.
- **DefinitionObjects Chunk**: Contains an indexed collection of `Object` chunks.
  - Each `Object` defines:
    - `GUID`: Component type GUID (defines whether it is a Slider, Divide Curve, Python Script, etc.).
    - `Container`: Contains `Name`, `NickName`, `InstanceGuid` (unique UUID for this specific instance), and canvas `Attributes` (`Pivot`, `Bounds`).
    - `param_input` / `InputParam`: Input ports. Wires are established by setting `Source` (pointing to the upstream output parameter's `InstanceGuid`) and `SourceCount`.
    - `param_output` / `OutputParam`: Output ports with their own `InstanceGuid`.
    - `ScriptSource` / `CodeInput`: Embedded C# or Python script strings.
- **Formats**:
  - `.gh`: Pure raw DEFLATE-compressed binary stream of the chunk tree (`zlib.decompress(data, -zlib.MAX_WBITS)`).
  - `.ghx`: Plain-text XML serialization of the exact same chunk tree. Both formats open identically in Rhino.

---

## 2. The `gh_toolkit` Engine

The skill comes bundled with `scripts/gh_toolkit.py` (and in your project's `tools/gh_toolkit.py`).

### CLI Commands:
```bash
# Inspect components, parameters, scripts, and canvas topology
python3 <skill_dir>/scripts/gh_toolkit.py info <file.gh|file.ghx>

# Convert binary .gh to readable XML .ghx
python3 <skill_dir>/scripts/gh_toolkit.py to-ghx input.gh output.ghx

# Convert XML .ghx to binary .gh
python3 <skill_dir>/scripts/gh_toolkit.py to-gh input.ghx output.gh

# Convert .gh/.ghx to JSON Graph IR (for inspection or LLM analysis)
python3 <skill_dir>/scripts/gh_toolkit.py to-json input.gh graph.json

# Batch extract all embedded GhPython (.py) and C# (.cs) scripts
python3 <skill_dir>/scripts/gh_toolkit.py extract-scripts <dir> --out ./extracted_scripts
```

### Python API (Direct Ingestion & Modification):
```python
from gh_toolkit import read_gh_binary, write_gh_binary, read_ghx, write_ghx, GHGraph, GHBuilder

# Load definition
archive = read_gh_binary("my_file.gh") # or read_ghx("my_file.ghx")

# Convert to high-level graph
graph = GHGraph.from_archive(archive)
for comp in graph.components:
    print(comp.name, comp.pivot, comp.inputs, comp.outputs)

# Programmatically build a new definition
builder = GHBuilder(name="ParametricFacade")

# 1. Add Sliders
builder.add_slider(alias="s_count", nickname="Count", min_val=1, max_val=50, current_val=10, pivot=(100, 100))
builder.add_slider(alias="s_gap", nickname="Gap", min_val=0.1, max_val=5.0, current_val=1.2, pivot=(100, 180))

# 2. Add GhPython Script Component
script_code = """
# Inputs: count, gap
# Outputs: pts, lines
import Rhino.Geometry as rg

pts = []
for i in range(int(count)):
    pts.append(rg.Point3d(i * gap, (i % 2) * gap * 0.5, 0))
"""
builder.add_python_script(
    alias="py_masonry",
    code=script_code,
    inputs=["count", "gap"],
    outputs=["pts"],
    pivot=(350, 120)
)

# 3. Connect Wires
builder.connect("s_count.out", "py_masonry.count")
builder.connect("s_gap.out", "py_masonry.gap")

# 4. Save directly as .gh or .ghx
builder.save_gh("ParametricFacade.gh")
builder.save_ghx("ParametricFacade.ghx")
```

---

## 3. Component GUID Reference (Most Common)

| Component Name | Type GUID | Key Inputs | Key Outputs |
|---|---|---|---|
| **Number Slider** | `57da07bd-ecab-415d-9d86-af36d7073abc` | (internal slider bounds) | `Output` |
| **Panel** | `ca916113-d820-437b-9994-6ab08216173b` | `in` (optional) | `out` |
| **GhPython Script** | `410755b1-224a-4c1e-a407-bf32fb45ea7e` | Dynamic (`x`, `y`, ...) | `out`, `a`, ... |
| **C# Script** | `04d46c59-f81d-407b-871d-f8fa79244093` | Dynamic (`x`, `y`, ...) | `out`, `A`, ... |
| **Construct Point** | `35520be3-db72-4638-b7eb-ee7fbbeec2c0` | `X`, `Y`, `Z` | `Pt` |
| **Vector XYZ** | `91e84aa9-94b1-419b-ab09-9069d31d45dc` | `X`, `Y`, `Z` | `V` |
| **Divide Curve** | `26d11e4f-6f9a-412e-a55e-f00e932b53f6` | `C` (Curve), `N` (Count), `K` (Kinks) | `P` (Points), `T` (Tangents), `t` (Params) |
| **Circle** | `8b6e680a-9d6e-4bb5-a36c-9c748c08197c` | `P` (Plane), `R` (Radius) | `C` (Circle) |
| **Move** | `8ec0a1cf-b8d4-49a6-bd27-4bf69147514a` | `G` (Geometry), `T` (Translation Vector) | `G` (Geometry) |
| **Series** | `26c518b2-570a-4a25-a13a-a1b7e6184a44` | `S` (Start), `N` (Step), `C` (Count) | `S` (Series List) |
| **Remap Numbers** | `42c1143c-ae74-4b53-9a3b-2ee0fbb1a98e` | `V` (Value), `S` (Source Domain), `T` (Target Domain) | `M` (Mapped Values) |
| **Distance** | `7d100085-f5da-485a-8b83-a41e974e64f0` | `A` (Point A), `B` (Point B) | `D` (Distance) |

*For complete lookup across all 636 components discovered in the repository, consult `<skill_dir>/resources/component_catalog.json`.*

---

## 4. Data Tree & Wire Mechanics

1. **Parameter Access Types**:
   - `Access = 0` (`item`): The component executes once for every individual item in the data stream.
   - `Access = 1` (`list`): The component receives the whole list in one execution (e.g. polyline from points).
   - `Access = 2` (`tree`): The component receives the full nested data tree structure (e.g. `GH_Structure`).
2. **Wiring Invariants**:
   - An input parameter connects to an output parameter by adding an item named `Source` with `type_code = 9` (`gh_guid`) containing the upstream output parameter's `InstanceGuid`.
   - Update `SourceCount` (`type_code = 3`) to match the number of active input connections.
3. **Canvas Auto-Layout Rule**:
   - When placing components programmatically, space them cleanly to prevent canvas overlapping:
     - Horizontal offset between connected columns: `+220` to `+280` pixels on X axis.
     - Vertical spacing between parallel components: `+80` to `+120` pixels on Y axis.

---

## 5. Editing Existing Definitions Workflow

When a user asks to modify an existing `.gh` or `.ghx` definition:
1. **Inspect First**: Run `python3 gh_toolkit.py info <file>` to identify component names and instance GUIDs.
2. **Convert to .ghx or JSON if needed**: If you need to make structural edits, convert to `.ghx` or load with `read_gh_binary`.
3. **Apply Edits**:
   - To change numeric parameters (e.g., slider values), update the `Value` item under the slider's `Slider` chunk.
   - To replace or enhance embedded logic, edit the `CodeInput` (GhPython) or `ScriptSource` (C#) string.
   - To rewire, update the `Source` item on the destination `param_input`.
4. **Save & Verify**: Save the definition back to `.gh` or `.ghx`. Verify using `info` that component counts and wire counts are preserved.

---

## 6. Heteroptera Plugin Deep Engineering

Heteroptera (developed by Amin Bahrami) is a dominant plugin in the user's definitions (accounting for 152 components across Networks, Vectors, Uncertainty, Streaming, Geometry, Maths, and Utilities).

### 6.1 Topological Conventions & Data Trees
- **`Node→Node` (tree)**: The primary graph representation where branch `{i}` lists all adjacent node indices connected to Node `i`.
- **`Edge→Node` (tree)**: Branch `{e}` contains the 2 endpoint node indices `[NodeA, NodeB]`.
- **`Cell→Cell` / `Cell→Node`**: Planar room and plot adjacencies generated by `Topology Of Adjacencies` and `Cycle from Topology`.
- **Reconstruction Invariant**: Always pipe raw geometric adjacencies (`Topology Of Adjacencies`) through `Reconstruct Topology` before feeding to `Space Syntax` or graph traversal components to ensure disconnected nodes and naked boundary edges are indexed cleanly.

### 6.2 Key Heteroptera Component GUIDs
| Component Name | Nickname | Type GUID | Subcategory | Key Ports |
|---|---|---|---|---|
| **Space Syntax** | `SpaceSyntax` | `d4077291-8c30-4313-8bb3-45a86138c521` | Networks | In: `Node→Node`, `Source`, `Depth` / Out: `Node SpaceSyntax`, `Connection SpaceSyntax` |
| **Topology Of Adjacencies** | `Adjacency` | `980bd972-3623-40a9-85d9-89807ce118c9` | Networks | In: `Polylines`, `Method`, `Tolerance` / Out: `Cell→Cell` |
| **Reconstruct Topology** | `ReconTopo` | `683305c6-fd18-4102-b142-f5c799d7069c` | Networks | In: `Node→Node`, `Edge→Node`, `Points (Optional)` / Out: `Node→Node`, `Points`, `Lines` |
| **Shortest Route** | `ShortRoute` | `992702c7-9416-4663-8be4-beb8521810ba` | Networks | In: `Node→Node`, `Start`, `End` / Out: `Route`, `Length`, `Edges` |
| **Proximity Network** | `ProxNet` | `8b05233a-b681-40b2-8b83-51b2cdd459c5` | Networks | In: `Points`, `Distance`, `Max Neighbors` / Out: `Node→Node`, `Lines` |
| **Center** | `Center` | `3c5edcba-b7a5-4710-b076-4b19a7080a2b` | Geometry | In: `Geometry` / Out: `Center`, `Area`, `Volume` |
| **Normalizer** | `Normalizer` | `5d820462-ea9b-4663-875f-b519c0de2340` | Maths | In: `Numbers` / Out: `Numbers`, `Domain` |
| **Slingshot Allocator** | `Slingshot` | `ef32b535-71bb-4573-b27e-85a0cbb75225` | Uncertainty | In: `Indices`, `Distribution`, `Seed` / Out: `Allocation` |
| **Weighted Allocator** | `WeightAlloc` | `5c8e312d-1ea2-45e3-8557-46e7f12e8417` | Uncertainty | In: `Weights`, `Count`, `Seed` / Out: `Indices` |
| **Careless Range** | `Careless` | `85a0889c-482a-4318-b2e3-2e40d6c1b35b` | Uncertainty | In: `Domain`, `Steps`, `Jitter`, `Seed` / Out: `Values` |
| **Stream Freeze / Gate** | `Freeze` | `8e6c73df-9730-4e00-a548-5c468e82efea` | Streaming | In: `Data`, `Freeze` / Out: `Data` |
| **Symmetric Domain** | `SymDomain` | `17342b5c-486a-493f-846f-c12e8739121a` | Maths | In: `Value` / Out: `Domain` |
| **ToolsUnicode** | `Unicode` | `3782b5f1-3ec6-419f-9c02-86e115bc5c9a` | Utilities | In: `Text`, `Encoding` / Out: `Text` |

*For complete port schemas and documentation of all 152 components, refer to `<skill_dir>/resources/heteroptera_catalog.json` and `<skill_dir>/resources/heteroptera_reference.md`.*

### 6.3 Heteroptera CLI & Programmatic Builder
```bash
# Query the Heteroptera catalog (list by subcategory or all)
python3 <skill_dir>/scripts/gh_toolkit.py heteroptera --list [networks|vectors|uncertainty|streaming|geometry|maths|utilities]

# Inspect exact input/output types, nicknames, and access modes
python3 <skill_dir>/scripts/gh_toolkit.py heteroptera --info "Space Syntax"

# Audit a definition for Heteroptera components and pipelines
python3 <skill_dir>/scripts/gh_toolkit.py heteroptera --audit my_definition.gh

# View canonical wiring recipes
python3 <skill_dir>/scripts/gh_toolkit.py heteroptera --recipes
```

#### Synthesizing Heteroptera Workflows with `GHBuilder`:
```python
from gh_toolkit import GHBuilder

builder = GHBuilder(name="SpaceSyntaxAnalysis")

# Option 1: One-line canonical Space Syntax synthesis
pipeline_ids = builder.add_space_syntax_pipeline(start_pivot=(100, 100))

# Option 2: Custom assembly of Heteroptera components
c_center = builder.add_heteroptera_component("Center", "c_center", (200, 100))
c_adj = builder.add_heteroptera_component("Topology Of Adjacencies", "c_adj", (200, 220))
c_recon = builder.add_heteroptera_component("Reconstruct Topology", "c_recon", (420, 160))

builder.connect("c_adj.Cell→Cell", "c_recon.Node→Node")
builder.connect("c_center.Center", "c_recon.Points (Optional)")

builder.save_gh("SpaceSyntaxAnalysis.gh")
builder.save_ghx("SpaceSyntaxAnalysis.ghx")
```

