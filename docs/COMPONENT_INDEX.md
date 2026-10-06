# Compact Component & GUID Quick-Reference
> High-density lookup table of core Grasshopper and Heteroptera components.

## 1. Core Native Grasshopper Components
| Component | Nick | Type GUID | Category | Key Inputs | Key Outputs |
|---|---|---|---|---|---|
| **Number Slider** | `Slider` | `57da07bd-ecab-415d-9d86-af36d7073abc` | Params | `-` | `Output` |
| **Panel** | `Panel` | `ca916113-d820-437b-9994-6ab08216173b` | Params | `in` | `out` |
| **GhPython Script** | `Python` | `410755b1-224a-4c1e-a407-bf32fb45ea7e` | Maths | `x, y, ...` | `out, a, ...` |
| **C# Script** | `C#` | `04d46c59-f81d-407b-871d-f8fa79244093` | Maths | `x, y, ...` | `out, A, ...` |
| **Construct Point** | `Pt` | `35520be3-db72-4638-b7eb-ee7fbbeec2c0` | Vector | `X, Y, Z` | `Pt` |
| **Vector XYZ** | `Vec` | `91e84aa9-94b1-419b-ab09-9069d31d45dc` | Vector | `X, Y, Z` | `V` |
| **Unit Z** | `Z` | `620e231d-b8eb-4e67-9bf4-e758a01f5647` | Vector | `Factor` | `V` |
| **Divide Curve** | `Div` | `26d11e4f-6f9a-412e-a55e-f00e932b53f6` | Curve | `C, N, K` | `P, T, t` |
| **Circle** | `Cir` | `8b6e680a-9d6e-4bb5-a36c-9c748c08197c` | Curve | `P, R` | `C` |
| **Rectangle** | `Rec` | `6c459846-95ff-4be5-a4b5-4b08709ca587` | Curve | `P, X, Y, R` | `R, L` |
| **Move** | `Move` | `8ec0a1cf-b8d4-49a6-bd27-4bf69147514a` | Transform | `G, T` | `G` |
| **Rotate** | `Rot` | `2e4dc27f-9721-4fce-bc0c-ee43e6206dbe` | Transform | `G, A, P` | `G` |
| **Series** | `Series` | `26c518b2-570a-4a25-a13a-a1b7e6184a44` | Sets | `S, N, C` | `S` |
| **Range** | `Range` | `fbdb108a-cf8e-4735-86ef-d7ee76569ec1` | Sets | `D, N` | `R` |
| **Remap Numbers** | `Remap` | `42c1143c-ae74-4b53-9a3b-2ee0fbb1a98e` | Maths | `V, S, T` | `M` |
| **Distance** | `Dist` | `7d100085-f5da-485a-8b83-a41e974e64f0` | Vector | `A, B` | `D` |
| **List Item** | `Item` | `2e1f6e2b-2e9a-4a69-a1c2-6f29a071597d` | Sets | `L, i, W` | `i` |
| **List Length** | `Lng` | `b5883ef8-2b8e-4a66-be99-231362e67df1` | Sets | `L` | `L` |
| **Merge** | `Merge` | `46eac1d6-4444-42ea-9e79-bc91ae79b882` | Sets | `D1, D2, ...` | `R` |
| **Entwine** | `Entwine` | `300405fc-a86e-44d4-9d51-40ff42cbb9a3` | Sets | `D0, D1, ...` | `R` |
| **Trim Tree** | `Trim` | `441b8981-d147-4929-873b-eb6368d90472` | Sets | `T, D` | `T` |
| **Custom Preview** | `Preview` | `2e3c0b56-3c5e-4efb-91c6-29177e7d6cfb` | Display | `G, M, S` | `-` |

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
