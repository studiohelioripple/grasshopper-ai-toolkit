---
name: grasshopper
description: >-
  Premier computational design engine and specialist for Rhino and Grasshopper. Backed by zero-dependency binary .gh/.ghx decompiler/builder, 212 verified native components, 152 Heteroptera components, 42 LegoPod components, 14 Magpie machine learning components, complete Rajaa Issa & Tedeschi data-tree theory, 96 design pattern recipes, and automated Yak package installer.
  Use for ANY of: Grasshopper or Rhino parametric modeling questions, algorithmic design, "build me a definition", facade paneling, attractor patterns, generative massing, diagrid/gridshell, waffle sectioning;
  component queries (exact port names, types, defaults, GUIDs); data-tree debugging (graft, flatten, simplify, flip matrix, Split Tree masks, Path Mapper, matching mismatches);
  inspecting, decompiling, converting, or modifying .gh binary or .ghx XML files; programmatic graph synthesis via Python GHBuilder; Space Syntax and topological network analysis; Kangaroo 2 form-finding or Galapagos optimization.
---

# Grasshopper Computational Engineering & Synthesis Skill

A unified, high-performance suite combining:
1. **Zero-Dependency Engine**: Decompile binary `.gh` via raw DEFLATE streams, convert lossless between `.gh` <-> `.ghx` <-> JSON, and programmatically synthesize definitions via Python `GHBuilder`.
2. **Verified Knowledge Base**: 212 native components, 152 Heteroptera components, 42 LegoPod components, 14 Magpie machine learning components, 96 workflow patterns, 127 architectural glossary terms, and complete data-tree mathematics.
3. **Automated Package Management**: Automated Yak package manager detection and 1-click install/upgrade of Heteroptera.

---

## 1. Fast Action Matrix

| User Goal | Tool / Command | Primary Reference |
|---|---|---|
| **Inspect `.gh` / `.ghx` definition** | `python3 <skill_dir>/scripts/gh_toolkit.py info <file.gh>` | Section 4 |
| **Convert `.gh` <-> `.ghx` <-> JSON** | `python3 <skill_dir>/scripts/gh_toolkit.py to-ghx <in> <out>` | Section 4 |
| **Check Live Rhino 8 Connection** | `python3 <skill_dir>/scripts/gh_toolkit.py live status` | Section 4 & Workflow 5 |
| **List / Inspect Live Canvas Objects** | `python3 <skill_dir>/scripts/gh_toolkit.py live list` | Section 4 & Workflow 5 |
| **Add Component to Live Canvas** | `python3 <skill_dir>/scripts/gh_toolkit.py live add "<Name>" --x 100 --y 100` | Section 4 & Workflow 5 |
| **Wire Live Canvas Components** | `python3 <skill_dir>/scripts/gh_toolkit.py live wire <src> <dst>` | Section 4 & Workflow 5 |
| **Mutate Live Slider / Panel Value** | `python3 <skill_dir>/scripts/gh_toolkit.py live set <target> <value>` | Section 4 & Workflow 5 |
| **Recompute Live Canvas Solution** | `python3 <skill_dir>/scripts/gh_toolkit.py live solve` | Section 4 & Workflow 5 |
| **Save Live Canvas Quietly** | `python3 <skill_dir>/scripts/gh_toolkit.py live save [path.ghx]` | Section 4 & Workflow 5 |
| **Open Definition on Live Canvas** | `python3 <skill_dir>/scripts/gh_toolkit.py live open <path.ghx>` | Section 4 & Workflow 5 |
| **Lookup Native Component Pins** | `python3 <skill_dir>/scripts/gh_toolkit.py native --info "<Name>"` | `references/NATIVE_COMPONENTS.md` |
| **Lookup Heteroptera Component** | `python3 <skill_dir>/scripts/gh_toolkit.py heteroptera --info "<Name>"` | `references/HETEROPTERA_COMPONENTS.md` |
| **Lookup LegoPod Component** | `python3 <skill_dir>/scripts/gh_toolkit.py legopod --info "<Name>"` | `references/LEGOPOD_COMPONENTS.md` |
| **Lookup Magpie ML Component** | `python3 <skill_dir>/scripts/gh_toolkit.py magpie --info "<Name>"` | `references/MAGPIE_COMPONENTS.md` |
| **Check / Install Heteroptera Plugin** | `python3 <skill_dir>/scripts/gh_toolkit.py heteroptera --install` | Section 4 |
| **Debug Data-Tree Mismatches** | Apply diagnostic decision tree & matching proofs | `references/DATA_TREES.md` |
| **Lookup Parametric Recipes** | Grep canonical pattern collection (96 recipes) | `references/NATIVE_PATTERNS.md` |
| **Lookup Tri-Plugin Patterns** | Grep tri-plugin production cookbook (6 patterns) | `references/TRI_PLUGIN_PATTERNS.md` |
| **Audit & Optimize Definition** | `python3 <skill_dir>/scripts/gh_toolkit.py audit <file>` | Section 4 |
| **Synthesize Tri-Plugin Pipeline** | `python3 <skill_dir>/scripts/gh_toolkit.py synthesize <tpl> -o <out>` | Section 4 & 5 |
| **Check Version Errata / Replacements** | Check modern replacements (Kangaroo 2, Anemone) | `references/ERRATA_MODERNIZATION.md` |
| **Batch extract GhPython / C# scripts**| `python3 <skill_dir>/scripts/gh_toolkit.py extract-scripts <dir>` | `references/SCRIPT_LIBRARY.md` |
| **Synthesize New Definition (.gh/.ghx)**| Programmatic Python `GHBuilder` API | Section 5 |


