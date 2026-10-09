# Compact Component & GUID Quick-Reference
> High-density lookup table of core Grasshopper and Heteroptera components.

## 1. Core Native Grasshopper Components
| Component | Nick | Type GUID | Category | Key Inputs | Key Outputs |
|---|---|---|---|---|---|
| **Number Slider** | `Slider` | `57da07bd-ecab-415d-9d86-af36d7073abc` | Params | `-` | `Output` |
| **Panel** | `Panel` | `ca916113-d820-437b-9994-6ab08216173b` | Params | `in` | `out` |
| **GhPython Script** | `Python` | `410755b1-224a-4c1e-a407-bf32fb45ea7e` | Maths | `x, y, ...` | `out, a, ...` |
| **C# Script** | `C#` | `04d46c59-f81d-407b-871d-f8fa79244093` | Maths | `x, y, ...` | `out, A, ...` |
| **Construct Point** | `Pt` | `3581f42a-9592-4549-bd6b-1c0fc39d067b` | Vector | `X, Y, Z` | `Pt` |
| **Vector XYZ** | `Vec` | `56b92eab-d121-43f7-94d3-6cd8f0ddead8` | Vector | `X, Y, Z` | `V` |
| **Unit Z** | `Z` | `9103c240-a6a9-4223-9b42-dbd19bf38e2b` | Vector | `Factor` | `V` |
| **Divide Curve** | `Div` | `2162e72e-72fc-4bf8-9459-d4d82fa8aa14` | Curve | `C, N, K` | `P, T, t` |
| **Circle** | `Cir` | `807b86e3-be8d-4970-92b5-f8cdcb45b06b` | Curve | `P, R` | `C` |
| **Rectangle** | `Rec` | `d93100b6-d50b-40b2-831a-814659dc38e3` | Curve | `P, X, Y, R` | `R, L` |
| **Move** | `Move` | `b40f28a2-ba30-4ac2-afe5-a6ece7f985fc` | Transform | `G, T` | `G` |
| **Rotate** | `Rot` | `b661519d-43fd-4e5a-b244-d54d9fae2bde` | Transform | `G, A, P` | `G` |
| **Series** | `Series` | `e64c5fb1-845c-4ab1-8911-5f338516ba67` | Sets | `S, N, C` | `S` |
| **Range** | `Range` | `9445ca40-cc73-4861-a455-146308676855` | Sets | `D, N` | `R` |
| **Remap Numbers** | `Remap` | `2fcc2743-8339-4cdf-a046-a1f17439191d` | Maths | `V, S, T` | `M` |
| **Distance** | `Dist` | `93b8e93d-f932-402c-b435-84be04d87666` | Vector | `A, B` | `D` |
| **List Item** | `Item` | `285ddd8a-5398-4a3e-b3c2-361025711a51` | Sets | `L, i, W` | `i` |
| **List Length** | `Lng` | `1817fd29-20ae-4503-b542-f0fb651e67d7` | Sets | `L` | `L` |
| **Merge** | `Merge` | `3cadddef-1e2b-4c09-9390-0e8f78f7609f` | Sets | `D1, D2, ...` | `R` |
| **Entwine** | `Entwine` | `c9785b8e-2f30-4f90-8ee3-cca710f82402` | Sets | `D0, D1, ...` | `R` |
| **Trim Tree** | `Trim` | `1177d6ee-3993-4226-9558-52b7fd63e1e3` | Sets | `T, D` | `T` |
| **Custom Preview** | `Preview` | `537b0419-bbc2-4ff4-bf08-afe526367b2c` | Display | `G, M, S` | `-` |

## 2. Heteroptera Plugin Components (Top Selected)
| Component | Nick | Type GUID | Category | Key Inputs | Key Outputs |
|---|---|---|---|---|---|
| **Space Syntax** | `SpaceSyntax` | `d4077291-8c30-4313-8bb3-45a86138c521` | Heteroptera.Networks | `Node->Node, Source, Depth` | `Node SS, Conn SS` |
| **Topology Of Adjacencies** | `Adjacency` | `980bd972-3623-40a9-85d9-89807ce118c9` | Heteroptera.Networks | `Polylines, Method, Tol` | `Cell->Cell` |
| **Reconstruct Topology** | `ReconTopo` | `683305c6-fd18-4102-b142-f5c799d7069c` | Heteroptera.Networks | `Node->Node, Edge->Node, Pts` | `Node->Node, Pts, Lines` |
| **Shortest Route** | `ShortRoute` | `992702c7-9416-4663-8be4-beb8521810ba` | Heteroptera.Networks | `Node->Node, Start, End` | `Route, Length, Edges` |
| **Proximity Network** | `ProxNet` | `8b05233a-b681-40b2-8b83-51b2cdd459c5` | Heteroptera.Networks | `Points, Distance, MaxN` | `Node->Node, Lines` |
| **Center** | `Center` | `3c5edcba-b7a5-4710-b076-4b19a7080a2b` | Heteroptera.Geometry | `Geometry` | `Center, Area, Vol` |
| **Fast Sweep** | `FastSweep` | `a9ffec44-c715-4ba8-9c60-c3d56fcfd515` | Heteroptera.Geometry | `Rail, Section` | `Brep` |
| **Cycle By Planar Mapping** | `CyclePlanar` | `116b47c0-f472-4911-b4fa-4d1e3895e8e3` | Heteroptera.Geometry | `Points, Plane` | `Cycles` |
| **Normalizer** | `Normalizer` | `5d820462-ea9b-4663-875f-b519c0de2340` | Heteroptera.Maths | `Numbers` | `Numbers, Domain` |
| **Symmetric Domain** | `SymDomain` | `17342b5c-486a-493f-846f-c12e8739121a` | Heteroptera.Maths | `Value` | `Domain` |
| **Weighted Allocator** | `WeightAlloc` | `5c8e312d-1ea2-45e3-8557-46e7f12e8417` | Heteroptera.Uncertainty | `Weights, Count, Seed` | `Indices` |
| **Slingshot Allocator** | `Slingshot` | `ef32b535-71bb-4573-b27e-85a0cbb75225` | Heteroptera.Uncertainty | `Indices, Dist, Seed` | `Allocation` |
| **Careless Range** | `Careless` | `85a0889c-482a-4318-b2e3-2e40d6c1b35b` | Heteroptera.Uncertainty | `Domain, Steps, Jitter, Seed` | `Values` |
| **Stream Freeze** | `Freeze` | `8e6c73df-9730-4e00-a548-5c468e82efea` | Heteroptera.Streaming | `Data, Freeze` | `Data` |
| **ToolsUnicode** | `Unicode` | `3782b5f1-3ec6-419f-9c02-86e115bc5c9a` | Heteroptera.Utilities | `Text, Encoding` | `Text` |
| **Curve Force Field** | `CrvField` | `3ae586b6-bfb0-456d-8ca1-45bc8ba342df` | Heteroptera.Vectors | `Curves, Radius, Force` | `Field` |
| **Point Force Field** | `PtField` | `f64860b7-4b7f-4b07-9e90-c24c25f46a2a` | Heteroptera.Vectors | `Points, Radius, Force` | `Field` |
| **Evaluate Field** | `EvalField` | `df6c413b-8217-4560-b6ce-b7a421272eb7` | Heteroptera.Vectors | `Field, SamplePoints` | `Vectors` |

*For all 152 Heteroptera components, run `gh-toolkit heteroptera --list all` or inspect `docs/HETEROPTERA_REFERENCE.md`.*
