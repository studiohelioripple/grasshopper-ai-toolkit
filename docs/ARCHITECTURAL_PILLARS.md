# Architectural Pillars & Repository Taxonomy

This document indexes and categorizes the **193 parametric Grasshopper definitions** within this repository into **8 distinct functional architectural pillars**.

---

## 1. Parametric Masonry, Brick Systems & Hanging Stones (56 Definitions)
**Domain:** Computational masonry, variable mortar gaps, rotation offset pairing, robotic/manual fabrication layouts, and stone facade assembly with automated technical drawings.

* **Core Architectural Workflow:**
  * Uses stochastic allocators to prevent repetitive patterns while preserving structural stability.
  * Employs custom C# derotation math paired with Heteroptera `Symmetric Domain` (`[-θ, +θ]`) to orient masonry blocks to complex target surfaces.
* **Representative Definitions:**
  * `Bricks Free Catalog.gh`, `Bricks Free varigap.gh`, `Bricks Free varigap 2.gh`, `Bricks Free varigap Block.gh`, `Bricks Free varigap Pairing Rotation-Offset parametric.gh`
  * `Bricks NonRect Walls.gh`, `Bricks OPT.gh`, `Bricks UT.gh`, `Align bricks.gh`, `Smart Bricks.gh`, `Modular Bricks.gh`, `Jagged Bricks.gh`
  * `Hanging Stones 3d fnl-Technical Drawing.gh`, `Hanging Stones 3d i-Technical Drawing recurrent +3D.gh`, `Hanging Stones 3d fnl-baker.gh`
* **Key Components:**
  * Heteroptera: `Weighted Allocator`, `Slingshot Allocator`, `Careless Range`, `Center`, `Stream Freeze / Gate`, `Symmetric Domain`
  * Native: `Divide Surface`, `Vector 2Pt`, `Orient`, `Transform`

---

## 2. Spatial Networks, Space Syntax & Topological Graph Analysis (21 Definitions)
**Domain:** Floorplan room connectivity, architectural space syntax, shortest route navigation, planar face cycles, and dual network extraction.

* **Core Architectural Workflow:**
  * Extracts adjacency matrices from room polylines without relying on metric distances.
  * Derives topological depth, connectivity, choice, and integration.
  * Normalizes integration indices (`[0.0, 1.0]`) to drive architectural heatmap gradients.
* **Representative Definitions:**
  * `topology-spacesyntax.gh`, `topology-spacesyntax.ghx`
  * `heteroptera/shortestWalk.gh`, `heteroptera/regions.gh`, `heteroptera/toplogy-manipulation.gh`
  * `organizedBubbleDiagram.gh`, `Codes Pattern.gh`, `StairTagMatch.gh`, `TagMatch.gh`
* **Key Components:**
  * Heteroptera: `Space Syntax`, `Topology Of Adjacencies`, `Reconstruct Topology`, `Shortest Route`, `Enumerator`, `Topology Embody`, `Cycle By Planar Mapping`, `Normalizer`

---

## 3. Architectural Facades & Envelopes (19 Definitions)
**Domain:** Multi-story parametric envelopes, fenestration rhythms, Mondrian subdivisions, vertical louvers, and edge flushings.

* **Core Architectural Workflow:**
  * Planar face partitioning of building facades into hierarchical mullion networks.
  * Rail sweeping of aluminum and stone frame sections along complex border profiles.
* **Representative Definitions:**
  * `4 MONDRIAN fACAD I.gh`, `4 MONDRIAN fACAD.gh`, `MondriFacad+Frame+pat.gh`, `MondriFacad+Frame.gh`, `MondriPlanes.gh`
  * `facade vertical.gh`, `facade vertical para.gh`, `facade vertical SW.gh`, `facade vertical rnd extend.gh`, `facade vertical para-tx.gh`
  * `Windows Frame.gh`, `ordibehesht Windows Frame.gh`, `ramsar facad cube.gh`, `standard flushing.gh`, `offset flushing.gh`
* **Key Components:**
  * Heteroptera: `Fast Sweep`, `Center`, `Symmetric Domain`, `Cycle By Planar Mapping`, `Network From Lines`

---

## 4. Vector Fields, Kangaroo Physics & Computational Morphogenesis (19 Definitions)
**Domain:** Particle flow simulations, curve force fields, cellular biological growth (scutoid cells), tensile membrane relaxation, and vortex trapping.

