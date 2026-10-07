# Tri-Plugin Architectural Patterns Catalog: Heteroptera + LegoPod + Magpie

> **Purpose**: A comprehensive cookbook of 6 verified production patterns fusing **Heteroptera** (topology & fields), **Magpie** (machine learning & feature extraction), and **LegoPod** (BIM metadata, user dictionaries & block hierarchies).

---

## Pattern 1: Spatial Network Morphology & Autonomous Node Clustering

### Context & Intent
In complex urban layouts, campus plans, or high-density architectural programs, spatial integration must be evaluated topologically. Native Grasshopper workarounds rely on brute-force distance matrix calculations that choke on large graphs. This pattern uses **Heteroptera** for topological graph reconstruction and Space Syntax, **Magpie** for unsupervised clustering of node integration behaviors, and **LegoPod** to attach cluster tags directly into Rhino geometry user-dictionaries.

### Canonical Node Graph
```
=== Section 1: Topological Spatial Graph (Heteroptera) ===
Boundary Polylines (Params > Geometry) [PL]
  -> Center (Heteroptera > Geometry) [Center]
  -> Topology Of Adjacencies (Heteroptera > Networks) [Adj]
Center.C -> Reconstruct Topology.Points (Optional)
Adj.Cell→Cell -> Reconstruct Topology.Node→Node {branches: N}
Reconstruct.Node→Node -> Space Syntax.Node→Node
Slider[0..50, 0] -> Space Syntax.Source
Slider[1..15, 6] -> Space Syntax.Depth
Space Syntax.Node SpaceSyntax -> Normalizer.Numbers {flat, N nodes}

=== Section 2: Cognitive Clustering (Magpie) ===
Normalizer.Numbers -> Clustering Machine.Inputs {flat list}
Slider[2..10, 4] -> Clustering Machine.Clusters
Slider[1..100, 42] -> Clustering Machine.Random Seed
Normalizer.Numbers -> PCA Machine.Data
Slider[1..3, 2] -> PCA Machine.Dimension

=== Section 3: Object Metadata & BIM Packaging (LegoPod) ===
Panel["IntegrationCluster"] -> User Dictionary.Keys
Clustering Machine.ClusterNumber -> User Dictionary.Values {flat}
User Dictionary.Dictionary -> Build Attribute.Dictionary
Panel["Spatial_Zone"] -> Build Attribute.Layer
Clustering Machine.ClusterNumber -> Gradient.t -> Build Attribute.Color
Build Attribute.Attribute -> Reconstruct.Points -> Quick Baker.Geometries
```

### Data Tree States & Invariants
- `Adj.Cell→Cell`: Nested integer topology tree `{i}` containing topological neighbor indices.
- `Space Syntax.Node SpaceSyntax`: Flat integer array of integration depth scores.
- `Normalizer.Numbers`: Normalized domain `[0.0, 1.0]`.
- `Clustering Machine.ClusterNumber`: Integer cluster assignments (`0` to `K-1`).

---

## Pattern 2: Continuous Curvature Vector Fields & Modular Facade Blocks

### Context & Intent
Generating dynamic facade envelopes using continuous vector fields. Instead of placing independent panels, **Heteroptera** computes a smooth curvature field across the envelope, **Magpie** reduces panel orientation states via PCA to cluster panels into standard fabrication families, and **LegoPod** defines modular block definitions and instantiates them via 3D transformation matrices.

### Canonical Node Graph
```
=== Section 1: Surface Curvature Field (Heteroptera) ===
Base Surface (Params > Geometry) [Srf]
  -> Curvature Field (Heteroptera > Vectors) [CurvField]
CurvField.Field -> Field Booster.Field
Slider[0.5..5.0, 1.5] -> Field Booster.Boost
Field Booster.Field -> Traverse On Field.Field
Divide Surface.Points -> Traverse On Field.Points

=== Section 2: Dimensionality Reduction & Family Classification (Magpie) ===
Traverse On Field.Vectors -> PCA Machine.Data {N x 3 deformation vectors}
Slider[1..3, 2] -> PCA Machine.Dimension
PCA Machine.Result Vectors -> Correlation Matrix.Data
PCA Machine.Proportions -> Panel [Variance Explained]

=== Section 3: Modular Block Definition & Placement (LegoPod) ===
Unit Panel Geometry (Params > Geometry) [PanelGeo]
  -> Define Block.Geometries
Panel["ModularFacade_TypeA"] -> Define Block.Name
Plane.WorldXY -> Define Block.RefPlane
Define Block.Definition -> Insert Block by Transform.Definition
Traverse On Field.Transforms -> Insert Block by Transform.Transform
Panel["FacadeUnit"] -> Build Attribute.Name
Build Attribute.Attribute -> Define Block.Attributes (Optional)
```

### Data Tree States & Invariants
- `Curvature Field`: Evaluates principal curvature tensors across UV surface domains.
- `PCA Machine.Result Vectors`: 2D principal component projections of 3D spatial field deformations.
- `Insert Block by Transform`: Transforms unit block instances without duplicating geometry definitions in the Rhino document.

---

## Pattern 3: Topological Cycle Extraction & Adaptive Louver Inpainting