---

## 2. Canonical Notation & Provenance Invariants

When explaining definitions, authoring workflows, or communicating graphs to the user, **always use canonical notation**:

- **Component Instance**: `ComponentName (Tab > Section) [Alias]`
  *Example*: `Divide Curve (Curve > Division) [Divide]`
- **Wire Connection**: `ComponentA.OutputName -> ComponentB.InputName {tree state}`
  *Example*: `Divide.P -> Line.A {flat, N+1 pts}`
- **Data Tree States Annotated Per Wire**: `{flat | grafted | branches: N x M}`
- **Sliders & Inputs**: `Slider[min..max, default] -> Component.Input`
- **Definition Sections**: `=== Section: Name ===` in topological execution order.

### Strict Anti-Hallucination Invariant
1. **No Port Fabrication**: Port names, types, and defaults must come from `references/NATIVE_COMPONENTS.md`, `gh-toolkit native --info`, or `gh-toolkit heteroptera --info`.
2. Any component not in the verified references must be explicitly tagged **`[UNVERIFIED — not in knowledge base]`**.
3. **Tree States are Load-Bearing**: Branch arithmetic must be explicitly annotated whenever data structure changes (e.g. `graft -> {N x 1}`, `cross-reference -> N*M`, `Divide Curve open -> N+1`).
4. **Provenance Tags**: Preserve source tags when quoting (`[STATED, AAD p.X]`, `[VERIFIED]`, `[INFERRED]`).

### Tri-Plugin Priority & Synthesis Invariants
When solving computational design tasks, always prioritize the specialized tri-plugin ecosystem:
1. **Heteroptera (Algorithmic Priority)**:
   - Always prioritize Heteroptera for topological networks, Space Syntax, adjacency graphs, vector fields (`Field Booster`, `Curvature Field`), cycle detection, and stream multiplexing over clumsy native workarounds.
   - Pipe spatial graphs through `Topology Of Adjacencies` -> `Reconstruct Topology` -> `Space Syntax` -> `Normalizer`.
2. **LegoPod (Object, Meta-Data & Block Specialist)**:
   - Always use LegoPod for attaching typed Rhino user-dictionaries (`UserDic_Build`), custom geometry attributes (`Build Attribute`), block definitions/instances (`Define Block`, `Insert Block by Transform`), and TSV schedule exports (`Table TSV-Data`).
   - Never output anonymous un-attributed geometry when downstream BIM or assembly is intended.
