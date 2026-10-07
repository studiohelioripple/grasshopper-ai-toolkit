# Heteroptera Component Reference

Comprehensive reference for **Heteroptera** (v8.2.2) in Grasshopper.
Total verified components: **152**.
Synthesized directly via offline assembly analysis and runtime parameter reflection.

## Table of Contents

- [Vectors](#vectors) — 36 components
- [Utilities](#utilities) — 14 components
- [Uncertainty](#uncertainty) — 22 components
- [Streaming](#streaming) — 16 components
- [Networks](#networks) — 31 components
- [Maths](#maths) — 18 components
- [Geometry](#geometry) — 14 components
- [NAN](#nan) — 1 components

---

## Vectors

### Align On Field Goal
- **Tab**: Heteroptera > Vectors | **Type GUID**: `4c5667c7-1355-44c5-9cf9-5681f45c7818`
- **Alias**: `AlignOnField`
- **Inputs**:
  - `Line` (`L`): Line [item] — Line to be aligned
  - `Field` (`F`): Field [item] — Field to align on
  - `Directional` (`D`): Boolean [item] — Force to align the line on the field based on line direction
  - `Strength` (`S`): Number [item] — Weight of the goal
- **Outputs**:
  - `Goal` (`G`): Generic Data [item] — FieldAlign Goal
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Along Field Goal
- **Tab**: Heteroptera > Vectors | **Type GUID**: `bcdc5af8-5cf9-4a14-a45f-a8ee76f576bb`
- **Alias**: `FieldAlonge`
- **Inputs**:
  - `Point` (`P`): Point [item] — Effected point
  - `Field` (`F`): Field [item] — Field to align on
  - `ForceType` (`D`): Integer [item] — ForceType
  - `Factor` (`F`): Number [item] — Factor
  - `Strength` (`S`): Number [item] — Weight of the goal
- **Outputs**:
  - `Goal` (`G`): Generic Data [item] — FieldAlign Goal
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Angle Goal
- **Tab**: Heteroptera > Vectors | **Type GUID**: `dda0a520-8b67-4b99-8499-fbcd872dd834`
- **Alias**: `Angle`
- **Inputs**:
  - `Line` (`L`): Line [item] — Line to align
  - `Direction` (`V`): Vector [item] — Vector to calculate angle from
  - `Angle` (`A`): Number [item] — Aligning angle
  - `Approach` (`A`): Number [item] — [0..1]  from Axis-Align to Cross-Align, 0.5 = Perpendicular
  - `Strength` (`S`): Number [item] — Weight of the goal
- **Outputs**:
  - `Goal` (`G`): Generic Data [item] — Angled-Direction Goal
- **Behavior**: A Kangaroo-Goal, to maintain the angle of a line respect to a given vector by an angle
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Erector Goal
- **Tab**: Heteroptera > Vectors | **Type GUID**: `e8d56afb-15b2-4ef3-bea6-27b861bda314`
- **Alias**: `Erector`
- **Inputs**:
  - `Points` (`P`): Point [list] — Chain of points to rectify
  - `Relaxation` (`R`): Number [item] — Length relaxation
  - `Strength` (`S`): Number [item] — Weight of the goal
- **Outputs**:
  - `Goal` (`G`): Generic Data [item] — Erection Goal
- **Behavior**: A Kangaroo-Goal, to erect a chain of points
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Slop Gole
- **Tab**: Heteroptera > Vectors | **Type GUID**: `9e812d8c-07db-4270-a873-9556394a0016`
- **Alias**: `Slope`
- **Inputs**:
  - `Line` (`L`): Line [item] — Line whose slope is constrained
  - `Slope` (`S`): Number [item] — Target slope as a percentage of height to planar distance 0.1 means 10%, and 1.0 is considered 100% 
  - `Plane` (`P`): Plane [item] — Plane from which to calculate slope
  - `Approach` (`A`): Number [item] — [0.0 ~ 1.0]  from Axis-Align to Cross-Align, 0.5 = Perpendicular
  - `Strength`: Number [item] — Weight of the goal
- **Outputs**:
  - `Goal` (`G`): Generic Data [item] — Angled-Direction Goal
- **Behavior**: A Kangaroo goal that keeps the slope of the given line relative to a plane
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Trap Goal
- **Tab**: Heteroptera > Vectors | **Type GUID**: `ac4728f6-a875-46be-b648-fa54ebe252eb`
- **Alias**: `TrapForce`
- **Inputs**:
  - `Line` (`L`): Line [item] — Line between a pair of point
  - `Space` (`S`): Number [item] — The space within force would be eased down
  - `Criteria` (`C`): Number [item] — The criteria distance scope for decay
  - `Decay` (`D`): Number [item] — Decay-factor in [1/l^d]  where is the calculated distance =  len/criteria and, d=decay-factor 
  - `Strength` (`S`): Number [item] — Weight of the goal
- **Outputs**:
  - `Goal` (`G`): Generic Data [item] — FieldAlign Goal
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Display Fied
- **Tab**: Heteroptera > Vectors | **Type GUID**: `860267d8-1aef-4aae-b93b-e678c3b31871`
- **Alias**: `Display Field`
- **Inputs**:
  - `Field` (`F`): Field [list] — Field to evaluate
  - `Rectangle` (`R`): Rectangle [item] — Domain of the grid
  - `Size` (`S`): Number [item] — Distance between points of the grid
- **Outputs**: none
- **Behavior**: Display Field
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Display Tensors
- **Tab**: Heteroptera > Vectors | **Type GUID**: `b0eb2796-9ea6-4019-9854-07e94a4952df`
- **Alias**: `Field@Point`
- **Inputs**:
  - `Field` (`F`): Field [list] — Field to evaluate
  - `Point` (`P`): Point [list] — Point to evaluate at
- **Outputs**:
  - `Tensor` (`T`): Vector [item] — Field tensor at the sample location
  - `Scale` (`S`): Number [item] — Scalar Value
  - `Color` (`C`): Colour [item] — Directional color of the tensor at the sample location
- **Behavior**: Display Field at point
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Eponential Effective Vectors
- **Tab**: Heteroptera > Vectors | **Type GUID**: `8b1e5637-9a87-491e-92d6-ce1a9f6c5ec1`
- **Alias**: `E-Vectors`
- **Inputs**:
  - `Points` (`P`): Point [item] — The base-point from which vectors would be calculated
  - `Attractors` (`A`): Point [list] — List of Attractor Points
  - `Radius` (`P`): Number [item] — The optional number, to the power of which the force would decay by distance. . Setting the number to 2 applies the inverse-square law for distance. If omitted, the default value of 1 is used, which means for example if the distance is doubled the force will be half
- **Outputs**:
  - `Vectors` (`V`): Vector [item] — The  Bounded (normalized Set) respectively effective vectors
  - `Max-D` (`D`): Number [item] — The maximum distance
  - `Max-V` (`X`): Number [item] — The maximum intensity
  - `Mean-V` (`V`): Number [item] — The Average intensity
- **Behavior**: Calculates the exponential effective attraction vectors
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Field Booster
- **Tab**: Heteroptera > Vectors | **Type GUID**: `ebaf9ed8-eabe-44b0-8035-00694e624a14`
- **Alias**: `FBooster`
- **Inputs**:
  - `Field` (`F`): Field [item] — Base Field
  - `Booster` (`B`): Field [item] — Booster field
  - `Boost` (`V`): Number [item] — Boost Value. The power value booster.
- **Outputs**:
  - `Field` (`F`): Field [item] — The resultant field
- **Behavior**: Boost a field's tensors by another field.
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Field Contour
- **Tab**: Heteroptera > Vectors | **Type GUID**: `d1ce6b5a-a0b3-4f4e-ba55-6e5b7f402bc8`
- **Alias**: `Contour`
- **Inputs**:
  - `Field` (`F`): Field [list] — Field to evaluate
  - `Section` (`S`): Rectangle [item] — Rectangle describing section
  - `Value` (`V`): Number [list] — Charge value in scalar field to draw contour line for
  - `Size` (`S`): Number [item] — Detail size
- **Outputs**:
  - `Contour` (`C`): Curve [item] — IsoCurve Contour Lines
- **Behavior**: Create MetaBall-Like contours out of a field
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Field Projector
- **Tab**: Heteroptera > Vectors | **Type GUID**: `12cae02c-544d-4df8-970d-ec2c02b02f12`
- **Alias**: `FProjector`
- **Inputs**:
  - `Field` (`F`): Field [item] — Input Field to Project (Base Field)
  - `Datum` (`D`): Generic Data [item] — Object to project the field on. Supported types as a Datum are:  [Plane, MetaVector, Field, Surface, Mesh]
  - `Absolute` (`A`): Boolean [item] — Absolute Projection. If true, the tensor will be calculated from the projection point on datum, otherwise the projection just be applied to the vector in place  
- **Outputs**:
  - `Field` (`F`): Field [item] — The resultant field
- **Behavior**: Project a field on a datum.
A datum can be [Plane, MetaVector, Field, Mesh, Surface] 
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Field Wiper
- **Tab**: Heteroptera > Vectors | **Type GUID**: `0ecca535-04d6-47d0-a00f-6b6cd2db111c`
- **Alias**: `FWiper`
- **Inputs**:
  - `Field` (`F`): Field [item] — Base-Field, which would be wiped locally.
  - `Element` (`E`): Generic Data [list] — A list comprising elements of type: [Point, Plane, Curve, Surface or Mesh] as the wiper set 
  - `Distance` (`D`): Number [list] — Effective Distance for each element
  - `Charge` (`C`): Number [list] — List of charging values
- **Outputs**:
  - `Field` (`F`): Field [item] — The resultant field
- **Behavior**: Locally wipe out a field using a geometric element as an attractor.
 It either weakens or enervates the tensors nearby to the given geometric object.
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Gaussian Effective Vectors
- **Tab**: Heteroptera > Vectors | **Type GUID**: `5584d798-a7b2-44f6-9ea6-571d264dd744`
- **Alias**: `G-Vectors`
- **Inputs**:
  - `Points` (`P`): Point [item] — The base-point from which vectors would be calculated
  - `Attractors` (`A`): Point [list] — List of Attractor Points
  - `Distance` (`D`): Number [item] — Effective Distance in 'Gaussian Law' function application. It is the maximum effective distance.
- **Outputs**:
  - `Vector` (`V`): Vector [item] — The  Bounded (normalized Set) respectively effective vectors
- **Behavior**: Calculates the Gaussian effective attraction vectors
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Radar Vector
- **Tab**: Heteroptera > Vectors | **Type GUID**: `62248a4c-b131-4b9f-935b-d81b3e24c76a`
- **Alias**: `Radar`
- **Inputs**:
  - `MetaVector` (`V`): MetaVector [item] — MetaVector Source
  - `Number` (`N`): Integer [item] — the numbers of circular distribution vectors 
  - `Coefficient` (`C`): Number [item] — Coefficient Factor
- **Outputs**:
  - `Vectors` (`V`): Vector [item] — Distribution Vector-set
- **Behavior**: Generate circular antenna distributed vectors from input vectors
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Rotate Field
- **Tab**: Heteroptera > Vectors | **Type GUID**: `357d5cef-228b-4448-b7fb-c4e8514465d8`
- **Alias**: `FRotate`
- **Inputs**:
  - `Field` (`F`): Field [item] — Input base Field whose tensors are to rotate
  - `Axis` (`A`): Field [item] — Axis field whose tensors are used as the rotation axes.
  - `Rotary` (`R`): Field [item] — Rotary Field whose scalar values affect the angle of rotation
  - `Factor ` (`C`): Number [item] — The coefficient factor for the rotation angle
- **Outputs**:
  - `Field` (`F`): Field [item] — The resultant field
- **Behavior**: Rotate a field's tensors by other fields
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Transform By Field
- **Tab**: Heteroptera > Vectors | **Type GUID**: `aaadfd74-bb86-4b9f-8c77-0c40b9856d25`
- **Alias**: `Field-Xform`
- **Inputs**:
  - `Field` (`F`): Field [list] — Field as transformer
  - `Geometry` (`G`): Geometry [list] — Geometry to transform,Geometries could be:  Point, Line, Curve, Mesh, TwistedBox, Surface
  - `Force` (`F`): Number [item] — Force
  - `Iteration` (`I`): Integer [item] — Number of steps
- **Outputs**:
  - `Geometry` (`G`): Geometry [item] — Geometry
- **Behavior**: Transform a geometry recursively through a field
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Traverse On Field
- **Tab**: Heteroptera > Vectors | **Type GUID**: `dc3a2d9d-35cb-45e3-9e9d-40ff99aadb0c`
- **Alias**: `F-Traveler`
- **Inputs**:
  - `Field` (`F`): Field [list] — Field as transformer
  - `Point` (`P`): Point [item] — Traverse starting point
  - `Charge` (`C`): Number [item] — Effecting charge factor
  - `Iteration` (`I`): Integer [item] — Number of steps
- **Outputs**:
  - `Curve` (`C`): Geometry [item] — Curve
- **Behavior**: Creates the traverse path on a field from a source point
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Curvature Field
- **Tab**: Heteroptera > Vectors | **Type GUID**: `edd2fa07-463f-4e0e-87c4-ad9135d07695`
- **Alias**: `CurvatureF`
- **Inputs**:
  - `Curve` (`C`): Curve [item] — The source curve to create field based on
  - `Distance` (`D`): Number [item] — Gassian effective distance. The distance within which the field can affect.
  - `Charge` (`C`): Number [item] — The strength of the field
- **Outputs**:
  - `Field` (`F`): Field [item] — The resultant field
- **Behavior**: Create a field based on a curve's curvature'
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Curve Along Field
- **Tab**: Heteroptera > Vectors | **Type GUID**: `1e9fe404-c030-48e3-8f9a-92adecf288f3`
- **Alias**: `AlongF`
- **Inputs**:
  - `Curve` (`C`): Curve [item] — The source curve to create field based on
  - `Distance` (`D`): Number [item] — Gassian effective distance. The distance within which the field can affect.
  - `Angle` (`A`): Number [item] — The Optional Rotation Angle. By this angle tensors will rotate around their datum axis.
  - `Charge` (`C`): Number [item] — The strength of the field
- **Outputs**:
  - `Field` (`F`): Field [item] — The resultant field
- **Behavior**: Create a field that is tangent-aligned to the given curve
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Drag Field
- **Tab**: Heteroptera > Vectors | **Type GUID**: `78deecaa-a5c1-43db-b5ce-802392f25416`
- **Alias**: `DragF`
- **Inputs**:
  - `Line` (`L`): Line [item] — Location and Direction of DragField
  - `Radius` (`R`): Number [item] — Radius of the point object
- **Outputs**:
  - `Field` (`F`): Field [item] — Field due to point charge
- **Behavior**: Create a drag field, 'Drag Field' represents the Gaussian effect of a single vector in an area with a certain distance.
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Gaussian Effect Field
- **Tab**: Heteroptera > Vectors | **Type GUID**: `e4fc250b-7b39-4246-8984-ada57c327e2b`
- **Alias**: `GPF`
- **Inputs**:
  - `Point` (`P`): Point [item] — Location of point charge
  - `Distance` (`D`): Number [item] — The effective distance of charge potential
  - `Charge` (`C`): Number [item] — Charge of point object
- **Outputs**:
  - `Field` (`F`): Field [item] — Field due to point charge
- **Behavior**: Create a point attractor field with Gaussian decay within a certain distance
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Monotone Field
- **Tab**: Heteroptera > Vectors | **Type GUID**: `4fc272e5-ccef-4dc7-88ee-0d96a430830c`
- **Alias**: `MonoF`
- **Inputs**:
  - `Vector` (`V`): Vector [item] — Uniform tensor
- **Outputs**:
  - `Field` (`F`): Field [item] — Monotone Field
- **Behavior**: Create a simple monotone field out of a vector
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Noise Field
- **Tab**: Heteroptera > Vectors | **Type GUID**: `8cf6d5b7-8579-48a9-9bc6-28bd950bb9e1`
- **Alias**: `Noise-F`
- **Inputs**:
  - `Point` (`P`): Point [item] — (Optional) Location of point charge. If omitted, the field would affect infinitely.
  - `Distance` (`D`): Number [item] — Maximum effective distance. If omitted, the field would affect infinitely. 
  - `Scale` (`S`): Number [item] — Charging Value 
  - `Charge` (`C`): Number [item] — Charging Value 
- **Outputs**:
  - `Field` (`F`): Field [item] — Field due to point charge
- **Behavior**: Generate a Simplex-Noise Field
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### On-Curve Field
- **Tab**: Heteroptera > Vectors | **Type GUID**: `d6511411-e70c-4240-9f9f-73c2e409ce6a`
- **Alias**: `CurF`
- **Inputs**:
  - `Curve` (`C`): Curve [item] — The source curve to create field based on
  - `Distance` (`D`): Number [item] — Gassian effective distance. The distance within which the field can affect.
  - `Angle` (`A`): Number [item] — The Optional Rotation Angle. By this angle tensors will rotate around their datum axis.
  - `Charge` (`C`): Number [item] — The strength of the field
- **Outputs**:
  - `Field` (`F`): Field [item] — The resultant field
- **Behavior**: Create a curve Gaussian attractor field
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Radio Field
- **Tab**: Heteroptera > Vectors | **Type GUID**: `770d763f-52a7-47a6-a744-e877402da146`
- **Alias**: `RadioF`
- **Inputs**:
  - `Point` (`P`): Point [item] — Location of point charge
  - `MetaVector` (`V`): MetaVector [item] — Vector of point object
  - `Attenuation` (`A`): Number [item] — The number to the power of which the primary vector would be intensified. The higher value means more concentration.
  - `Span` (`S`): Number [item] — The number, the product with the vector's length, defines the field's effective distance. 
  - `Charge` (`C`): Number [item] — The number, the product of which, with the length of the vector, define the effective distance of the field. 
- **Outputs**:
  - `Field` (`F`): Field [item] — Field due to point charge
- **Behavior**: Create a Radio field out of  a meta-vector's' elements
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Surface Curvature Field
- **Tab**: Heteroptera > Vectors | **Type GUID**: `cd076db2-2faf-4d17-b216-b4a4edd61950`
- **Alias**: `SCF`
- **Inputs**:
  - `Surface` (`S`): Surface [item] — Surface
  - `Distance` (`D`): Number [item] — Gassian effective distance. The distance within which the field can affect.
  - `Curvature` (`C`): Integer [item] — Curvature Type
  - `Tensity` (`T`): Integer [item] — Tensity calculating method
  - `Charge` (`C`): Number [item] — The strength of the field
- **Outputs**:
  - `Field` (`F`): Field [item] — The resultant field
- **Behavior**: Create a field influenced by a surface's curvature'
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Trap Field
- **Tab**: Heteroptera > Vectors | **Type GUID**: `8c4e5ed3-b0f6-463e-bc07-98ccbdcd74c4`
- **Alias**: `TrapF`
- **Inputs**:
  - `Element` (`E`): Generic Data [item] — A Plane, Curve, Surface, or mesh as a trap object
  - `Effective-Distance` (`D`): Number [item] — Effective distance within which the force would be active
  - `Space-Range` (`S`): Number [item] — The territory distance within which the gravity force would be eased.
  - `Charge` (`C`): Number [item] — Field Charge
- **Outputs**:
  - `Field` (`F`): Field [item] — The resultant field
- **Behavior**: Create 'Trap Field' by a Point, Curve, Plane, Surface, or a mesh. A trap field is a Gaussian attractor point with an additional 'Range' feature which expresses the distance near the element within which the tensors would be decaying.
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Attractor
- **Tab**: Heteroptera > Vectors | **Type GUID**: `1ed2e466-91c8-46db-be8e-4d3b14fc9144`
- **Inputs**:
  - `Points` (`P`): Point [tree] — Set of nodes to calculate the value from
  - `Attractors` (`A`): Geometry [list] — List of Points, Curves, Meshes, Surfaces or Breps as an attractor set
- **Outputs**:
  - `Value` (`V`): Number [item] — The set of Values between 0~1 per points
- **Behavior**: Magnetic attractor with normalized value. It is a quick multi-type  multi-attractor returning a congestive always-normal value between 0~1
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Bionic Attractor
- **Tab**: Heteroptera > Vectors | **Type GUID**: `a8d8eb34-fb6d-4526-85a6-84e05e1e971b`
- **Alias**: `Biottractor`
- **Inputs**:
  - `Points` (`P`): Point [list] — Points to calculate from
  - `Attractor` (`A`): Point [list] — A list of points as an attractor set
  - `Strength` (`S`): Number [list] — Strength of  each attractor [0~1]
  - `Coefficient ` (`C`): Number [item] — Coefficient number  that can be >0 or <0  
- **Outputs**:
  - `Value` (`V`): Number [item] — Output value per each point
- **Behavior**: Advanced multi-attraction system for finding a Congestive value 
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Bulge
- **Tab**: Heteroptera > Vectors | **Type GUID**: `65deb735-6b3d-40f0-b0dc-f31e38c9ae3b`
- **Inputs**:
  - `Plane` (`P`): Plane [item] — A set of Base-Planes or Particles to create tensors from
  - `Source` (`S`): Point [list] — Bulging attractor points used as 'Daemon'
  - `Strength` (`S`): Number [list] — The force to move
  - `Constrain` (`C`): Integer [item] — Constrain Mode
  - `Project` (`P`): Boolean [item] — Apply the dot-product coefficient in constraint mode for the result vectors
- **Outputs**:
  - `Result Plane` (`P`): Plane [item] — Result Plane
  - `Vector` (`V`): Vector [item] — Translating vectors
- **Behavior**: Bulge set of points by some Bulger points
Transforming Vectors are generated in 3-dimensional space by default, but Right-click to choose [Planar] mode if you desire to calculate it along the given plane.
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Construct Meta-Vector
- **Tab**: Heteroptera > Vectors | **Type GUID**: `3c74c84f-1cba-4d76-850e-0ee2ba83e5fb`
- **Alias**: `MetaVector`
- **Inputs**:
  - `Vector` (`V`): Vector [list] — List of vectors
  - `IsAxis` (`B`): Boolean [item] — If true, the reverse vectors will be added
- **Outputs**:
  - `MetaVector` (`M`): MetaVector [item] — Constructed MetaVector
- **Behavior**: Construct a meta-vector out of set of vector elements. A Meta-Vector is a conceptual class consisting of a set of vectors as its components. 
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Plane By Line
- **Tab**: Heteroptera > Vectors | **Type GUID**: `64c15bf2-be0a-43b6-9798-b8e32a335d13`
- **Alias**: `LinePlane`
- **Inputs**:
  - `Line` (`L`): Line [item] — Line as axis
  - `Axis` (`A`): Integer [item] — The axis that the line is assumed to represent.
- **Outputs**:
  - `Plane` (`P`): Plane [item] — Result Plane
- **Behavior**: Creates a plane by its corresponding line
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Project On Vector
- **Tab**: Heteroptera > Vectors | **Type GUID**: `8ab763f7-6c05-41da-a8ec-a34c2df68e69`
- **Alias**: `PVector`
- **Inputs**:
  - `Vector` (`V`): Vector [item] — The vector would be projected on a direction vector
  - `Direction` (`D`): Vector [item] — The vector on which the other vector would be projected
  - `Radius (Optional)` (`P`): Number [item] — Optional Exponential Factor
- **Outputs**:
  - `Vector` (`V`): Vector [item] — Result Vector
  - `Vector` (`P`): Vector [item] — Positive Result Vector
- **Behavior**: Project a vector on another vector(direction).
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Similar Vectors
- **Tab**: Heteroptera > Vectors | **Type GUID**: `c9f04c67-2fbf-4b8f-822e-9db6f561cd33`
- **Alias**: `Similar Vector`
- **Inputs**:
  - `MetaVector` (`M`): MetaVector [item] — Base MetaVector
  - `Vector` (`V`): Vector [list] — Vectors to evaluate
- **Outputs**:
  - `Index` (`I`): Integer [item] — Element index
  - `Selected` (`S`): Vector [item] — Selected MetaVector Element
  - `Absolute` (`A`): Vector [item] — Reoriented vector based on Meta-vector. The length of the result equals the element vector.
  - `Project` (`P`): Vector [item] — Projected vector on Meta-vector. The length of the result vector is the product of input vector .
  - `Product` (`P`): Vector [item] — Product-vector on Meta-vector. The result vector's length is the product of both element and input vector.
- **Behavior**: Select the most similar vector from MetaVector elements.
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Translated Plane
- **Tab**: Heteroptera > Vectors | **Type GUID**: `85d12ba8-002b-43c1-9e7a-496d43d3126d`
- **Alias**: `TransPlane`
- **Inputs**:
  - `Plane` (`P`): Plane [item] — Plane to move
  - `X Amount` (`X`): Number [item] — Amount of transpose along the plane's X axis
  - `Y Amount` (`Y`): Number [item] — Amount of transpose along the plane's Y axis
  - `Z Amount` (`Z`): Number [item] — Amount of transpose along the plane's Z axis
- **Outputs**:
  - `Plane` (`P`): Plane [item] — The result plane
- **Behavior**: Move a plane along its axes
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

## Utilities

### Camera Story
- **Tab**: Heteroptera > Utilities | **Type GUID**: `46f0586c-9cde-4dd9-a8f2-6797716ec9ea`
- **Alias**: `Cam Story`
- **Inputs**:
  - `Time` (`T`): Number [item] — The value in the timeline must be 0~1 in Normalized mode and not larger than the last frame's index in Frame-Index mode
  - `Control` (`C`): Integer [item] — Control Parameter which could be used for  reset or holding  add key..    0: Edge State → Ready to add frame via Add_Frame button     1: Reset → Clearing all saved key frames from memory    2: Hold → Adding frame in each iteration (Optional)
- **Outputs**: none
- **Behavior**: Create a camera storyline.. Right-click and select [Automatic!] option to enable auto-sequenced mode or choose one of the available interpolation modes if you need.
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Capture
- **Tab**: Heteroptera > Utilities | **Type GUID**: `748cf031-09e6-4ed4-b2e1-550856297fe0`
- **Inputs**:
  - `Path` (`P`): Text [item] — File path for captured frames
  - `Filename` (`F`): Text [item] — Filename for captured frames
  - `Ext` (`E`): Integer [item] — Image type(Optional)
  - `X-Size` (`X`): Integer [item] — Optional X pixel Size
  - `Y-Size` (`Y`): Integer [item] — Optional Y pixel Size
- **Outputs**:
  - `Filename` (`F`): Text [item] —  Captured frame's filename
- **Behavior**: Auto-naming Viewport Capture. Right-click and select [Automatic!] option to to automatic mode or choose the other options if you need.
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Encrypt / Decrypt
- **Tab**: Heteroptera > Utilities | **Type GUID**: `d0413d23-9c3e-4273-b588-1fbb5110ce8e`
- **Alias**: `CodeMachine`
- **Inputs**:
  - `Lace` (`S`): Text [item] — Lace for Encryption/Decryption
  - `Password` (`P`): Text [item] — The key for encryption or decryption
- **Outputs**:
  - `Lace` (`S`): Text [item] — The encrypted or decrypted string
- **Behavior**: Encrypt and Decrypt a string with a password (key string)
 Right-click to choose the method of encryption/decryption
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Http Request
- **Tab**: Heteroptera > Utilities | **Type GUID**: `67df74e2-c68a-4462-89c9-f8c24cdc67af`
- **Alias**: `Http_Request`
- **Inputs**:
  - `URL`: Text [item] — API's URL
  - `Data`: Text [list] — Data as keys and values separated by a delimiter in the following format >> key:value
  - `Delimiter` (`D`): Text [item] — Delimiter
  - `Auth` (`A`): Text [item] — Authentication
  - `RequestType` (`RT`): Integer [item] — Request Type
  - `DataType` (`CT`): Integer [item] — Content Type
- **Outputs**:
  - `Result` (`R`): Text [item] — Result
- **Behavior**: Restful API Request
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### ToolsUnicode
- **Tab**: Heteroptera > Utilities | **Type GUID**: `0b818ccd-9148-4b5d-ae45-ffb6ed648594`
- **Alias**: `Unicode`
- **Inputs**:
  - `Index` (`I`): Integer [item] — Index of Unicode
- **Outputs**:
  - `Unicode` (`U`): Text [item] — Unicode character
- **Behavior**: Generating Unicode Character
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### GenePool Controller
- **Tab**: Heteroptera > Utilities | **Type GUID**: `b98efeeb-d07c-4d86-9c83-24244283066e`
- **Alias**: `Pool Controller`
- **Inputs**:
  - `<Gene Pool` (`<`): Generic Data [list] — input jack  (Connect a GenePool here to control it) 
  - `Count` (`C`): Integer [item] — Number of sliders
  - `Range` (`R`): Domain [item] — The domain of sliders
  - `Decimal` (`D`): Integer [item] — Decimal place for sliders' change
  - `Randomness` (`R`): Number [item] — The amount of randomization with Blot!
- **Outputs**: none
- **Behavior**: GNC
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### GraphMapper Controller
- **Tab**: Heteroptera > Utilities | **Type GUID**: `5b21fc0d-18a2-45aa-bf2f-5bce28f35d58`
- **Alias**: `GraphMapperController`
- **Inputs**:
  - `<Graph Mapper` (`<`): Generic Data [tree] — input jack  (Connect a GenePool here to control it) 
  - `Input Range` (`I`): Domain [item] — The domain of sliders
  - `Output Range` (`O`): Domain [item] — The domain of sliders
  - `Decimal` (`D`): Curve [item] — Decimal place for sliders' change
- **Outputs**: none
- **Behavior**: Controlling Interval, Decimal-Number and the number of sliders in a GenePool
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Allocate By Index
- **Tab**: Heteroptera > Utilities | **Type GUID**: `6e93c41d-c3fd-405f-b072-3f0b3134321f`
- **Alias**: `i-Allocator`
- **Inputs**:
  - `Index` (`i`): Integer [tree] — The list of indexes as branch per each item
  - `Data` (`A`): Generic Data [tree] — Contains a collection of generic data
- **Outputs**:
  - `Data` (`A`): Generic Data [item] — Contains a collection of generic data
- **Behavior**:  Allocate each item to a specific index of branches. Right-Click to choose[Preserve structure] to maintain the given data structure and add Sub Branches to the main branches if needed.
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Allocate By Key
- **Tab**: Heteroptera > Utilities | **Type GUID**: `fc3defa8-3ccc-4cf4-9482-bfbe00c8e70e`
- **Alias**: `Key-Allocator`
- **Inputs**:
  - `Key Tag` (`K`): Text [tree] — Set of keys to allocate data to branches by that
  - `Data` (`A`): Generic Data [tree] — Contains a collection of generic data
- **Outputs**:
  - `Branch Name` (`S`): Text [item] — Branch Tag 
  - `Data` (`A`): Generic Data [item] — Contains a collection of generic data
- **Behavior**: Allocate each item to a specific string for each branch
Right-click to choose [Preserve structure] if you want to maintain the given data structure and just add Sub Branches to the main Branches
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Allocate By Value
- **Tab**: Heteroptera > Utilities | **Type GUID**: `476458a3-6f6b-4d57-9000-9faea816758d`
- **Alias**: `Domain-Allocator`
- **Inputs**:
  - `Number` (`N`): Integer [item] — The number of branches, data must be allocated to
  - `Domain` (`D`): Domain [item] — Optional domain for values
  - `Value` (`V`): Number [tree] — The values, data must be allocated based on
  - `Data` (`A`): Generic Data [tree] — Contains a collection of generic data
- **Outputs**:
  - `Intervals` (`I`): Domain [item] — Divided intervals
  - `Index Tree` (`i`): Integer [item] — The allocating index structure of data
  - `Data` (`A`): Generic Data [item] — Contains a collection of generic data
- **Behavior**:  Allocate each item to specific branches by the position of its value within the range
Right-click on branch allocator icon and choose "Preserve structure" if you want to maintain data structure and just add Sub Branches to the main Branches
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### ToolsHeteroDispatch
- **Tab**: Heteroptera > Utilities | **Type GUID**: `eff025df-741d-4c6d-aa47-9e13f8113092`
- **Alias**: `Dispatch`
- **Inputs**:
  - `Data` (`D`): Generic Data [list] — Data list
  - `Pattern` (`P`): Integer [list] — Dispatching pattern
- **Outputs**: none
- **Behavior**: Dispatch the items in a list into multiple target lists based on a pattern of indexes.
Right-click to choose the [Purge Outputs] option to remove useless Output parameters
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Tools EmptyStructure
- **Tab**: Heteroptera > Utilities | **Type GUID**: `d0827056-57f4-458f-9667-6bed4cfdbd71`
- **Alias**: `O-Tree`
- **Inputs**:
  - `Paths` (`P`): Path [list] — List of paths to make a tree based on
- **Outputs**:
  - `Tree` (`T`): Generic Data [item] — Empty Tree
- **Behavior**: Create an empty tree structure out of a list of paths
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Tools ExtendBranch
- **Tab**: Heteroptera > Utilities | **Type GUID**: `40e82d12-916d-4f5c-b450-45b6523f7ad3`
- **Alias**: `ExtendPath`
- **Inputs**:
  - `Path` (`P`): Path [item] — Path to add elements to
  - `Element` (`E`): Integer [item] — Element to add to the given Path
- **Outputs**:
  - `Path` (`P`): Path [item] — Result Path
- **Behavior**: Add an extra element at the beginning (Prepend) or end (Append) of a path
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Pick Object
- **Tab**: Heteroptera > Utilities | **Type GUID**: `54143992-a5df-4fa8-9d1f-0ac0a9db7c86`
- **Alias**: `Selection`
- **Inputs**:
  - `Live` (`L`): Boolean [item] — Live-Mode Enabling. With a Live-Mode state, the component will refresh once rhino objects are selected or deselected.
- **Outputs**:
  - `GUID` (`G`): Guid [item] — Dynamic referenced selected ID
- **Behavior**: Pick selected objects in rhino. . Right-click and select [Automatic!] option to interactively update with selection change if you need.
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

## Uncertainty

### Noise Oscilator
- **Tab**: Heteroptera > Uncertainty | **Type GUID**: `8bc04d26-8e9d-44fc-b727-ac397bf25bf7`
- **Alias**: `Noise`
- **Inputs**:
  - `Likelihood` (`L`): Number [item] — Likelihood of events that causes the noise
  - `Steps` (`S`): Integer [item] — Interval of time for digesting events as a smooth behavior 
  - `Number` (`N`): Integer [item] — The number of  oscillators
- **Outputs**:
  - `Noise` (`N`): Number [item] — Oscillating Noise Numbers
- **Behavior**: Noise Oscillator(streaming noise)
Right-click to choose the internal timer (with three options), or turn off the internal engine and use a Grasshopper timer instead.
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Wandering Vectors
- **Tab**: Heteroptera > Uncertainty | **Type GUID**: `c9b63451-4aee-457d-b646-dd3e81a884eb`
- **Alias**: `Wandering`
- **Inputs**:
  - `Likelihood` (`L`): Number [item] — Likelihood of events that causes the noise
  - `Steps` (`S`): Integer [item] — Interval of time for digesting events as a smooth behavior 
  - `Number` (`N`): Integer [item] — The number of  wandering vectors
- **Outputs**:
  - `Vector` (`V`): Vector [item] — Wandering vector
- **Behavior**: Generating multiple live wandering vectors
Right-click to choose options if needed
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Biased Distribution
- **Tab**: Heteroptera > Uncertainty | **Type GUID**: `7ef90b26-7c4a-4ae6-a9f4-b5ab41959458`
- **Alias**: `Distribution`
- **Inputs**:
  - `Points` (`P`): Point [list] — List of points by which probability will be calculated
  - `Source` (`S`): Point [tree] — Source Objects
  - `Seed` (`S`): Integer [item] — Seed Number for randomization
  - `Bias` (`B`): Number [item] — Bias number for distribution 
  - `Ambient` (`A`): Number [item] —  Ambient force efficiency. Ambient is the probability that the Point belongs to none of the sources.  
- **Outputs**:
  - `Biased Points` (`B`): Point [item] — Allocated points based on each attractor-point
  - `Ambient Points` (`A`): Point [item] — Points belonging to none of the defined sources
  - `Index` (`I`): Integer [item] — set number of listed points
- **Behavior**: Distributes input points into different branches. The result is a point tree based on the corresponding attractors, so each point belongs to the branch associated with its nearest attractor. If the Ambient value is greater than zero, points may be assigned to the Ambient branch. Double-click to change preview colors or add available items.
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Positional Possibility
- **Tab**: Heteroptera > Uncertainty | **Type GUID**: `51a3d54e-7dc2-4f00-a106-d9babccb22bd`
- **Alias**: `PositionalPosib`
- **Inputs**:
  - `Data` (`D`): Generic Data [list] — An object list to select from
  - `Values` (`V`): Number [list] — Set of values for each of points
  - `Randomness` (`R`): Number [item] — Randomness value for existence likelihood (0~1)
  - `Possibility` (`P`): Number [item] — Possibility value for existence likelihood
  - `Seed` (`S`): Integer [item] — Seed Number for randomization
- **Outputs**:
  - `P`: Generic Data [item] — Possible objects 
  - `Possibility` (`P`): Boolean [item] — Possibility of source points
- **Behavior**: Calculates the possibility of the existing points by assigning the given values to them
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Possibility By Attractor
- **Tab**: Heteroptera > Uncertainty | **Type GUID**: `ec99b9a5-e0bb-4b2a-8f22-cf6a70d3268e`
- **Alias**: `Possib^A`
- **Inputs**:
  - `Points` (`P`): Point [list] — Points to affect
  - `Attractors` (`J`): Geometry [list] — Set of points or curves to define attractor system by
  - `Randomness` (`R`): Number [item] — Randomness value for existence likelihood (0~1)
  - `Possibility` (`P`): Number [item] — Possibility value for existence likelihood (0~1)
  - `Seed` (`S`): Integer [item] — Seed Number for randomization
- **Outputs**:
  - `Points` (`P`): Point [item] — Possible points 
  - `Possibility` (`P`): Boolean [item] — Possibility of source points
- **Behavior**: Calculates the possibility of existing points by their adjacency to set of attractors 
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Curvy Point-Emiter
- **Tab**: Heteroptera > Uncertainty | **Type GUID**: `a7f40860-95ed-4980-b144-551209c73c6d`
- **Alias**: `C-Emitter`
- **Inputs**:
  - `Curve` (`C`): Curve [item] — Curve as Emitter Source
  - `Radius` (`R`): Domain [item] — The radius interval of scattering range
  - `Number` (`N`): Integer [item] — The number of generated point for each source
  - `Seed (Optional)` (`S`): Integer [item] — Optional seed to generate random points. If omitted, it uses a random seed generator.
- **Outputs**:
  - `Points` (`P`): Point [item] — Generated points
- **Behavior**: Emit a bunch of random points around the given curve
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Gaussian Random
- **Tab**: Heteroptera > Uncertainty | **Type GUID**: `5c51d021-2046-4c53-b4d4-c11d87b4ebc3`
- **Alias**: `GaussianRandom`
- **Inputs**:
  - `Number` (`N`): Integer [item] — The number of random numbers
  - `Mu Factor` (`M`): Number [item] — The mean (center) of distribution
  - `Sigma` (`S`): Number [item] — The standard deviation (effective radius) of distribution
  - `Seed` (`S`): Integer [item] — Optional Seed
- **Outputs**:
  - `Random` (`R`): Number [item] — Random Number
- **Behavior**: Generates Gaussian random numbers
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Point Emitter
- **Tab**: Heteroptera > Uncertainty | **Type GUID**: `3eb90341-5bbe-455b-b67d-2ae61893d64c`
- **Alias**: `Emitter`
- **Inputs**:
  - `Emitter` (`E`): Plane [item] — Emitter Source
  - `Radius` (`R`): Domain [item] — The radius interval of scattering range
  - `Number` (`N`): Integer [item] — The number of generated points per each source
  - `Tendency` (`T`): Number [item] — Tendency to source
  - `Seed (Optional)` (`S`): Integer [item] — Optional seed for generating random points. If omitted, a random seed generator is used
- **Outputs**:
  - `Points` (`P`): Point [item] — Generated points
- **Behavior**: Emit a bunch of points from each source point (You can also use F5 key or Grasshopper Timer to refresh the component)
Right-click to choose [Planar] mode to generate points constrained to the given plane
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Random Vectors
- **Tab**: Heteroptera > Uncertainty | **Type GUID**: `92fc91ad-6f86-4712-950a-2daf203be40d`
- **Alias**: `RandVect`
- **Inputs**:
  - `Number` (`N`): Integer [item] — Number of directions
  - `Length` (`L`): Domain [item] — Domain of possible length for vectors
- **Outputs**:
  - `Vectors` (`V`): Vector [item] — Generated Directions
- **Behavior**: Create random vectors in random directions with diverse lengths in a specific domain. 
Right-click to choose [Planar] mode if needed
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Random Direction
- **Tab**: Heteroptera > Uncertainty | **Type GUID**: `c84cfe41-e531-47ff-968d-bd251669970a`
- **Alias**: `RND Direction`
- **Inputs**:
  - `Number` (`N`): Integer [item] — Number of directions
- **Outputs**:
  - `Vectors` (`V`): Vector [item] — Generated Directions
- **Behavior**: Create random unit vectors- 
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Random Plane
- **Tab**: Heteroptera > Uncertainty | **Type GUID**: `3bdc9558-d69d-45ed-998b-bddfc8cb05f0`
- **Alias**: `RandomPlane`
- **Inputs**:
  - `Origin` (`P`): Point [item] — Origin Point
- **Outputs**:
  - `Plane` (`P`): Plane [item] — Random plane
- **Behavior**: Create a random plane on a point
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Random Position
- **Tab**: Heteroptera > Uncertainty | **Type GUID**: `6ab52d67-14ff-4bc4-8fe4-6046ddcdbab6`
- **Alias**: `RNDPOS`
- **Inputs**:
  - `Rectangle` (`R`): Rectangle [item] — Rectangle as the bound for the positions
  - `Number` (`N`): Integer [item] — The number of generations
  - `Edge Offset (Optional)` (`Z`): Number [item] — Maximum normal offset
  - `Seed (Optional)` (`S`): Integer [item] — Optional generator seed
- **Outputs**:
  - `Points` (`P`): Point [item] — Random positions
  - `Normalized position` (`P`): Generic Data [item] — Normalized 2D positions
  - `Distance` (`D`): Number [item] — Distance from the base Plane
- **Behavior**: Generate Random positions bounded by a rectangle, Z value Defines the Maximum possible distance for positions along the rectangle's normal direction.
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Simplex Vector
- **Tab**: Heteroptera > Uncertainty | **Type GUID**: `f0df6e5a-955b-4129-aacb-954c5701254a`
- **Alias**: `SimplexVector`
- **Inputs**:
  - `Points` (`P`): Point [list] — List of sample points
  - `Time` (`t`): Number [item] — (Optional) t parameter as 4th dimension
  - `Scale` (`S`): Number [item] — Slevelmplex Nolevelse Scale
- **Outputs**:
  - `Vector` (`V`): Vector [item] — Simplex Noise Vectors
  - `Color` (`C`): Colour [item] — Simplex Noise Color
- **Behavior**: Generates a Simplex-Noise Vector set
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Cheater Dice
- **Tab**: Heteroptera > Uncertainty | **Type GUID**: `31acfb8c-2aff-438c-afaa-1499e2aa990c`
- **Alias**: `Cheater_Dice`
- **Inputs**:
  - `Data` (`D`): Generic Data [list] — Possible data for dice
  - `Chance` (`C`): Number [list] — Chance of election for each item
  - `Number` (`N`): Integer [item] — Number of dice rolls
  - `Seed (Optional)` (`S`): Integer [item] — Optional Seed Dice
- **Outputs**:
  - `Result` (`R`): Generic Data [item] — the set of result data
  - `Index` (`I`): Integer [item] — Index of selected items
- **Behavior**: Dice with unequal chances for items
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Dice
- **Tab**: Heteroptera > Uncertainty | **Type GUID**: `7683942e-cf86-40f7-84a9-6f8f4ab6a312`
- **Inputs**:
  - `Data` (`D`): Generic Data [list] — Possible data for dice
  - `Number` (`N`): Integer [item] — Number of dice rolls
  - `Seed (Optional)` (`S`): Integer [item] — Optional Seed Dice
- **Outputs**:
  - `Result` (`R`): Generic Data [item] — the set of result data
  - `Index` (`I`): Integer [item] — Index of selected items
- **Behavior**: Rolls a die containing possible data N times and extracts N random items. Results may repeat. Right-click and choose [Just Once] to remove repeated random results.
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Slingshot Allocator
- **Tab**: Heteroptera > Uncertainty | **Type GUID**: `3febb59d-224c-4f37-b753-b236e9ab3214`
- **Alias**: `Slingshot`
- **Inputs**:
  - `Data` (`D`): Generic Data [list] — Data items to get distributed
  - `Number` (`N`): Integer [item] — The number of branches
  - `Seed` (`S`): Integer [item] — Optional seed number
- **Outputs**:
  - `Data Tree` (`D`): Generic Data [item] — The tree of data
- **Behavior**: Allocate each item of one list to random branches; distributions can be made by three different algorithms.  The number of branches is determined by N.
 -Arbitrary Distribution: with different branch size.
 -Homogeneous Distribution: with same branch size as far as possible.
 -Equal Distribution: with the exact same branch size, it culls overload items randomly.
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Weighted Allocator
- **Tab**: Heteroptera > Uncertainty | **Type GUID**: `1c651cc5-ba61-45c5-98a0-85bf33f046df`
- **Alias**: `Chance`
- **Inputs**:
  - `Data` (`D`): Generic Data [list] — Data items to get distributed
  - `Chance List` (`C`): Number [list] — List of numbers that define the chance of each branch
  - `Seed` (`S`): Integer [item] — Seed of the chance
- **Outputs**:
  - `Data Tree` (`D`): Generic Data [item] — The tree of data
- **Behavior**: Randomly Allocates Items to different branches by defining the chance of each branch. so each item tends to belong to the branch with a higher chance
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Careless Range
- **Tab**: Heteroptera > Uncertainty | **Type GUID**: `5d492c6f-0a6f-440b-a35b-78d9f8aef4d7`
- **Alias**: `CarelessRange`
- **Inputs**:
  - `Domain` (`D`): Domain [item] — Domain of numeric range
  - `Steps` (`N`): Integer [item] — Number of steps
  - `Errancy` (`E`): Number [item] — Errancy of numbers, it must be between 0~1
  - `Seed` (`S`): Integer [item] — Seed number for randomization
- **Outputs**:
  - `Range` (`R`): Number [item] — Uneven range
  - `Interval` (`I`): Domain [item] — Unevenly divided intervals
- **Behavior**: Divide a domain into randomly varied segments and return the numbers
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Randomize Numbers
- **Tab**: Heteroptera > Uncertainty | **Type GUID**: `8fa20aef-d145-43d2-a447-91617a072640`
- **Alias**: `Randomize`
- **Inputs**:
  - `Number` (`N`): Number [item] — Number to randomize
  - `Ratio` (`R`): Number [item] — Randomization ratio  (the best range is 0~1)
  - `Seed (Optional)` (`S`): Integer [item] — Random seed
- **Outputs**:
  - `Number` (`N`): Number [item] — Randomized number
- **Behavior**: Randomize Numbers by percentage
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Random Numbers
- **Tab**: Heteroptera > Uncertainty | **Type GUID**: `82cbfdc3-1fbd-4246-9cd2-6ad5b4768664`
- **Alias**: `Random`
- **Inputs**:
  - `Number` (`N`): Integer [item] — The number of random numbers
- **Outputs**:
  - `Random` (`R`): Number [item] — Random Number
- **Behavior**: Generates random numbers.
In 'Normal Mode', numbers are generated in the range [0, 1]; otherwise, the range is [-1 to 1] in 'Standard' or 'Gaussian' modes.
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Simplex Noise
- **Tab**: Heteroptera > Uncertainty | **Type GUID**: `e39432d4-b132-4311-8f97-f25ff35a6a8e`
- **Alias**: `SimplexNoise`
- **Inputs**:
  - `a`: Number [item] — a
  - `b`: Number [item] — b
  - `c`: Number [item] — c
  - `d`: Number [item] — d
  - `Scale` (`S`): Number [item] — Slevelmplex Nolevelse Scale
- **Outputs**:
  - `V`: Number [item] — V
- **Behavior**: Generates a Simplex-Noise number set
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Seed Generator
- **Tab**: Heteroptera > Uncertainty | **Type GUID**: `c6c66486-96fe-436c-ad8d-3739d139f129`
- **Alias**: `Seed`
- **Inputs**:
  - `Number` (`N`): Integer [item] — The number of random numbers
- **Outputs**:
  - `Random` (`R`): Integer [item] — Random Number
- **Behavior**: Generate a unique seed number each time it's recalled -
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

## Streaming

### Display Particles
- **Tab**: Heteroptera > Streaming | **Type GUID**: `bbd7a071-679a-46fd-a79e-60f5726f75f6`
- **Alias**: `AgentDisplay`
- **Inputs**:
  - `Particle Agents` (`P`): Point [list] — Set of moving points
  - `Thikness` (`T`): Number [item] — Longevity of trails
  - `Color` (`C`): Colour [item] — Agent color to display
- **Outputs**: none
- **Behavior**: Displays a trailing chain for a set of moving nodes.
If N > 1, the output is represented as a tree structure.
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Particle Trailer
- **Tab**: Heteroptera > Streaming | **Type GUID**: `ef2ee297-cadc-41a4-a239-14adffb129f5`
- **Alias**: `Trailer`
- **Inputs**:
  - `Points` (`P`): Point [list] — Set of Points
- **Outputs**:
  - `Lines` (`L`): Line [item] — Trail of each point
- **Behavior**: Generate a set of lines from each point of the current list to their peers from the previous list of points
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Number Buffer
- **Tab**: Heteroptera > Streaming | **Type GUID**: `01b26c10-9097-46fa-ab98-4fb33d301818`
- **Alias**: `NumberBuffer`
- **Inputs**:
  - `Reset` (`Rs`): Boolean [item] — Vacate the stack
  - `Numbers` (`N`): Number [list] — Numbers to add to the previous stack
- **Outputs**:
  - `Result` (`R`): Number [item] — Result Stack
- **Behavior**: After being recalled, the input number is added to the sum of the previous input numbers.
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Vector Buffer
- **Tab**: Heteroptera > Streaming | **Type GUID**: `196fc676-6935-4443-bfe6-9c0c3fbddf07`
- **Alias**: `VectorBuffer`
- **Inputs**:
  - `Reset` (`Rs`): Boolean [item] — Vacate the stack
  - `Vectors` (`V`): Vector [list] — Vector to add to the previous stack
- **Outputs**:
  - `Result` (`R`): Vector [item] — Result Stack
- **Behavior**: Once recalled, it adds the input vector to the previous stack of input vectors
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Mesh Traveler
- **Tab**: Heteroptera > Streaming | **Type GUID**: `bce411fe-138e-4a81-a259-2c78756dc5b0`
- **Alias**: `MeshTraveler`
- **Inputs**:
  - `Point` (`P`): Point [list] — Initial state points
  - `Vectors` (`V`): Vector [list] — Vector to add to the prior stack
  - `Fetter` (`F`): Number [item] — Fetter amount (0~1)
  - `Sensitivity` (`S`): Number [item] — Tendency to reach the mesh from a distance
  - `Mesh` (`M`): Mesh [item] — Constraining mesh
  - `Reset` (`R`): Boolean [item] — Vacate the stack
- **Outputs**:
  - `Points` (`P`): Point [item] — Result Stack
  - `Number` (`N`): Integer [item] — Iteration Number
- **Behavior**: Mass additive Vector buffer, considering a mesh as a constraint
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Ease Changes
- **Tab**: Heteroptera > Streaming | **Type GUID**: `0c862b62-435b-4ce6-918f-ebebfd6661fd`
- **Alias**: `Ease`
- **Inputs**:
  - `Number` (`N`): Number [list] — Changing numbers
  - `Rate` (`t`): Number [item] — Changing rate (0~1)
- **Outputs**:
  - `Number` (`N`): Number [item] — Smooth-changing numbers
- **Behavior**: It changes numbers smoothly during lapses.
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Glitch Reduction
- **Tab**: Heteroptera > Streaming | **Type GUID**: `daa2cc5a-cb66-4b0a-aadb-fc2d37da433e`
- **Alias**: `GlitchReduction`
- **Inputs**:
  - `Number` (`N`): Number [list] — Streaming numbers
  - `Range` (`R`): Integer [item] — The range to be observed
  - `Tolerance` (`T`): Number [item] — Tolerance
- **Outputs**:
  - `Smooth` (`S`): Number [item] — Smooth streaming numbers
  - `De-glitched` (`D`): Number [item] — De-glitched streaming numbers
- **Behavior**: De-Glitching/Smoothing streaming numbers (replacing the irrelevant numbers with the earlier relevant ones)
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Time Shift
- **Tab**: Heteroptera > Streaming | **Type GUID**: `3ee1c8b9-fb6e-4eb8-b983-c8f61deb7f4a`
- **Alias**: `TimeShift`
- **Inputs**:
  - `Data` (`D`): Generic Data [tree] — Data for buffering
  - `Capacity` (`C`): Integer [item] — Capacity
- **Outputs**:
  - `Data` (`D`): Generic Data [item] — buffered Data
- **Behavior**: Shifts a list of changing data to the previous data state by n steps
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Capacitor
- **Tab**: Heteroptera > Streaming | **Type GUID**: `cf1b1c1b-255f-45c4-9581-1505cc138897`
- **Inputs**:
  - `Data` (`D`): Generic Data [tree] — Data for buffering
  - `Capacity` (`C`): Integer [item] — Capacity
- **Outputs**:
  - `Data` (`D`): Generic Data [item] — buffered Data
- **Behavior**: Multi-Step Buffer
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### OilCan
- **Tab**: Heteroptera > Streaming | **Type GUID**: `361a89d9-89a5-4715-9a77-fe6e321df627`
- **Inputs**:
  - `Data List` (`L`): Generic Data [list] — List of items to tap
  - `Reset` (`R`): Boolean [item] — Reset
  - `Drop` (`D`): Boolean [item] — Drop trigger (set to true to run this component
  - `Drop Mode` (`M`): Integer [item] — Define how to drop the items    0:Loop   1:Ping-Pong    2:Deadened    3:Repeat last (Optional)
- **Outputs**:
  - `Drop` (`D`): Generic Data [item] — The current drop of the list
- **Behavior**: Every time it is invoked, it drops one item from the given list respectively
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Tap Buffer
- **Tab**: Heteroptera > Streaming | **Type GUID**: `cdde7e87-8f75-4d79-96c3-597e97dbd0b5`
- **Alias**: `Tap`
- **Inputs**:
  - `Reset` (`R`): Boolean [item] — Reset
  - `incremental` (`I`): Boolean [item] — Set to true for incremental counting; otherwise, counting is decremental
  - `Valve` (`V`): Integer [item] — Delay between consecutive drops in milliseconds  For cutting the running flow set the value to 0 (<5)  To prevent  counting in each iteration set this value to -1
  - `Counter Target` (`C`): Integer [item] — Optional target number at which to stop
  - `Hold` (`H`): Boolean [item] — Hold the last number in buffer
- **Outputs**:
  - `Drop` (`D`): Number [item] — Drop Count
- **Behavior**: A controllable trigger with a step counter
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Event Gate
- **Tab**: Heteroptera > Streaming | **Type GUID**: `fbcbbce0-e482-4e6b-b2d4-059a728896e9`
- **Alias**: `Event`
- **Inputs**:
  - `Data` (`D`): Generic Data [item] — Latest streaming data item
- **Outputs**:
  - `Data` (`D`): Generic Data [item] — Data to determine whether it has been updated from the previous one  (Receiving consecutive similar data prevents downstream expiration)
  - `IsNew?` (`N`): Boolean [item] — True: as receiving new data False: while receiving consecutive data
- **Behavior**: It passes data only if incoming is updated (data with a different value from the previous one)
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Event Toggle
- **Tab**: Heteroptera > Streaming | **Type GUID**: `65e9ffe9-c030-497b-ae99-73fd7bc5d15a`
- **Alias**: `e-Toggle`
- **Inputs**:
  - `Boolean` (`B`): Boolean [item] — Input streaming boolean value
- **Outputs**:
  - `Switch` (`S`): Boolean [item] — Boolean Switch , toggling as a new true receive after a false value
- **Behavior**: A Boolean toggle, responding to the first 'True' value after a chain of 'False' values.It prevents downstream kicks (Downstream Expiration) by default. It can be altered within the menu
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Holding Gate
- **Tab**: Heteroptera > Streaming | **Type GUID**: `5785c4f3-f26c-41cb-8c03-903b227d7ee4`
- **Alias**: `Hold`
- **Inputs**:
  - `Data` (`D`): Generic Data [tree] — Streaming Data
- **Outputs**:
  - `Data` (`D`): Generic Data [item] — Passed Data
- **Behavior**: Replaces NULL items with the most recent valid data from the data history.
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Splited Gate
- **Tab**: Heteroptera > Streaming | **Type GUID**: `99ed6506-9378-4a8d-9162-08b1dc1a73dd`
- **Alias**: `Spited_Gate`
- **Inputs**:
  - `Data` (`D`): Generic Data [tree] — Data to pass
  - `Gate` (`G`): Boolean [item] — Passing Gate
- **Outputs**: none
- **Behavior**: Controls the flow of data through a receiver
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Stream Freeze / Gate
- **Tab**: Heteroptera > Streaming | **Type GUID**: `f1ffc10a-a9ac-4c54-810a-22e411650467`
- **Alias**: `Freeze/Gate`
- **Inputs**:
  - `Data` (`D`): Generic Data [tree] — Streaming Data
  - `Passing Switch` (`S`): Boolean [item] — Passing switch
- **Outputs**:
  - `Data` (`D`): Generic Data [item] — Passed Data
- **Behavior**: Determines whether streaming data is allowed to pass through or not.
Data can be controlled downstream through a component's solution, preventing unwanted ticks.
 To keep the last received data choose the [Hold-Data] within the menu options.
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

## Networks

### Construct Hyper-Index
- **Tab**: Heteroptera > Networks | **Type GUID**: `6688bc47-6d95-4fb4-9e3a-db299e402901`
- **Alias**: `HyperIndex`
- **Inputs**:
  - `Path` (`P`): Path [item] — Data tree branch path
  - `Item` (`i`): Integer [item] — Item index
- **Outputs**:
  - `HyperIndex` (`I`): HyperIndex [item] — Data tree hyper index
- **Behavior**: Constructs a Hyper-Index. A Hyper-Index combines a [Path] and an [Index]. It is useful for identifying a specific node within a list of node lists or a node data tree.
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Flatten Inter-Network
- **Tab**: Heteroptera > Networks | **Type GUID**: `10ca81e2-21ad-4776-91fe-872517e7d8d3`
- **Alias**: `FlatNet`
- **Inputs**:
  - `Node → [Node]` (`N→[N]`): HyperIndex [tree] — The topology of nodes of other networks connected to one. Each Node's definition would rely on an 'InterNode' in this case. Each Path in this data-tree describes both the index of the network and the index of the indicated Node {...;<Network_Index>;<Node_Index>}
- **Outputs**:
  - `Node→Node` (`N→N`): Integer [item] — Node→Node Topology. It indicates the all nodes connected to one another.
  - `Edge→Node` (`E→N`): Integer [item] — Edge→Node Topology. It indicates a pair of nodes defining one edge.
  - `BackNodes` (`N`): HyperIndex [item] — a list of hyper-nodes corresponding to each node
- **Behavior**: Breaks down inter-topology to flat topology
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Inter-Networt Topology
- **Tab**: Heteroptera > Networks | **Type GUID**: `35e18f5c-e3ed-4fda-95c5-4ec473b288f2`
- **Alias**: `InterTopologyComponent`
- **Inputs**:
  - `Layers`: Integer [list] — A list of numbers representing the size of each layer (Branch)
  - `Points`: Point [tree] — Optional points as Data-tree corresponding to layers
  - `Node → [Node]` (`N→[N]`): HyperIndex [tree] — The topology of nodes of other networks connected to one. Each Node's definition would rely on an 'InterNode' in this case. Each Path in this data-tree describes both the index of the network and the index of the indicated Node {...;<Network_Index>;<Node_Index>}
  - `Rect`: Rectangle [item] — Rectangle frame to fit diagram within the viewport frame
  - `Tags`: Text [tree] — Strings as items' tag
- **Outputs**:
  - `Node → [Node]` (`N→[N]`): HyperIndex [item] — The topology of nodes of other networks connected to one. Each Node's definition would rely on an 'InterNode' in this case. Each Path in this data-tree describes both the index of the network and the index of the indicated Node {...;<Network_Index>;<Node_Index>}
  - `Edge → [Node]` (`E→[N]`): HyperIndex [item] — It indicates the pairs of nodes that define existing edges across multiple networks. Each node's definition would rely on an 'InterNode' in this case.  
  - `Lines`: Line [item] — Connection lines
  - `Points`: Point [item] — Remap points branched within the frame
  - `Curves`: Curve [item] — Remap connections within the rectangle frame 
- **Behavior**: Topology of connected nodes of different branches
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Modify Inter-Network
- **Tab**: Heteroptera > Networks | **Type GUID**: `a1af6491-b14c-4305-8ac3-79756827bbfc`
- **Alias**: `InterTopDraw`
- **Inputs**:
  - `Curve` (`C`): Curve [list] — Base curves
  - `Node → [Node]` (`N→[N]`): HyperIndex [tree] — The topology of nodes of other networks connected to one. Each Node's definition would rely on an 'InterNode' in this case. Each Path in this data-tree describes both the index of the network and the index of the indicated Node {...;<Network_Index>;<Node_Index>}
  - `Reverse` (`R`): Boolean [item] — Reversing ending vectors
- **Outputs**:
  - `P`: Point [item] — P
  - `S`: Point [item] — S
  - `Ts`: Vector [item] — Ts
  - `E`: Point [item] — E
  - `Te`: Vector [item] — Te
  - `Edge→Node` (`E→N`): Integer [item] — Edge→Node Topology. It indicates a pair of nodes defining one edge.
- **Behavior**: Modify and visualize a network's Inter-Topology
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Unflatten Inter-Network
- **Tab**: Heteroptera > Networks | **Type GUID**: `9f1b9b49-8332-400e-bad8-23354d907e2c`
- **Alias**: `UnflattNet`
- **Inputs**:
  - `Node→Node` (`N→N`): Integer [tree] — Node→Node Topology. It indicates the all nodes connected to one another.
  - `Partition` (`N`): Integer [list] — List of level indices corresponding to each node
- **Outputs**:
  - `Node → [Node]` (`N→[N]`): HyperIndex [item] — The topology of nodes of other networks connected to one. Each Node's definition would rely on an 'InterNode' in this case. Each Path in this data-tree describes both the index of the network and the index of the indicated Node {...;<Network_Index>;<Node_Index>}
  - `Edge → [Node]` (`E→[N]`): HyperIndex [item] — It indicates the pairs of nodes that define existing edges across multiple networks. Each node's definition would rely on an 'InterNode' in this case.  
- **Behavior**: Unflatten a network into an inter-network.
Creates inter-topology from flat topology by partitioning the nodes
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Cycle By Planar Mapping
- **Tab**: Heteroptera > Networks | **Type GUID**: `d3b52f74-953e-49d1-8981-7f859fe13b15`
- **Alias**: `NetRegion`
- **Inputs**:
  - `Node→Node` (`N→N`): Integer [tree] — Node→Node Topology. It indicates the all nodes connected to one another.
  - `Points` (`P`): Point [tree] — Topology nodes
  - `Base` (`B`): Plane [item] — Optional coordinate system or center used to find the regions. Omit this parameter to use the auto-fit plane or central point
  - `Method` (`M`): Integer [item] — Calculation method:  0:  Planar   1:  Spherical 2:  Terrain 3:  Dynamic Terrain
  - `Boundary` (`K`): Boolean [item] — Keeping the boundary in networks' cells
- **Outputs**:
  - `Cells`: Curve [item] — Cell Polyline
  - `Dual-Net` (`[NET]`): TopoCycle [item] — Dual-Topology Network containing topological Cycles
  - `Cell→Node` (`C→N`): Integer [item] — Cell→Node Topology
  - `Boundary-Node` (`B→N`): Integer [item] — The Boundary by nodes
  - `Boundary-Edge` (`B→E`): Integer [item] — The Boundary by edges
  - `Boundary` (`Bound`): Curve [item] — Boundary polyline
  - `Single Lines` (`Singles`): Line [item] — List of single lines. A single line cannot enclose adjoining cells.
- **Behavior**: Create Regions and Dual-Topology from network topology
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Box Adjacency
- **Tab**: Heteroptera > Networks | **Type GUID**: `a8cc964e-1d82-4e8c-b0a6-c8896ac01ffb`
- **Alias**: `Box_Adjacency`
- **Inputs**:
  - `Boxes` (`B`): Box [list] — List of boxes
- **Outputs**:
  - `Box-Box` (`B→B`): Integer [item] — Boxes connected to each box.
  - `Pairing` (`C→B`): Integer [item] — Box pairing of each connection
  - `M`: Matrix [item] — M
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Cycle from Lines
- **Tab**: Heteroptera > Networks | **Type GUID**: `0a979eb8-cdce-4744-8465-75e59b8627e7`
- **Alias**: `CyclefromLines`
- **Inputs**:
  - `Lines` (`L`): Line [list] — Lines to find regions in between
- **Outputs**:
  - `Cells`: Curve [item] — Cell Polyline
  - `Dual-Net` (`[NET]`): TopoCycle [item] — Dual-Topology Network containing topological Cycles
  - `Cell→Node` (`C→N`): Integer [item] — Cell→Node Topology
  - `Boundary-Node` (`B→N`): Integer [item] — The Boundary by nodes
  - `Boundary-Edge` (`B→E`): Integer [item] — The Boundary by edges
  - `Boundary` (`Bound`): Curve [item] — Boundary Polyline
  - `Single Lines` (`Singles`): Line [item] — List of single lines. A single line cannot enclose adjoining cells.
- **Behavior**: Calculate the topology of the adjacency and overlapping of a list of boxes
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Cycle from Topology
- **Tab**: Heteroptera > Networks | **Type GUID**: `d288a60e-dc0e-4e07-a36b-bf32a97b9336`
- **Alias**: `Cell By Topo`
- **Inputs**:
  - `Node→Node` (`N→N`): Integer [tree] — Node→Node Topology. It indicates the all nodes connected to one another.
  - `Number` (`N`): Integer [item] — The maximum allowed number of edges for polygons which must be greater than three
- **Outputs**:
  - `Dual-Net` (`[NET]`): TopoCycle [item] — Dual-Topology Network containing topological Cycles
  - `Cell→Node` (`C→N`): Integer [item] — Cell→Node Topology
  - `Naked Connections` (`NC`): Integer [item] — The index list of naked connections
- **Behavior**: Computes Topologic-Cells of a network
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Decompose Dual-Network
- **Tab**: Heteroptera > Networks | **Type GUID**: `ab9bc57e-f301-4f23-a8e0-82f67dbbd1c0`
- **Alias**: `CellTopology`
- **Inputs**:
  - `Dual-Net` (`[NET]`): TopoCycle [item] — Dual-Topology Network containing topological Cycles
- **Outputs**:
  - `Node→Node` (`N→N`): Integer [item] — Node→Node Topology. It indicates the all nodes connected to one another.
  - `Node→Edge` (`N→E`): Integer [item] — Node→Edge Topology
  - `Node→Cell` (`N→C`): Integer [item] — Node→Cell Topology
  - `Edge→Node` (`E→N`): Integer [item] — Edge→Node Topology. It indicates a pair of nodes defining one edge.
  - `Edge→Edge` (`E→E`): Integer [item] — Edge→Edge Topology
  - `Edge→Cell` (`E→C`): Integer [item] — Edge→Cell Topology
  - `Cell→Node` (`C→N`): Integer [item] — Cell→Node Topology
  - `Cell→Edge` (`C→E`): Integer [item] — Cell→Edge Topology
  - `Cell→Cell` (`C→C`): Integer [item] — Cell→Cell Topology
  - `Edge Type` (`T`): Text [item] — Edge Type:   Utmost: (with no adjacent region)   Exterior: (with just one adjacent region on one side)   Interior: (between two regions) 
- **Behavior**: Extract all features of a  dual topology
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Dual Graph
- **Tab**: Heteroptera > Networks | **Type GUID**: `4ea89768-639b-49f0-8806-98fb98cd66e3`
- **Alias**: `DualGraph`
- **Inputs**:
  - `Polygons` (`P`): Curve [list] — Input Polygons
- **Outputs**:
  - `Dual Graph` (`D`): Curve [item] — Dual graph as polygons
  - `Vertices` (`V`): Point [item] — The integrated collection of all vertices in topological order
  - `Centers` (`C`): Point [item] — The center points (the average point of all vertices of each polygon) regarded as the vertices in dual graph
  - `Node→Node` (`N→N`): Integer [item] — Node→Node Topology. It indicates the all nodes connected to one another.
  - `Cell→Cell` (`C→C`): Integer [item] — Cell→Cell Topology
- **Behavior**: Compute the dual graph of set of adjacent polygonal regions
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Match By Adjacency
- **Tab**: Heteroptera > Networks | **Type GUID**: `977c3a09-4282-4b0e-bd4e-7d95a7cfff5d`
- **Alias**: `MatchAdjacents`
- **Inputs**:
  - `Boundaries` (`G`): Geometry [list] — Geometry to match
  - `Point` (`P`): Point [list] — Points to match
  - `Distance` (`D`): Number [item] — Distance to Match
- **Outputs**:
  - `Point Index` (`G→P`): Integer [item] — The indexes points of corresponded to each geometries.
  - `Boundary Index` (`P→G`): Integer [item] — The Indexes of geometries corresponded to each point.
- **Behavior**: Indicates which geometry is closest to which point and the reverse.
It determines which points and geometries are associated with each other.
To match, the given point must be as close as the given distance.
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Match By Container
- **Tab**: Heteroptera > Networks | **Type GUID**: `bf62cd0a-28da-4c66-818e-0df66096936a`
- **Alias**: `MatchContainers`
- **Inputs**:
  - `Containers` (`G`): Geometry [list] — Containers to match
  - `Points` (`P`): Point [list] — Points to match
- **Outputs**:
  - `Point Index` (`G→P`): Integer [item] — The geometries' indexes matched with each point. To match, points must be within the geometry.
  - `Geometry Index` (`P→G`): Integer [item] — The Indexes of geometries matched with each Point. To match, points must be within the geometry.
- **Behavior**: This component indicates which containers contain which items and which items belong to which containers.
It determines which items and containers are associated with each other.
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Topology Of Adjacencies
- **Tab**: Heteroptera > Networks | **Type GUID**: `980bd972-3623-40a9-85d9-89807ce118c9`
- **Alias**: `Adjacency`
- **Inputs**:
  - `Polylines` (`PL`): Curve [list] — The orthographic polylines on which this component will compute the topological adjacency
  - `Method` (`M`): Integer [item] — The method of search:  0: Rectangular Polylines  1: Orthographic Polylines  2: Free Polylines
  - `Tolerance` (`T`): Number [item] — Searching distance
- **Outputs**:
  - `Cell→Cell` (`C→C`): Integer [item] — Cell→Cell Topology
- **Behavior**: Computes adjacency relationships among a list of polylines. Polylines do not need to share points to be matched as adjacent cells; edge alignment is the key criterion. This component offers three computation modes with different complexity levels and is most useful for very complex networks.
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Minimum Spanning Tree
- **Tab**: Heteroptera > Networks | **Type GUID**: `82007cc8-ba8a-4296-a884-2ccc131b2faf`
- **Alias**: `MST`
- **Inputs**:
  - `Base Points` (`P`): Point [list] — Points to Create Network
  - `Node→Node` (`N→N`): Integer [tree] — Node→Node Topology. It indicates the all nodes connected to one another.
- **Outputs**:
  - `Node→Node` (`N→N`): Integer [item] — Node→Node Topology. It indicates the all nodes connected to one another.
  - `Edge→Node` (`E→N`): Integer [item] — Edge→Node Topology. It indicates a pair of nodes defining one edge.
  - `Lines` (`L`): Line [item] — MST Network lines
- **Behavior**: Calculates Minimum Spanning, a network in which all nodes are connected without any cycle, having the minimum possible total edge weight. An alternative is also provided to provide a pre-existing network containing all possibilities of connectivity with the points. Otherwise, it will calculate the result with all possible connections between nodes given by Delaunay-Mesh.
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Networt Matching Path
- **Tab**: Heteroptera > Networks | **Type GUID**: `78cd5f70-7e6f-45b2-a76a-c584d66190a9`
- **Alias**: `MatchingPath`
- **Inputs**:
  - `Points` (`P`): Point [list] — Network nodes
  - `Node→Node` (`N→N`): Integer [tree] — Node→Node Topology. It indicates the all nodes connected to one another.
  - `Curves` (`C`): Curve [item] — Guiding curve
- **Outputs**:
  - `Path` (`P`): Curve [item] — Polyline as the resulting path
  - `Index` (`I`): Integer [item] — List of point indexes
- **Behavior**: Find the closest network path related to the given curve
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Shortest Route
- **Tab**: Heteroptera > Networks | **Type GUID**: `992702c7-9416-4663-8be4-beb8521810ba`
- **Alias**: `ShortestRoute`
- **Inputs**:
  - `Edge→Node` (`E→N`): Integer [tree] — Edge→Node Topology. It indicates a pair of nodes defining one edge.
  - `Weights` (`W`): Number [list] — An optional list of weights corresponding to connections
  - `Node A` (`A`): Integer [item] — Index of the starting node
  - `Node B` (`B`): Integer [item] — Index of the Ending node
- **Outputs**:
  - `Nodes` (`N`): Integer [item] — List of step nodes(Points)' indices traversed in the result route
  - `Segments` (`S`): Integer [item] — List of step edges(Connections)' indices traversed in the result route
  - `Cost` (`C`): Number [item] — Aggregated weight of the shortest path
- **Behavior**: Find the shortest route through a network between two nodes
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Space Syntax
- **Tab**: Heteroptera > Networks | **Type GUID**: `d4077291-8c30-4313-8bb3-45a86138c521`
- **Alias**: `SpaceSyntax`
- **Inputs**:
  - `Node→Node` (`N→N`): Integer [tree] — Node→Node Topology. It indicates the all nodes connected to one another.
  - `Source` (`I`): Integer [item] — The index of the source node
  - `Depth` (`D`): Integer [item] — Depth number in a topological space of the network
- **Outputs**:
  - `Node SpaceSyntax` (`NS`): Integer [item] — Space Syntax by nodes indices
  - `Connection SpaceSyntax` (`CS`): Integer [item] — Space Syntax by connection indices
- **Behavior**: Generate Space-Syntax out of a network
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Travelling Salesman Problem
- **Tab**: Heteroptera > Networks | **Type GUID**: `352ee824-6d27-4818-b9d7-4eb3d9ec40b6`
- **Alias**: `TSP`
- **Inputs**:
  - `Points` (`P`): Point [list] — Point list from which to generate an incident network
  - `Start`: Integer [item] — The index of the starting point
  - `Ants`: Integer [item] — The number of Ants(agents)
  - `Iteration`: Integer [item] — Cost (Distance) per connection
  - `Decay`: Number [item] — Decay factor of pheromones per iteration 
  - `Alpha`: Number [item] — The power by which the values of segments would affect the attractiveness of selectable nodes
  - `Beta`: Number [item] — The power by which shorter segments (with  lower cost) gain values
  - `Seed`: Integer [item] — Random Seed
- **Outputs**:
  - `Path` (`P`): Curve [item] — The optimum path
  - `Length` (`L`): Number [item] — The accumulative length of segments the path
  - `Path` (`P`): Integer [item] — The optimum result path
  - `Edge→Node` (`E→N`): Integer [item] — Edge→Node Topology. It indicates a pair of nodes defining one edge.
  - `Lines` (`L`): Line [item] — MST Network lines
- **Behavior**: Solves TSP within the given network with ant-colonies algorithm. It finds the optimum Path s which visits every node
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Weighted MinSpanTree
- **Tab**: Heteroptera > Networks | **Type GUID**: `dd149812-ef6b-44f3-8e10-0a786ab23498`
- **Alias**: `MST`
- **Inputs**:
  - `Edge→Node` (`E→N`): Integer [tree] — Edge→Node Topology. It indicates a pair of nodes defining one edge.
  - `Weight` (`W`): Number [list] — Weights or Lengths of the connections.
- **Outputs**:
  - `Node→Node` (`N→N`): Integer [item] — Node→Node Topology. It indicates the all nodes connected to one another.
  - `Edge→Node` (`E→N`): Integer [item] — Edge→Node Topology. It indicates a pair of nodes defining one edge.
- **Behavior**: Creates a minimum spanning tree from an existing network with connection weights.
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Display Topology
- **Tab**: Heteroptera > Networks | **Type GUID**: `e5c0836b-4b6c-4bba-96d7-b116925ce07e`
- **Alias**: `TopoDisplay`
- **Inputs**:
  - `Node→Node` (`N→N`): Integer [tree] — Node→Node Topology. It indicates the all nodes connected to one another.
  - `Circle`: Circle [item] — Circle to map into 
  - `T.Size`: Number [item] — Text Size
  - `TagList`: Text [list] — Optional Text list
- **Outputs**:
  - `BackNodes`: Plane [item] — BackNodes
  - `Curves`: Curve [item] — Curves
  - `Edge→Node` (`E→N`): Integer [item] — Edge→Node Topology. It indicates a pair of nodes defining one edge.
- **Behavior**: Display a network connection topology
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Display ArrowLines
- **Tab**: Heteroptera > Networks | **Type GUID**: `5087e0af-cf9d-43e5-83a7-019f3535b246`
- **Alias**: `DisplayArrowLines`
- **Inputs**:
  - `Line` (`L`): Line [list] — Line to display
  - `Unitize` (`U`): Boolean [item] — If true, the Line will be unitized to display
  - `Scale` (`S`): Number [item] — Display Scale
  - `Offset` (`O`): Number [item] — Offset of starting point
  - `Thickness` (`T`): Integer [item] — Offset of starting point
  - `Color` (`C`): Colour [item] — Offset of starting point
  - `Size` (`S`): Number [item] — Offset of starting point
- **Outputs**:
  - `Start` (`P`): Point [item] — Starting point
- **Behavior**: Displays lines with arrow
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Enumerator
- **Tab**: Heteroptera > Networks | **Type GUID**: `d4dec5d2-32d8-45f5-b85c-f5110edc522b`
- **Inputs**:
  - `Object` (`G`): Geometry [list] — List of geometric objects
- **Outputs**:
  - `Numbers` (`N`): Integer [item] — Input object's index numbers
  - `Color` (`C`): Colour [item] — The colors correspond to the branches
- **Behavior**: Enumerate  geometries
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Topology Embody
- **Tab**: Heteroptera > Networks | **Type GUID**: `bbe60ab6-bbe4-40ec-80b0-1bc45a7455bc`
- **Alias**: `Embody`
- **Inputs**:
  - `Indexes` (`i`): Integer [tree] — set of the point indexes (CT or RT)
  - `Points` (`P`): Point [tree] — Points, by which the lines or polylines will be constructed 
  - `Closed` (`C`): Boolean [item] — If true, the created polyline will be closed
- **Outputs**:
  - `Curves` (`C`): Curve [item] — Lines(from edge topology) or Polylines(from region topology)
- **Behavior**: Create Lines or Closed Polylines from topology
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Boolean Topology
- **Tab**: Heteroptera > Networks | **Type GUID**: `3d787d85-0c7b-4eea-8179-03890934f951`
- **Alias**: `TopoBoolean`
- **Inputs**:
  - `Topo A` (`A`): Integer [tree] — Topology A (it can be either Node→Node  or Edge→Node topology)
  - `Topo B` (`B`): Integer [tree] — Topology B (it can be either Node→Node or Edge→Node topology)
  - `Mode` (`M`): Integer [item] — Boolean Mode:  0:Union  1:Subtract  2:Intersect
- **Outputs**:
  - `Node→Node` (`N→N`): Integer [item] — Node→Node Topology. It indicates the all nodes connected to one another.
  - `Edge→Node` (`E→N`): Integer [item] — Edge→Node Topology. It indicates a pair of nodes defining one edge.
- **Behavior**: Perform Union, Subtraction, or Intersection on a pair of networks
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Modify Topology
- **Tab**: Heteroptera > Networks | **Type GUID**: `e5c0836b-4b6c-4bba-96d7-b116625ce07e`
- **Alias**: `NetworkEditor`
- **Inputs**:
  - `Number`: Integer [item] — Node Number
  - `Node→Node` (`N→N`): Integer [tree] — Node→Node Topology. It indicates the all nodes connected to one another.
- **Outputs**:
  - `Node→Node` (`N→N`): Integer [item] — Node→Node Topology. It indicates the all nodes connected to one another.
  - `Edge→Node` (`E→N`): Integer [item] — Edge→Node Topology. It indicates a pair of nodes defining one edge.
- **Behavior**: Edit the topology of a network or create a network by topology
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Reconstruct Topology
- **Tab**: Heteroptera > Networks | **Type GUID**: `683305c6-fd18-4102-b142-f5c799d7069c`
- **Alias**: `ReConstNet`
- **Inputs**:
  - `Node→Node` (`N→N`): Integer [tree] — Node→Node Topology. It indicates the all nodes connected to one another.
  - `Edge→Node` (`E→N`): Integer [tree] — Edge→Node Topology. It indicates a pair of nodes defining one edge.
  - `Points (Optional)` (`P`): Point [list] — Optional connection nodes
  - `Curves (Optional)` (`C`): Curve [list] — Optional network connections
- **Outputs**:
  - `Node→Node` (`N→N`): Integer [item] — Node→Node Topology. It indicates the all nodes connected to one another.
  - `Edge→Node` (`E→N`): Integer [item] — Edge→Node Topology. It indicates a pair of nodes defining one edge.
  - `Points` (`P`): Point [item] — Connection BackNodes
  - `Lines` (`L`): Line [item] — Network Lines
- **Behavior**: Recreate Lines from topology or convert different types of network topology.
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Network From Geometry
- **Tab**: Heteroptera > Networks | **Type GUID**: `02b557fe-64cf-48e0-aed4-4ac2f1bdb11b`
- **Alias**: `GeoNet`
- **Inputs**:
  - `Geometry` (`G`): Geometry [item] — Mesh or Brep from which to extract topology
- **Outputs**:
  - `Node→Node` (`N→N`): Integer [item] — Node→Node Topology. It indicates the all nodes connected to one another.
  - `Node→Edge` (`N→E`): Integer [item] — Node→Edge Topology
  - `Node→Cell` (`N→C`): Integer [item] — Node→Cell Topology
  - `Edge→Node` (`E→N`): Integer [item] — Edge→Node Topology. It indicates a pair of nodes defining one edge.
  - `Edge→Edge` (`E→E`): Integer [item] — Edge→Edge Topology
  - `Edge→Cell` (`E→C`): Integer [item] — Edge→Cell Topology
  - `Cell→Node` (`C→N`): Integer [item] — Cell→Node Topology
  - `Cell→Edge` (`C→E`): Integer [item] — Cell→Edge Topology
  - `Cell→Cell` (`C→C`): Integer [item] — Cell→Cell Topology
- **Behavior**: Create a network topology from Mesh or Brep
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Network From Lines
- **Tab**: Heteroptera > Networks | **Type GUID**: `80cb43bb-53ac-4e4c-bfb1-34e1e899748e`
- **Alias**: `L-Net`
- **Inputs**:
  - `Lines` (`L`): Line [list] — Initial lines to get network from
  - `Tolerance` (`T`): Number [item] — Optional Tolerance
- **Outputs**:
  - `Node→Node` (`N→N`): Integer [item] — Node→Node Topology. It indicates the all nodes connected to one another.
  - `Edge→Node` (`E→N`): Integer [item] — Edge→Node Topology. It indicates a pair of nodes defining one edge.
  - `Points` (`P`): Point [item] — Network nodes
  - `Lines` (`L`): Line [item] — Geometrical connection lines belong to each initial line
- **Behavior**: Creates a network from a set of crossing lines.
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Proximity Inter-Network
- **Tab**: Heteroptera > Networks | **Type GUID**: `595932bc-be73-4d97-8548-725d68e26dbf`
- **Alias**: `H-Net`
- **Inputs**:
  - `Points` (`P`): Point [tree] — Point tree from which to create an inter-network
  - `Distance` (`d`): Domain [item] — The searching distance to find connection
  - `Number` (`n`): Integer [item] — The maximum number of the junction from each node
- **Outputs**:
  - `Node → [Node]` (`N→[N]`): HyperIndex [item] — The topology of nodes of other networks connected to one. Each Node's definition would rely on an 'InterNode' in this case. Each Path in this data-tree describes both the index of the network and the index of the indicated Node {...;<Network_Index>;<Node_Index>}
  - `Edge → [Node]` (`E→[N]`): HyperIndex [item] — It indicates the pairs of nodes that define existing edges across multiple networks. Each node's definition would rely on an 'InterNode' in this case.  
  - `Lines` (`L`): Line [item] — Network lines
- **Behavior**: Create an Inter-Network between adjacent points from multiple sets
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Proximity Network
- **Tab**: Heteroptera > Networks | **Type GUID**: `8b05233a-b681-40b2-8b83-51b2cdd459c5`
- **Alias**: `ProxyNet`
- **Inputs**:
  - `Points` (`P`): Point [list] — Point list from which to generate an incident network
  - `Distance` (`d`): Domain [item] — Optional searching distance domain to make connection within
  - `Number` (`n`): Integer [item] — Optional maximum number of connections for each node
- **Outputs**:
  - `Node→Node` (`N→N`): Integer [item] — Node→Node Topology. It indicates the all nodes connected to one another.
  - `Edge→Node` (`E→N`): Integer [item] — Edge→Node Topology. It indicates a pair of nodes defining one edge.
  - `Lines` (`L`): Line [item] — Network lines
- **Behavior**: Extract Proximity Network out of a list of points.
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

## Maths

### Expand Domain
- **Tab**: Heteroptera > Maths | **Type GUID**: `edfa2481-a46b-4654-8322-308d2364d876`
- **Alias**: `DExpand`
- **Inputs**:
  - `Domain` (`D`): Domain [item] — Initial domain
  - `T0` (`A`): Number [item] — Number, subtracting from Starting value of a numeric domain
  - `T1` (`B`): Number [item] —  Number, adding to the Ending value of a numeric domain
- **Outputs**:
  - `Interval` (`D`): Domain [item] —  Expanded/ Shrinked Domain
- **Behavior**: Expand or shrink a domain
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Intersect Domains
- **Tab**: Heteroptera > Maths | **Type GUID**: `6dc51bda-1c9e-490f-8179-fcb0f9706a87`
- **Alias**: `Domain^`
- **Inputs**:
  - `Domain` (`D`): Domain [list] — A set of intervals to calculate their intersections
- **Outputs**:
  - `Domain` (`D`): Domain [item] — An interval for intersection
- **Behavior**: Calculate an interval by intersecting two intervals
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Interval Connection
- **Tab**: Heteroptera > Maths | **Type GUID**: `b09d7684-3abf-4fb1-9ae0-3dcfa8df4138`
- **Alias**: `IntervalConnection`
- **Inputs**:
  - `A`: Domain [item] — First Interval
  - `B`: Domain [item] — Second Interval
  - `Tolerance` (`T`): Number [item] — Calculation tolerance
- **Outputs**:
  - `Connected` (`CON`): Boolean [item] — Are input intervals connected
  - `Overlap` (`OVR`): Boolean [item] — Do the input intervals have a range in common
  - `Sub-domain` (`SUB`): Boolean [item] — Is A sub-domain of B
  - `Super-domain` (`SUP`): Boolean [item] — Is A super-domain of B
- **Behavior**: Check the connectivity of a pair of intervals
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Subtract Domains
- **Tab**: Heteroptera > Maths | **Type GUID**: `a12a67b7-3216-4967-8f67-bee7031b9045`
- **Alias**: `Dom-`
- **Inputs**:
  - `Domains` (`D`): Domain [list] — Domains to subtract from
  - `Voids` (`V`): Domain [list] — Domains as Voids
- **Outputs**:
  - `Domains` (`D`): Domain [item] — Merged Domains
- **Behavior**: Calculate the result of subtraction from a set of domains by another set of domains
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Symmetric Domain
- **Tab**: Heteroptera > Maths | **Type GUID**: `fa118de4-0330-41ac-b2a0-d32a4f8963ed`
- **Alias**: `SymmetricDomain`
- **Inputs**:
  - `Length` (`X`): Number [item] — Length of the domain
  - `Base` (`O`): Number [item] — Center of the domain
- **Outputs**:
  - `Interval` (`D`): Domain [item] — Symmetrical Domain
- **Behavior**: Generate the symmetrical domain based on 'O' and length of 'X' 
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Symmetric Domain Expand
- **Tab**: Heteroptera > Maths | **Type GUID**: `132d83e4-a47b-4dc2-95dc-8e332f7df65f`
- **Alias**: `SymetricDomainExpand`
- **Inputs**:
  - `Domain` (`D`): Domain [item] — Domain to extend
  - `Number` (`N`): Number [item] — Length of extension (use a negative value to shrink domains
- **Outputs**:
  - `Interval` (`D`): Domain [item] — Extended domain
- **Behavior**: BiExtend or shrink a domain with symmetrical value
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Union Intervals
- **Tab**: Heteroptera > Maths | **Type GUID**: `14ecd90a-e55d-4aac-82b4-1b54d6e16540`
- **Alias**: `Dom+`
- **Inputs**:
  - `Domains` (`D`): Domain [list] — Domains to overlap
- **Outputs**:
  - `Domains` (`D`): Domain [item] — Merged Domains
- **Behavior**: Merge and union a set of domains
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Closest Numbers
- **Tab**: Heteroptera > Maths | **Type GUID**: `745ee08a-a3f9-4bbe-b604-7b765ddb7af1`
- **Alias**: `CN`
- **Inputs**:
  - `Number Set` (`D`): Number [list] — The set of numbers, searching in
  - `Search` (`S`): Number [item] — Number that is searched for
  - `Count` (`N`): Integer [item] — The number of results of closest numbers
- **Outputs**:
  - `Closest Numbers` (`R`): Number [item] — The closest numbers in in set D to number S
- **Behavior**: Find a set of closest Numbers to a specific number (The closest numbers in set D to number S)
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### In-Common Numbers
- **Tab**: Heteroptera > Maths | **Type GUID**: `b774ad09-a926-4c1a-899d-00a3457b0769`
- **Alias**: `LCM/GMD`
- **Inputs**:
  - `Numbers` (`N`): Integer [list] — A set of Integers
- **Outputs**:
  - `GCD`: Integer [item] — Greatest common divisor
  - `LCM`: Integer [item] — Least common multiple
- **Behavior**: Retrieve 'Greatest common divisor' and 'Least common multiple' from a set of integers
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Min / Max
- **Tab**: Heteroptera > Maths | **Type GUID**: `7c9d9882-545d-434b-9850-2f3c6b01296b`
- **Alias**: `Extremes`
- **Inputs**:
  - `Number` (`N`): Number [list] — Set of Numbers
- **Outputs**:
  - `Minimum` (`Min`): Number [item] — Minimum
  - `Maximum` (`Max`): Number [item] — Maximum
- **Behavior**: Extract the minimum and the maximum value of a list of numbers
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Normalizer
- **Tab**: Heteroptera > Maths | **Type GUID**: `4bd25213-fe16-44cb-a3f1-1a7814872363`
- **Alias**: `Edge`
- **Inputs**:
  - `Numbers` (`N`): Number [tree] — List of numbers to normalize
- **Outputs**:
  - `Numbers` (`N`): Number [item] — Normalized Numbers
- **Behavior**: Normalize a list of numbers
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Numbers On Grid
- **Tab**: Heteroptera > Maths | **Type GUID**: `68201ce2-db0e-472e-ad5c-ac232d382c85`
- **Alias**: `GridNums`
- **Inputs**:
  - `Number` (`N`): Integer [item] — Number to put in the grid
  - `Row Size` (`S`): Integer [item] — Number of items in a row
  - `X`: Number [item] — X size
  - `Y`: Number [item] — Y size
- **Outputs**:
  - `Column` (`C`): Integer [item] — Column of the number of the grid
  - `Row` (`R`): Integer [item] — Column of the number of the grid
  - `Vectors` (`V`): Vector [item] — Output vectors
- **Behavior**: Put numbers in a grid with a specified max column number and return the row number and the column number 
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Number Digitizer
- **Tab**: Heteroptera > Maths | **Type GUID**: `1144d014-b0ae-458d-acfe-033059e28889`
- **Alias**: `Digitizer`
- **Inputs**:
  - `Number` (`N`): Number [item] — Number to Digitize
  - `Scope` (`S`): Number [item] — Digitizing scope size
- **Outputs**:
  - `Number` (`N`): Number [item] — Digitized number
- **Behavior**: modularize(digitize) a number by specific Scope size 
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Number Limiter
- **Tab**: Heteroptera > Maths | **Type GUID**: `62a82c5c-5279-4545-b583-398ce98adf80`
- **Alias**: `Boundary`
- **Inputs**:
  - `Number` (`N`): Number [item] — Number
  - `Domain` (`D`): Domain [item] — Domain
  - `Limitation Mode` (`M`): Integer [item] — Define how to limit the number:   0:Wrap   1:Ping-pong   2.Sinusoidal   3.Bound   4.Survive (Optional)
- **Outputs**:
  - `Number` (`N`): Number [item] — Bounded number
- **Behavior**: Limit a number within a specific domain
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Graph-Mapper +
- **Tab**: Heteroptera > Maths | **Type GUID**: `310f9597-267e-4471-a7d7-048725557528`
- **Alias**: `Mapper+`
- **Inputs**:
  - `Curve` (`C`): Curve [item] — External curve as a graph
  - `Boundary` (`R`): Rectangle [item] — Optional rectangle boundary. If omitted, the curve bounds are used
  - `Numbers` (`x`): Number [list] — List of input numbers
  - `Input` (`In `): Domain [item] — Optional input domain. If omitted, it defaults to 0-1 in "Normalize" mode, or to the input list interval in "AutoDomain" mode
  - `Output` (` Out`): Domain [item] — Optional output domain. If omitted, it defaults to 0-1 in "Normalize" mode, or to the input list interval in "AutoDomain" mode
- **Outputs**:
  - `Number` (`N`): Number [item] — Output Numbers
- **Behavior**: External Graph mapper
Right-click to choose [AutoDomain] mode to define the output domain based on the input interval; otherwise it is set to 0-1 in "Normalized" mode.
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Incline Value
- **Tab**: Heteroptera > Maths | **Type GUID**: `e676ed31-181c-4e23-baea-0acf99744098`
- **Alias**: `Bias`
- **Inputs**:
  - `X` (`x`): Number [list] — Numbers to feed
  - `Bias Number` (`t`): Number [item] — Number between 0-1 as the tendency to Start-End
  - `Interval` (`I`): Domain [item] — Optional bounding domain
- **Outputs**:
  - `Value` (`V`): Number [item] — The output values
- **Behavior**: Bias a set of numbers by conic function
Right-click to use "Bipolar" mode if you need to bias numbers based on Bipolar Conic Function instead of Conic Function.
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Interpolate +
- **Tab**: Heteroptera > Maths | **Type GUID**: `a86dc076-80b5-4617-ae2b-39a2389583d0`
- **Alias**: `Interp+`
- **Inputs**:
  - `Data` (`D`): Generic Data [list] — Data to interpolate (almost everything).  Number, Point, Vector, Color, Plane, Circle ,Rectangle, Interval, 2D Interval,  Complex Number, Curve,  Mesh, Surface
  - `Parameter` (`t`): Number [item] — Collection of weights for each value
- **Outputs**:
  - `Arithmetic mean` (`AM`): Generic Data [item] — Arithmetic mean of all input values
- **Behavior**: Interpolate a collection of almost every interpolative data.
Data can be: {Number, Complex, Color, Vector, Point, Line, Domain 1D & 2D, Plane, Box, TwistedBox,  Rectangle, Circle, Arc, Transform, Curve, Surface, and Mesh}
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Weighted Average +
- **Tab**: Heteroptera > Maths | **Type GUID**: `ec3e5cfc-9a0a-4a31-8027-96f28dd764fb`
- **Alias**: `Wav+`
- **Inputs**:
  - `Input` (`I`): Generic Data [list] — Input values for averaging
  - `Weights` (`W`): Number [list] — Collection of weights for each value
- **Outputs**:
  - `Arithmetic mean` (`AM`): Generic Data [item] — Arithmetic mean (average) of all input values
- **Behavior**: Solve the arithmetic weighted average for a set of items
The items could be:
{Number, Complex, Color, Vector, Point, Line, Domain 1D&2D, Plane, Box, TwistedBox, Rectangle, Circle, Arc, Transform, Curve, Surface and Mesh}
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

## Geometry

### Directional Curve
- **Tab**: Heteroptera > Geometry | **Type GUID**: `0f03372f-1f18-4488-b4ad-f011add62251`
- **Alias**: `DireCurve`
- **Inputs**:
  - `Line` (`L`): Line [item] — Line to create a curve from
  - `Plane` (`P`): Plane [item] — A plane from which the direction is obtained
  - `Direction` (`D`): Integer [item] — Choice number that selects which vector is taken from the plane
- **Outputs**:
  - `Curve` (`C`): Curve [item] — Result Curve
- **Behavior**: Convert a line to a directional curve based on a plane
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Geometric Cycles
- **Tab**: Heteroptera > Geometry | **Type GUID**: `16362dda-b3cb-4e17-aab5-9ed839601ba4`
- **Alias**: `GeoCycle`
- **Inputs**:
  - `Curves` (`C`): Curve [list] — Curve to get regions from
- **Outputs**:
  - `Regions` (`R`): Curve [item] — Regions calculated from input curves
- **Behavior**: Create Cycles from a list of curves
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Geometric Shadow
- **Tab**: Heteroptera > Geometry | **Type GUID**: `a9135eb6-4641-4a0e-935f-e3acb2ac805c`
- **Alias**: `Shadow`
- **Inputs**:
  - `Emitter` (`E`): Point [item] — Emitter Location
  - `Objects` (`G`): Geometry [list] — Objects to make projections out of
  - `Screen` (`S`): Plane [item] — Screen plane
- **Outputs**:
  - `Shadow Boundary` (`B`): Curve [item] — Projected curves
  - `Visible Curves` (`V`): Curve [item] — Visible curves
- **Behavior**: Create a 2d drawing on a plane out of a set of objects. Right-click and select [Automatic!] option to put it into interactive computation mode if you need.
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Overlay
- **Tab**: Heteroptera > Geometry | **Type GUID**: `4fad8d51-7136-4d0f-8ad2-3dce22e16f42`
- **Inputs**:
  - `Curves` (`C`): Curve [list] — Overlaying  shapes
  - `Plane` (`P`): Plane [item] — Optional base-plane
- **Outputs**:
  - `Result` (`R`): Curve [item] — Result outlines of boolean difference (A - B)
- **Behavior**: Overlay shapes in order
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Anchor Sweep
- **Tab**: Heteroptera > Geometry | **Type GUID**: `a99d89cd-3491-4468-bed6-e2097c4b82d2`
- **Alias**: `AnchorSweep`
- **Inputs**:
  - `Rail` (`C`): Curve [item] — Curve as a sweep rail
  - `Section` (`S`): Curve [item] — Optional profile for sweep
  - `Point` (`P`): Point [item] — Base Point
- **Outputs**:
  - `Fast_Sweep` (`S`): Brep [item] — Created Fast_Sweep
- **Behavior**: Quick section sweep with anchor
Right-click to either impose [RoadLike] mode, or use [Horizontal] balancing
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Fast Sweep
- **Tab**: Heteroptera > Geometry | **Type GUID**: `22c98f27-af52-438d-a71a-033cf4899a64`
- **Alias**: `FastSweep`
- **Inputs**:
  - `Rail` (`C`): Curve [item] — Curve as a sweep rail
  - `X`: Number [item] — if using a custom section, it controls the normalized horizontal position of the section. Otherwise, define the width of the default rectangle profile
  - `Y`: Number [item] —  if using a custom section, it controls the normalized vertical position of the section. Otherwise, define the height of the default rectangle profile
  - `Section` (`S`): Curve [item] — Optional profile for sweep
- **Outputs**:
  - `Fast_Sweep` (`S`): Brep [item] — Created Fast_Sweep
- **Behavior**: Quick single-section sweep
Right-click to either impose [RoadLike] or [Horizontal] balancing modes
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Fit Box
- **Tab**: Heteroptera > Geometry | **Type GUID**: `3ea79867-3271-4a5c-9344-1a58cd223aab`
- **Inputs**:
  - `Mesh` (`M`): Mesh [item] — Mesh to fit
- **Outputs**:
  - `Box` (`B`): Box [item] — Fit box
  - `Plane` (`P`): Plane [item] — Fit plane
- **Behavior**: Creates a smart minimum oriented bounding box fit to an input mesh (handles boxes, pipes, cylinders, etc.)
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Center
- **Tab**: Heteroptera > Geometry | **Type GUID**: `3c5edcba-b7a5-4710-b076-4b19a7080a2b`
- **Inputs**:
  - `Geometry` (`G`): Geometry [list] — Geometry to get the space-domain center from
- **Outputs**:
  - `Center` (`C`): Point [item] — Center
  - `Dimension` (`D`): Number [item] — Diagonal size of geometry's bounding box
- **Behavior**: Returns the center of the geometry and the diagonal of its bounding box as the dimension. Right-click to choose options.
[ForAll]: Calculates the center point for a group of geometries.
Position options:
[Spatial]: Spatial domain center.
[Planar]: Center projected onto the XY plane.
[Basement]: Center of the base plane
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Evaluate Rectangle
- **Tab**: Heteroptera > Geometry | **Type GUID**: `d1263d7a-dde0-45e0-a11a-01122cda5808`
- **Alias**: `EvalRect`
- **Inputs**:
  - `Rectangle` (`R`): Rectangle [item] — Domain of the grid
  - `U`: Number [item] — U Coordinate to evaluate
  - `V`: Number [item] — V Coordinate to evaluate
- **Outputs**:
  - `Point` (`P`): Point [item] — Point at normalized{uv}
- **Behavior**: Evaluate a rectangle at normalized{uv} parameter
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Grid In Rectangle
- **Tab**: Heteroptera > Geometry | **Type GUID**: `7102dfd1-14ad-430f-941b-e92fbbbdcdf5`
- **Alias**: `Grid`
- **Inputs**:
  - `Rectangle` (`R`): Rectangle [item] — Domain of the grid
  - `Size` (`S`): Number [item] — Distance between points of the grid
  - `V-Size` (`V`): Number [item] — Optional distance between grid points in the V direction. If omitted, the V size matches the U size.
- **Outputs**:
  - `Points` (`P`): Point [item] — Grid Points
  - `U`: Number [item] — Normalized U parameter
  - `V`: Number [item] — Normalized V parameter
- **Behavior**: Create a grid of points using a rectangle. If you're not satisfied using the [Exact Size] of the cells, you can Right-click to choose the related option.
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Group By Axis
- **Tab**: Heteroptera > Geometry | **Type GUID**: `23aa9ff3-bbec-4583-af94-1175e520d72d`
- **Alias**: `AxisGroup`
- **Inputs**:
  - `Lines` (`L`): Line [list] — Lines for grouping
  - `Tolerance` (`T`): Number [item] — Deviation tolerance
  - `Overlapping` (`O`): Boolean [item] — If true, the lines must overlap to be considered part of the same group
- **Outputs**:
  - `Lines` (`L`): Line [item] — Lines grouped by own axis
  - `Indices` (`i`): Integer [item] — Lines indices grouped by own axis
- **Behavior**: Group a list of 2d lines by their own axis
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Modular Points
- **Tab**: Heteroptera > Geometry | **Type GUID**: `4592834c-3a89-422d-a2c1-ef2c35efe477`
- **Alias**: `Modular`
- **Inputs**:
  - `Point` (`P`): Point [item] — Point to Digitize
  - `Scope` (`S`): Number [item] — Digitizing scope size
- **Outputs**:
  - `Point` (`P`): Point [item] — Digitized Point
- **Behavior**: Modularize(digitize) a point by specific Scope size
Right-click to choose Which Directions (X/Y/Z) are affected by Modularpoints
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Planarize Curve
- **Tab**: Heteroptera > Geometry | **Type GUID**: `cc820e4c-a146-4e68-81d0-e6ff3ef3dbeb`
- **Alias**: `CPL`
- **Inputs**:
  - `Curve` (`C`): Curve [list] — Curve to planarize
- **Outputs**:
  - `Planar curve` (`C`): Curve [item] — Planarized Curve
  - `Plane` (`P`): Plane [item] — Nearest plane to the curve
  - `Deviation ` (`D`): Number [item] — Maximum deviation
- **Behavior**: Planarizing  a curve Once working with multiple Curves: you can Right-click to choose the "ForAll" option if desire to Planarize  all curves Based on the same Plane.
Below it, You can find two different options to define this single plane ( Based on the first/ Average)
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

### Shell From Grid
- **Tab**: Heteroptera > Geometry | **Type GUID**: `1e5d93bd-f364-438a-9f95-63b9a8f53935`
- **Alias**: `Shell`
- **Inputs**:
  - `Points` (`P`): Point [tree] — a Point tree as the initiative grid
- **Outputs**:
  - `Geometrlevelc` (`G`): Geometry [item] — Surface , Mesh or lattice, which is created by grid
- **Behavior**: Create Surface, Mesh or net from a Tree of points
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]

## NAN

### Find Cycles
- **Tab**: Heteroptera > NAN | **Type GUID**: `2f4c5017-b987-4635-a9ac-d9f1ad2b7fdc`
- **Alias**: `Cycle`
- **Inputs**:
  - `Curves` (`C`): Curve [list] — Curve to get regions from
- **Outputs**:
  - `Regions` (`R`): Curve [item] — Regions calculated from input curves
  - `Segments` (`S`): Curve [item] — Regions calculated from input curves
  - `Points` (`P`): Point [item] — Regions calculated from input curves
  - `Regions` (`R`): TopoCycle [item] — Regions calculated from input curves
- **Behavior**: Create Cycles from a list of curves
- **Provenance**: [VERIFIED, Heteroptera.gha v8.2.2 & C# Source]