### Context & Intent
Detecting closed volumetric cells or polygonal loops in architectural wireframes. Heteroptera features dedicated cycle-finding algorithms that extract polygonal rings from raw wireframes. LegoPod then creates hatch boundaries and color-coded material attributes.

### Canonical Node Graph
```
=== Section 1: Wireframe Graph & Cycle Extraction (Heteroptera) ===
Network Curves (Params > Geometry) [Crvs]
  -> Topology Of Adjacencies (Heteroptera > Networks) [Adj]
Adj.Cell→Cell -> Cycle By Planar Mapping (Heteroptera > Networks) [Cycles]
Cycles.Polylines -> Center (Heteroptera > Geometry) [Center]

=== Section 2: Planar Boundary Sorting & Gating (Heteroptera) ===
Cycles.Polylines -> Area.Geometry
Area.Area -> Careless Range (Heteroptera > Maths) [Range]
Range.Values -> ANSI Gate (Heteroptera > Streaming) [Gate]

=== Section 3: Hatching & Material Attribution (LegoPod) ===
Gate.Passed -> Create Hatch.Curves
Slider[0..5, 1] -> Create Hatch.PatternIndex
Panel["Wood_Louver"] -> Build Attribute.Material
Build Attribute.Attribute -> Paint Attribute.Attribute
Gate.Passed -> Paint Attribute.Geometries
```

---

## Pattern 4: Adaptive Stream Multiplexing & Supervised Classification

### Context & Intent
In responsive or multi-objective design explorations, geometric streams must be dynamically gated and categorized. Heteroptera manages stream routing through ANSI-gates and latch switches; Magpie trains a classification machine on performance metrics; LegoPod logs the data into TSV tables.

### Canonical Node Graph
```
=== Section 1: Performance Metric Evaluation (Native) ===
Massing Geometry [Geo] -> Solar Analysis + Floor Area Ratio
Metrics [Solar, FAR, Cost] -> Magpie: Classification Machine.Inputs

=== Section 2: Supervised Neural Classification (Magpie) ===
Training Features -> Classification Machine.Inputs
Training Labels -> Classification Machine.Labels
Slider[0.01..0.5, 0.05] -> Classification Machine.LearningRate
Classification Machine.Predicted -> Panel [Classified Type]

=== Section 3: Adaptive Stream Routing (Heteroptera) ===
Classification Machine.Predicted -> Event Driven Gate (Heteroptera > Streaming) [Gate]
Massing Geometry -> Gate.Data

=== Section 4: BIM TSV Schedule Export (LegoPod) ===
Classification Machine.Predicted -> User Dictionary.Values
Panel["BIM_Classification"] -> User Dictionary.Keys
User Dictionary.Dictionary -> Table TSV-Data.Data
Panel["\t"] -> Table TSV-Data.Format
Table TSV-Data.Data -> Panel [TSV Schedule Output]
```

---

## Pattern 5: Parametric Product Catalog & Metadata Schedule

### Context & Intent
Generating a manufactured architectural product line (e.g. modular casework, curtain wall mullions, structural brackets). LegoPod provides industrial-grade block definitions, user dictionaries, and formatted TSV data exports.

### Canonical Node Graph
```
=== Section 1: Parametric Component Matrix (Native) ===
Box Parameters (W, H, D) -> Box Primitive
Box Primitive -> LegoPod: User Dictionary (Keys: ["Width", "Height", "Depth", "SKU"])

=== Section 2: Attribute Construction (LegoPod) ===
User Dictionary.Dictionary -> Build Attribute.Dictionary
Panel["Assembly_Cabinet"] -> Build Attribute.Name
Panel["Millwork_Layer"] -> Build Attribute.Layer
Color Swatch -> Build Attribute.Color

=== Section 3: Definition & Schedule Table (LegoPod) ===
Box Primitive -> Define Block.Geometries
Build Attribute.Attribute -> Define Block.Attributes (Optional)
Panel["Unit_Block_A"] -> Define Block.Name
User Dictionary.Dictionary -> Table TSV-Data.Data
Table TSV-Data.Data -> Panel [Catalog Schedule]
```

---

## Pattern 6: Uncertainty-Driven Morphogenesis via Non-Uniform Random Fields

### Context & Intent
Standard Grasshopper `Random` generates uniform random distributions, which produce unnatural, unorganic patterns. Heteroptera provides continuous noise and statistical distributions (Gaussian, Simplex, Poisson), while Magpie computes winner indices and LegoPod places fitted instance bounding boxes.

### Canonical Node Graph
```
=== Section 1: Non-Uniform Random Field Generation (Heteroptera) ===
Grid Points (Params > Geometry) [Pts]
  -> Gaussian (Heteroptera > Uncertainty) [Gauss]
Slider[0.0..10.0, 2.5] -> Gauss.StandardDeviation
Slider[0.0..100.0, 50.0] -> Gauss.Mean
Gauss.Numbers -> Noise Field (Heteroptera > Vectors) [NoiseField]

=== Section 2: Stochastic Selection & Winner Index (Magpie) ===
NoiseField.Vectors -> Winner Index.Inputs
Winner Index.Index -> List Item.Index

=== Section 3: Parametric Bounding Box Fitting (LegoPod) ===
List Item.Items -> Bounding Box.Geometry
Bounding Box.Box -> Insert Block by Box.Box
Define Block.Definition -> Insert Block by Box.Definition
```