3. **Magpie (Machine Learning Specialist)**:
   - Always use Magpie for unsupervised clustering (`Clustering Machine`), dimensionality reduction (`PCA Machine`), manifold learning (`T-SNE`), Kohonen Self-Organizing Maps (`KohMap Machine`), and covariance analysis (`Correlation Matrix`).
4. **Native Grasshopper**:
   - Reserve native GH for basic geometry primitives, math sliders, panels, and standard data tree structuring.

Consult `references/TRI_PLUGIN_ARCHITECTURE.md` for complete cross-plugin workflows and recipes.

---

## 3. The 4 Cognitive Agent Workflows

### Workflow 1 — Answering Component & Geometric Concepts
1. Query component schemas via `gh-toolkit native --info "<Name>"` or `gh-toolkit heteroptera --info "<Name>"`.
2. Check `references/ERRATA_MODERNIZATION.md` for ecosystem changes:
   - Kangaroo 1 -> **Kangaroo 2**
   - HoopSnake / Loop -> **Anemone**
   - Tree8 `Allocate N` -> native **`Partition List`**
   - MeshEdit `Triangulate` -> native **`Triangulate`**
3. Consult `references/GEOMETRY_GLOSSARY.md` for formal mathematical definitions (Brep, anticlastic curvature, knot vectors, affine vs Euclidean transforms).

### Workflow 2 — Designing New Node Graphs
1. Restate design intent into sequential geometric operations.
2. Match stages against recipes in `references/NATIVE_PATTERNS.md` (96 recipes) or `references/ARCHITECTURAL_RECIPES.md` (8 architectural pillars).
3. Verify tree arithmetic using `references/DATA_TREES.md`.
4. Output in **Canonical Notation** (Section 2), followed by a **Data Tree Rationale** paragraph and **Predicted Failure Points**.
5. When requested or appropriate, synthesize the definition directly into a runnable `.gh` / `.ghx` file via Python `GHBuilder` (Section 5).

### Workflow 3 — Inspecting & Decompiling Definitions
1. Run `gh-toolkit info <file.gh>` to inspect canvas census, component counts, and embedded scripts.
2. If detailed XML inspection is required, convert via `gh-toolkit to-ghx <file.gh> <file.ghx>` or export Graph IR via `gh-toolkit to-json <file.gh> graph.json`.
3. Resolve component GUIDs using `resources/guid-map.json` and `resources/native_catalog.json`.
4. Extract any embedded scripts via `gh-toolkit extract-scripts <dir>`.

### Workflow 4 — Debugging Data-Tree Mismatches
1. Identify symptom class:
   - Wrong item pairing -> *List Matching mismatch* (Shortest vs Longest vs Cross Reference).
   - Diagonal lines instead of grid -> *Missing Cross Reference or Graft*.
   - Global operation executed per-branch -> *Needs Flatten*.
   - One-to-many relationship failing -> *Needs Graft on the singular list*.
2. Consult the decision-logic table in `references/DATA_TREES.md`:
   - Split Tree: check mask syntax (`{0;[0,2]}`, `{?}`, `{0;!(1)}`).
   - Path Mapper: check lexical mapping expressions (`{A;B}(i) -> {A}(B)`).
   - Prescribe minimal tree operations with before/after tree states shown.

### Workflow 5 — Live Canvas Inspection & Interactive Editing (Rhino 8)
When the user is running Rhino 8 and asks to inspect, debug, modify, or add components to their **current/active Grasshopper document**:
1. **Verify Connection**:
   - Run `gh-toolkit live status` (or `python3 <skill_dir>/scripts/gh_toolkit.py live status`).
   - If not connected, instruct the user to run `StartScriptServer` in the Rhino 8 command line.
2. **Inspect Active Canvas**:
   - Run `gh-toolkit live list` to see all objects, instance GUIDs, pins, and current slider/panel values.
   - Use `gh-toolkit live list --json` to get the complete live DAG topology.
