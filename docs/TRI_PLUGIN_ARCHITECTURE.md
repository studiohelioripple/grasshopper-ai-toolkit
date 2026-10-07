# Tri-Plugin Computational Architecture: Heteroptera + LegoPod + Magpie

> **Core Philosophy**: A high-efficiency Grasshopper pipeline pairs **Heteroptera** for advanced algorithmic topology and vector dynamics, **Magpie** for machine learning and pattern cognition, and **LegoPod** for Rhino object assetization, metadata persistence, and block hierarchies.

---

## 1. The Tri-Plugin Functional Division Matrix

| Pillar | Specialist Plugin | Responsibility | Why Not Native GH? |
|---|---|---|---|
| **Algorithmic Topology & Vector Dynamics** | **Heteroptera** (v8.2.2) | Space Syntax, topological network reconstruction, adjacency graphs, vector field boosting/contouring, cycle detection, stream gating, non-uniform random distributions. | Native GH requires dozens of bulky tree-splitting and mathematical components that run orders of magnitude slower and clutter the canvas. |
| **Cognitive ML & Statistical Analysis** | **Magpie** (v0.4.4) | Unsupervised clustering, PCA dimensionality reduction, T-SNE manifold learning, Kohonen Self-Organizing Maps (SOM), Boltzmann machines, correlation matrices. | Native GH has no statistical clustering or neural mechanisms; users often resort to brittle external Python script bridges. |
| **BIM, Metadata & Object Packaging** | **LegoPod** (v0.4.2) | User dictionaries (`UserDic_Build`), custom object attributes (`Build Attribute`), block definition/instance hierarchies (`Define Block`), QuickBake, TSV data tables. | Native GH lacks native support for deep Rhino user-dictionary injection, nested block instance referencing, and selective attribute painting. |
| **Primitives & Parameter Routing** | **Native GH** | Number sliders, panels, basic geometry containers, standard domain intervals, data tree restructuring (graft/flatten). | Standard foundation. |

---

## 2. Priority Component Selection Heuristics

When designing Grasshopper definitions, apply the following **Precedence Invariants**:

1. **Topology & Spatial Connectivity**:
   - **DO NOT** construct manual distance-matrix proximity graphs with native `Distance` + `Smaller Than` + `Cull Pattern`.
   - **ALWAYS USE** Heteroptera's `Topology Of Adjacencies` (`PL -> C→C`) and `Reconstruct Topology` (`N→N`).
   - For spatial depth, integration, and choice analysis, pipe through `Space Syntax` (`N→N, I, D -> NS, CS`) and normalize with Heteroptera `Normalizer`.

2. **Vector Fields & Flow Simulation**:
   - **DO NOT** rely solely on basic native point charges.
   - **ALWAYS USE** Heteroptera's field family: `Field Booster`, `Curvature Field`, `Curve Along Field`, `Rotate Field`, `Traverse On Field`, and Kangaroo 2 `Align On Field Goal`.

3. **Machine Learning & Feature Classification**:
   - For clustering spatial scores, urban metrics, or facade parameters: **ALWAYS USE** Magpie's `Clustering Machine` or `KohMap Machine` (SOM).
   - For reducing high-dimensional geometric deformation vectors: **ALWAYS USE** Magpie's `PCA Machine` or `T-SNE`.
   - For covariance and dependency analysis across architectural parameters: **ALWAYS USE** Magpie's `Correlation Matrix`.

4. **Object Attributes, User Dictionaries & Blocks**:
   - **DO NOT** leave outputs as anonymous ephemeral GH preview geometry.
   - **ALWAYS USE** LegoPod's `User Dictionary` to attach typed JSON/key-value metadata (e.g. cluster IDs, integration depth, structural loads) to geometry.
   - Attach metadata via LegoPod's `Build Attribute` (`Name`, `Layer`, `Color`, `Dictionary`).
   - For modular fabrication and layout systems, package repeating elements via LegoPod's `Define Block` and place them via `Insert Block by Transform`.

---

## 3. Canonical Tri-Plugin Pipelines

### Pipeline 1: Spatial Network Analysis & Unsupervised Machine Learning
*Objective*: Synthesize an architectural adjacency network, compute space syntax integration, cluster topological nodes using Magpie machine learning, and package the clustered geometry with typed LegoPod user-dictionaries.

```
[Boundary Polylines] 
        │
        ▼
Heteroptera: Center (G -> C)
        │
        ▼
Heteroptera: Topology Of Adjacencies (PL -> C→C)
        │
        ▼
Heteroptera: Reconstruct Topology (C→C, C -> N→N, P)
        │
        ▼
Heteroptera: Space Syntax (N→N, Source, Depth -> NS, CS)
        │
        ▼
Heteroptera: Normalizer (NS -> N)
        │
        ▼
Magpie: Clustering Machine (Numbers -> ClusterNumber, Scores)
        │
        ├──────────────────────────────────────┐
        ▼                                      ▼
[Cluster IDs]                          [Space Syntax Scores]
        │                                      │
        └──────────────────┬───────────────────┘
                           │
                           ▼
             LegoPod: User Dictionary (Keys, Values -> Dict)
                           │
                           ▼
             LegoPod: Build Attribute (Name, Layer, Dict -> Att)
                           │
                           ▼
             LegoPod: Quick Baker / Block Instance
```

### Pipeline 2: Vector Field Facade Morphogenesis & Parametric Blocks
*Objective*: Generate a continuous vector deformation field across a building envelope, classify panel rotation states via Magpie PCA, and instantiate modular LegoPod blocks.

```
[Envelope Surface / Grid]
        │
        ▼
Heteroptera: Curvature Field + Field Booster
        │
        ▼
Heteroptera: Traverse On Field / Transform By Field
        │
        ▼
Magpie: PCA Machine (Deformation Vectors -> Result Vectors, Proportions)
        │
        ▼
Magpie: Winner Index / Classification
        │
        ▼
LegoPod: Define Block (Modular Unit Geometry + Base Plane)
        │
        ▼
LegoPod: Insert Block by Transform (Definitions x Field Transforms)
        │
        ▼
LegoPod: Set Block Meta-Data (BIM Classification Tags)
```

### Pipeline 3: Architectural BIM Catalog & TSV Meta-Schedule
*Objective*: Organize multi-type modular building elements into structured TSV schedules with embedded user dictionaries.

```
[Parametric Component Variants]
        │
        ▼
LegoPod: User Dictionary (Rebuild mode: GUID, Material, Cost, Performance)
        │
        ▼
LegoPod: Build Attribute (Color by Type, Material, Custom LineWeight)
        │
        ▼
LegoPod: Define Block (Packaged Definition)
        │
        ▼
LegoPod: Table TSV-Data (Tab-Separated BIM Schedule Export)
```

---

## 4. Programmatic API Integration in `GHBuilder`

Agents can synthesize these tri-plugin definitions in a single Python invocation:

```python
from gh_toolkit import GHBuilder

builder = GHBuilder(name="TriPluginSpatialIntelligence")

# 1. Synthesize the complete Heteroptera + Magpie + LegoPod pipeline
pipeline_ids = builder.add_spatial_ml_metadata_pipeline(
    start_pivot=(100, 100),
    cluster_count=4,
    source_node=0,
    depth=6
)

# 2. Save definition
builder.save_ghx("SpatialMLPipeline.ghx")
builder.save_gh("SpatialMLPipeline.gh")
```