* **Core Architectural Workflow:**
  * Field-driven particle dynamics and continuous vector flow across surfaces.
  * Custom physics goals constraining geometry to flow lines within Kangaroo 2.
* **Representative Definitions:**
  * `boundling.gh`, `boundling2.gh`, `field 2.gh`, `jiji.gh`
  * `Saveh/scutoid (2).gh`, `Saveh/scutoid kangaroo.gh`, `Saveh/scutoid-m.gh`, `Saveh/scutoid.gh`
  * `Saveh/pomegrant.gh`, `Saveh/hydra-filler.gh`, `Saveh/MioFlow.gh`, `oricave.gh`, `Dew.gh`, `Bending.gh`
* **Key Components:**
  * Heteroptera: `Trap Goal`, `Align On Field Goal`, `Along Field Goal`, `Slop Gole`, `Simplex Noise`, `On-Curve Field`
  * Kangaroo 2: `Solver`, `Show`, `LengthGoal`

---

## 5. GIS, Urban Analysis & Architectural Production (17 Definitions)
**Domain:** City-scale GIS cartography (Rasht, Saveh, Canada), Persian/Farsi BIM tags, automated door/window schedules, and floorplan production.

* **Core Architectural Workflow:**
  * Importing shapefiles and CAD plot polylines into Grasshopper.
  * Ensuring proper bidirectional text rendering for Farsi / Persian / Arabic room tags and schedule legends via `ToolsUnicode`.
* **Representative Definitions:**
  * `Gis Rasht.gh`, `Rasht Attribute farsi.gh`, `Rasht Attribute.gh`, `Rasht BC.gh`, `piner Rasht.gh`, `Saveh/gis_import.gh`, `giscanada.gh`
  * `Plans.gh`, `Plans Additive Mahmoodie.gh`, `Elevation-Plan Aligner.gh`, `Dimension.gh`, `doortable.gh`, `doortables.gh`, `StoryTag.gh`
* **Key Components:**
  * Heteroptera: `ToolsUnicode`, `Allocate By Key`, `Match By Container`

---

## 6. Tessellation, Islamic Geometry & Parametric Patterns (16 Definitions)
**Domain:** Girih Islamic tile generation, Muqarnas modules, Escher-style geometric morphing, parametric hatching, and Parakeet tessellations.

* **Core Architectural Workflow:**
  * Periodic and non-periodic geometric patterns, attractor-graded perforations, and boundary region hatching.
* **Representative Definitions:**
  * `Escher/escher.gh`, `Escher/Parakeet.gha`
  * `pattern parakeet.gh`, `Pattern-Genrator.gh`, `Pattern-Cataloge-Genrator.gh`, `Muqa.gh`, `ravaq.gh`
  * `grid-morph-grade-attactor.gh`, `Att Hatches.gh`, `Att Hatches2.gh`, `AggriLand.gh`
* **Key Components:**
  * Parakeet, Heteroptera `Geometric Cycles`, `Grid In Rectangle`, `Interpolate +`

---

## 7. Parametric Product Assembly, Catalog Generation & Taxonomy (13 Definitions)
**Domain:** Modular furniture configuration, parametric shelving, component variation generation, and Rhino Block instance automation.

* **Representative Definitions:**
  * `Final Approach Product.gh`, `GeneralApproach Product.gh`, `Neo Approach Product.gh`, `StructureTree Mapper Product.gh`, `products 2.gh`
  * `books.gh` (151 components: parametric library storage system)
  * `Block-Catalog.gh`, `InstanceManager_Example.gh`, `taxonomyExample.gh`
* **Key Components:**
  * Heteroptera: `Seed Generator`, `Allocate By Index`, `Translated Plane`

---

## 8. Algorithmic Solvers, Math & Combinatorics (10 Definitions)
**Domain:** Discrete mathematical logic, chess constraint satisfaction (8-Queens problem), non-orientable topological surfaces (Möbius), and web API integration.

* **Representative Definitions:**
  * `8Queens.gh`, `8Queens With BruteEngine C#.gh`, `8Queens With BruteEngine.gh`, `8vazir.gh`
  * `Mobius Transform.gh`, `mobius-infinity.gh`, `river probability.gh`, `http-json.gh`, `webrequest.gh`
* **Key Components:**
  * Embedded C# backtracking engines, GhPython combinatorics, `Accord.dll`, `System.Net.Http`
