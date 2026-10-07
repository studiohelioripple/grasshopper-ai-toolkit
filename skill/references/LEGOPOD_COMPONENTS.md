# LegoPod Component Reference

Comprehensive reference for **LegoPod** (v0.4.2) in Grasshopper.
Total verified components: **42**.
Synthesized directly via offline assembly analysis and runtime parameter reflection.

## Table of Contents

- [Files](#files) — 3 components
- [Blocks](#blocks) — 14 components
- [Odds](#odds) — 7 components
- [Attributes](#attributes) — 6 components
- [Text](#text) — 10 components
- [Hatch](#hatch) — 2 components

---

## Files

### Build Attribute
- **Tab**: LegoPod > Files | **Type GUID**: `3497e94a-b35d-4d20-aae3-9eb2f7d09542`
- **Alias**: `AttBuild`
- **Inputs**:
  - `Name` (`N`): Text [item] — Name
  - `Layer` (`L`): Text [item] — Layer
  - `Color` (`C`): Colour [item] — Color
  - `Material` (`M`): Material [item] — Material
  - `Thickness` (`T`): Number [item] — Plot LineWeight  0:Default LineWeight -1:By Layer -2:By Parent -3:No Print
  - `ArrowHead` (`A`): Integer [item] — Arrowhead type
  - `Dictionary` (`D`): Dictionary [item] — Dictionary
  - `Attribute` (`A`): Attribute [item] — Base attribute to modify
  - `Lable` (`L`): Text [item] — Grouping Lable implemented by QuickBake component
- **Outputs**:
  - `Attribute` (`A`): Attribute [item] — Rhino geometry attribute
- **Behavior**: Construct an Obj.Attribute
- **Provenance**: [VERIFIED, LegoPod.gha v0.4.2 Assembly Reflection]

### Directory
- **Tab**: LegoPod > Files | **Type GUID**: `59df5675-db8e-4b22-95b8-21546f32aba7`
- **Inputs**:
  - `FilePath` (`P`): Text [item] — Path to get directory from
  - `Pattern` (`S`): Text [item] — Searching wildcard Pattern 
  - `All` (`T`): Boolean [item] — If false it searches just top folder if true it searches all subfolders
- **Outputs**:
  - `Files` (`F`): Text [list] — Search result
- **Behavior**: Retrieves the list of existing files within a folder
- **Provenance**: [VERIFIED, LegoPod.gha v0.4.2 Assembly Reflection]

### File Info
- **Tab**: LegoPod > Files | **Type GUID**: `2b8ed0ba-82f9-423e-8c19-f6e3df1e2427`
- **Alias**: `FileInfo`
- **Inputs**:
  - `FilePath` (`F`): Text [item] — Filepath to decompose
- **Outputs**:
  - `Name` (`N`): Text [item] — Pure Name of the file
  - `Extension` (`E`): Text [item] — extension of the file
  - `Filename` (`F`): Text [item] — file full name
  - `Path` (`P`): Text [item] — folder address of the file
  - `Size` (`S`): Integer [item] — File Size
- **Behavior**: Decompose a file info
- **Provenance**: [VERIFIED, LegoPod.gha v0.4.2 Assembly Reflection]

## Blocks

### Define Block
- **Tab**: LegoPod > Blocks | **Type GUID**: `44578fdc-bd75-4477-b782-04b4fc1d6d67`
- **Alias**: `DefBlock`
- **Inputs**:
  - `Geometries` (`G`): Geometry [list] — Geometries
  - `Attributes (Optional)` (`A`): Attribute [list] — Optional attributes 
  - `Name` (`N`): Text [item] — Name
  - `RefPlane` (`P`): Plane [item] — Reference Plane
- **Outputs**:
  - `Definition` (`D`): Block_Definition [item] — Instance reference definition
- **Behavior**: Define or modify an instance definition 
- **Provenance**: [VERIFIED, LegoPod.gha v0.4.2 Assembly Reflection]

### X-Ref Block
- **Tab**: LegoPod > Blocks | **Type GUID**: `418d8cc8-c46a-4bfa-8c4d-ca6c10f766bc`
- **Alias**: `XRef`
- **Inputs**:
  - `FilePath` (`F`): Text [list] — Reference File
  - `Name (Optional)` (`N`): Text [list] — Optional Name for the definition ,if omitted the filename will be used
  - `Define` (`D`): Boolean [item] — Define activation or updating toggle 
- **Outputs**:
  - `Definitions` (`D`): Block_Definition [list] — Instance Reference definitions
- **Behavior**: External Block from other .3dm files
- **Provenance**: [VERIFIED, LegoPod.gha v0.4.2 Assembly Reflection]

### File BlockStatistics
- **Tab**: LegoPod > Blocks | **Type GUID**: `e479cfd0-0f6b-49e8-8b12-4386d7d8c953`
- **Alias**: `FileStatistics`
- **Inputs**:
  - `FilePath` (`F`): Text [item] — .3dm Filepath to get statistics from
- **Outputs**:
  - `Definitions` (`D`): Text [list] — List of all Defined Blocks in the .3dm file
  - `References` (`R`): Text [list] — The names of used Blocks in the .3dm file 
  - `Numbers` (`N`): Integer [list] — Usage number of each block
- **Behavior**: Get the Instance statistics from a .3dm file
- **Provenance**: [VERIFIED, LegoPod.gha v0.4.2 Assembly Reflection]

### Block Explode
- **Tab**: LegoPod > Blocks | **Type GUID**: `88d3c3d6-46e5-4415-b974-4bf9826f7463`
- **Alias**: `BlockExplode`
- **Inputs**:
  - `Definition` (`D`): Block_Definition [item] — A Block-Definition to be decomposed
- **Outputs**:
  - `Objects` (`G`): Geometry [list] — Comprised referenced Objects (the objects within the block)
  - `Attribute` (`A`): Attribute [list] — Objects attribute
  - `Guid` (`G`): Guid [item] — Definition ID
  - `Boundingbox` (`B`): Box [item] — Instance's boundingbox
  - `References` (`R`): Block_Instance [list] — The list of instance objects of this definition existing in the active rhino document
- **Behavior**: Decompose a Block-Definition to its components
- **Provenance**: [VERIFIED, LegoPod.gha v0.4.2 Assembly Reflection]

### Block List
- **Tab**: LegoPod > Blocks | **Type GUID**: `2afd1473-67e9-4a6f-93aa-05a78133a71b`
- **Alias**: `BlockList`
- **Inputs**:
  - `Pattern (Optional)` (`S`): Text [item] — Optional string pattern to filter instances not matching the pattern (Regex)
- **Outputs**:
  - `Definitions` (`D`): Block_Definition [list] — Block Definition List
- **Behavior**: Retrieves the list of the instance definitions in the current document
- **Provenance**: [VERIFIED, LegoPod.gha v0.4.2 Assembly Reflection]

### Instance List
- **Tab**: LegoPod > Blocks | **Type GUID**: `57cfcfd9-29a7-4abc-91e8-30a44e5ce225`
- **Alias**: `InstanceList`
- **Inputs**:
  - `Definitions` (`D`): Block_Definition [item] — Block Definition
- **Outputs**:
  - `Instances` (`I`): Block_Instance [list] — Block Instance Lists
- **Behavior**: Retrieves the list of the instance_definitions in the current document
- **Provenance**: [VERIFIED, LegoPod.gha v0.4.2 Assembly Reflection]

### Instance Decompose
- **Tab**: LegoPod > Blocks | **Type GUID**: `c5f68246-b41d-426f-b8aa-f08907190fee`
- **Alias**: `InstanceDecompose`
- **Inputs**:
  - `Instance` (`I`): Block_Instance [item] — BlockInstance to decompose
- **Outputs**:
  - `Definition` (`D`): Block_Definition [item] — Reference Block
  - `Plane` (`P`): Plane [item] — Insertion Anchor-Plane
  - `Transform` (`X`): Transform [item] — Insertion Transform
  - `Box` (`B`): Box [item] — Bounding Box
  - `X-Scale` (`XS`): Number [item]
  - `Y-Scale` (`YS`): Number [item]
  - `Z-Scale` (`ZS`): Number [item]
- **Behavior**: Decompose BlockInstance to its components
- **Provenance**: [VERIFIED, LegoPod.gha v0.4.2 Assembly Reflection]

### Discover Nested Blocks
- **Tab**: LegoPod > Blocks | **Type GUID**: `84b062a8-44e7-4faf-b5f2-393e8d46f781`
- **Alias**: `DiscoverNested`
- **Inputs**:
  - `Block_Instance` (`B`): Block_Instance [item] — Block_Instance
  - `Block_Definition` (`B`): Block_Definition [item] — Block_Definition
- **Outputs**:
  - `Plane` (`P`): Plane [list] — The location of found items
- **Behavior**: Recursively finds the location of requested nested blocks within a given Instance
- **Provenance**: [VERIFIED, LegoPod.gha v0.4.2 Assembly Reflection]

### Rename Block
- **Tab**: LegoPod > Blocks | **Type GUID**: `986cb469-9852-4287-8cb6-3c95b5721f11`
- **Alias**: `RenameBlock`
- **Inputs**:
  - `Block_Definition` (`B`): Block_Definition [item] — Block_Definition
  - `Name` (`N`): Text [item] — Optional Block new name
  - `Description` (`D`): Text [item] — Optional new Block Description
- **Outputs**: none
- **Behavior**: Edit a Block's' name and description
- **Provenance**: [VERIFIED, LegoPod.gha v0.4.2 Assembly Reflection]

### Nested Count
- **Tab**: LegoPod > Blocks | **Type GUID**: `10e4b152-421e-4469-b946-219828c12bc7`
- **Alias**: `NestedCount`
- **Inputs**:
  - `Wrapper` (`W`): Block_Definition [item] — The wrapper-block to search within
  - `Nested` (`N`): Block_Definition [item] — The nested-block to search for
- **Outputs**:
  - `Number` (`N`): Integer [item] — The number of found nested blocks within the wrapper
- **Behavior**: Calculate recursively the number of all requested nested-block within a wrapper-block
- **Provenance**: [VERIFIED, LegoPod.gha v0.4.2 Assembly Reflection]

### Insert Block by Box
- **Tab**: LegoPod > Blocks | **Type GUID**: `8af1e6a9-7ed9-4062-9082-430ca082f158`
- **Alias**: `BlockBox`
- **Inputs**:
  - `TransformBox` (`B`): Box [item] — Transform reference box
- **Outputs**: none
- **Behavior**: Fit and place an instance object into a reference box
- **Provenance**: [VERIFIED, LegoPod.gha v0.4.2 Assembly Reflection]

### Insert Block
- **Tab**: LegoPod > Blocks | **Type GUID**: `0ef76392-9302-47f3-bee7-ba3314b8e805`
- **Alias**: `BlockInsert`
- **Inputs**:
  - `Plane` (`PL`): Plane [item] — Base of the reference object
  - `X scale` (`XS`): Number [item] — Scale factor on X axis of placing reference object 
  - `Y scale (Optional)` (`YS`): Number [item] — Optional scale factor on Y axis of placing reference object (uniform scale if omitted)
  - `Z scale (Optional)` (`ZS`): Number [item] — Optional scale factor on Z axis of placing reference object (uniform scale if omitted)
- **Outputs**: none
- **Behavior**: Insert an Instance object
- **Provenance**: [VERIFIED, LegoPod.gha v0.4.2 Assembly Reflection]

### Insert Block by Transform
- **Tab**: LegoPod > Blocks | **Type GUID**: `620fa209-80d7-418c-9328-119d8d901ccd`
- **Alias**: `BlockTransform`
- **Inputs**:
  - `Transform` (`X`): Transform [item] — Transform reference box
- **Outputs**: none
- **Behavior**: Insert blocks by transform data
- **Provenance**: [VERIFIED, LegoPod.gha v0.4.2 Assembly Reflection]

### Replace Block
- **Tab**: LegoPod > Blocks | **Type GUID**: `fe88ce5b-6683-45ff-9c61-b4b518762ee1`
- **Alias**: `BlockReplace`
- **Inputs**:
  - `Instance` (`A`): Block_Instance [item] — The Instance to be replace with another
  - `Block` (`B`): Block_Definition [item] — Block definition with which the the object will be replaced 
- **Outputs**: none
- **Behavior**: Replace a Block Instance with another definition and optional applying transform
- **Provenance**: [VERIFIED, LegoPod.gha v0.4.2 Assembly Reflection]

## Odds

### Quick Baker
- **Tab**: LegoPod > Odds | **Type GUID**: `6bec70a6-9af2-4d17-b712-c9d41c02bb70`
- **Alias**: `QB`
- **Inputs**:
  - `Geometry` (`G`): Geometry [list] — Geometry to bake
  - `Attribute` (`A`): Attribute [list] — RET_get_Description
- **Outputs**:
  - `GUID` (`G`): Guid [list] — ID of baked geometry
- **Behavior**: Bakes the given geometries with attribute and grouping features
- **Provenance**: [VERIFIED, LegoPod.gha v0.4.2 Assembly Reflection]

### Replace Objects
- **Tab**: LegoPod > Odds | **Type GUID**: `6886ad52-7a40-442b-a34d-fa3ebd09b8cc`
- **Alias**: `Replace`
- **Inputs**:
  - `Rhino Geometry` (`R`): Guid [item] — Reference Rhino-Object to replace
  - `Geometry` (`G`): Geometry [item] — Basic geometry to replace with (Brep,Surface,Curve,Point)
- **Outputs**: none
- **Behavior**: Click on Replace Button to Replace a Rhino-object with another geometry
- **Provenance**: [VERIFIED, LegoPod.gha v0.4.2 Assembly Reflection]

### Transform
- **Tab**: LegoPod > Odds | **Type GUID**: `9d88571d-f47e-4dbc-b641-62de283a38aa`
- **Alias**: `Xform`
- **Inputs**:
  - `Rhino Geometry` (`G`): Guid [item] — Geometry to transform
  - `Transform` (`X`): Transform [item] — Transformation Data
- **Outputs**: none
- **Behavior**: Click on Xform Button to Transform a geometry in rhino by a transform information
- **Provenance**: [VERIFIED, LegoPod.gha v0.4.2 Assembly Reflection]

### Group
- **Tab**: LegoPod > Odds | **Type GUID**: `b3083e4c-d7bc-4009-b6bd-6cc7e4c7d270`
- **Inputs**:
  - `Rhino Geometry` (`G`): Guid [list] — Reference Geometries in rhino to Group
  - `Group Name` (`N`): Text [item] — Optional name for the group
  - `Active` (`A`): Boolean [item] — Constant Activation
- **Outputs**: none
- **Behavior**: Group reference geometries in rhino scene
Either click on component's group button to activate it for once, or set (A)Constant Activation True to group all geometries immediately when they're defined as (G) inputs
- **Provenance**: [VERIFIED, LegoPod.gha v0.4.2 Assembly Reflection]

### Ovulate
- **Tab**: LegoPod > Odds | **Type GUID**: `a4d56174-78c6-4157-8bd9-058f9e5e48ac`
- **Inputs**:
  - `Geometry` (`G`): Geometry [tree] — Geometry to bake
  - `Attribute (Optional)` (`A`): Attribute [tree] — RET_get_Description
  - `Boundary` (`R`): Rectangle [item] — Bounding rectangle bound for baking geometry
  - `Iteration (Optional)` (`N`): Integer [item] — Optional external forced iteration number, if omitted the internal incremental number would be used
- **Outputs**:
  - `Vector` (`V`): Vector [item] — Vector of current position
  - `Number` (`N`): Integer [item] — Number of iteration
  - `Rectangle` (`R`): Rectangle [item] — The latest baking frame
- **Behavior**: Bake multiple items by sequence, ordered in a grid.
- **Provenance**: [VERIFIED, LegoPod.gha v0.4.2 Assembly Reflection]

### Create Table
- **Tab**: LegoPod > Odds | **Type GUID**: `ade7fd21-8d0f-4caf-8722-b142ff73c134`
- **Alias**: `Table`
- **Inputs**:
  - `Plane` (`P`): Plane [item] — Table location
  - `Headings` (`H`): Text [list] — Table Headings
  - `Data` (`D`): Text [tree] — Datatree to put into a table
  - `Header-Style` (`HS`): Text [item] — TextStyle for Headers
  - `Data-Style` (`DS`): Text [item] — TextStyle for values
  - `X-Margin` (`X`): Number [item]
  - `Y-Margin` (`Y`): Number [item]
- **Outputs**:
  - `Text` (`T`): Text [list] — Texts
  - `Text` (`T`): Text [list] — Texts
  - `Bound` (`R`): Rectangle [item]
  - `H`: Line [list]
  - `V`: Line [list]
- **Behavior**: Creates a table of data
- **Provenance**: [VERIFIED, LegoPod.gha v0.4.2 Assembly Reflection]

### Create Text
- **Tab**: LegoPod > Odds | **Type GUID**: `cd4fc408-b955-46ea-ab76-8236e449a3e0`
- **Alias**: `CreateText`
- **Inputs**:
  - `Location` (`L`): Plane [item] — Location of the Text
  - `Text` (`T`): Text [item] — Text to bake
  - `Size` (`S`): Number [item] — Text Size
  - `Attribute` (`A`): Attribute [item] — Attribute
  - `Justification` (`J`): Integer [item] — Text Justification (Optional)
- **Outputs**:
  - `Text` (`T`): Text [item] — Text
- **Behavior**: Creates Either TextDot or 3d-Text
- **Provenance**: [VERIFIED, LegoPod.gha v0.4.2 Assembly Reflection]

## Attributes

### Paint Attribute
- **Tab**: LegoPod > Attributes | **Type GUID**: `44fd137c-cc6f-4baa-a6f0-d1a34939215b`
- **Alias**: `Paint`
- **Inputs**:
  - `Rhino Geometry` (`G`): Guid [item] — Referenced Geometries in rhino
  - `Attribute` (`A`): Attribute [item] — Attribute data based on which the geometry would change
- **Outputs**:
  - `Message` (`M`): Text [item] — Output messages
- **Behavior**: Change the attribute of a Referenced Geometries in rhino. (Apply an attribute partly on an object)
- **Provenance**: [VERIFIED, LegoPod.gha v0.4.2 Assembly Reflection]

### Get Block Meta-Data
- **Tab**: LegoPod > Attributes | **Type GUID**: `f4087d2b-e9ea-4a91-8f35-2677e4dbf3dc`
- **Alias**: `SetBlockMetaData`
- **Inputs**:
  - `Block_Definition` (`B`): Block_Definition [item] — Block_Definition
  - `Keys` (`K`): Text [list] — Optional User Keys
- **Outputs**:
  - `Keys` (`K`): Text [list] — Block Mapping-Keys
  - `Values` (`V`): Generic [list] — Block Mapping-Values
- **Behavior**: Extract Meta-Data out of a Block-Definition
- **Provenance**: [VERIFIED, LegoPod.gha v0.4.2 Assembly Reflection]

### User Dictionary
- **Tab**: LegoPod > Attributes | **Type GUID**: `5c99298a-bdc9-4e96-9d6e-4d423254578c`
- **Alias**: `Dict`
- **Inputs**:
  - `Keys` (`K`): Text [list] — List of keys
  - `Values` (`V`): Text [list] — List of valus
  - `Merge` (`M`): Integer [item] — RET_ToString
- **Outputs**:
  - `Dictionary` (`D`): Dictionary [item] — Dictionary
- **Behavior**: Add user-dictionary to attribute
- **Provenance**: [VERIFIED, LegoPod.gha v0.4.2 Assembly Reflection]

### Get User-Dictionary
- **Tab**: LegoPod > Attributes | **Type GUID**: `c1d173fd-7921-45bd-9842-31a6a6991590`
- **Alias**: `UserDict`
- **Inputs**:
  - `Attribute` (`A`): Attribute [item] — Rhino geometry attribute
  - `Keys` (`K`): Text [list] — Optional User Keys
- **Outputs**:
  - `Keys` (`K`): Text [list] — User dictionary Keys
  - `Values` (`V`): Text [list] — User dictionary Values
- **Behavior**: Gets the user dictionary from an attribute
- **Provenance**: [VERIFIED, LegoPod.gha v0.4.2 Assembly Reflection]

### Set Block Meta-Data
- **Tab**: LegoPod > Attributes | **Type GUID**: `632c8255-9f86-41a2-8bad-aa13fdfc6e47`
- **Alias**: `SetBlockMetaData`
- **Inputs**:
  - `Block_Definition` (`B`): Block_Definition [item] — Block_Definition
  - `Keys` (`K`): Text [list] — Block Mapping-Keys
  - `Values` (`V`): Generic [list] — Block Mapping-Values
- **Outputs**: none
- **Behavior**: Put Meta-Data into a Block-Definition
- **Provenance**: [VERIFIED, LegoPod.gha v0.4.2 Assembly Reflection]

### Explode Attribute
- **Tab**: LegoPod > Attributes | **Type GUID**: `2333767b-7851-4b9a-b08a-fa805af378cb`
- **Alias**: `AttExplode`
- **Inputs**:
  - `Attribute` (`A`): Attribute [item] — Attribute
- **Outputs**:
  - `Name` (`N`): Text [item] — Name
  - `Layer` (`L`): Text [item] — Layer
  - `Color` (`C`): Colour [item] — Color
  - `Material` (`M`): Material [item] — Material
  - `Thickness` (`T`): Number [item] — Plot Line weight
- **Behavior**: Deconstruct an Obj.Attribute
- **Provenance**: [VERIFIED, LegoPod.gha v0.4.2 Assembly Reflection]

## Text

### Vertex Meta-Data
- **Tab**: LegoPod > Text | **Type GUID**: `d7093d8f-5492-4f72-824a-2a0a94a7163d`
- **Alias**: `MMD`
- **Inputs**:
  - `Mesh` (`M`): Mesh [item] — Base mesh as the vertices set container
  - `Key` (`K`): Text [item] — Meta-data key
  - `Values` (`V`): Generic [list] —  a tree of Values. A list for each vertex is required
- **Outputs**:
  - `values` (`V`): Generic [list] — List of values respectively related to each vertex
- **Behavior**: Extract meta-data from or inject it into a mesh's vertices
- **Provenance**: [VERIFIED, LegoPod.gha v0.4.2 Assembly Reflection]

### Hatch Create
- **Tab**: LegoPod > Text | **Type GUID**: `8c08bb14-7e00-4c56-95c6-bb9887122fdc`
- **Alias**: `Hatch`
- **Inputs**:
  - `Curve` (`C`): Curve [list] — Close Curves as boundaries
  - `Pattern` (`P`): Hatch_Pattern [item]
  - `Rotation` (`R`): Number [item] — Pattern rotation
  - `Scale` (`S`): Number [item] — Pattern scale
  - `Origin` (`O`): Point [item] — Pattern BasePoint
  - `Attribute` (`A`): Attribute [item] — Attribute
  - `Bake` (`B`): Boolean [item] — Baking switch
- **Outputs**:
  - `Hatch` (`H`): Hatch [list] — Hatch objects
- **Behavior**: Creates Hatch within a boundary curve
- **Provenance**: [VERIFIED, LegoPod.gha v0.4.2 Assembly Reflection]

### Table TSV-Data
- **Tab**: LegoPod > Text | **Type GUID**: `1fe49c7b-0aa8-469f-87aa-7ee7ff9a60a9`
- **Alias**: `TSV`
- **Inputs**:
  - `Data` (`D`): Text [list] — data in format of TSV or CSV
  - `Format` (`F`): Integer [item] — Input Data Format (Separator options)
  - `Flip` (`S`): Boolean [item] — Flip Matrix
- **Outputs**:
  - `Data` (`D`): Text [tree] — Structured Data
- **Behavior**: Convert TSV (Tab Separated Data) to GH Data-Structure
- **Provenance**: [VERIFIED, LegoPod.gha v0.4.2 Assembly Reflection]

### Table GapFiller
- **Tab**: LegoPod > Text | **Type GUID**: `7c6371e0-18e4-441b-a36d-e09d53d514a5`
- **Alias**: `GapFiller`
- **Inputs**:
  - `Fields` (`F`): Text [tree] — Items to be matching key
  - `Values` (`V`): Generic [tree] — Values related to the keys
  - `Gap-Filler` (`G`): Generic [item] — Optional item to replace with all Nulls
- **Outputs**:
  - `Fields` (`F`): Text [list] — Fields
  - `Values` (`V`): Text [tree] — Values
  - `Data` (`D`): Text [tree] — Aggregated fields with values
- **Behavior**: fill relative data gaps with a default value
- **Provenance**: [VERIFIED, LegoPod.gha v0.4.2 Assembly Reflection]

### Text-Group by Pattern
- **Tab**: LegoPod > Text | **Type GUID**: `b09c19c8-d076-481a-a20a-922160ea4a58`
- **Alias**: `TextG-RegX`
- **Inputs**:
  - `Text` (`T`): Text [list] — Text objects' ids to group
  - `Pattern` (`P`): Text [item] — RegEx Pattern for matching texts
  - `Ignore-Case` (`C`): Boolean [item] — If true, letters' case would be ignored 
- **Outputs**:
  - `Matched` (`M`): Text [tree] — Matched Texts
  - `Unmatched` (`U`): Text [list] — Unmatched Texts
  - `Keys` (`K`): Text [tree] — Matched keys
- **Behavior**: Groups text objects by their contents matched with RegEx patterns
- **Provenance**: [VERIFIED, LegoPod.gha v0.4.2 Assembly Reflection]

### Text-Group by Property
- **Tab**: LegoPod > Text | **Type GUID**: `5706e11c-ef26-4e05-9816-19476140f122`
- **Alias**: `TextG-Prop`
- **Inputs**:
  - `Text` (`T`): Text [list] — Text objects' ids to group
  - `Mode` (`M`): Integer [item] — Grouping Mode
- **Outputs**:
  - `Text` (`T`): Text [tree] — Texts in Groups
  - `Keys` (`K`): Generic [tree] — Grouping keys
- **Behavior**: Groups text objects by their properties
- **Provenance**: [VERIFIED, LegoPod.gha v0.4.2 Assembly Reflection]

### Explode Text
- **Tab**: LegoPod > Text | **Type GUID**: `e0a71e36-0024-4d69-9f18-b8caac092f89`
- **Alias**: `TextBomb`
- **Inputs**:
  - `Text` (`T`): Text [item] — Text
- **Outputs**:
  - `Location` (`P`): Plane [item] — AnchorPoint of the text
  - `Text` (`T`): Text [item] — Text String
  - `Size` (`S`): Number [item] — Text Size
  - `Justification` (`J`): Text [item] — Text Justification
  - `Style` (`S`): Text [item] — Annotation Style
  - `Attribute` (`A`): Attribute [item] — Attribute
- **Behavior**: Extract the properties from  Text or TextDot objects
- **Provenance**: [VERIFIED, LegoPod.gha v0.4.2 Assembly Reflection]

### Edit Text
- **Tab**: LegoPod > Text | **Type GUID**: `f37ae308-eecb-4dec-99b0-e36f8bae899c`
- **Alias**: `TXTEdit`
- **Inputs**:
  - `Text` (`T`): Text [item] — Rhino Text (Or TextDot) to edit
  - `Text` (`C`): Text [item] — Text-Content String
  - `Height` (`H`): Number [item] — Text Height
  - `Style` (`S`): Text [item] — Text-Style
- **Outputs**: none
- **Behavior**: Modify text objects
- **Provenance**: [VERIFIED, LegoPod.gha v0.4.2 Assembly Reflection]

### Style From Text
- **Tab**: LegoPod > Text | **Type GUID**: `36a16613-68c4-4664-ab07-f523b6a49b4e`
- **Alias**: `StyleOfText`
- **Inputs**:
  - `Text` (`T`): Text [item] — A Text object based on which Style will be redefined
  - `Style` (`S`): Text [item] — Annotation-Style name to create or modify
- **Outputs**: none
- **Behavior**: Defines a new or modifies an existing annotation-style matching with the given text object
- **Provenance**: [VERIFIED, LegoPod.gha v0.4.2 Assembly Reflection]

### Create Text (Style)
- **Tab**: LegoPod > Text | **Type GUID**: `62638394-0c01-4bdb-a093-e0da687e201c`
- **Alias**: `Style Text`
- **Inputs**:
  - `Location` (`L`): Plane [item] — Location of the Text
  - `Text` (`T`): Text [item] — Text to bake
  - `StyleName` (`S`): Text [item] — Text-StyleName Name. If the styleName with the name doesn't exist a new styleName styleName with such name will be created
  - `Attribute` (`A`): Attribute [item] — Attribute
- **Outputs**:
  - `Text` (`T`): Text [item] — Text
- **Behavior**: Creates Text with a text-style
- **Provenance**: [VERIFIED, LegoPod.gha v0.4.2 Assembly Reflection]

## Hatch

### Hatch Modify
- **Tab**: LegoPod > Hatch | **Type GUID**: `2f7a55c9-9dd4-475c-8bca-4e48be2f9ba5`
- **Alias**: `Hatch_Modify`
- **Inputs**:
  - `Hatch` (`H`): Hatch [item] — Hatch
  - `Pattern` (`P`): Hatch_Pattern [item] — RET_ToString
  - `Rotation` (`R`): Number [item] — Pattern rotation
  - `Scale` (`S`): Number [item] — Pattern scale
- **Outputs**: none
- **Behavior**: Modify Hatch
- **Provenance**: [VERIFIED, LegoPod.gha v0.4.2 Assembly Reflection]

### Hatch Explode
- **Tab**: LegoPod > Hatch | **Type GUID**: `28a23713-5c1c-423a-9838-a8fa66b79ef3`
- **Alias**: `ExplodeHatch`
- **Inputs**:
  - `Hatch` (`H`): Hatch [item] — Hatch
- **Outputs**:
  - `Boundaries` (`C`): Curve [list] — Hatch boundaries
  - `Pattern` (`P`): Hatch_Pattern [item] — Index of hatch pattern
  - `Scale` (`S`): Number [item] — Hatch pattern Scale
  - `Rotation` (`R`): Number [item] — Hatch pattern rotation
  - `Area` (`A`): Number [item] — Hatch Area
  - `Lines` (`L`): Line [list] — Pattern Lines
- **Behavior**: Explodes a hatch into components
- **Provenance**: [VERIFIED, LegoPod.gha v0.4.2 Assembly Reflection]