3. **Perform Live Mutations**:
   - **Add Component**: `gh-toolkit live add "<Name>" --x 250 --y 150` (supports Native, Heteroptera, LegoPod, Magpie).
   - **Wire Pins**: `gh-toolkit live wire <src_id_or_name> <dst_id_or_name> -s 0 -t 0`
   - **Update Values**: `gh-toolkit live set <slider_or_panel> <new_val>`
   - **Unwire Pins**: `gh-toolkit live unwire <dst_id_or_name> -t 0`
   - **Remove**: `gh-toolkit live remove <id_or_name>`
4. **Trigger Recompute**:
   - Run `gh-toolkit live solve` to expire the solution, recalculate geometry, and refresh viewport preview.
5. **Quiet Persistence**:
   - Run `gh-toolkit live save [path]` to persist the active canvas to `.ghx` or `.gh` without UI prompts.

---

## 4. Toolkit CLI Cheatsheet

```bash
# 1. Inspect definition metadata & canvas components
python3 <skill_dir>/scripts/gh_toolkit.py info path/to/definition.gh

# 2. Lossless format conversion
python3 <skill_dir>/scripts/gh_toolkit.py to-ghx input.gh output.ghx
python3 <skill_dir>/scripts/gh_toolkit.py to-gh input.ghx output.gh
python3 <skill_dir>/scripts/gh_toolkit.py to-json input.gh graph.json

# 3. Live Rhino 8 & Grasshopper Canvas Operations
python3 <skill_dir>/scripts/gh_toolkit.py live status
python3 <skill_dir>/scripts/gh_toolkit.py live list
python3 <skill_dir>/scripts/gh_toolkit.py live add "Number Slider" --x 100 --y 100
python3 <skill_dir>/scripts/gh_toolkit.py live add "Panel" --x 300 --y 100
python3 <skill_dir>/scripts/gh_toolkit.py live add "Divide Curve" --x 500 --y 100
python3 <skill_dir>/scripts/gh_toolkit.py live wire "Number Slider" "Divide Curve" -s 0 -t "N"
python3 <skill_dir>/scripts/gh_toolkit.py live set "Number Slider" 24.0
python3 <skill_dir>/scripts/gh_toolkit.py live set "Panel" "Automated Agent Parameter"
python3 <skill_dir>/scripts/gh_toolkit.py live solve
python3 <skill_dir>/scripts/gh_toolkit.py live save ./LiveCanvasSnapshot.ghx
python3 <skill_dir>/scripts/gh_toolkit.py live open ./SynthesizedWorkflow.ghx

# 4. Batch extract embedded GhPython & C# scripts
python3 <skill_dir>/scripts/gh_toolkit.py extract-scripts ./definitions --out ./scripts

# 5. Native Grasshopper Component Inspection (212 cataloged components)
python3 <skill_dir>/scripts/gh_toolkit.py native --info "Divide Curve"
python3 <skill_dir>/scripts/gh_toolkit.py native --list Curve

# 6. Heteroptera Plugin Inspection & Automated Installer
python3 <skill_dir>/scripts/gh_toolkit.py heteroptera --status
python3 <skill_dir>/scripts/gh_toolkit.py heteroptera --install
python3 <skill_dir>/scripts/gh_toolkit.py heteroptera --info "Space Syntax"
python3 <skill_dir>/scripts/gh_toolkit.py heteroptera --list networks
python3 <skill_dir>/scripts/gh_toolkit.py heteroptera --recipes

# 7. LegoPod Plugin Inspection (42 cataloged components)
python3 <skill_dir>/scripts/gh_toolkit.py legopod --info "Build Attribute"
python3 <skill_dir>/scripts/gh_toolkit.py legopod --list Blocks

# 8. Magpie ML Plugin Inspection (14 cataloged components)
python3 <skill_dir>/scripts/gh_toolkit.py magpie --info "Correlation Matrix"
python3 <skill_dir>/scripts/gh_toolkit.py magpie --list Machines
```


---

## 5. Programmatic Graph Synthesis (`GHBuilder`)

Synthesize valid, ready-to-open Rhino definitions in pure Python without needing Rhino installed:

```python
from gh_toolkit import GHBuilder

builder = GHBuilder(name="ParametricCircleGrid")

# 1. Add Numeric Sliders
s_rad = builder.add_slider("s_rad", "Radius", min_val=1.0, max_val=20.0, current_val=5.0, pivot=(100, 100))
s_cnt = builder.add_slider("s_cnt", "Count", min_val=3, max_val=50, current_val=12, pivot=(100, 180))

# 2. Add Native & Plugin Components by Name (unified resolution)
c1 = builder.add_component("Circle (plane + radius)", "c1", pivot=(320, 120))
div = builder.add_component("Divide Curve", "div", pivot=(540, 120))
att = builder.add_component("Build Attribute", "att", pivot=(760, 120))  # LegoPod
ss = builder.add_component("Space Syntax", "ss", pivot=(980, 120))       # Heteroptera

# 3. Connect Wires: <alias>.<output> -> <alias>.<input>
builder.connect("s_rad.out", "c1.R")
builder.connect("c1.C", "div.C")
builder.connect("s_cnt.out", "div.N")

# 4. Inject Custom GhPython or C# Scripts
code = "import Rhino.Geometry as rg\npts = [rg.Point3d(p.X, p.Y, p.Z + 10) for p in pts_in]"
py_comp = builder.add_python_script("py_lift", code, inputs=["pts_in"], outputs=["pts_out"], pivot=(1200, 120))
builder.connect("div.P", "py_lift.pts_in")

# 5. Save as Binary .gh or XML .ghx
builder.save_gh("CircleGrid.gh")
builder.save_ghx("CircleGrid.ghx")
```

---

## 6. Comprehensive Knowledge Base Directory

* **[Tri-Plugin Computational Architecture](references/TRI_PLUGIN_ARCHITECTURE.md)**: Heteroptera (topology) + Magpie (ML) + LegoPod (BIM assets & metadata).
* **[Tri-Plugin Production Patterns](references/TRI_PLUGIN_PATTERNS.md)**: 6 verified cookbooks fusing topology, machine learning, and block metadata.
* **[Data Tree Theory & Decision Logic](references/DATA_TREES.md)**: Complete branch-matching mathematics, Split Tree grammar, and Path Mapper expressions.
* **[212 Native Component Schemas](references/NATIVE_COMPONENTS.md)**: Exhaustive port specifications, behaviors, and GUIDs.
* **[152 Heteroptera Component Schemas](references/HETEROPTERA_COMPONENTS.md)**: Vectors, Networks, Space Syntax, Uncertainty, Streaming.
* **[42 LegoPod Component Schemas](references/LEGOPOD_COMPONENTS.md)**: Blocks, Attributes, User Dictionaries, QuickBake, Hatches.
* **[14 Magpie Machine Learning Schemas](references/MAGPIE_COMPONENTS.md)**: PCA, T-SNE, Boltzmann, Kohonen Maps, Neural Networks.
* **[96 Parametric Design Patterns](references/NATIVE_PATTERNS.md)**: Field-tested recipes for attractors, paneling, meshes, Kangaroo 2, and Galapagos.
* **[Errata & Modernization](references/ERRATA_MODERNIZATION.md)**: 2014-vs-2026 plugin deprecations and replacements.
* **[Computational Geometry Glossary](references/GEOMETRY_GLOSSARY.md)**: 127 architectural geometry terms defined.
* **[Architectural Pillars & Recipes](references/ARCHITECTURAL_RECIPES.md)**: Production workflows (Masonry, Space Syntax, GIS, Section Slicing).
* **[Curated Script Library](references/SCRIPT_LIBRARY.md)**: Idiomatic GhPython & C# scripts.
* **[GUID Map](resources/guid-map.json)**: 127 component GUIDs extracted from McNeel production definitions.
* **[Native Catalog](resources/native_catalog.json)**: 212 components structured JSON index.
* **[Heteroptera Catalog](resources/heteroptera_catalog.json)**: 152 components indexed with full port metadata.
* **[LegoPod Catalog](resources/legopod_catalog.json)**: 42 components indexed with full port metadata.
* **[Magpie Catalog](resources/magpie_catalog.json)**: 14 machine-learning components indexed with full port metadata.
