# Grasshopper Workflow-Pattern Cookbook

Canonical, deduplicated recipe collection synthesized from raw book extractions:
- **AAD** = Tedeschi, Wirz, Andreani — *AAD Algorithms-Aided Design* (2014), extracted as `aad-part1.md`…`aad-part6.md` (PDF pages 1–498, cited below as `AAD pt.N p.X`)
- **Essential** = Rajaa Issa — *Essential Algorithms and Data Structures for Grasshopper*, 2nd ed., extracted as `essential-part1.md`, `essential-part2.md` (cited below as `Essential pt.N p.X`)

Only patterns actually present in the raw extraction files are included. No wiring has been invented: where a raw pattern's diagram was stated as illegible or the source gave no component-level wiring, the recipe is marked **[PARTIAL]** and the limitation is stated explicitly. Page numbers reproduce whatever the raw files cited (printed-page convention, occasionally PDF-page where that is what the source used).

---

## Table of Contents

| # | Category | Recipes |
|---|---|---|
| 1 | [Fundamentals — Points, Curves, Vectors](#1-fundamentals--points-curves-vectors) | 13 |
| 2 | [List Operations](#2-list-operations) | 9 |
| 3 | [Data-Tree Manipulation & List Matching](#3-data-tree-manipulation--list-matching) | 15 |
| 4 | [Attractor Patterns](#4-attractor-patterns) | 6 |
| 5 | [Grids & Paneling](#5-grids--paneling) | 10 |
| 6 | [Surface Subdivision & Morphing](#6-surface-subdivision--morphing) | 5 |
| 7 | [Curvature & Developable-Surface Analysis](#7-curvature--developable-surface-analysis) | 3 |
| 8 | [Mesh & Subdivision](#8-mesh--subdivision) | 8 |
| 9 | [Physics / Form-Finding — Kangaroo](#9-physics--form-finding--kangaroo) | 8 |
| 10 | [Optimization — Goat / Galapagos / Karamba / Millipede](#10-optimization--goat--galapagos--karamba--millipede) | 5 |
| 11 | [Fabrication — Sectioning, Waffling, Printing](#11-fabrication--sectioning-waffling-printing) | 4 |
| 12 | [Recursion / Loops — HoopSnake & Loop Plug-in](#12-recursion--loops--hoopsnake--loop-plug-in) | 4 |
| 13 | [Environmental Analysis — GECO / Ecotect](#13-environmental-analysis--geco--ecotect) | 6 |

**Total: 96 recipes** (stats block at end of file).

---

## 1. Fundamentals — Points, Curves, Vectors

### Parametric Two-Point Line
- Purpose: Build a fully associative line from six coordinate sliders so moving any slider updates the line live.
- Difficulty: basic
- Chain:
  ```
  === Section: Parametric two-point line ===
  Slider[X coordinate] -> ConstructPoint(Pt).X {flat}
  Slider[Y coordinate] -> ConstructPoint(Pt).Y {flat}
  Slider[Z coordinate, 0] -> ConstructPoint(Pt).Z {flat}
  ConstructPoint(A).Pt -> Line(Ln).A {flat}
  ConstructPoint(B).Pt -> Line(Ln).B {flat}
  Line(Ln).L -> output {flat, single line}
  ```
- Tree handling notes: Everything is a single item; no grafting needed. Demonstrates that one small definition produces three distinct outputs (2 points + 1 line) simultaneously.
- Failure modes: Line shows orange ("Input parameter A/B failed to collect data") if A/B unwired; shows red ("Data conversion failed from Number to Point") if a raw number is wired into A/B instead of a Point.
- Source: [STATED, AAD pt.1 p.44,47] merged with the equivalent Essential build: [STATED, Essential pt.1 p.11-12 (Example 1-3-3)].

### Circle from Plane + Radius (the "intermediate process" pattern)
- Purpose: Teach the canonical 4-step algorithm design process (Output → Key process → Input → Intermediate process) using a circle that needs a Plane, not just a point.
- Difficulty: basic
- Chain:
  ```
  === Section: Circle via intermediate Plane ===
  Panel[0,0,0] -> Plane(Pln) {intermediate process}
  Plane(Pln) -> Circle(Cir).P {flat}
  Panel[2] -> Circle(Cir).R {flat}
  Circle(Cir).C -> output {flat, single circle}
  ```
- Tree handling notes: Flat throughout. The lesson is structural (why an intermediate step is needed), not tree-shape.
- Failure modes: Feeding a bare Point into Circle's plane-typed input (P) rather than constructing a Plane first will not give the expected orientation; Center Box/Circle-style primitives that expect a Plane silently default to World XY if unwired.
- Source: [STATED, AAD pt.1 p.35 (Figure 1.1)] merged with [STATED, Essential pt.1 p.6, p.10-11 (Examples 1-2-2, 1-3-2)].

### Curve Endpoints & Midpoint Snaps (Grasshopper's answer to CAD Osnap)
- Purpose: Replicate CAD Object-Snap behavior (endpoint, midpoint, centroid) using explicit components, since GH has no click-to-snap.
- Difficulty: basic
- Chain:
  ```
  === Section: 1.7.1 Object snap in Grasshopper ===
  Crv -> PointOnCurve[slider 0..1, 0.50] {flat}  -- arc-length midpoint
  Crv -> EndPoints(End).C -> End.S, End.E {flat}  -- start/end points
  Crv1 -> Area1(Area).G -> Area1.C {centroid}
  Crv2 -> Area2(Area).G -> Area2.C {centroid}
  Area1.C -> Line(Ln).A ; Area2.C -> Line(Ln).B {flat}  -- centroid-to-centroid connector
  ```
- Tree handling notes: All flat/single-item. Point On Curve reparameterizes internally by arc length (0=start,1=end,0.5=true midpoint) — no explicit Reparameterize needed for this component specifically.
- Failure modes: Confusing Point On Curve (arc-length based) with Evaluate Curve (parametric-t based) — only the former reliably gives the geometric midpoint at 0.5.
- Source: [STATED, AAD pt.1 p.61-63].

### Curve Division Family — Divide Curve vs Divide Length vs Divide Distance vs Contour
- Purpose: Choose the correct subdivision algorithm — by count, by fixed arc-length, by radial-distance stepping, or by planar slicing — and understand that dividing produces parallel Points + Tangents + Parameters outputs from one curve input.
- Difficulty: basic
- Chain:
  ```
  === Section: Curve division family ===
  Crv -> Divide (Curve>Division).C ; Slider[Count, N] -> Divide.N -> Divide.P {N+1 pts open / N pts closed}, Divide.T (tangents), Divide.t (params) {flat}
  Crv -> DivLength.C ; Slider[Length, L] -> DivLength.L -> DivLength.P {fixed arc-length segments, leftover arc at end} {flat}
  Crv -> DivDist.C ; Slider[Distance, D] -> DivDist.D -> DivDist.P {sequential circle-intersection stepping, leftover arc} {flat}
  Crv, StartPt P, direction N, Slider[D] -> Contour.C/.P/.N/.D -> intersection points at each D-spaced parallel cut {flat}
  ```
- Tree handling notes: All four outputs stay flat/single-branch for a single input curve; feeding a LIST of curves promotes the output to a tree (one branch per curve) — see recipe "Deconstruct-Point → Entwine" and Essential's tree-generation notes for that transition.
- Failure modes: Divide Curve's K input and T/t outputs are shown on every diagram in AAD pt.1 but never explained in that book (K = kinks, T/t = tangent + parameter, per general GH knowledge — not asserted by the source itself); Divide Length/Distance both leave an uneven "leftover arc" if the curve length isn't an exact multiple of the spacing value; an open curve yields N+1 points for N segments while a closed curve yields exactly N (start/end coincide).
- Source: [STATED, AAD pt.1 p.64-65,75-82 / AAD pt.3 p.132-134] merged with [STATED, Essential pt.1 p.35 (Figure 39)].

### Robust Curve-Midpoint Evaluation (Reparameterize vs. normalized-t vs. domain-math)
- Purpose: Avoid the classic bug of assuming a curve's native parametric domain is [0,1] when evaluating with Evaluate Curve.
- Difficulty: intermediate
- Chain:
  ```
  === Section: Robust midpoint, three equivalent fixes ===
  -- naive (WRONG unless domain happens to be 0-1):
  Crv -> Eval.C ; Panel[0.5] -> Eval.t -> Eval.P {wrong point if native domain != 0-1}
  -- Fix A: compute the true midpoint from the curve's own domain
  Crv -> Domain -> DeDomain(DeDomain).I -> S,E
  S,E -> Expression("(x+y)/2").x,y -> R -> Eval.t ; Crv -> Eval.C {correct point}
  -- Fix B: force the curve's domain to [0,1]
  Crv -> [right-click Reparameterize] -> Eval.C ; Panel[0.5] -> Eval.t {correct point}
  -- Fix C: use the evaluator's own normalized-parameter toggle
  Crv -> Eval.C ; Panel[0.5] -> Eval.t ; Toggle[True] -> Eval.N {correct point}
  ```
- Tree handling notes: Flat/single-item throughout; the issue is domain semantics, not tree shape. Reparameterize does NOT fix curve direction (start/end orientation) — that is a separate operation (Flip Curve).
- Failure modes: `t=0.5` is generally NOT the geometric midpoint because parametric "speed" is uneven near concentrations of control points, even after rebuilding with uniformly spaced control points; this remains true after Reparameterize normalizes the *domain* — it does not equalize arc-length speed, it only rescales the numbers.
- Source: [STATED, AAD pt.3 p.124-127 (t is not arc length)] merged with [STATED, Essential pt.1 p.20,24 (Figures 25, 27/28)].

### Flip Curve to Unify Mixed Directions
- Purpose: Normalize inconsistent curve start/end directions across a batch of curves, single-curve or list-wide.
- Difficulty: basic
- Chain:
  ```
  === Section: Flip with guide curve, batch normalize ===
  Curve1(L→R), Curve2(L→R), Curve3(R→L), Curve4(R→L) -> Merge.D1..D4 -> Merge.R {4 items, mixed direction}
  Curve4 -> Flip.G {guide curve, direction to match}
  Merge.R -> Flip.C -> Flip.C {all 4 now R→L} {flat, 4 items}
  ```
- Tree handling notes: Merge collapses all curves into one flat list before the single Flip call evaluates each item against the guide and flips only mismatched ones — one operation instead of N manual flips.
- Failure modes: Reparameterizing a curve's domain does NOT fix its direction — these are independent operations; use Flip Curve specifically for direction.
- Source: [STATED, AAD pt.3 p.128-130].

### Vector Construction & Rescaling
- Purpose: Build, unitize, and rescale vectors explicitly (GH does not do implicit vector math the way interactive CAD does).
- Difficulty: basic
- Chain:
  ```
  === Section: Vector build + rescale ===
  PtA, PtB -> Vec2Pt.A, .B -> V (vector), L (length) {flat}
  V -> Unit(Unit Vector).V -> V {unitized, length 1}
  V -> Amp(Amplitude).V ; Slider[Amplitude] -> Amp.A -> V {rescaled to arbitrary length}
  V -> AxB.A ; Slider[B] -> AxB.B -> R {scalar-multiplied vector; N<0 reverses sense}
  V, AnchorPt -> VDis.V, .A {visual confirmation only}
  ```
- Tree handling notes: Flat/single item; scales cleanly to lists of vectors via default list matching.
- Failure modes: Vectors are invisible in the Rhino viewport by default — a Vector Display component is mandatory to see them; N<0 in scalar multiplication reverses the vector's sense, not just its magnitude.
- Source: [STATED, AAD pt.3 p.185-187].

### Move via Scaled Unit-Axis Vector
- Purpose: Translate geometry along a world axis using a slider-scaled Unit X/Y/Z vector — the standard GH substitute for interactive "move" gizmos.
- Difficulty: basic
- Chain:
  ```
  === Section: 1.7.4 Moving an object / vectors ===
  Geo -> Move.G {flat}
  Slider[Factor, 2] -> UnitX.F -> UnitX.V -> Move.T {flat}
  Move.G -> output {moved geometry}
  ```
- Tree handling notes: Feeding a LIST into T (e.g. from a Series) while G stays a single item broadcasts G against every vector, producing one moved copy per list item (list-matching "single item vs list" case) — this is the seed of the 1D-Array recipe below.
- Failure modes: Forgetting to disable the original geometry's preview leaves the un-moved original and the moved copy visually overlapping.
- Source: [STATED, AAD pt.1 p.66].

### Rotate About a Derived Face-Plane vs. an Explicit Axis
- Purpose: Rotate geometry about a plane derived from its own face (not a world axis), and understand the degrees→radians requirement.
- Difficulty: intermediate
- Chain:
  ```
  === Section: Rotate about a self-derived tangent plane ===
  Geo -> DeBrep(Deconstruct Brep).B -> DeBrep.F {faces list}
  DeBrep.F -> Item.L ; Slider[Index] -> Item.i -> Item.i {one face}
  Item.i -> EvalSrf.S ; MDSlider[0.5,0.5] -> EvalSrf.uv -> EvalSrf.N -> Pl(Plane Normal).Z
  EvalSrf.P -> Pl.O -> Pl.P -> Rotate.P
  Geo -> Rotate.G ; Slider[Degrees] -> Rad.D -> Rad.R -> Rotate.A -> Rotate.G {rotated geometry}
  -- equivalent via an explicit axis line instead of a plane:
  EvalSrf.P -> Line(SDL).S ; EvalSrf.N -> Line.D -> Line.L -> RotAx.X
  Geo -> RotAx.G ; Rad.R -> RotAx.A -> RotAx.G
  ```
- Tree handling notes: Flat/single item; generalizes to N floors by feeding a LIST of angles from a Series into Rotate Axis's A-input while reusing one shared axis Line — this is the "twisted tower" pattern (progressive rotation, relative angle = twist angle / (floor count − 1)).
- Failure modes: Rotate and Rotate Axis both require angle in radians — a Degrees slider must always be piped through Radians first.
- Source: [STATED, AAD pt.3 p.189-193 (single rotation + twisted-tower variant)].

### Scale — Uniform and Per-Object Variable (vase/barrel forms)
- Purpose: Scale one object about a chosen center, or scale a stack of objects by a different factor each — the basis of vase/barrel/hourglass silhouettes.
- Difficulty: basic → intermediate
- Chain:
  ```
  === Section: Uniform scale ===
  Geo -> Scale.G ; Pt -> Scale.C ; Slider[Factor, 0<F, never 0] -> Scale.F -> Scale.G {flat}
  === Section: Per-object variable scale (linear) ===
  Geo(list of N boxes) -> Volume.G -> Volume.C {N centroids} -> Scale.C ; Geo -> Scale.G
  Series[Start,Step,Count=N] -> Series.S -> Scale.F -> Scale.G {N boxes, each its own factor}
  === Section: Symmetric/parabolic scale (equation or Graph Mapper) ===
  Dom[1,N] -> Range.D ; (ListLength-1) -> Range.N -> Range.R {x-values}
  Panel["-(1/10)*x^2+x+1"] -> Eval.F ; Range.R -> Eval.x -> Eval.r -> Scale.F  {symmetric factor list -> barrel form}
  -- Graph Mapper variant replaces Eval: Range.R -> GraphMapper[Parabola/Sine/custom] -> Scale.F
  ```
- Tree handling notes: One base geometry + a LIST of transform parameters (T/F/A) is the book's standard "single item vs list" broadcast pattern for stacking/scaling — not narrated explicitly as a tree rule by the source, but shown repeatedly across all three variants.
- Failure modes: Scale's F must be a positive number and can never be exactly 0 ("a null scale factor is a mathematical error"); Range generates N+1 values for N steps, so matching one factor per existing object requires subtracting 1 from the object count first (via A−B) before feeding Range.N; Graph Mapper has two independent domains (input A, output B) that must both be set — forgetting to match domain A to the real upstream range silently mismaps.
- Source: [STATED, AAD pt.3 p.196-202].

### Orient — Combined Translate+Rotate to Reposition Geometry
- Purpose: Move geometry from an arbitrary "as generated" plane to a target plane in one step, replacing separate Move+Rotate chains (e.g. flattening curved ribs onto XY for fabrication layout).
- Difficulty: intermediate
- Chain:
  ```
  === Section: Orient — flattening ribs onto XY, list version ===
  Srf(list of ribs) -> EvalSrf.S ; MDSlider[0.5,0.5] -> EvalSrf.uv -> EvalSrf.N -> Neg.x -> Pl.Z ; EvalSrf.P -> Pl.O -> Pl.P -> Orient.A {list of initial planes, one per rib}
  Slider[Step] -> Series.N ; Srf -> Lng.L -> Series.C -> Series.S -> Y(UnitY).F -> Y.V -> Move.T ; Pt -> Move.G -> Move.G -> XY.O -> XY.P -> Orient.B {evenly spaced target planes}
  Srf -> Orient.G -> Orient.G {list of ribs, each flattened and laid out in a row} {list, N ribs, item-wise matched}
  ```
- Tree handling notes: Both the initial-plane list (A) and target-plane list (B) must be the same length and index-matched to the geometry list — standard list matching, no grafting required.
- Failure modes: None stated beyond the general Orient A/B plane-order requirement (swap of A/B reverses which plane is "from" vs "to").
- Source: [STATED, AAD pt.3 p.193-194].

### Container Components & Data-Source Precedence
- Purpose: Understand the three ways data enters a GH definition (internally-set, Rhino-referenced, externally wired) and which wins when more than one is present.
- Difficulty: basic
- Chain: n/a — this is a concept/rule pattern rather than a wired chain, reproduced here because both books teach it as a load-bearing workflow rule that governs every other recipe.
- Tree handling notes: n/a.
- Failure modes: Externally supplied (wired) data ALWAYS overrides internally-set or Rhino-referenced values on the same parameter — a frequent silent-confusion source when a value was previously set locally and a new wire is later added; referenced Rhino geometry is lost if the Rhino file isn't saved alongside the .gh file; the standard "Point" container and the standard "Construct Point" component both display as "Pt" on canvas but are functionally different (one stores/references, one computes from X/Y/Z).
- Source: [STATED, AAD pt.1 p.49-52] merged with [STATED, Essential pt.1 p.12-13].

### Curve-Aligned Circles → Loft (variable-thickness pipe / ribbed surface)
- Purpose: Build a tube or ribbed freeform surface by placing oriented circles (or arcs) along a curve's division points and lofting through them.
- Difficulty: intermediate
- Chain:
  ```
  === Section: Variable-thickness pipe (Essential 2_5_1) ===
  Line -> Random(domain, N, seed).R = "radii list"
  Line -> Random#2(domain, N).R -> Sort(ascending).K = "sorted parameters"  {MUST sort before evaluating, else Loft twists}
  Line -> Eval.C ; sorted parameters -> Eval.t -> Eval.P (centers), Eval.T (tangents/normals)
  Eval.P -> Circle(point+normal variant).C ; Eval.T -> Circle.N ; radii list -> Circle.R -> Circle.C {list of circles}
  Circle.C -> Loft.C -> Loft.L {flat, variable-thickness pipe surface}
  === Section: Ribbed surface via Arc3Pt (AAD 2.2) ===
  Crv1 -> Divide1.C ; Crv2 -> Divide2.C {same Count slider} -> Divide1.P, Divide2.P {matched point pairs}
  Divide1.P -> Ln.A ; Divide2.P -> Ln.B -> Ln.L {connecting lines} -> [Point On Curve, t=0.5] -> midpoints
  midpoints -> Move.G ; Slider[Factor] -> Z.F -> Z.V -> Move.T -> Move.G {midpoints offset in Z}
  Divide1.P -> Arc.A ; Move.G -> Arc.B ; Divide2.P -> Arc.C -> Arc.A {bulging ribs}
  Arc.A -> Loft.C -> Loft.L {ribbed/fluted freeform surface}
  ```
- Tree handling notes: Both variants stay flat/single-branch; correctness depends entirely on ORDER (sorted parameters, or matched division counts across two curves), not on tree depth.
- Failure modes: Randomly-generated curve parameters MUST be sorted before evaluating+lofting in sequence, or the resulting cross-sections are visited out of order, producing a twisted/self-intersecting surface; Loft can produce a non-smooth/faceted surface with too few sections unless Loft Options' Rebuild is used.
- Source: [MERGED — same "curve division + normals → cross-section → loft" pattern] [STATED, Essential pt.1 p.44-47 (2_5_1)] and [STATED, AAD pt.1 p.96-99].

---

## 2. List Operations

### List Item vs Cull Index (keep vs. remove by index)
- Purpose: Extract a specific item (List Item) or discard specific items while keeping the rest (Cull Index) — the two are functional opposites that share near-identical wiring, a frequent confusion.
- Difficulty: basic
- Chain:
  ```
  === Section: List Item ===
  Divide.P -> ListItem.L {flat} ; Slider[Index] -> Item.i -> Item.i {single item, or a filtered sub-list if i is itself a list of indices}
  === Section: Cull Index ===
  Divide.P -> CullIndex(Cull i).L {flat, N items} ; Slider[Indices] -> Culli.I -> Culli.L {N-minus-culled-count items}
  ```
- Tree handling notes: Flat both ways; List Item's i-input branches its own behavior — one index in → one datum out, a LIST of indices in → a filtered sub-list out.
- Failure modes: Cull Index is explicitly "the reverse function" of List Item — mixing them up (expecting keep-behavior from Cull Index) silently produces the opposite result.
- Source: [STATED, AAD pt.1 p.72-77] merged with [STATED, Essential pt.1 p.19, 37].

### Cull Pattern — Repeating Boolean Mask (+ Invert)
- Purpose: Keep/remove list items via a short True/False pattern that automatically tiles across the whole list, regardless of list length.
- Difficulty: basic
- Chain:
  ```
  === Section: Cull Pattern, 2-value and 3-value masks ===
  BooleanToggle[True], BooleanToggle[False] -> Merge.D1,D2 -> Merge.R {2-item pattern}
  Divide.P -> Cull.L {11 items} ; Merge.R -> Cull.P -> Cull.L {tiles True/False across all 11: keeps 0,2,4,6,8,10}
  -- 3-value pattern (True,True,False) tiled the same way keeps a denser 2-of-3 subset
  -- Invert: the same pattern list can select the COMPLEMENT subset via Cull Pattern's own Invert toggle, avoiding a second hand-authored pattern
  ```
- Tree handling notes: Pattern length need not match data length — GH tiles/repeats it automatically end-to-end.
- Failure modes: None additional beyond standard tiling surprises if the pattern length isn't a clean divisor of intent (e.g. expecting exactly "every other" but supplying a 3-item pattern).
- Source: [STATED, AAD pt.1 p.78-80] merged with [STATED, Essential pt.1 p.19, 38, 50 (Invert)].

### Dispatch — One-Step Split into Kept/Discarded
- Purpose: Split one list into a True-subset and a False-subset in a single component, instead of two inverted Cull Pattern calls.
- Difficulty: basic
- Chain:
  ```
  === Section: Dispatch replacing double Cull ===
  Crv -> DArc.A -> R -> Eval.x ; Panel["x>8"] -> Eval.F -> Eval.r -> Dispatch.P
  Crv -> Dispatch.L -> Dispatch.A {True subset}, Dispatch.B {False subset}
  ```
- Tree handling notes: Both outputs stay flat, same branch structure as input, each holding a complementary subset — critically, unlike Cull Pattern, Dispatch never discards data; both halves remain available downstream.
- Failure modes: Choosing Cull Pattern when both subsets are actually needed later forces rebuilding the discarded half from scratch — Dispatch avoids this by design.
- Source: [STATED, AAD pt.2 p.107-109] merged with [STATED, Essential pt.1 p.18, 38].

### Shift List with Wrap (rotate/offset connectivity)
- Purpose: Re-index a list by an integer offset, with or without wrap-around, to build cross-connections between two curves/lists (e.g. a diagrid zig-zag).
- Difficulty: basic
- Chain:
  ```
  === Section: Shift for diagrid zig-zag ===
  Curve01.Divide.P -> Line.A {flat, 11 items}
  Curve02.Divide.P -> Shift.L ; Slider[Shift,1] -> Shift.S ; Toggle[True] -> Shift.W -> Shift.L {offset by 1, wrapped}
  Shift.L -> Line.B -> Line.L {11 lines, point i on Curve01 to point i+1 on Curve02, incl. one wrap-around connector}
  ```
- Tree handling notes: Flat; W=true re-appends items that fall off one end onto the other (list length unchanged — a rotating shift); W=false discards them instead (list shortens by |S|).
- Failure modes: Toggling W changes the OUTPUT LENGTH, not just item order — a detail that can silently break a downstream component expecting a fixed count; to remove an unwanted wrap-around connector specifically, disable its preview and Cull Index the offending line by position rather than un-wrapping the whole shift.
- Source: [STATED, AAD pt.1 p.80-82, p.195-196 (diagrid)] merged with [STATED, Essential pt.1 p.38-40].

### Split List — Break One List into Two by Index
- Purpose: Divide a single list into a "before" and "after" segment at a chosen index.
- Difficulty: basic
- Chain:
  ```
  === Section: Split List, differential Extrude ===
  Geo(11 circles) -> Split.L ; Slider[Index,3] -> Split.i -> Split.A {indices 0-2}, Split.B {indices 3-10}
  Slider[200]->UnitZ.F->UnitZ.V->Extr.D ; Split.A -> Extr.B -> Extr.E {3 tall cylinders}
  Slider[100]->UnitZ.F->UnitZ.V->Extr.D ; Split.B -> Extr.B -> Extr.E {8 short cylinders}
  ```
- Tree handling notes: Flat; result is {branches: A=3 items, B=8 items} — the two outputs are independent lists, not a tree.
- Failure modes: Setting the split Index equal to the list's total length makes A = the entire list and B = empty — a boundary case worth checking in parametric definitions where the index is itself variable.
- Source: [STATED, AAD pt.2 p.83-84].

### Sort List + Reverse List
- Purpose: Order a numeric (or key-driven) list ascending/descending, or flip item order outright.
- Difficulty: basic
- Chain:
  ```
  Panel[Num list] -> Sort.K -> Sort.K(out) {ascending}
  Sort.K(out) -> Reverse(Rev).L -> Panel[descending]
  ```
- Tree handling notes: Flat; Reverse is also available as a right-click "Reverse" option directly on any input slot without a separate component.
- Failure modes: None specific beyond standard key/parallel-list mismatch if a second "carried" list (e.g. sorting curves by length) isn't the same length as the key list.
- Source: [STATED, AAD pt.2 p.85-86] merged with [STATED, Essential pt.1 p.19].

### Weave — Interleave Multiple Streams Back into One Order
- Purpose: Recombine two or more separately filtered/culled subsets into a single interleaved sequence (the inverse of Cull Pattern/Dispatch).
- Difficulty: intermediate
- Chain:
  ```
  === Section: Truss "middle points" reconstruction ===
  Divide.P -> Cull1.L ; [False,True]->Cull1.P -> Cull1.L(out) = "Bottom points"
  Divide.P -> Cull2.L ; [True,False]->Cull2.P -> Cull2.L(out) = "Top points"
  Top points -> Move.G ; Slider[Height]->UnitZ.F->UnitZ.V->Move.T -> Move.G(out) {moved Top}
  Bottom points, Move.G(out) -> Weave.[0],[1] ; Pattern -> Weave.P -> Weave.W = "Middle points" {restored alternating order}
  ```
- Tree handling notes: Where Cull Pattern/Dispatch SPLIT one list, Weave does the opposite — it takes N separate streams and interleaves them per an index pattern into one list; used repeatedly to rebuild alternating top/bottom truss geometry and to interleave 3 corner-point sets into one triangle-per-branch tree (Essential's triangle/plate tutorials).
- Failure modes: The two (or more) streams being woven must already carry matching internal order — Essential's Zigzag tutorial explicitly notes that positive/negative split trees need their internal item order corrected (e.g. via Reverse) BEFORE weaving, not just correct membership.
- Source: [STATED, Essential pt.2 p.50, 92-101].

### Jitter — Randomize List Order
- Purpose: Randomly reorder a list's items (distinct from randomizing their values) — e.g. for chaotic linework.
- Difficulty: basic
- Chain:
  ```
  PointsA -> Jitter.L ; Slider[Jitter factor, Seed] -> Jitter.J,.S -> Jitter.V (scrambled order), Jitter.I (new index order)
  Jitter.V -> Line.A ; PointsB -> Line.B -> chaotic connective pattern
  ```
- Tree handling notes: Flat; output length unchanged, only order changes.
- Failure modes: None stated beyond the general reminder that a fixed Seed reproduces the identical "random" reorder.
- Source: [STATED, Essential pt.1 p.40].

### Subset — Extract a Contiguous Index Range
- Purpose: Select a contiguous window of a list by an index Domain, rather than a single index or a repeating pattern.
- Difficulty: basic
- Chain:
  ```
  Num[5 values] -> SubSet.L ; Panel[Domain "1 to 3"] -> SubSet.D -> SubSet.L(out) {3 items} , SubSet.I(out) {indices used: 1,2,3}
  ```
- Tree handling notes: Flat.
- Failure modes: None stated.
- Source: [STATED, Essential pt.1 p.38].

---

## 3. Data-Tree Manipulation & List Matching

### List/Data Matching — Longest, Shortest, Cross Reference
- Purpose: Understand and explicitly control how GH pairs items when two+ lists of different lengths feed the same component — the single most consequential "silent bug" source in both books.
- Difficulty: intermediate
- Chain:
  ```
  === Section: Three matching modes on the same inputs A=[1,2], B=[1,2,3,4,5] ===
  A,B -> Addition.A,.B (default/no forcing) -> R=[2,4,5,6,7]  -- "Long List": GH repeats A's LAST item (2) to match B's length
  A,B -> Long("Repeat Last").A,.B -> Addition -> R=[2,4,5,6,7]  -- explicit form of the default, same result
  A,B -> Short("Trim End").A,.B -> Addition -> R=[2,4]  -- both truncated to the SHORTER length (2); trailing B items discarded
  A,B -> CrossRef("Holistic").A,.B -> Addition -> R=[2,3,4,5,6, 3,4,5,6,7] {10 items = 2x5 cartesian product}
  ```
- Tree handling notes: Cross Reference generalizes to N inputs (A,B,C,...), output length = the PRODUCT of all input lengths; swapping which list is A vs B changes the RESULT ORDER (not the value set) — "order of input matters."
- Failure modes: GH's silent default ("Long List," repeat-the-shorter-list's-LAST-item) is easily confused with a naive expectation of cyclic tiling of the whole short list — the two give different, both plausible-looking results for the same raw inputs; Cross Reference's output grows multiplicatively and can explode combinatorially with even modestly long lists; feeding two same-length lists into a two-input component (e.g. two Divide Curve outputs into a Line) implicitly pairs by position and does NOT let you pick one arbitrary cross-pair.
- Source: [MERGED] [STATED, AAD pt.2 p.90-95 (Chunk 1, Data Matching / Cross Reference "Holistic")] and [STATED, Essential pt.1 p.41-43 (Figures 45-49, "2_4 List matching")].

### Cartesian-Product Grid via Cross Reference (2D/3D arrays, cube of points)
- Purpose: Turn two or three independent 1D sequences into a full 2D/3D grid (5×5 or 5×5×5 lattice, or a 6×6×6 cube of points) — the standard fix for the "diagonal instead of grid" data-matching pitfall.
- Difficulty: intermediate
- Chain:
  ```
  === Section: 2D grid via one Cross Reference (AAD) ===
  Series[0,2,5].S -> X.F -> X.V (5 X-vectors) ; Series[0,2,5].S -> Y.F -> Y.V (5 Y-vectors)
  Geo -> Move1.G ; X.V -> Move1.T -> Move1.G {5 cubes along X} {flat, 5 items}
  Move1.G -> CrossRef.A ; Y.V -> CrossRef.B -> CrossRef.A,B {25 items each, cartesian product}
  CrossRef.A -> Move2.G ; CrossRef.B -> Move2.T -> Move2.G {25 cubes = 5x5 grid} {flat, 25 items}
  === Section: 3D lattice, two chained Cross References ===
  (as above) -> Move2.G -> CrossRef2.A ; Z.V -> CrossRef2.B -> A,B {125 items each} -> Move3.G/.T -> Move3.G {5x5x5 lattice}
  === Section: N-way Cross Reference, cube of points (Essential) ===
  Panel[Num, 6 values 0-5] -> CrossRef.A, .B, .C {same list wired to all 3 inputs} -> A,B,C each 216 items (6^3)
  A,B,C -> ConstructPoint.X,.Y,.Z -> Pt.Pt {216-point 6x6x6 cube} {flat, single branch}
  ```
- Tree handling notes: Every stage stays FLAT (single branch) — the "grid" is a flat list whose length equals the product of the inputs; no grafting is used to build the grid, Cross Reference alone does the cartesian expansion.
- Failure modes: Skipping Cross Reference and instead wiring two independent N-length vector series directly into a two-stream component under default (Long List) matching yields only N outputs arranged DIAGONALLY, not the intended N×N grid — this exact pitfall and fix pair appears (and is explicitly narrated) in both source books.
- Source: [MERGED] [STATED, AAD pt.2 p.90-94 (Chunks: "Data Matching pitfall," "Cross Reference fix," "Cross Reference x2")] and [STATED, Essential pt.1 p.43-45 (2_4_1 "cube of points" tutorial)].

### Custom Cyclic-Repeat Matching (List Length + Repeat)
- Purpose: Force a short list to tile its WHOLE pattern cyclically (not just repeat its last item) to match a longer list's length, generically (without hardcoding the target length).
- Difficulty: intermediate
- Chain:
  ```
  === Section: Repeat Data / Repeat, generic-length pattern ===
  Slider[Data1],[Data2],[Data3] -> Merge.D1,D2,D3 -> Merge.R {short list, e.g. [3,4] or [2,6,1]}
  OtherList -> ListLength(Lng).L -> Panel[target length] {or: Geo -> Lng.L, generic — not hardcoded}
  Merge.R -> Repeat.D ; Lng.L -> Repeat.L -> Repeat.D(out) {short list CYCLICALLY tiled to target length, e.g. [1,2]->[1,2,1,2,1]}
  Repeat.D(out) -> Addition.A ; OtherList -> Addition.B -> R {differs from default Long-List result on the same raw inputs}
  ```
- Tree handling notes: Flat; the point of the recipe is that this differs structurally from GH's own default matching (which repeats only the LAST item), even though both are "valid-looking" ways to reconcile unequal lengths.
- Failure modes: Confusing "repeat the last item" (GH default / Long) with "repeat the whole pattern" (Repeat component) silently produces different, both plausible, results from identical raw inputs — the book stresses deliberately choosing which is intended; hardcoding a target length instead of deriving it via List Length breaks if input sizes later change.
- Source: [MERGED] [STATED, AAD pt.2 p.95, 99 (Repeat Data merge example; alternating rib heights, Figure 2.2)] and [STATED, Essential pt.1 p.43, 48 (Figure 50; "Custom list matching tutorial" 2_5_2)].

### Data-Structure-Dependent Execution (Mass Addition item/list/tree demo)
- Purpose: Internalize the foundational Grasshopper rule that identical values, organized differently (item / list / tree), make the SAME component produce structurally different results.
- Difficulty: intermediate
- Chain:
  ```
  === Section: Mass Addition on 3 structures of the same values ===
  Num[1] -> Panel {item, 1 branch x 1} -> MassAddition(MA).I -> R = 1  (identity)
  Num[1,2,3,4] -> Panel {list, 1 branch x 4} -> MA.I -> R = 10  (sum of the whole list)
  Num[grafted, 3 branches: [1,2,3,4]/[5,6,7]/[8,9]] -> Panel {tree} -> MA.I -> R = [10,18,17]  (one sum PER branch)
  ```
- Tree handling notes: Wire-display convention as a quick visual diagnostic: a single item draws as one solid line, a list as a double solid line, a tree as a double DASHED line — readable at a glance without opening a Panel.
- Failure modes: "It is essential to be fully aware of the data structure before using [a component]" — the same wiring pattern silently means something different depending on upstream tree shape.
- Source: [STATED, Essential pt.1 p.33-34].

### Grafting for Full Cross-Product Pairing
- Purpose: Convert a flat list into a tree with one item per branch, most often so two independently transformed streams can be paired per-branch downstream (e.g. before Merge+Loft, or before Mesh Colours).
- Difficulty: intermediate
- Chain:
  ```
  Num(flat, N=5) -> Graft.T -> Graft.T(out) {grafted: 5 branches x 1 item each}
  -- variable-depth input still grafts one new terminal branch per LEAF item regardless of starting depth:
  Num(variable-depth tree, 4 branches) -> Graft.T -> Graft.T(out) {8 branches x 1, one new deepest branch per leaf}
  -- canonical paired-use case (chapter-5 grafting rule):
  OriginalEdges -> Graft1.T -> T {grafted} ; ScaledEdges -> Graft2.T -> T {grafted}
  Graft1.T, Graft2.T -> Merge.D1,D2 -> Merge.R -> Loft.C {pairs original-to-scaled per branch, not a flat mismatched list}
  ```
- Tree handling notes: Grafting is explicitly described as "unintuitive" because it deliberately increases structural complexity, but it is the mechanism that forces full one-to-one pairing (as opposed to Cross Reference's all-to-all pairing).
- Failure modes: Skipping the graft-before-merge step lets Merge/Loft see flat/mismatched lists instead of one-item-per-branch pairs, producing wrong geometry rather than an error.
- Source: [STATED, Essential pt.2 p.69-70 (Fig.68)] merged with [STATED, AAD pt.6 p.452, 458 ("the two data flows are required to be grafted before they are merged")].

### Flattening a Tree to a Single List
- Purpose: Collapse any tree (any depth, any branch count) into one branch, in deterministic lowest-path-first order — needed whenever a downstream component (e.g. Surface From Points, or a third-party mesh exporter) requires one simple ordered list.
- Difficulty: basic
- Chain:
  ```
  Num(tree, 5 branches x 1) -> Flatten.T -> Flatten.T(out) {flat: 1 branch x 5}
  -- variable-depth case: Num(4 branches x 2) -> Flatten.T -> Flatten.T(out) {flat: 1 branch x 8, ascending path order}
  ```
- Tree handling notes: Order is always "branches read starting with the lowest-index trunk," items concatenated sequentially — deterministic and independent of nesting depth.
- Failure modes: Feeding un-flattened (tree-structured) data into a component that expects a single list can silently truncate to just the LAST branch rather than erroring (documented concretely for Ecotect mesh export: Mesh Explode's per-mesh branches must be Flatten-ed before EcoMeshExport, or only the last branch's faces get exported).
- Source: [STATED, Essential pt.2 p.70 (Fig.70)] merged with [STATED, AAD pt.3 p.220-221 (Flatten Tree component)] and [STATED, AAD pt.6 p.453-454 (Flatten-before-Ecotect-export gotcha)].

### Entwine vs Merge (parallel branches vs. concatenation)
- Purpose: Distinguish "combine N lists into N separate branches" (Entwine) from "combine N lists into one big flat list" (Merge) — two similar-looking components that solve different problems.
- Difficulty: basic
- Chain:
  ```
  FirstList(4), SecondList(4) -> Entwine.[0;0],[0;1] -> Entwine.R {branches: 2 x 4, values kept separate}
  FirstList(4), SecondList(4) -> Merge.D1,D2 -> Merge.R {flat: 1 branch x 8, simple concatenation}
  ```
- Tree handling notes: Entwine creates a NEW tree with one branch per input stream and no value combination; Merge concatenates everything, losing the separation between original inputs entirely.
- Failure modes: Choosing Merge when downstream logic needs the streams kept separate (or vice versa) is a common structural mismatch — check whether the goal is "keep apart" or "join into one."
- Source: [STATED, Essential pt.2 p.71].

### Flip Matrix (Transpose a Tree)
- Purpose: Regroup elements that share the same index across branches into new branches — a matrix transpose for trees, used to build cross-connections between parallel rows (e.g. purlins linking parallel trusses).
- Difficulty: intermediate
- Chain:
  ```
  Num(tree: 2 branches x 4 items) -> Flip.D -> Flip.D(out) {branches: 4 x 2, transposed}
  -- unequal branch length: Num(2 branches, N=4 and N=2) -> Flip.D -> Flip.D(out) {4 branches, each N=2, missing slots padded with <null>}
  -- variable branch DEPTH (not just length): Flip errors entirely — "there is no logical solution to flip"
  ```
- Tree handling notes: Flip requires uniform branch DEPTH (nesting level) to run at all; it tolerates uniform-depth-but-unequal-LENGTH branches by null-padding.
- Failure modes: `<null>` placeholders inserted for uneven branches will break most downstream math/geometry components unless explicitly cleaned (Clean Tree, "Remove nulls") first; on a mixed-depth tree Flip shows a hard error (red component), not a degraded result.
- Source: [STATED, Essential pt.2 p.71-72 (Figs.72-74)].

### Simplify / Clean / Trim / Explode Tree (cleanup family)
- Purpose: Remove accumulated structural cruft (redundant nesting, nulls, empty branches) after chaining several tree-generating operations.
- Difficulty: intermediate
- Chain:
  ```
  Num(tree, redundant nesting {0;0}...{0;4}) -> Simplify.T -> Simplify.T(out) {simplified to {0}...{4}, same item counts}
  ```
- Tree handling notes: Simplify Tree removes superfluous leading/trailing zero levels WITHOUT changing item counts or values; Clean Tree removes null elements; Trim Tree removes empty branches; Explode Tree ("BANG!") splits every branch out into its own separate output, individually addressable (used e.g. to isolate 8 box-corner points for selective Move before Twisted Box).
- Failure modes: "Complex data structures are hard to match" — chaining many tree operations without periodic Simplify accumulates nesting that silently breaks later matching; Path Mapper is explicitly the LAST resort ("least intuitive... can cause a loss of data") when Flatten/Graft/Flip/Split/Simplify are insufficient.
- Source: [STATED, Essential pt.2 p.72 (Simplify)] merged with [STATED, AAD pt.4 p.328 (Graft + Explode Tree "BANG!" to isolate Bounding Box corners for Box Morph)].

### Branch + Tree Statistics — Dynamic Path/Branch Extraction
- Purpose: Extract a specific branch or item by its path address, either hardcoded or dynamically discovered (so the definition still works if branch count changes).
- Difficulty: intermediate
- Chain:
  ```
  === Hardcoded path ===
  Num(tree) -> Branch.T ; Panel["{0;0;0}"] -> Branch.P -> Branch.B {branch extracted, flat}
  === Dynamic path via Tree Statistics ===
  Num(tree) -> TStat.T -> TStat.P (all paths), TStat.L (item counts per branch), TStat.C (branch count)
  TStat.P -> Item[i=0].L -> Branch1.P {first branch's own path} ; Item[i=-1] (wrap) -> Branch2.P {last branch}
  Num -> Branch1.T, Branch2.T -> Branch1.B, Branch2.B -> Addition.A,.B -> R {"add first + last branch," no hardcoded path text}
  ```
- Tree handling notes: TStat.P returns the tree's own path list as data, letting List Item (with negative/wrap indexing for "last") select a branch address dynamically instead of typing a literal path string.
- Failure modes: Path numbering is a convention chosen by whichever component generated the tree — branches don't have to start at 0 or be contiguous, so hardcoded path strings are fragile versus TStat-driven addressing.
- Source: [STATED, Essential pt.2 p.65-67].

### Relative Item — Offset-Mask Addressing for Diagonal/Grid Connectivity
- Purpose: Connect an item at one grid address to another item at a fixed relative offset (branch±N, index±M) in one operation — e.g. diagonal neighbors in a point grid, or corresponding points across two different grids.
- Difficulty: advanced
- Chain:
  ```
  === Section: 3_6_1 Relative items — diagonal grid connectivity ===
  SqGrid[Branch spans, Element spans] -> SqGrid.P {branches: M x N point grid}
  SqGrid.P -> RelItem.T ; Panel["{+1}[+1]"] -> RelItem.O -> RelItem.A {base addresses}, RelItem.B {diagonal +1 branch / +1 index neighbors}
  RelItem.A -> Ln.A ; RelItem.B -> Ln.B -> Ln.L {diagonal connector lines}
  === Section: Relative Item between two DIFFERENT trees ===
  Tree1, Tree2(e.g. a Move-offset duplicate) -> RelItem2.T(one tree per slot) ; Panel["{-1}[0]"] -> RelItem2.O -> A,B -> Ln.A/.B -> L
  ```
- Tree handling notes: Offset-string grammar is `{branch offset}[index offset]`. Relative Item internally builds TWO new correlated output trees (A, B) whose corresponding branches/items are exactly the pairs the offset describes; addresses that would fall outside the original tree's bounds are silently dropped, so output trees are typically SMALLER than the input (e.g. a 4×3 grid reduces to matched 3×2 A/B trees under a `{+1}[+1]` diagonal offset, since the last branch/index has no +1 neighbor).
- Failure modes: The output-tree-shrinkage behavior at grid edges is easy to miss if not explicitly checked; building a full truss connectivity pattern (bottom/top chords + diagonal webs) requires composing Cull Pattern (split into interleaved sub-grids) with two or more Relative Item passes using complementary offset masks.
- Source: [MERGED — diagrid/diagonal-connectivity family, see also the surface-based diagrid recipe in §5] [STATED, Essential pt.2 p.76-81 (3_6_1, 3_6_1_A, 3_6_1_B)].

### Split Tree (Mask Grammar) + Combine — Lossless Subset Transform & Recombine
- Purpose: Select an arbitrary subset of a tree by a rich path/index mask, transform only that subset, then losslessly reassemble the full tree.
- Difficulty: advanced
- Chain:
  ```
  === Section: 3_6_2 Split Tree — subset transform and recombine ===
  SqGrid.P {branches: 6 x 10} -> Split.D ; Panel["{*}[(1,2,3) or (7,8,9)]"] -> Split.M -> Split.P (Positive), Split.N (Negative)
  Split.P -> Move.G {transform ONLY the selected subset} -> Move.G(out)
  Move.G(out), Split.N -> Combine.[0],[1] -> Combine.R {recombined full tree} -> PLine.V -> PLine.Pl
  ```
- Tree handling notes: Mask grammar: `{ ; ; }` = branch mask, `[ ]` = item mask (omit = select all), `*` = wildcard (any integers), `?` = any single integer, bare integer = exact match, `!` negates, `(a,b,c)` = one-of-list, `(a to b)` = inclusive range, `(a,b,...)` = open arithmetic sequence (optionally bounded `...,n`), boolean `and`/`or` combine rules. BOTH Split outputs retain the exact original branch paths and item counts — excluded elements are simply absent/null in that output — which is what makes the subsequent Combine lossless.
- Failure modes: A negated infinite sequence like `!(3,5,...)` also matches everything to the LEFT of the sequence start (the sequence does not extend leftward) — an easy source of an unintentionally broader selection than assumed; the source's own worked example for a combined `or` mask has a stated discrepancy between the mask literal integers and its prose description, transcribed as printed rather than silently corrected.
- Source: [STATED, Essential pt.2 p.81-86 (3_6_2, 3_6_2_A, 3_6_2_B)].

### Path Mapper — Source→Target Path Remapping
- Purpose: Author an arbitrary path transformation (regroup, promote item-index into path, or both at once) when Graft/Flatten/Flip/Split cannot express the needed restructuring.
- Difficulty: advanced
- Chain:
  ```
  === Section: Partitions — group corresponding branches across two trees, then expose items as branches ===
  Tree(10 branches, 2 sources x 5 branches) -> PathMapper1[{A;B;C} -> {A;C;B}] -> PathMapper1(out) {still 10 branches, reordered so same-branch/different-tree pairs sit adjacently}
  PathMapper1(out) -> PathMapper2[{A;B;C}(i) -> {A;B;i}(C)] -> PathMapper2(out) {55 branches x 2, one branch per corresponding point-pair} -> PLine.V -> PLine.Pl
  -- combined single-step equivalent: Tree -> PathMapper[{A;B;C}(i) -> {A;C;i}(B)] -> PLine  ("not always possible, but can save processing time")
  === Built-in presets (right-click) ===
  Num(10 branches x 11) -> PathMapper[Null Mapping] {unchanged} | [Flatten Mapping] {1 branch x 110} | [Graft Mapping] {110 branches x 1} | [Reverse Mapping] {unchanged structure, item order reversed per branch} | [Renumber Mapping] {flattens nested path depth to sequential top-level numbers, item counts unchanged}
  ```
- Tree handling notes: Named constants available inside target-path expressions: `item_count`, `path_count`, `path_index`. Source path is fixed (read from input, uneditable); only the target expression is authored.
- Failure modes: Explicitly flagged by the source as "perhaps the least intuitive to use and can cause a loss of data" — reach for it only when simpler tools (Graft/Flatten/Flip/Split) cannot express the needed restructuring; combining two mapping operations into one expression is possible and saves overhead, but "combining is not always possible," with no further criteria given for when it fails.
- Source: [STATED, Essential pt.2 p.86-91 (3_6_3, 3_6_3_A)].

### Deconstruct-Point → Entwine (rebuild a tree from parallel coordinate lists)
- Purpose: Decompose a point list into three parallel coordinate lists, then reassemble them as a labeled 3-branch tree (or vice versa) — the standard "de-interleave / re-interleave" pattern for XYZ data.
- Difficulty: intermediate
- Chain:
  ```
  Pt(list of 5 points) -> pDecon.P {flat, 1 branch} -> pDecon.X, .Y, .Z {each a flat list of 5 numbers}
  pDecon.X -> Entwine.[0;0] ; pDecon.Y -> Entwine.[0;1] ; pDecon.Z -> Entwine.[0;2] -> Entwine.R {branches: 3 x 5}
  ```
- Tree handling notes: Entwine here is used specifically to LABEL which branch is X/Y/Z, as opposed to Merge, which would irreversibly concatenate the three coordinate streams into one flat list.
- Failure modes: None specific beyond the general Entwine-vs-Merge confusion documented above.
- Source: [STATED, Essential pt.2 p.60].

### Allocate N (third-party) — Flat List into Fixed-Size Branches
- Purpose: Split a flat list into equal-size branches (e.g. group a flat point list into columns) using the third-party Tree8 plug-in.
- Difficulty: intermediate
- Chain:
  ```
  === Section: Split point grid into sorted column branches ===
  Pt -> pDecon.P ; pDecon.Y -> Sort.K ; Pt -> Sort.A {flat list, N points}
  Sort.A -> AllocN.Data ; Slider["Number of Items", 6] -> AllocN.N -> AllocN.Data {grafted: branches 4 x 6, paths {0;0}..{0;3}}
  -- each branch (column) initially has RANDOMLY ordered rows; a second pDecon+Sort re-sorts WITHIN each branch by Y:
  AllocN.Data -> pDecon2.P ; pDecon2.Y -> Sort2.K ; AllocN.Data -> Sort2.A -> Sort2.A(out) {same 4x6 branch structure, rows now ordered}
  Sort2.A(out) -> SrfGrid.P {P input set to flatten mode} ; Slider["U Count",4] -> SrfGrid.U -> SrfGrid.S {4x6 grid surface}
  ```
- Tree handling notes: Sort applied AFTER a tree-producing operation (AllocN) operates PER-BRANCH automatically — each of the 4 columns is independently re-sorted by its own Y values, branch structure preserved.
- Failure modes: Allocate N is a third-party component (Tree8 plug-in by Jissi Choi, part of the STRAUTO toolset) — a definition using it will not open correctly without that plug-in installed; Surface From Points additionally requires its point input explicitly set to "flatten" mode to correctly interpret the tree as a row-by-row grid.
- Source: [STATED, AAD pt.4 p.251-252 (Fig 5.5-5.6)].

---

## 4. Attractor Patterns

### Point-Attractor Distance-Remap Scaling (canonical attractor recipe)
- Purpose: Modify geometry (here, scale) based on distance from a point — the foundational "measure → remap → apply" attractor pipeline reused by every other recipe in this section.
- Difficulty: intermediate
- Chain:
  ```
  === Section: Point-attractor circle-grid scaling ===
  Slider[R] -> Cir.R -> Cir.C {unit circle} -> [2D array via Series+Move+CrossRef, see §3] -> grid.G {e.g. 20x20 circles} {flat}
  grid.G -> Area.G -> Area.C {centroid per circle}
  Pt(attractor) -> Dist.A ; Area.C -> Dist.B -> Dist.D {distances}
  Dist.D -> Bnd.N -> Bnd.I {source domain, auto min/max}
  Slider[Domain start=0.010, end=0.8] -> Dom.I {target domain, deliberately not exactly 0}
  Dist.D -> ReMap.V ; Bnd.I -> ReMap.S ; Dom.I -> ReMap.T -> ReMap.R {per-circle scale factors}
  grid.G -> Scale.G ; Area.C -> Scale.C ; ReMap.R -> Scale.F -> Scale.G {scaled circles, radiating density gradient}
  ```
- Tree handling notes: Entirely flat — the attractor pipeline operates item-wise across the grid list, no grafting required; moving the attractor point live-updates the whole field.
- Failure modes: Using exactly 0 as a Remap target-domain endpoint yields a Scale factor of 0, which is invalid ("a scaling factor of zero would yield null results") — use a small nonzero value (e.g. 0.010) instead.
- Source: [STATED, AAD pt.2 p.112-114].

### Curve-Attractor Distance-Remap
- Purpose: Same pipeline as the point attractor, but measuring distance to a curve instead of a point, producing a banded/wavy field.
- Difficulty: intermediate
- Chain:
  ```
  Crv(attractor curve) -> CrvCP.C ; Area.C(centroids) -> CrvCP.P -> CrvCP.D {distance to nearest point on curve}
  CrvCP.D -> Bnd.N -> Bnd.I ; Dom[0.010,0.8].I -> ReMap.S,.T ; CrvCP.D -> ReMap.V -> ReMap.R -> Scale.F -> Scale.G
  -- variant: drive Z-height instead of scale, feeding a surface —
  Dom[3,15].I -> ReMap.T ; ReMap.R -> Z.F -> Z.V -> Move.T ; centroids -> Move.G -> Move.G -> SrfGrid.P -> SrfGrid.S {undulating landscape}
  ```
- Tree handling notes: Identical flat structure to the point-attractor recipe; only the distance-measuring component changes (Curve Closest Point instead of Distance).
- Failure modes: Same zero-scale-factor caution as the point attractor.
- Source: [STATED, AAD pt.2 p.115-116].

### Multi-Attractor Summation with Domain Inversion
- Purpose: Combine two or more point attractors into one summed field, and invert which end of the effect (near vs. far) grows vs. shrinks by swapping the target domain's start/end.
- Difficulty: intermediate
- Chain:
  ```
  Point01, Point02 -> Dist1.A/.B, Dist2.A/.B (vs. centroids) -> Dist1.D, Dist2.D
  Dist1.D -> A+B.A ; Dist2.D -> A+B.B -> A+B.R {summed distance field}
  A+B.R -> Bnd.N -> Bnd.I {source domain}
  Variant A: Dom[0.01,0.82].I -> ReMap.T {near-attractor circles shrink most}
  Variant B: Dom[0.82,0.01].I -> ReMap.T {inverted: near-attractor circles grow largest}
  A+B.R -> ReMap.V ; Bnd.I -> ReMap.S -> ReMap.R -> Scale.F -> Scale.G
  ```
- Tree handling notes: Flat; Addition operates item-wise across the two distance lists before the single Remap/Scale pass.
- Failure modes: Same zero-scale-factor caution; swapping only the two domain endpoint VALUES (not the wiring) is sufficient to fully invert the effect — easy to forget when debugging "backwards" results.
- Source: [STATED, AAD pt.2 p.116-117].

### Limiting Attractor Operating Range (Division + Minimum clamp)
- Purpose: Confine an attractor's visible influence to roughly a fixed radius, beyond which all geometry receives the same capped, uniform transform.
- Difficulty: intermediate
- Chain:
  ```
  Pt(attractor) -> Dist.A ; centroids -> Dist.B -> Dist.D {raw distances}
  Slider[B=25.000] -> A/B.B ; Dist.D -> A/B.A -> A/B.R {distance normalized by a 25-unit "operating range"}
  Slider[B=0.800] -> Min.B ; A/B.R -> Min.A -> Min.R {any normalized distance > 0.8 clamped down to 0.8}
  grid.G -> Scale.G ; Area.C -> Scale.C ; Min.R -> Scale.F -> Scale.G
  ```
- Tree handling notes: Flat; Minimum here performs ELEMENT-WISE clamping of every value in a list against a scalar cap — not list-reduction to a single smallest value, an easy component-name misreading.
- Failure modes: Confusing Minimum's element-wise-clamp behavior with a "find the smallest value" reduction; beyond the operating-range radius, ALL affected geometry receives the identical capped factor rather than a continuously growing/shrinking one — a deliberate design trade-off, not a bug.
- Source: [STATED, AAD pt.2 p.117-118].

### Gradient-Colored Attractor-Field Visualization
- Purpose: Visualize a remapped attractor field (e.g. scale factor) directly as a color gradient on the geometry, for QA or presentation.
- Difficulty: basic
- Chain:
  ```
  ReMap.R -> Gradient.t ; Gradient[L0,L1 color stops] -> Preview.S
  Scale.G -> Boundary.E -> Boundary.S -> Preview.G {viewport shows dark-to-light coding of the scale factor per circle}
  ```
- Tree handling notes: Flat; Gradient is an input-type component mapping a 0-1 parameter to an interpolated color.
- Failure modes: None stated beyond ensuring the same per-item field (ReMap.R) feeds both the Gradient and the transform being visualized, or the coloring will not match the geometry.
- Source: [STATED, AAD pt.2 p.114-115].

### Image-Sampler-Driven Attractor Pattern (grayscale → scale/offset)
- Purpose: Use a raster image as a continuous 2D scalar field, sampling per-panel brightness to drive scale factors or offset heights — producing halftone-like or "fading relief" patterns.
- Difficulty: advanced
- Chain:
  ```
  === Section: Image-driven circle pattern ===
  Pt(grid) -> SrfCP.P ; Srf -> SrfCP.S -> SrfCP.uvP -> EvalSrf.uv ; Srf -> EvalSrf.S -> EvalSrf.P,.N
  Pt -> Circle.C ; EvalSrf.N -> Circle.N ; Slider[Radius] -> Circle.R -> Circle.C {uniform grid of circles}
  SrfCP.uvP -> ImageSampler[grayscale] -> intensities(0..1) -> Scale.F ; Circle.C -> Scale.G ; EvalSrf.P -> Scale.C -> Scale.G {circles scaled by local brightness}
  -- zero-intensity fix: ImageSampler -> Max.A ; Panel[0.1] -> Max.B -> Max.R -> Scale.F {floors pure-black-derived factors above 0}
  === Section: Fading 3D diamond-panel relief (per-panel pyramid apex offset) ===
  Diamond(LunchBox).Diamonds -> DeBrep.B -> DeBrep.V {corner pts} ; Srf -> Area.G -> Area.C {panel centroid}
  EvalSrf.N -> AxB.A ; ImageSampler[grayscale] -> AxB.B -> AxB.R {per-panel brightness-scaled offset} -> Move.T ; Area.C -> Move.G -> Move.G
  corner pts, offset apex -> [Merge, both grafted per panel] -> Del(Delaunay Mesh).P ; per-panel Plane Normal -> Del.Pl {grafted to match}
  ```
- Tree handling notes: The circle-grid variant stays flat; the diamond-relief variant requires BOTH the corner-point stream and the offset-apex stream to be grafted per panel before Merge, and the per-panel Plane Normal must also be grafted to match, so Delaunay Mesh produces one correctly-oriented pyramid per branch/panel.
- Failure modes: Images with pure-black areas return intensity 0, an invalid Scale factor — floor with Maximum against a small nonzero value; because each panel sits in a different local plane, using one constant GLOBAL offset direction (instead of each panel's own local surface normal) produces visibly mis-oriented pyramids.
- Source: [MERGED — same Image-Sampler-as-scalar-field technique reused twice within AAD] [STATED, AAD pt.3 p.203-206] and [STATED, AAD pt.4 p.288-290].

---

## 5. Grids & Paneling

### 1D Array via Series + Move
- Purpose: Build an evenly (or unevenly) spaced row of copies along one axis — the seed pattern behind every grid/lattice recipe below.
- Difficulty: basic
- Chain:
  ```
  Slider[Start=0] -> Series.S ; Slider[Step=2] -> Series.N ; Slider[Count=5] -> Series.C -> Series.S {0,2,4,6,8} {flat}
  Series.S -> UnitX.F -> UnitX.V {5 translation vectors}
  Geo -> Move.G ; UnitX.V -> Move.T -> Move.G {5 copies along X} {flat, 5 items}
  ```
- Tree handling notes: Single geometry + a LIST of vectors broadcasts via default list matching to N copies — flat throughout.
- Failure modes: A Start value of exactly 0 makes the first copy overlap the original (first vector is the zero vector) — easy to mistake for a bug when comparing renders.
- Source: [STATED, AAD pt.1 p.88-90].

### Diagonal Grid / Diagrid Connectivity — Three Methods
- Purpose: Build a diagonal structural grid (diagrid), by whichever mechanism fits the source geometry: two curves + Shift List, a flat point grid + Relative Item, or a subdivided surface + corner-vertex extraction + Project.
- Difficulty: advanced
- Chain:
  ```
  === Method 1 — two curves, Shift List zig-zag (2D) ===
  Curve01.Divide.P -> Line.A {flat, 11 items}
  Curve02.Divide.P -> Shift.L ; Slider[Shift,1] -> Shift.S ; Toggle[True] -> Shift.W -> Shift.L -> Line.B -> Line.L {zig-zag diagonal connectors}
  === Method 2 — flat point grid, Relative Item offset mask ===
  SqGrid.P -> RelItem.T ; Panel["{+1}[+1]"] -> RelItem.O -> RelItem.A, RelItem.B -> Ln.A/.B -> Ln.L {diagonal connector lines}
  === Method 3 — subdivided surface, corner-vertex diagonals + Project ===
  Srf -> Divide(Divide Domain²).I ; Slider[U,V] -> Divide.U,.V -> Divide.S
  Srf -> SubSrf(Isotrim).S ; Divide.S -> SubSrf.D -> SubSrf.S {N sub-surfaces}
  SubSrf.S -> DeBrep.B -> DeBrep.V {V0..V3 per sub-surface, grouped}
  DeBrep.V -> 4x Item[i=0..3] {"vertex slot k of every sub-surface" as one flat parallel list}
  Item(V0) -> Ln1.A ; Item(V1) -> Ln1.B -> Ln1.L {diagonal V0-V1, one per sub-surface}
  Item(V1) -> Ln2.A ; Item(V3) -> Ln2.B -> Ln2.L {diagonal V1-V3}
  Ln1.L, Ln2.L -> Project.C ; Srf -> Project.B -> Project.C {snapped onto the true curved surface}
  ```
- Tree handling notes: Methods 1 and 2 stay flat/list-based (no branch nesting). Method 3's key trick is running Deconstruct Brep + 4× List Item on the ENTIRE sub-surface list at once (not on a single Item-selected piece) — this "decompose then re-index by position" idiom is what lets a diagrid recipe validated on one sub-surface scale to the whole surface unchanged.
- Failure modes: Method 3's diagrid only touches the TRUE curved surface at sub-surface corners — everywhere else it floats off the surface unless every sub-surface happens to be planar; Project is required afterward for true surface-coincidence. Method 2's Relative Item shrinks the output tree at grid edges (see the Relative Item recipe in §3). Method 1's wrap-around connector (index N back to index 0) may need to be explicitly Cull-Index'd out if a closed loop isn't wanted.
- Source: [MERGED — same design pattern, three distinct GH mechanisms] [STATED, AAD pt.1 p.81-82,195-196 (Method 1)], [STATED, Essential pt.2 p.76-81 (Method 2, Relative Item)], and [STATED, AAD pt.3 p.155-158 (Method 3, "Diagrid generation logic")].

### Square Grid Component (branch/element span grid)
- Purpose: Build a rectangular point grid directly as a tree (one branch per row) using a single native component, rather than composing Series + Cross Reference by hand.
- Difficulty: intermediate
- Chain:
  ```
  Slider["Branch spans"] -> SqGrid.Ex ; Slider["Element spans"] -> SqGrid.Ey -> SqGrid.P {branches: (Ex+1) x (Ey+1)}, SqGrid.C (cell polylines)
  SqGrid.C -> Points.P {index-tag each point for verification}
  ```
- Tree handling notes: Output P is natively a tree (one branch per row/column) — no Cross Reference or grafting needed to get grid structure, unlike the Series+Move+CrossRef method in §3.
- Failure modes: None specific stated beyond general Ex/Ey naming ("Branch spans" controls branch count, "Element spans" controls per-branch item count) being easy to swap by mistake.
- Source: [STATED, Essential pt.2 p.77-78].

### Voronoi Diagram — Bounded vs. Radius-Clipped
- Purpose: Generate a planar Voronoi tessellation, either fully tiled (bounded by a region curve) or clipped to individual circles per seed.
- Difficulty: intermediate
- Chain:
  ```
  Panel[P: points] -> Voronoi.P ; Panel["rectangle (Crv)"] -> Voronoi.B ; XY[O] -> Voronoi.Pl -> Voronoi.C {flat, fully-tessellated cells}
  -- with explicit radius (added to the same wiring):
  Slider["Radius", 2.6] -> Voronoi.R -> Voronoi.C {cells clipped to individual 2.6-radius circles — overlapping/rounded shapes, not a clean tiling}
  ```
- Tree handling notes: Flat list of closed curves, one per seed point.
- Failure modes: No Radius input defaults to INFINITE radius (full tessellation) — supplying a finite radius instead intentionally breaks the clean tiling into separate, possibly overlapping circular clips; don't supply a radius by accident when a full tessellation was intended.
- Source: [STATED, AAD pt.4 p.282-283].

### Voronoi-Skin Panelization (pyramid-per-cell via Delaunay, weld & smooth)
- Purpose: Sculpt a 3D "skin" from a flat Voronoi diagram by building one pyramidal mesh per cell (boundary vertices as base, offset centroid as apex), then welding and smoothing into one continuous surface.
- Difficulty: advanced
- Chain:
  ```
  Panel[P] -> Voronoi.P -> Voronoi.C {planar Voronoi cells}
  Voronoi.C -> Disc(Discontinuity).C -> Disc.P {grafted; one branch per cell = that cell's boundary vertices}
  Voronoi.C -> Area.G -> Area.C {centroid per cell} -> Move.G ; Slider[Factor,-0.5] -> Z.F -> Z.V -> Move.T -> Move.G {grafted; one branch per cell = translated centroid}
  Disc.P -> Merge.D1 ; Move.G -> Merge.D2 -> Merge.R {grafted, one branch per cell}
  Merge.R -> Del(Delaunay Mesh).P ; XY[O] -> Del.Pl -> Del.M {branches: one pyramid mesh per cell — disconnected}
  Del.M -> wbJoin(Weaverbird "Join Meshes and Weld").M+ {set to flatten} -> wbJoin.M
  wbJoin.M -> wbCatmullClark.M ; Slider[Level,3] -> .L -> .O {single continuous smoothed pyramidal Voronoi skin}
  ```
- Tree handling notes: BOTH the boundary-vertex stream and the offset-centroid stream are explicitly grafted (one branch per cell) before Merge, so Delaunay Mesh's per-branch operation returns one discrete mesh per cell rather than one flat mesh — this is a load-bearing example of the "graft-before-merge" rule from §3.
- Failure modes: Skipping the join+weld step and smoothing the disconnected per-cell meshes directly leaves each pyramid smoothed independently with visible GAPS between cells — join/weld must happen before Catmull-Clark, not after.
- Source: [STATED, AAD pt.4 p.283-286].

### Voronoi Pattern Projected onto a Freeform Surface [PARTIAL]
- Purpose: Reproduce a flat Voronoi tessellation's topology conformed onto a curved surface via UV remapping, instead of physically bending the planar diagram.
- Difficulty: advanced
- Chain:
  ```
  Panel[P] -> Voronoi.P -> Voronoi.C {planar Voronoi as before}
  Voronoi.C -> Disc.C -> Disc.P -> pDecon.P -> pDecon.X, .Y
  pDecon.X -> Bnd_1.N -> Bnd_1.I -> ReMap_1.S ; pDecon.X -> ReMap_1.V -> ReMap_1.R -> Pt.X
  pDecon.Y -> Bnd_2.N -> Bnd_2.I -> ReMap_2.S ; pDecon.Y -> ReMap_2.V -> ReMap_2.R -> Pt.Y
  Srf -> EvalSrf.S ; Pt(remapped XY pair, reused as target-surface UV) -> EvalSrf.uv -> EvalSrf.P -> PLine.V -> PLine {Voronoi topology, now lying on the freeform surface}
  ```
- Tree handling notes: X and Y coordinates are independently Bounds+Remap'd into the 0-1 domain, then reused directly as the target (reparameterized) surface's UV coordinates.
- Failure modes: **[PARTIAL — diagram partially illegible in source]** — some individual wire endpoints among pDecon/Bnd/ReMap/Pt are not fully resolved at rendered resolution in the raw extraction; overall data flow is confirmed by body text.
- Source: [STATED, AAD pt.4 p.287] [DIAGRAM PARTIALLY ILLEGIBLE in source].

### Diamond-Panel Relief Pattern Driven by Grayscale Image
- Purpose: See the "Image-Sampler-Driven Attractor Pattern" recipe in §4 — the Diamond Panels (LunchBox) variant is the canonical worked example of this technique and is cross-referenced here as a paneling recipe.
- Difficulty: advanced
- Chain: See §4, "Image-Sampler-Driven Attractor Pattern," second variant.
- Tree handling notes: See §4.
- Failure modes: See §4.
- Source: [STATED, AAD pt.4 p.288-290] (cross-reference, not duplicated in full here to avoid redundant wiring).

### Chebyshev-Net Equal-Edge-Length Grid (geometric construction) [PARTIAL]
- Purpose: Build a grid whose every edge has an identical physical length regardless of surface curvature (useful for gridshells built flat and then deformed into curved form).
- Difficulty: advanced
- Chain:
  ```
  === Section: Chebyshev-net geometric construction (conceptual) ===
  Point0(on surface) with transverse curves u,v through it
  Circle0(center=Point0, radius=L) ∩ u-isocurve -> Point1 ; ∩ v-isocurve -> Point2
  Circle1(center=Point1,radius=L), Circle2(center=Point2,radius=L) -> mutual intersection -> Point3
  {Point0,Point1,Point2,Point3} = one equal-edge-length module; repeat across all 4 quadrants -> full grid
  -- 3D/surface-based extension replaces circles with spheres of radius L, intersected with surface S
  ```
- Tree handling notes: n/a — no Grasshopper canvas is shown for this technique anywhere in the source.
- Failure modes: **[PARTIAL — no GH canvas shown in source, conceptual/geometric-construction only]**. The source explicitly states "Grasshopper does not provide a built-in component that allows users to perform iterations and create a Chebyshev-net" — building the full grid requires a third-party iteration/looping add-on (see §12), deferred by the book to a chapter outside the extracted page range. A Chebyshev-net also cannot achieve both equal edge length AND full domain coverage simultaneously — an equidistant grid leaves a "leftover" untiled boundary area, unlike a uv-domain-based grid (equal coverage, unequal edges).
- Source: [STATED, AAD pt.3 p.161-165] [NOT IN SOURCE: Grasshopper implementation].

### Space-Frame / Pyramidal Module Extension of a Diagrid
- Purpose: Extend the surface-based diagrid (Method 3 above) into a 3D space-frame by adding an offset apex per sub-surface and connecting it to all 4 corners.
- Difficulty: advanced
- Chain:
  ```
  Srf -> Divide(Divide Domain²).I ; sliders -> Divide.U,.V -> Divide.S
  Srf -> SubSrf.S ; Divide.S -> SubSrf.D -> SubSrf.S -> DeBrep.B -> DeBrep.F,.E,.V
  DeBrep.F -> EvalSrf.S ; MDSlider[0.5,0.5] -> EvalSrf.uv -> EvalSrf.P (center), EvalSrf.N (normal)
  EvalSrf.P -> Line.S ; EvalSrf.N -> Line.D ; Slider[Length] -> Line.L -> Line.L -> End.C -> End.E {apex point offset above center}
  DeBrep.V -> Item[i=0..3] (4 corners) ; End.E -> Ln.A ; Item.i -> Ln.B -> Ln.L {strut from apex to each corner}
  ```
- Tree handling notes: Same "decompose whole list, then re-index by position" idiom as the surface-based diagrid — scales from one sub-surface to the whole divided surface unchanged.
- Failure modes: Same edge/corner considerations as the diagrid Method 3.
- Source: [STATED, AAD pt.3 p.160].

### Striped/Contiguous Panel Selection via 1-Axis Divide + Cull Pattern
- Purpose: Select contiguous "stripes" of panels along one subdivision axis by dividing heavily in one direction only and culling with a short repeating pattern.
- Difficulty: intermediate
- Chain:
  ```
  Srf -> Divide.I ; Slider[U Count=1] -> Divide.U ; Slider[V Count=99] -> Divide.V -> Divide.S
  Srf -> SubSrf.S ; Divide.S -> SubSrf.D -> SubSrf.S {99 contiguous strips along V}
  Toggle[True],[True],[False] -> Merge.D1,D2,D3 -> Merge.R {repeating T,T,F}
  SubSrf.S -> Cull.L ; Merge.R -> Cull.P -> Cull.L {2 of every 3 strips retained}
  ```
- Tree handling notes: Flat list of sub-surfaces; dividing 1×N (instead of N×N) is what turns the subdivision into contiguous stripes rather than a checkerboard.
- Failure modes: None specific stated.
- Source: [STATED, AAD pt.3 p.150-151].

---

## 6. Surface Subdivision & Morphing

### Surface Analysis Toolkit (Evaluate Surface, MD Slider, Surface CP, Isocurve)
- Purpose: The surface-domain analog of the curve-analysis toolkit — evaluate position/normal/tangent-plane at a uv point, convert a world point to local uv, and extract isocurves.
- Difficulty: intermediate
- Chain:
  ```
  Srf(Reparameterized) -> EvalSrf.S ; MDSlider[u,v] -> EvalSrf.uv -> EvalSrf.P, .N, .F
  Pt -> SrfCP.P ; Srf -> SrfCP.S -> SrfCP.P'(closest pt), .uvP (local uv), .D (displacement; P=P', D=0 if Pt already on surface)
  Srf -> Iso.S ; MDSlider[u,v] -> Iso.uv -> Iso.U, Iso.V {the two isocurves crossing at that uv point}
  ```
- Tree handling notes: Flat/single item; scales to a grid of uv samples via Divide Surface (see §5's grid recipes).
- Failure modes: Every NURBS surface has a hidden rectangular u/v domain even when its visible outline is circular/star-shaped/trimmed — forgetting this causes confusion when control-point grids or isocurve behavior don't match visual intuition.
- Source: [STATED, AAD pt.3 p.144-148].

### Uniform Surface Subdivision via Isotrim + Divide Domain²
- Purpose: Split a surface into a regular grid of untrimmed sub-surface pieces (as opposed to just a grid of points).
- Difficulty: intermediate
- Chain:
  ```
  Srf -> Divide(Divide Domain²).I ; Slider[U Count],[V Count] -> Divide.U,.V -> Divide.S {list of uv sub-domains}
  Srf -> SubSrf(Isotrim).S ; Divide.S -> SubSrf.D -> SubSrf.S {N untrimmed sub-surfaces, relative to the PARENT domain}
  ```
- Tree handling notes: Flat list, N = U×V sub-surfaces.
- Failure modes: Isotrim's sub-surface outputs keep the ORIGINAL parent surface's domain (e.g. a corner piece reads [0,0.1]×[0,0.2]) — NOT automatically reset to [0,1]×[0,1] — Reparameterize must be explicitly applied per-piece if independent uv addressing is needed.
- Source: [STATED, AAD pt.3 p.148-150].

### Uneven Surface Subdivision via Graph Mapper
- Purpose: Redistribute a subdivision grid unevenly (dense here, sparse there) by warping the U and V cutting domains independently through a Graph Mapper before reconstructing the 2D domain.
- Difficulty: advanced
- Chain:
  ```
  Srf -> Divide.I ; Slider[U,V] -> Divide.U,.V -> Divide.S -> DeDom2.I -> DeDom2.U, .V
  DeDom2.U -> GraphMapper1[Bezier] -> remapped U ; DeDom2.V -> GraphMapper2[Bezier] -> remapped V
  remapped U, remapped V -> Dom².U,.V -> Dom².I²
  Srf -> SubSrf.S ; Dom².I² -> SubSrf.D -> SubSrf.S {unevenly spaced sub-surface grid}
  ```
- Tree handling notes: Flat; the Graph Mapper operates on the 1D domain BEFORE reconstruction into a 2D domain — not on the sub-surface list itself.
- Failure modes: Graph Mapper has two independent internal domains (input A, output B, set via double-click) — domain A must match the real upstream range (e.g. matching the Construct Domain used earlier) or the mapping silently mismatches; also, Graph Mapper cannot be driven by a Number Slider and therefore cannot itself be exposed as a Galapagos genome variable (see §10) — expose the upstream sliders it depends on instead.
- Source: [STATED, AAD pt.3 p.151] merged with [STATED, AAD pt.6 p.484 (Galapagos-driven Graph Mapper limitation)].

### Geodesic Surface Split + Rebuild Untrimmed Piece
- Purpose: Split a surface along the shortest-path curve between two of its points, then rebuild one resulting trimmed fragment as an untrimmed surface.
- Difficulty: advanced
- Chain:
  ```
  Srf -> DeBrep.B -> DeBrep.E (4 edges) -> Item[i=0].L -> Item.i (edge0) ; Item[i=2].L -> Item.i (edge2, opposite)
  Item(edge0) -> Eval.C ; Slider[t] -> Eval.t -> Eval.P (point S) ; Item(edge2) -> Eval.C (same t) -> Eval.P (point E)
  Srf -> Geodesic.S(surface) ; point S -> Geodesic.S(start) ; point E -> Geodesic.E -> Geodesic.G
  Geodesic.G -> SrfSplit.C ; Srf -> SrfSplit.S -> SrfSplit.F {2 trimmed pieces}
  SrfSplit.F -> Item[i=1].L -> Item.i -> DeBrep.B -> DeBrep.E (4 edges) -> 4x Item[i=0..3] -> EdgeSrf.A,B,C,D -> EdgeSrf.S {rebuilt untrimmed}
  ```
- Tree handling notes: Flat throughout; the "rebuild untrimmed" step (Deconstruct Brep → 4 edges → Edge Surface) is the general-purpose recipe for converting ANY trimmed fragment back to an untrimmed surface, not specific to geodesics.
- Failure modes: None specific beyond the standard trimmed-vs-untrimmed distinction (§ Fundamentals).
- Source: [STATED, AAD pt.3 p.154-155].

### Box Morph / Twisted Box / Surface Box (cage-style deformation)
- Purpose: Deform arbitrary geometry from a reference bounding box to a differently-shaped target box (analogous to Rhino's Cage Edit) — used to re-impose a twisted-tower silhouette onto a plain surface of revolution.
- Difficulty: advanced
- Chain:
  ```
  RailRev.S -> BBox.C -> B {reference box: straight bounding box}
  BBox.B -> DeBrep.B -> V {8 corner points} -> Graft.D -> T -> BANG!(Explode Tree) -> (0)...(7) {8 individually addressable corners}
  (2 selected corners) -> Move.G ; Slider[Factor] -> Z.F -> Z.V -> Move.T {push 2 corners along Z}
  Moved corners + 6 unmoved BANG! outputs -> TBox.A..H -> B {target box: a twisted deformation of the reference box}
  RailRev.S -> Morph.G ; BBox.B -> Morph.R ; TBox.B -> Morph.T -> Morph.G {surface re-morphed into the twisted silhouette}
  ```
- Tree handling notes: Grafting the 8 corner points then exploding them via BANG! is what allows exactly 2 of 8 to be individually re-wired through Move while the other 6 pass through unchanged into Twisted Box's 8 named inputs.
- Failure modes: The 2 corners chosen and the Z-offset direction/magnitude directly control the deformation's character — no automated validity check is stated; Surface Box is the companion component for conforming twisted boxes directly to a surface+domain+height rather than 8 explicit points.
- Source: [STATED, AAD pt.4 p.210-213, p.327-328].

---

## 7. Curvature & Developable-Surface Analysis

### Curvature Evaluation via Osculating Circle
- Purpose: Compute curvature at a point on a curve or surface (Principal, Gaussian, Mean) via the osculating-circle definition (k = 1/r).
- Difficulty: intermediate
- Chain:
  ```
  === Curve curvature, two equivalent routes ===
  Crv -> Curvature.C ; Slider[t] -> Curvature.t -> Curvature.P, .K (vector), .C (osculating circle)
  Curvature.K -> VLen.V -> VLen.L {route 1: |curvature vector|}
  Curvature.C -> DArc.A -> DArc.R ; DArc.R -> A/B.A ; Panel[1] -> A/B.B -> A/B.R {route 2: 1/radius — both routes agree}
  === Surface curvature at a uv point ===
  MDSlider[0.5,0.5] -> PrincipalCurvature.uv ; Srf -> PrincipalCurvature.S -> F, C1, C2, K1, K2 (principal directions/curves/vectors)
  MDSlider[0.5,0.5] -> SurfaceCurvature.uv ; Srf -> SurfaceCurvature.S -> F, G (Gaussian), M (Mean)
  ```
- Tree handling notes: Flat/single item; generalizes to a grid via Divide Surface feeding the uv input (see the developable-test and curvature-pattern recipes).
- Failure modes: Circles are DEFINED to have negative curvature by convention in this analysis, so Mean Curvature can come out negative (e.g. −0.03 on a cylinder) — an Absolute component is required before thresholding it as a physical radius; signed curvature for a planar curve is positive when the osculating circle lies to the curve's LEFT of travel, negative to the right.
- Source: [STATED, AAD pt.3 p.136-138, 169].

### Developable-Surface Test via Osculating Circles
- Purpose: Test whether a surface (or a grid of points on it) is developable (zero Gaussian curvature) by checking whether each principal-direction osculating circle degenerates into a line.
- Difficulty: advanced
- Chain:
  ```
  === Single point ===
  Srf(S1) -> Osc(Osculating Circles).S ; MDSlider[0.5,0.5] -> Osc.uv -> Osc.C1, Osc.C2
  Osc.C1 -> Line {cast attempt} ; Osc.C2 -> Line {cast attempt}
  -- developable at that point: one cast succeeds (line-like), one fails (still circular) -- non-developable: BOTH fail
  === Generalized over a grid ===
  Srf -> SDivide.S ; Slider[V Count] -> SDivide.U,.V -> SDivide.uv -> Osc.uv (via relay) ; Srf -> Osc.S
  Osc.C1 -> Line {tested per point} ; Osc.C2 -> Line {tested per point} {list, item-wise}
  ```
- Tree handling notes: The single-point test is flat/item-wise; the grid-generalized version simply routes SDivide's uv LIST into the same Osc→Line pipeline — no grafting needed, per-item wiring is implicit in the diagram's parallel structure.
- Failure modes: Using developable PRIMITIVES (cone, cylinder) to isolate developable sub-surfaces by trimming can give false positives/negatives if the tested geometry isn't genuinely trimmed from a truly developable base surface; naively dividing two arbitrary rail curves into equal parts and connecting corresponding points does NOT guarantee a developable ruled surface (twist angle is not guaranteed zero) — dedicated third-party algorithms are required for guaranteed-developable ruling search.
- Source: [STATED, AAD pt.3 p.175-176].

### Curvature-Driven Perforation Pattern
- Purpose: Generate a circle-perforation pattern whose density/scale visually expresses surface curvature (larger openings where curvature is higher).
- Difficulty: advanced
- Chain:
  ```
  Srf -> Divide(Divide Domain²).I ; Slider[U Count] -> Divide.U -> Divide.S -> SubSrf(Isotrim).D ; Srf -> SubSrf.S -> SubSrf.S {N sub-surfaces}
  SubSrf.S -> EvalSrf.S ; MDSlider[0.5,0.5] -> EvalSrf.uv -> EvalSrf.P, .N
  EvalSrf.P -> Circle(CNR).C ; EvalSrf.N -> Circle.N ; Slider[Radius] -> Circle.R -> Circle.C {list of circles, one per sub-surface}
  -- curvature-driven radius refinement:
  SubSrf.S -> SurfaceCurvature.S ; MDSlider[0.5,0.5] -> .uv -> .M(Mean Curvature) -> Abs.x -> Abs.y -> Min.A ; Slider[B=0.15] -> Min.B -> Min.R {replaces the flat Radius slider}
  Min.R -> Eval[expr "x>0.025"].x -> Eval.r(boolean) -> Cull.P ; Circle.C -> Cull.L -> Cull.L {filtered circles, curvature above threshold only}
  Cull.L -> SrfSplit.C ; InitialSurface -> SrfSplit.S -> SrfSplit.F {index 0 = holed main surface, 1..N = "scrap" pieces}
  SrfSplit.F -> Culli(Cull Index).L ; Panel[0] -> Culli.I -> Culli.L {removes index 0, isolating the perforation openings}
  ```
- Tree handling notes: Flat list of sub-surfaces/circles throughout; no tree branching required.
- Failure modes: Mean Curvature must be passed through Absolute before use as a physical radius (can be negative); Surface Split's own output convention places the "main" trimmed surface at index 0 and "scrap" pieces at 1..N — easy to invert accidentally when Cull-Indexing.
- Source: [STATED, AAD pt.3 p.177-179].

---

## 8. Mesh & Subdivision

### Building Meshes by Topology (orientation/winding)
- Purpose: Construct a mesh explicitly from vertex + face-connectivity data, and understand vertex winding order (front vs. back face orientation).
- Difficulty: intermediate
- Chain:
  ```
  Panel[Pt: 3 points] -> ConMesh.V
  Slider["Corner A",0] -> Triangle.A ; Slider["Corner B",1] -> Triangle.B ; Slider["Corner C",2] -> Triangle.C
  Triangle.F -> ConMesh.F -> ConMesh.M {single triangular face, counterclockwise = front-facing}
  -- multi-face: lists of corner indices per vertex slot, e.g. A=[0,2], B=[1,1], C=[2,3] -> Triangle.A/B/C -> ConMesh -> orientable 2-face mesh IF both faces wind the same way
  -- Quad variant: Quad.A/B/C/D from 4 corner-index lists -> ConMesh.F
  ```
- Tree handling notes: Flat lists of corner indices, one item per face; the same-length lists across A/B/C(/D) are matched index-by-index into one face per position.
- Failure modes: Connecting a second face's vertices in the WRONG (opposite) rotational direction relative to its neighbor produces a non-orientable/incompatible mesh, shown by Grasshopper/Rhino shading the incompatible face darker (back-facing) than its light (front-facing) neighbor; "Preview Mesh Edges" must be manually enabled (Display menu) to see wireframe edges, or a constructed mesh displays as a shaded surface with none visible.
- Source: [STATED, AAD pt.4 p.263-266].

### Delaunay Triangulation of a Point Set
- Purpose: Triangulate an arbitrary point set while avoiding thin/skinny triangles, by maximizing the minimum angle of the triangulation.
- Difficulty: basic
- Chain:
  ```
  Pt -> Del(Delaunay Mesh).P ; (Pl input: plane[s] where the algorithm operates) -> Del.M {flat}
  ```
- Tree handling notes: Flat; per-branch when fed grafted/tree input (see Voronoi-Skin recipe in §5, which relies on exactly this per-branch behavior).
- Failure modes: Skinny/thin triangles from arbitrary (non-Delaunay) triangulation are explicitly called out as producing inaccurate results in particle-spring simulations and FEM analysis — a concrete reason to prefer Delaunay.
- Source: [STATED, AAD pt.4 p.266-268].

### NURBS-to-Mesh Conversion via Mesh UV (+ T-node matching for welding)
- Purpose: Convert an untrimmed NURBS surface to a quad mesh with a specified U/V resolution, and keep multiple adjoining converted surfaces weld-compatible.
- Difficulty: intermediate
- Chain:
  ```
  Srf -> MeshUV.S ; Slider[U Count],[V Count] -> MeshUV.U,.V -> MeshUV.M {quad mesh}
  -- multi-surface weld compatibility:
  Srf1,Srf2,Srf3 -> MeshUV_1/2/3.S ; SAME U/V count sliders shared across all three -> M1,M2,M3 {vertex counts coincide at shared edges}
  M1 -> Merge.D1 ; M2 -> Merge.D2 ; M3 -> Flip(Mesh Flip).M -> Merge.D3 {Flip corrects a face-winding mismatch before joining}
  Merge.R -> wbJoin(Weaverbird "Join Meshes and Weld").M+ {set to flatten} -> wbJoin.M {single continuous mesh}
  ```
- Tree handling notes: Flat; T-node avoidance is a numeric-matching concern (same U/V counts across adjoining pieces), not a tree-shape one.
- Failure modes: Mesh Surface/Mesh UV conversion is ONLY reliable for UNTRIMMED surfaces — a trimmed surface either approximates its boundary (Mesh Surface) or preserves it but introduces thin triangles near it (Mesh Brep); mismatched U/V counts between adjoining surfaces create "T-nodes" (vertices lying ON but not COINCIDENT with a neighbor's edge) that cannot weld correctly and cause SubD algorithms to treat each piece independently; a face-winding mismatch between adjoining converted pieces shows as a visible shading/shadow artifact along the shared edge and must be fixed with Mesh Flip before joining.
- Source: [STATED, AAD pt.4 p.269-272, 278-280].

### Weaverbird Loop Subdivision (triangular meshes)
- Purpose: Iteratively smooth a triangular mesh toward its theoretical limit surface, with configurable naked-edge (boundary) treatment.
- Difficulty: intermediate
- Chain:
  ```
  Panel[Mesh] -> wbLoop.M ; Slider["Level",1..3] -> wbLoop.L ; Slider["Smooth Naked Edges",0/1/2] -> wbLoop.S -> wbLoop.O
  ```
- Tree handling notes: Flat; a simple/schematic (low-poly) input mesh tends to produce a MORE refined output than an already-dense input.
- Failure modes: S=0 (Fixed) keeps boundary edges at their original position (unsmoothed); S=1 (Smooth) relaxes them toward a spline; S=2 (Corner Fixed) relaxes toward a spline except two pinned corner vertices; a mesh containing a hole tends to round the hole boundary into a pseudo-circular shape after subdivision.
- Source: [STATED, AAD pt.4 p.274-276].

### Weaverbird Catmull-Clark Subdivision (quad/tri meshes)
- Purpose: The quad/triangle-mesh analog of Loop Subdivision — smooth an arbitrary mesh toward its limit surface.
- Difficulty: intermediate
- Chain:
  ```
  Mesh -> wbCatmullClark.M ; Slider[Level] -> wbCatmullClark.L -> wbCatmullClark.O {smoothed quad/tri mesh}
  ```
- Tree handling notes: Flat; commonly the final step after Join+Weld in a multi-part-surface or Voronoi-skin pipeline (see §5).
- Failure modes: Applying Catmull-Clark to disconnected per-branch meshes (skipping join+weld) smooths each piece independently, leaving visible gaps between them.
- Source: [STATED, AAD pt.4 p.277, 280, 285-286].

### Cull-Adjacent-Faces Cleanup for Joined Mesh-Box Aggregations
- Purpose: Remove redundant internal/overlapping faces where two joined mesh boxes touch face-to-face, leaving only the true external skin.
- Difficulty: advanced
- Chain:
  ```
  Panel[Mesh] -> Explode.M -> Explode.F {individual single-face pieces}
  Explode.F -> Area.M (relay) -> Area.C {face centroids}
  Area.C -> CullPt("Cull Duplicates").P ; Slider["Tolerance",0.10] -> CullPt.T {mode: Average}
  CullPt.I -> Eval[expr "x is greater than or equal to 0"].x -> t {index pairs; -1 = no duplicate = true boundary face; a real pair = coincident/overlapping internal faces}
  Explode.F -> Cull(Cull Index).L ; (CullPt/Eval result) -> Cull.I -> Cull.L
  Cull.L -> Item["Leave One"].L -> i -> MJoin.M -> M {single mesh, internal overlapping faces removed}
  ```
- Tree handling notes: Flat throughout.
- Failure modes: **[PARTIAL — diagram partially illegible in source]** the precise division of labor between CullPt's I/V outputs, the "x ≥ 0" test, and the Cull/Item "Leave One" step is not fully resolved in the raw extraction; the overall intent (explode → find coincident centroids → discard internal/overlapping faces → rejoin) is explicit in the source text and figure caption.
- Source: [STATED, AAD pt.4 p.292] [DIAGRAM PARTIALLY ILLEGIBLE in source].

### Mesh Face-Orientation Compatibility & Mesh Flip
- Purpose: Diagnose and fix inconsistent face winding (orientability) between adjacent mesh faces or joined mesh pieces.
- Difficulty: intermediate
- Chain: See "Building Meshes by Topology" (winding demo) and "NURBS-to-Mesh Conversion" (Mesh Flip before joining) above — this entry consolidates the underlying rule rather than introducing new wiring.
- Tree handling notes: n/a.
- Failure modes: Two adjacent faces are "compatible" only if wound the same rotational direction; an orientable mesh has all face normals consistent; Grasshopper visually flags incompatible adjacent faces by shading them differently (front=light, back=dark) — Mesh Flip reverses a mesh's face direction to restore compatibility before joining/welding/subdividing.
- Source: [STATED, AAD pt.4 p.260-261, 264, 280].

### Faceted Pyramidal Panelization via Delaunay on a Freeform Surface [PARTIAL]
- Purpose: Build a raised diamond/pyramidal faceted panelization pattern over a freeform surface by triangulating surface-grid points merged with normal-offset centroids.
- Difficulty: advanced
- Chain:
  ```
  Srf -> TriB(LunchBox "Triangle Panels B").Srf ; Slider[U,V Divisions] -> TriB.U,.V -> TriB.Panels {triangular panels}
  TriB.Panels -> Area.G -> Area.C {centroid of each triangle}
  Srf -> SrfCP.S ; Area.C -> SrfCP.P -> SrfCP.uvP -> EvalSrf.uv ; Srf -> EvalSrf.S -> EvalSrf.N -> Move.T {translate centroid along surface normal}
  Area.C -> Move.G -> Move.G -> Merge.D1
  Srf -> DeBrep.B -> DeBrep.F/.E/.V -> [Construct Plane from surface data] -> Del.Pl
  Merge.R -> Del.P -> Del.M {triangulated grid of surface points merged with offset centroids -> raised diamond/pyramidal facets}
  ```
- Tree handling notes: Not stated explicitly beyond the merge of two point streams (surface grid points + offset centroids) feeding one Delaunay pass.
- Failure modes: **[PARTIAL — diagram partially illegible in source]** small print size obscures some wire endpoints in the raw extraction, particularly the exact routing from Deconstruct Brep into Construct Plane; overall topology and end result are clear from the accompanying image and caption text.
- Source: [STATED, AAD pt.4 p.269] [DIAGRAM PARTIALLY ILLEGIBLE in source].

---

## 9. Physics / Form-Finding — Kangaroo

### Kangaroo Pipeline Overview (discretize → particles/springs/forces/anchors → solver)
- Purpose: Understand the mandatory 3-stage structure of every Kangaroo definition before building one.
- Difficulty: intermediate
- Chain: n/a (conceptual scaffold underlying every recipe below).
- Tree handling notes: n/a.
- Failure modes: Kangaroo CANNOT process NURBS curves or surfaces directly — curves must be discretized to lines first, surfaces to meshes (points+lines); the Force-objects input on KangarooPhysics MUST be explicitly flattened (Springs output + Forces output are separate streams that need merging into one flat list); Boolean Toggle semantics are inverted from intuition — **False = simulation running, True = simulation stopped**; any change to upstream geometry requires manually resetting (SimulationReset) — Kangaroo does not auto-detect mid-run edits; anchor points must coincide EXACTLY with a particle (a point placed mid-spring has no effect); dragging anchor points live and then stopping/restarting without returning them to their original position will break the solver's restraint recognition.
- Source: [STATED, AAD pt.5 p.363-367].

### Cable / Catenary Simulation (fixed & movable anchors)
- Purpose: Discretize a line, convert to particles + springs, apply self-weight, and let the solver settle into a sagging catenary-like curve.
- Difficulty: intermediate
- Chain:
  ```
  === Section: 9.3 Cable simulation (basic 2-anchor) ===
  Crv -> Divide.C ; Slider[Count] -> Divide.N -> Divide.P {flat, N+1 points} -> Pt(container) {particles}
  Divide.t -> Shatter.t ; Crv -> Shatter.C -> Shatter.S {flat, N segments} -> Line(container) {springs}
  Line -> Springs.Connection AND Springs.Rest length {Rest Length = Start Length case}
  Pt -> UForce.Point ; Slider[Factor,-10] -> UnitZ.F -> UnitZ.V -> UForce.Force
  Crv -> End.C -> End.S, End.E -> Kangaroo.AnchorPoints
  Springs.S, UForce.U -> {flatten} -> Kangaroo.Force objects
  Shatter.S -> Kangaroo.Geometry ; Toggle -> Kangaroo.SimulationReset ; Timer[5ms] --dotted--> Kangaroo
  Kangaroo.GeometryOut -> live-updating sagging catenary-like polyline {flat, N segments}
  -- movable-anchor variant: replace End Points with a Point(container) set from Rhino-placed points; can be dragged live, or a 3rd mid-chain anchor added for a two-span sag
  ```
- Tree handling notes: Flat throughout; more Divide Curve points = more particles = shorter springs = a smoother, more deeply-sagging approximation (a resolution tradeoff, not a tree-structure one).
- Failure modes: See Kangaroo Pipeline Overview; fitting an Interpolate Curve through ParticlesOut for visual continuity looks smooth but is physically incorrect at multi-anchor junctions (implies bending stiffness the hinge-like particles cannot have).
- Source: [STATED, AAD pt.5 p.365-369].

### Hooke's-Law Verification & Rest-Length Pre-tension/Relaxation
- Purpose: Validate that Kangaroo's spring elongation matches the analytical Hooke's-Law prediction, and deliberately pre-tension or relax a spring via a Rest-Length factor.
- Difficulty: intermediate
- Chain:
  ```
  === Section: 9.4 Hooke's-law verification ===
  Crv(Start Length L) -> Springs.Connection AND Springs.Rest length (Rest=Start case) ; Slider[Stiffness] -> Springs.Stiffness
  Crv -> End.C -> S,E -> Kangaroo.AnchorPoints ; UForce fed by Unit Z[Factor=-100] -> Kangaroo.Force objects {flattened}
  Kangaroo.GeometryOut -> Len.C -> L {matches F/k hand calculation exactly}
  === Section: Rest-Length pre-tension / relaxation ===
  Line -> Len.C -> L -> A×B.A ; Slider[B=0.6 (pretension) or 1.2 (relaxation)] -> A×B.B -> A×B.R -> Springs.Rest length
  Line -> Springs.Connection (unscaled, directly) {Rest Length ≠ Start Length}
  ```
- Tree handling notes: Flat.
- Failure modes: Damping affects only how FAST the system reaches equilibrium, not the final resting length — do not use it to try to control final geometry; Upper/Lower Cutoff (both default 0 = no cutoff) and Plasticity govern additional spring-behavior limits with no worked example given in source.
- Source: [STATED, AAD pt.5 p.370-374].

### Analytic Catenary vs. Particle-Spring Approximation
- Purpose: Compare the exact mathematical catenary (via formula or the dedicated Catenary component) against a Kangaroo particle-spring approximation, and tune the approximation to hug the true curve.
- Difficulty: advanced
- Chain:
  ```
  === Analytic, formula method ===
  Dom[-5,5].I -> Range.D ; Slider[Steps=20] -> Range.N -> Range.R {21 x-values}
  Panel["2*Cosh(x/2)"] -> Eval.F ; Range.R -> Eval.X -> Eval.r {y-values, a=2}
  Range.R, Eval.r -> Short(Shortest List).A/.B {trim to matched length} -> Pt.X/.Y -> Pt.Pt -> IntCrv.V -> C {exact catenary}
  === Analytic, dedicated component ===
  PointA, PointB -> Catenary.A/.B ; Slider[Length] -> Catenary.L ; Slider[Factor] -> UnitZ.F -> V -> Neg.x -> y -> Catenary.G -> Catenary.C
  === Particle-spring approximation, tuned to nearly match ===
  PointA,B,C -> Arc3Pt.A/.B/.C -> Arc {arc-length pre-set equal to the target catenary length}
  Slider[Count=50] -> Divide.N ; Arc -> Divide.C -> Divide.P {51 points, each segment ~0.4 units — fine discretization limits stretch}
  Divide.P -> PLine.V -> Explode.C -> Explode.S {50 short segments} -> Line(container) -> Springs.Connection
  Line -> Len.C -> L -> A×B.A ; Slider[B=0.995] -> A×B.B -> A×B.R -> Springs.Rest length {near-inextensible: pre-tensioned}
  Slider[Stiffness=7000] -> Springs.Stiffness ; low self-weight per particle -> UForce.Force
  -- result: total measured length ~19.997 vs target 20, closely tracking the analytic curve
  ```
- Tree handling notes: Flat throughout.
- Failure modes: A true catenary requires 4 conditions (suspended by endpoints, perfectly flexible, uniformly dense, INEXTENSIBLE) — a plain spring-chain, no matter how high its Stiffness, can never be truly inextensible, so it only approximates, never exactly reproduces, a catenary shape unless discretized very finely with a near-1.0 (slightly <1) Rest-Length Factor and high Stiffness as shown; self-weight per particle should be calibrated as total structure weight ÷ particle count, not picked arbitrarily.
- Source: [STATED, AAD pt.5 p.375-381].

### Membrane / Cable-Net (corner-anchored, edge-anchored, minimal surface)
- Purpose: Turn a NURBS surface into a particle-spring "cable net" membrane and anchor it in different ways to get a hammock, tent, saddle, or soap-film-like minimal surface.
- Difficulty: advanced
- Chain:
  ```
  Srf -> MeshUV.S ; Slider[U,V Count] -> MeshUV.U,.V -> MeshUV.M
  MeshUV.M -> wbEdges.G -> L {edges, become springs} ; MeshUV.M -> wbVertices.G -> P {vertices, become particles}
  wbEdges.L -> Line(container) -> Springs.Connection ; Line -> Len.C -> L -> A×B.A ; Slider[B=1.0] -> A×B.B -> R -> Springs.Rest length
  wbVertices.P -> Pt(container) -> UForce.Point ; Slider[Factor=-20] -> UnitZ.F -> V -> UForce.Force
  -- corner-anchored: MeshUV.M -> MeshCorners.Mesh -> L -> Kangaroo.AnchorPoints {4-corner hammock/pillow shape}
  -- edge-anchored: MeshUV.M -> NakedVertices(NV).M -> NV.NakedPts -> Kangaroo.AnchorPoints {edge-supported tent/dome; mixing with 1+ interior anchors gives saddle/hypar shapes}
  -- minimal surface: set the Rest-Length Factor (A×B.B) to 0 -> every spring wants zero length -> soap-film-like drape
  ```
- Tree handling notes: Flat; Springs.S and UForce.U must be flattened together before Kangaroo.Force objects, per the Pipeline Overview rule.
- Failure modes: Anchor points must sit on actual particles (same rule as cables); a plain edges-only cable-net can freely rack into a diamond/parallelogram under shear (no shear stiffness) — see the diagonal-braced variant below to fix this.
- Source: [STATED, AAD pt.5 p.382-387].

### Diagonal-Braced Sheet-Like Membrane (shear resistance)
- Purpose: Add diagonal springs across each quad face so a cable-net membrane behaves like a continuous sheet material instead of a freely racking net.
- Difficulty: advanced
- Chain:
  ```
  MeshUV.M -> MeshExplode.M -> F {faces} -> wbVertices(2nd instance).G -> P {per-face vertex points}
  P -> Item×4[i=0,1,2,3] {four per-face corner-point lists}
  Item[0], Item[2] -> Ln.A/.B -> L {diagonal 1 per face} ; Item[1], Item[3] -> Ln.A/.B -> L {diagonal 2 per face}
  Ln1.L, Ln2.L -> Merge.D1/.D2 -> R {all diagonal lines}
  -- two parallel Springs From Line instances: Springs#1 <- wbEdges.L (mesh edges) ; Springs#2 <- Merge.R (diagonals)
  Springs#1.S, Springs#2.S, UForce.U -> {flatten} -> Kangaroo.Force objects
  ```
- Tree handling notes: Flat; both edge-springs and diagonal-springs are separately built then merged (flattened) into one Force-objects stream.
- Failure modes: One diagonal per quad gives asymmetric/direction-dependent stiffness (useful for anisotropic materials paired with different Rest Lengths per direction); reducing Rest Length Factor below 1.0 on this RIGID (diagonally braced) membrane produces origami-like CREASING rather than a smooth minimal-surface sag — qualitatively different from the same operation on a plain, un-braced cable-net; a triangulated mesh-sphere's diagonals coincide with real edges near the poles and must be deduplicated (removeDuplicateLines) before conversion to springs, or those regions get double-sprung.
- Source: [STATED, AAD pt.5 p.387-392].

### Shell Force for Bending Resistance (mesh-sphere drop test)
- Purpose: Add a bending-resistance ("Shell") force so a hinge-particle mesh does not crumple non-physically on collision with a rigid surface, and enable a virtual floor via Kangaroo Settings.
- Difficulty: advanced
- Chain:
  ```
  mesh-sphere -> MeshExplode.M -> F -> DeMesh.M -> V -> Item×4[0..3] -> Ln×2(diagonals) -> Merge(D1-D4) -> R {4-input Merge — see caveat below}
  mesh-sphere -> wbEdges.G -> L ; -> wbVertices.G -> P
  Merge.R (diagonals) -> removeDuplicateLines.L -> Q {deduplicated, pole-triangle overlaps removed}
  Q -> Line(container) -> Springs.Connection AND Springs.Rest length ; Slider[Stiffness=5000] -> Springs.Stiffness
  wbVertices.P -> Pt -> UForce.Point ; Slider[Factor=-18] -> UnitZ.F -> V -> UForce.Force
  mesh-sphere -> Shell.Mesh ; Slider[Strength=500] -> .Strength ; Slider[AngleFactor=1] -> .AngleFactor -> Shell.ShellForce
  Springs.S, UForce.U, Shell.ShellForce -> {flatten} -> Kangaroo.Force objects
  Slider[TimeStep=0.005], Toggle[Floor=True] -> Kangaroo Settings -> Kangaroo.Settings ; Toggle, Timer[5ms] -> Kangaroo
  ```
- Tree handling notes: **[PARTIAL — diagram partially illegible in source]** the exact 4th data stream feeding the 4-input Merge (D1–D4) in the mesh-sphere example is not clearly legible in the raw extraction beyond "mesh edges + diagonal/point sub-lists"; overall behavior (fewer springs double-counted at poles after dedup) is confirmed by body text.
- Failure modes: A mesh-sphere with high Stiffness AND diagonal bracing STILL crumples irreversibly on hitting a rigid floor unless a Shell force is added — neither high stiffness nor shear bracing alone addresses rotational/moment stiffness at the hinge-like particles.
- Source: [STATED, AAD pt.5 p.391-393] [4-input Merge source PARTIALLY ILLEGIBLE].

### Kangaroo Settings & Floor Collision
- Purpose: Bundle solver-wide parameters (tolerance, time step, sub-iterations, floor collision, drag, restitution, friction) into one Settings object.
- Difficulty: intermediate
- Chain: See "Shell Force" recipe above — Kangaroo Settings feeds `Kangaroo.Settings`; the Floor Boolean Toggle input specifically enables a virtual ground-plane collision.
- Tree handling notes: n/a.
- Failure modes: Without Floor=True, a falling object in a Kangaroo simulation passes through the world XY plane instead of resting on it.
- Source: [STATED, AAD pt.5 p.393].

---

## 10. Optimization — Goat / Galapagos / Karamba / Millipede

### Exact Optimization via Goat
- Purpose: Drive a Number Slider automatically to the value that minimizes/maximizes a single numeric Objective, using a local exact-solver plug-in — replacing imprecise manual slider-dragging.
- Difficulty: intermediate
- Chain:
  ```
  Pt("Point A") -> Dist.A ; Crv -> Eval.C ; Slider["t parameter",0..1] -> Eval.t -> Eval.P -> Dist.B -> Dist.D {flat, single value}
  Slider["t parameter"] -> Goat.Variables ; Dist.D -> Goat.Objective
  [Double-click Goat] -> Optimize for = Minimum ; Algorithm = "Local, linear approximations (COBYLA)" ; Stop if relative-change-in-variables < 0.001 OR runtime > 30s
  ```
- Tree handling notes: n/a — Goat operates on scalar sliders and one scalar objective, not on trees.
- Failure modes: Goat's Variables input only accepts Number Sliders; Local algorithms can converge on a LOCAL (not global) optimum since they only search near the starting value — for complex/non-convex problems, run a Global algorithm first, then refine with Local; manually dragging a slider to hunt for an optimum is explicitly called "inconvenient" and imprecise, motivating Goat/Galapagos in the first place.
- Source: [STATED, AAD pt.6 p.432-434].

### Heuristic Optimization via Galapagos
- Purpose: Use an evolutionary solver to search a multi-variable design space (via Gene Pool sliders) toward a minimized/maximized Fitness value — e.g. the shortest interpolated path between two fixed points on a freeform surface.
- Difficulty: advanced
- Chain:
  ```
  Pt(start) -> SrfCP_1.P ; Srf -> SrfCP_1.S -> uvP ; Pt(end) -> SrfCP_2.P ; Srf -> SrfCP_2.S -> uvP
  GenePool_U[N sliders,0..1] -> ConstructPoint.X ; GenePool_V[N sliders,0..1] -> ConstructPoint.Y -> Pt -> Merge.D2
  SrfCP_1.uvP -> Merge.D1 ; SrfCP_2.uvP -> Merge.D3 -> Merge.R -> CrvSrf.uv ; Srf -> CrvSrf.S -> CrvSrf.C, .L
  GenePool_U + GenePool_V (all sliders) -> Galapagos.Genome ; CrvSrf.L -> Galapagos.Fitness
  [Double-click Galapagos] -> Fitness = Minimize -> Solvers tab -> Start Solver; stop manually once top candidate ("V1") stabilizes
  ```
- Tree handling notes: n/a — Genome is any set of sliders embedded in one or more Gene Pool components; more sliders/Gene Count = finer control (and slower search).
- Failure modes: Evolutionary (Galapagos) solvers give NO run-to-run guarantee of an identical result, unlike exact solvers (Goat); Galapagos runs indefinitely with no automatic convergence stop — the source instructs stopping it manually once the top-ranked fitness value stabilizes; a Graph Mapper CANNOT be driven by a Number Slider and therefore cannot itself be wired as a Genome variable — expose upstream sliders that feed it instead.
- Source: [STATED, AAD pt.6 p.435-438, p.484].

### Target-Value (Goal-Seeking) Optimization Trick
- Purpose: Drive a solver toward a SPECIFIC target value (not a pure min/max) by minimizing the absolute difference between the raw Fitness and the target.
- Difficulty: intermediate
- Chain:
  ```
  Pt/Pt -> Dist.A/.B {flat} ; Slider["target value",500] -> A-B.A ; Dist.D -> A-B.B -> A-B.R -> Abs.x -> Abs.y
  Abs.y -> Galapagos.Fitness (set to Minimize) ; [sliders controlling the two points] -> Galapagos.Genome
  ```
- Tree handling notes: n/a.
- Failure modes: None specific beyond standard Galapagos caveats above.
- Source: [STATED, AAD pt.6 p.439].

### Karamba Shape Optimization (cross-section search via Galapagos)
- Purpose: Optimize a structure's cross-section selection (not its topology) to minimize displacement under load, using Karamba for FEA and Galapagos as the search engine.
- Difficulty: advanced
- Chain:
  ```
  PointA, PointB -> Ln.A/.B -> L -> LineToBeam.Line -> Elem
  PointA -> Supp.Pos|Ind ; all 6 Conditions toggles enabled -> Supp.Supp {fixed support}
  Slider[Factor=1] -> UnitZ.F -> V -> Rev.V ; PointB -> PLoad.Pos|Ind ; Rev output -> PLoad.Vec -> PLoad
  Panel["material index"] -> MatSelect.Name|Ind ; ReadMatTable.Mat -> MatSelect.Mat -> Mat
  Panel["cross-section index", Galapagos-controlled] -> CroSecSelect.Name|Ind ; ReadCSTable.CroSec -> CroSecSelect.CroSecs -> CroSec
  Pt,Elem,Supp,PLoad,CroSec,Mat -> Assemble.[inputs] -> Model -> Analyze.Model -> Model, Disp, G, Energy
  Analyze.Disp -> Num -> Galapagos.Fitness ; Galapagos.Genome -> [feedback] -> the cross-section-index slider
  ```
- Tree handling notes: n/a — operates on a single assembled Model object and a scalar Displacement, no tree branching involved.
- Failure modes: Genetic/evolutionary solvers are not guaranteed to find the true global optimum on complex problems — "experience demonstrates that... often the solution... is not 'the best one' but is closer to it"; shape optimization (this recipe) preserves the initial topology and only searches within it — conflating this with topology optimization (next recipe) misrepresents what each actually changes.
- Source: [STATED, AAD pt.5 p.406-410].

### Millipede Topology Optimization (2D Michell truss / MBB beam, 3D bridge)
- Purpose: Let a structural-optimization solver both remove AND (in the extended/XESO variant) add material within a fixed design domain, changing the structure's actual topology rather than just its dimensions.
- Difficulty: advanced
- Chain:
  ```
  === 2D: Michell truss ===
  Crv -> 2DBoundaryRegion.Boundary -> BReg -> Topostruct2DModel.M {merged, 1 of 3 wires}
  Toggle×6(X,Y,Z,RX,RY,RZ) -> StockSupportType -> SUP -> 2DSupportRegion.SUP ; Geo -> 2DSupportRegion.Boundary -> SReg -> Topostruct2DModel.M {2 of 3}
  Geo -> 2DBoundaryLoad.Boundary ; [load vector] -> 2DBoundaryLoad.L -> LReg -> Topostruct2DModel.M {3 of 3}
  Slider[XResolution] -> Topostruct2DModel.XR -> FE -> Topostruct2DSolver.FE {connect LAST — auto-triggers analysis}
  Slider[SWC],[Optimization Iterations],[Target Density] -> Topostruct2DSolver -> FE -> 2DMeshResult {von Mises/deflection color mesh} ; .maxu -> Panel
  === 2D: MBB beam (self-weight only, no load region) ===
  Geo×2 -> 2DBoundaryRegion.Boundary / 2DSupportRegion.Boundary ; two StockSupportType sets (X&Y fixed / Y only) ; no 2DBoundaryLoad
  === 3D: bridge ===
  3DDensityRegion(parallelepiped) marks a non-design-space volume kept unaltered ; remaining inputs are "the exact 3D transposition" of the 2D setup -> 3D solver -> 3DIsoMesh {renders geometry + stresses + max displacement}
  ```
- Tree handling notes: The Model input (M) accepts multiple simultaneous wire connections (BReg+SReg+LReg all into the same M pin) — standard GH multi-source-into-one-input concatenation, not an explicit Merge component.
- Failure modes: Topostruct2DModel's default XResolution (XR=12) is explicitly "too low for every type of application" — increase it, at the cost of computation time; connect the Solver's FE-input LAST, since it auto-starts analysis on first data — wiring it before other inputs (SWC, O, T) are set can trigger a premature/incomplete run; Optimization Iterations (O) should stay at 1 for controllability — higher values "may cause loss of control on the evolution process"; Target Density (T) near 0 discards excessive material, near 1 gives an "inadequate decrease of material" — both extremes give poor results; the load intensity value in 2DBoundaryLoad has NO effect on the topology result — only geometry/regions matter, so a fictitious load magnitude is safe to use; maxu (max displacement) is typically tiny relative to the model and is arbitrarily scaled up ONLY for deformed-shape preview — never mistake the exaggerated preview for the true magnitude; exact 3D-specific Millipede component names beyond 3DDensityRegion/3DIsoMesh are [NOT IN SOURCE].
- Source: [STATED, AAD pt.6 p.422-430].

---

## 11. Fabrication — Sectioning, Waffling, Printing

### Waffle Joint — Boolean-Difference Interlocking Slots [PARTIAL]
- Purpose: Notch two crossing planar ribs so they physically interlock (halved-lap joint) at every intersection — the core mechanism behind waffle-structure fabrication.
- Difficulty: intermediate
- Chain:
  ```
  === Section: Waffling node intersection (conceptual) ===
  1. Input: two planar rib surfaces/curves A, B crossing in an X
  2. Compute the intersection segment between A and B
  3. Construct domain box A' on rib A (width = material thickness S, extended slightly beyond depth, ">S") and B' on rib B
  4. Solid Difference: A − A' {slot cut into rib A}
  5. Solid Difference: B − B' {slot cut into rib B}
  6. Result: ribs A and B interlock at the crossing via matching notches
  ```
- Tree handling notes: n/a — no GH canvas is shown, only the geometric-construction logic.
- Failure modes: **[PARTIAL — component names not given in source]** the raw text describes only the generic "Solid Difference operation," not actual Grasshopper component names/wiring; no explicit minimum joint-clearance/kerf value is quantified beyond the qualitative ">S" note.
- Source: [STATED, AAD pt.5 p.336-337] [NOT IN SOURCE: component-level wiring].

### Unidirectional Sectioning + Profile Closing for CNC
- Purpose: Slice a freeform surface into parallel, evenly-spaced planar sections at an interval equal to material thickness, give each section real wall thickness, close it into one usable curve, and lay it flat for cutting.
- Difficulty: advanced
- Chain:
  ```
  Srf -> DeBrep.B -> V, E ; DeBrep.E -> Item[i=1].L -> i {one boundary edge}
  Item.i -> DivDist.C ; Slider[Distance = material thickness] -> DivDist.D -> P {plane-origin points, spaced at material thickness}
  Item.i -> End.C -> S,E -> Vec2Pt.A/.B -> V {single constant slicing direction from the same edge}
  DivDist.P -> Pl(Plane Normal).O ; Vec2Pt.V -> Pl.Z -> Pl.P {one plane per division point, all parallel}
  Srf -> Sec(Intersect).B ; Pl.P -> Sec.P -> C {section curves at every plane}
  Sec.C -> Offset.C ; Slider[Distance = −thickness] -> Offset.D ; Pl.P -> Offset.P -> C {each section offset inward}
  Offset.C -> Item[0].L -> i -> Divide.C ; Slider[Count=58] -> Divide.N -> P -> Nurbs.V -> C {smooth curve rebuilt through many points — removes sharp-corner kinks from the raw Offset}
  Sec.C -> End_1.C -> S,E ; Nurbs.C -> End_2.C -> S,E ; corresponding endpoints -> Ln_1/Ln_2.A/.B -> L {2 connecting segments}
  Sec.C, Nurbs.C, Ln_1.L, Ln_2.L -> Merge[mode: simplify].D1-D5 -> R -> Join.C -> C {one closed planar curve per section = the millable profile}
  Join.C -> Orient(4.2.3) -> laid flat, individually, onto XY {ready for CNC}
  ```
- Tree handling notes: Merge is explicitly set to "simplify" mode so all 4 pieces of one section collapse into a single flat branch, ensuring the subsequent Join only joins pieces belonging to the SAME section rather than accidentally joining pieces across sections.
- Failure modes: Sectioning/contouring can only ever achieve continuity PARALLEL to the cut planes — continuity NORMAL to them is structurally impossible with this technique, not a modeling error; offsetting a curve with sharp corners introduces kinks exactly at those corners, fixed by re-dividing and rebuilding as a smooth Nurbs Curve rather than trusting the raw Offset; most CNC machines cannot read NURBS curves directly — convert to arcs/polylines (dense-point polyline reconstruction, or Rhino's `Convert` command with a set tolerance) before transfer.
- Source: [STATED, AAD pt.4 p.330-334].

### 3D-Printable Parametric Vase Pipeline
- Purpose: Take an arbitrary profile curve to a genuinely printable (watertight, manifold, orientable, self-intersection-free) mesh, respecting a specific desktop-printer build volume, by combining stacking/tapering, twisted-loft rebuilding, Box Morph, meshing, smoothing, and wall-thickening.
- Difficulty: advanced
- Chain:
  ```
  === Step 1: stack + taper ===
  Crv -> Move.G ; Series[Start=0,Step,Count=N] -> Z.F -> V -> Move.T -> Move.G {N stacked copies, capped so Count x Step stays within build-volume Z}
  Move.G -> Area.G -> C {centroid per copy} ; Series.S -> A-B.A ; Slider[B=1] -> A-B.B -> R -> Range.N ; Dom.I -> Range.D -> Range.R
  Range.R -> GraphMapper[Bezier, out domain capped e.g. 0-2] -> R -> Scale.F ; Area.C -> Scale.C ; Move.G -> Scale.G -> G {tapering tower}
  === Step 2: rotate + loft (twisted, NOT yet printable) ===
  Series[Step,Count] -> RotAx.A ; Scaled curves -> RotAx.G ; [vertical axis through base centroid] -> RotAx.X -> RotAx.G
  RotAx.G -> Loft.C -> L {untrimmed twisted loft: no thickness, not watertight}
  === Step 3: rebuild smooth-edged equivalent via isocurve extraction + Rail Revolution ===
  base curve -> Eval.C @ t=1 -> P -> SrfCP.P ; Loft.L -> SrfCP.S -> uvP -> Iso.uv ; Loft.L -> Iso.S -> U {isocurve} -> End.C -> S,E
  centroid -> Ln.A ; isocurve End -> Ln.B -> L -> Merge -> Join.C {reproduces the profile's silhouette as one open curve}
  Join.C -> Divide.C ; Slider[Count=28] -> Divide.N -> P -> Nurbs.V -> C {smooth freeform curve through the points}
  Nurbs.C -> RailRev.P (profile) ; Nurbs.C -> RailRev.R (rail) ; axis line -> RailRev.A -> S {smooth-edged surface of revolution}
  === Step 4: Box Morph back into the twisted-tower silhouette ===
  RailRev.S -> BBox.C -> B {reference box} -> DeBrep.B -> V -> Graft.D -> T -> BANG! -> (0)...(7)
  2 selected corners -> Move.G ; Slider[Factor] -> Z.F -> V -> Move.T {push 2 corners along Z} ; moved + 6 unmoved -> TBox.A..H -> B {target box}
  RailRev.S -> Morph.G ; BBox.B -> Morph.R ; TBox.B -> Morph.T -> Morph.G {smooth-edged surface re-morphed into the twisted silhouette}
  === Step 5: mesh, smooth, thicken ===
  Morph.G -> MeshUV.S ; Slider[U Count=100] -> .U -> M -> wbCatmullClark.M ; Slider[Level=2] -> .L -> O -> wbThicken.M ; Slider[Distance=2.0] -> .D -> O {watertight printable mesh}
  ```
- Tree handling notes: Corner points are Grafted then exploded via BANG! (Explode Tree) specifically so exactly 2 of the 8 Bounding-Box corners can be individually re-wired through Move while the other 6 pass through unchanged into Twisted Box's 8 named inputs.
- Failure modes: An untrimmed lofted surface, however refined, is explicitly NOT printable — no thickness, not watertight (fails geometric criterion G1) until capped and thickened; a printable model must also satisfy G2 (manifold — no edge shared by >2 faces), G3 (orientable — consistent face normals), G4 (no self-intersections), plus practical constraints C1 (build-volume size), C2 (minimum wall thickness, technology-dependent), C3 (X/Y and Z print resolution), C4 (gravity/self-support); non-manifold geometry can arise from overlapped/duplicated objects — exactly what the "Cull-Adjacent-Faces Cleanup" recipe (§8) is designed to fix before printing; STL export always triangulates regardless of source type, and Binary STL is preferred over ASCII for file size.
- Source: [STATED, AAD pt.4 p.320-329].

### Robotic-Cast Variable-Volume Piece Generation (DRG) [PARTIAL]
- Purpose: Drive a 6-axis robotic arm to reorient a casting mold and vary poured volume per piece, producing a family of varied-yet-similar cast elements from one mold instead of one mold per unique shape.
- Difficulty: advanced
- Chain: n/a — the raw source's own canvas screenshot ("GH PARAMETRIC SCRIPT," Figure 4) is stated to be illegible even after 5× re-render and 2× digital upscaling; only the stated PURPOSE is preserved: "Robotic code was created with a DRG Grasshopper component that outputs angle rotations and volume measurements for each piece," producing 40 individually varied doubly-curved wall elements in 14 hours.
- Tree handling notes: **[NOT IN SOURCE — tree structure not stated, diagram too small to confirm branch counts]**.
- Failure modes: None extractable — this recipe is preserved specifically to document that the source material exists and was consulted, per the "never invent wiring" requirement, rather than to supply usable wiring.
- Source: [STATED, AAD pt.5 p.348-349, Figure 4] [DIAGRAM ILLEGIBLE in source — component names, ports, and slider values below legibility threshold].

---

## 12. Recursion / Loops — HoopSnake & Loop Plug-in

### Why Native Loops Are Impossible + Two Workarounds
- Purpose: Understand the structural reason ordinary Grasshopper cannot express feedback loops, and the two available workarounds.
- Difficulty: intermediate
- Chain:
  ```
  {same definition} Move.G -/-> Divide.C {FORBIDDEN — a downstream output can never feed back into an upstream input; GH solves strictly left-to-right}
  Workaround A: manually duplicate the whole definition N times in sequence (line0 -> [copy 1] -> line1 -> [copy 2] -> line2 -> ... ), each copy's output feeding the next copy's input directly — a straight chain, not a real loop
  Workaround B: a loop-enabling plug-in (HoopSnake or Loop) — see recipes below
  ```
- Tree handling notes: n/a.
- Failure modes: Grasshopper's dependency graph is strictly acyclic — this is a directed-acyclic-graph constraint, not a stylistic guideline; the source marks the forbidden pattern with a literal red "no entry" icon over the offending wire.
- Source: [STATED, AAD pt.4 p.298-299] (echoing the same left-to-right rule first stated at [STATED, AAD pt.1 p.59]).

### HoopSnake Basic Recursive Iteration
- Purpose: Use the third-party HoopSnake plug-in to feed a procedure's own final output back into its start, enabling true recursion (e.g. recursive line subdivision, or the Koch snowflake fractal).
- Difficulty: advanced
- Chain:
  ```
  === Section: HoopSnake-driven line-division recursion ===
  Panel[Crv: line 0] -> HS.S {edge condition} ; Slider["Termination Condition",3] -> HS.B*
  HS.F -> Divide.C {every loop-body reference to the seed is redirected to HS.F instead}
  {...procedure to repeat: Divide -> Shatter -> Item -> Move...}
  Move.G -> HS.D* {closes the loop}
  HS.C -> panel {cumulative Data Tree of every iteration, one branch per iteration} ; HS.I -> iteration counter
  -- operationally: double-click HS to open its floating control panel; Step = one iteration; Auto Loop All = run until I == B*; Reset All
  === Section: Koch snowflake, one iteration body ===
  Shatter.S -> Item[i=1].L -> i {middle-third segment} -> Len.C -> L -> Eval["(x/2)*sqrt(3)"].x -> r {equilateral-triangle height}
  Item.i -> Offset.C ; (negated height) -> Offset.D -> C {raised "peak" segment}
  Shatter.S -> Cull(Cull Index)[i=1].L -> L {removes the original middle, keeps segments 0 and 2}
  Offset.C -> End.C -> S,E -> Ln×2 (connect segment-0-end to peak-start, peak-end to segment-2-start) -> L
  Cull.L, Ln1.L, Ln2.L, Offset.C -> Merge.D1-D4 -> R {one 4-segment "tent" polyline replacing the straight line — one Koch iteration}
  ```
- Tree handling notes: HS.C accumulates the result of EVERY iteration as its own branch of one Data Tree — this is how a HoopSnake-driven recursive definition exposes its full iteration history, not just the final result.
- Failure modes: HoopSnake does NOT run as part of GH's normal automatic solver pass — it is a separate "engine" that must be manually started via its own floating control panel (Step or Auto Loop All), and Reset All between test runs is easy to forget; a simple/schematic (low-poly) starting edge condition generally produces a more refined recursive result than an already-dense one, echoing the same principle observed for mesh subdivision (§8).
- Source: [STATED, AAD pt.4 p.298-303].

### HoopSnake 3D Fractal (iterated Delaunay + centroid offset)
- Purpose: Grow an increasingly spiky, self-similar tridimensional fractal from a single flat triangle by repeatedly offsetting each face's centroid along its normal and re-triangulating.
- Difficulty: advanced
- Chain:
  ```
  Panel[Pt: 3 seed points] -> Del(Delaunay Mesh).P -> Del.M -> HS.S {edge condition: initial single-triangle mesh}
  Slider["Termination Condition",3] -> HS.B* ; HS.F -> FaceN.M {loop body} -> FaceN.C (centroid), FaceN.N (normal)
  FaceN.N -> AxB.A ; Panel[factor] -> AxB.B -> R -> Move.T ; FaceN.C -> Move.G -> G {centroid offset along normal}
  Move.G merged with the mesh's existing vertices -> Del.P {re-triangulate all points, old + new offset centroid, per face} -> Del.M -> HS.D* {closes the loop}
  HS.C -> panel[Mesh] {after N iterations: flat triangle -> single raised peak -> repeated smaller peaks on each sub-face}
  ```
- Tree handling notes: n/a beyond the standard HoopSnake per-iteration branch accumulation described above.
- Failure modes: **[PARTIAL — diagram partially illegible in source]** the exact roles of wbEdges and a Cross Reference ("Holistic") step in the merge-before-retriangulate wiring are not fully resolved in the raw extraction; the overall 3-step procedure (triangulate → offset each face centroid along its normal → re-triangulate) is explicit in the surrounding body text.
- Source: [STATED, AAD pt.4 p.305] [DIAGRAM PARTIALLY ILLEGIBLE in source].

### Loop Plug-in (Rnd/Store/Loop) — Sphere-Chain Generator [PARTIAL]
- Purpose: Use the alternative "Generation" add-on (Rnd + Store + Loop components) to iterate a procedure by substituting the final component's output back into the initial component's input, driven by a Timer — demonstrated growing a chain of tangent spheres.
- Difficulty: advanced
- Chain:
  ```
  Rnd(domain 0-1, count 3, refreshed by Timer or Recompute).R -> Item[indices 0,+1,+2] {u,v params + a radius value}
  XY[plane] -> Sph.B ; Panel[1] -> Sph.R -> S {initial sphere}
  Sph.S -> Eval.S ; Pt(u,v) -> Eval.uv -> P (point on sphere), N (normal)
  Eval.N -> Amp.V ; (random radius) -> Amp.A -> V {normal scaled by random radius}
  Eval.P -> Move.G ; Amp.V -> Move.T -> G {new sphere center, tangent to the initial sphere}
  Move.G -> Sph2.B ; (random radius) -> Sph2.R -> S {new tangent sphere}
  Sph2.S -> Store.B ; Toggle[False] -> Store.E -> T {stores the new sphere between updates}
  Store.T -> Loop {replaces Evaluate Surface's reparameterized S-input with Move's G-output, refreshes Rnd, closes the loop on each Timer tick}
  ```
- Tree handling notes: n/a — each Timer tick grows the chain by one more sphere; not narrated as a tree-shape mechanism.
- Failure modes: **[PARTIAL — diagram partially illegible in source]** the exact per-input parameter wiring of the Osc, DArc, Dup, and Loop components (visible only as unresolved text fragments in the raw extraction: "Move," "Rnd," "Eval," "0," "9999," "1," "False," "True") could not be confirmed; overall behavior (a wandering chain of dark small-radius / light large-radius spheres, colored via a parallel Remap→RGB→Custom Preview branch) is confirmed by body text.
- Source: [STATED, AAD pt.4 p.306-309] [DIAGRAM PARTIALLY ILLEGIBLE in source].

---

## 13. Environmental Analysis — GECO / Ecotect

### GECO Cascading-Connection Pattern
- Purpose: Understand the shared E(nable)/out/D(one) convention that every GECO component uses to sequence dependent Ecotect calculations.
- Difficulty: intermediate
- Chain:
  ```
  Toggle[True] -> Link Ecotect.E -> out -> Panel {connectivity check; keep EcoLink isolated, wired only to a Panel}
  ComponentA.D -> ComponentB.E {cascade: B only fires once A's Ecotect operation actually finishes}
  ```
- Tree handling notes: n/a.
- Failure modes: EcoLink turning ORANGE = the Ecotect connection failed (recoverable by toggling E False then True again); RED = Ecotect or GECO itself is not installed properly (a re-toggle will not fix this); GECO components are named differently on their ribbon/panel vs. once placed on canvas (e.g. "EcoSolCal" → "Insolation Calculations") — both names are worth knowing when searching.
- Source: [STATED, AAD pt.6 p.446-449].

### Sun Path, Solar Ray Vector & Cast Shadow
- Purpose: Compute a sun-path diagram, a solar ray vector for a specific day/time, and the cast shadow of a mesh onto a plane.
- Difficulty: intermediate
- Chain:
  ```
  Toggle[True] -> EcoSunPath.E ; Slider[Day],[Month] -> .D,.M ; "weather file"(File Path) -> .W -> .C (sundial curve), .S (sun path curve)
  EcoSunPath.D -> EcoSunRays.E {cascade} ; Day,Month(reused) -> .D,.M ; Slider[Time] -> .T -> .P,.V (solar ray vector)
  EcoSunRays.P -> VDis.A ; EcoSunRays.V -> VDis.V {verify vector}
  Mesh -> MShadow.M ; EcoSunRays.V -> MShadow.L -> MShadow.O -> Boundary.S {shadow contour as a planar surface}
  ```
- Tree handling notes: n/a.
- Failure modes: Weather files from the US DOE arrive as .EPW (EnergyPlus) and CANNOT be read by Ecotect directly — convert to .WEA via Ecotect's own Weather Manager first.
- Source: [STATED, AAD pt.6 p.448-449].

### Responsive Skin Driven by Solar Incidence Angle
- Purpose: Vary a facade's per-panel aperture size based on how directly each panel faces the sun at a chosen day/time.
- Difficulty: advanced
- Chain:
  ```
  Srf -> MeshUV.S ; Slider[U,V Count] -> .U,.V -> M -> FaceB.M -> B (per-face boundary curves) ; -> FaceN.M -> C (centers), N (normals)
  FaceN.N -> VDis.V {verify normal points INSIDE for this workflow} ; Rev.V -> V {reverse if needed}
  EcoSunRays.V -> Angle.A ; Rev.V -> Angle.B -> A(radians) -> Bnd.N -> Bnd.I {source domain of computed angles}
  Slider[Domain start=0.95,end=0.1] -> Dom.I {target domain}
  Angle.A -> ReMap.V ; Bnd.I -> ReMap.S ; Dom.I -> ReMap.T -> ReMap.R {per-panel scale factor}
  FaceB.B -> Scale.G ; FaceN.C -> Scale.C ; ReMap.R -> Scale.F -> Scale.G(scaled edges)
  FaceB.B -> Graft.T -> T {original edges, grafted} ; Scale.G -> Graft.T -> T {scaled edges, grafted}
  Graft(orig), Graft(scaled) -> Merge.D1,D2 -> R -> Loft.C -> L {variable-aperture cladding skin}
  ```
- Tree handling notes: Both the original-edge stream and the scaled-edge stream are EXPLICITLY grafted before Merge, so Loft pairs original-to-scaled per branch rather than seeing a flat mismatched list — the same "graft before merge" rule as §3.
- Failure modes: Face-normal direction requirement is CONTEXT-DEPENDENT and easy to get backwards: for THIS workflow (solar-incidence-driven skin) normals must point INSIDE the geometry, matching the solar ray's sense (Reverse if they point outward, as they did by default in the source's own example) — contrast with the Export-to-Ecotect recipe below, where normals must point OUTSIDE; always verify with Vector Display before proceeding; scale-factor values from the Remap must stay within domain (0,1] or the recipe breaks the same way "Scale factor of exactly zero" does elsewhere.
- Source: [STATED, AAD pt.6 p.450-452].

### Export Mesh to Ecotect + Import Analysis Results (insolation)
- Purpose: Push Grasshopper mesh geometry into Ecotect for analysis, then pull calculated per-face results (e.g. insolation) back into Grasshopper as a colored mesh.
- Difficulty: advanced
- Chain:
  ```
  Mesh -> Explode.M -> F -> FaceN.M -> C,N -> VDis {verify normals point OUTWARD for export}
  Explode.F -> Flatten.T -> T {REQUIRED — otherwise only the tree's LAST branch is exported}
  Toggle[True] -> ExportMeshToEcotect.E ; Flatten.T -> .M ; [C,N,F,T,M,Z optional: scale, delete-mode, grid-fit, ElementType, material, zone]
  ExportMeshToEcotect.D -> InsolationCalculations.E {cascade} ; "weather file" -> .W ; Slider[SkySubdivision] -> .S
  InsolationCalculations.D -> ObjectRequest.E {cascade} ; ExportMeshToEcotect.I -> ObjectRequest.I (face indices) ; .[A]=AttributeIndex
  ObjectRequest.RGB -> Graft.T -> T ; Mesh -> Graft.T -> T -> MCol.M,.C -> M {colour-mapped mesh}
  ```
- Tree handling notes: Mesh Explode's F output MUST be Flatten-ed before EcoMeshExport.M — without flattening, Ecotect silently imports ONLY the faces in the tree's last branch, dropping the rest without an error. Mesh and RGB-colour streams are each independently grafted before Mesh Colours, per the same graft-before-pair rule used throughout §3.
- Failure modes: Ecotect works EXCLUSIVELY on mesh geometry — never export NURBS/Breps directly; face-normal direction requirement here is the OPPOSITE of the Responsive-Skin recipe (must point outward, not inward) — do not conflate the two; the export [C] scale factor must match unit systems (0 = Rhino document already in mm; 1000 = Rhino document in meters) or geometry imports at the wrong scale; export [N]=2 (keep existing Ecotect geometry) "may lead to overlapping errors" if the two exported mesh sets are not guaranteed non-overlapping; Sky Subdivision trades accuracy for speed (smaller = more accurate/slower; the special value 50 is an explicit fast/approximate shortcut, not "more detailed").
- Source: [STATED, AAD pt.6 p.453-460].

### Analysis Grid — Auto-Fitted vs. Manually-Defined
- Purpose: Set up a grid of point-sensors for Ecotect analysis (e.g. daylight/visual comfort inside a room), either auto-fitted to already-exported geometry or manually specified.
- Difficulty: advanced
- Chain:
  ```
  === Auto-fitted ===
  ExportMeshToEcotect.D -> FitGrid.E {cascade} ; Slider[GridAxis,Type,CountCx/Cy/Cz] -> FitGrid -> D -> ImportAnalysisGrid.E {cascade}
  ImportAnalysisGrid.(P,U,V,H) -> MeshGrid.(P,U,V,H) ; .RGB/.Val -> MeshGrid.C -> M {colored grid mesh}
  === Manually defined ===
  Toggle[True] -> 2dAnalysisGrid.E ; Slider[GridAxis] -> .A ; Dom[W], Dom[H] -> .[W],[H] ; Slider[Cw,Ch] -> .[Cw],[Ch] -> out, D
  === Visual comfort of a room (east-facing glazing), combining export + grid + lighting calc ===
  "window" mesh -> ExportMeshToEcotect(1)[ElementType=6] ; "panels" mesh (flattened) -> ExportMeshToEcotect(2)[ModelNew=2, keeps window geometry]
  ExportMeshToEcotect(2).D -> FitGrid.E {cascade} -> LightingCalculations.E {cascade, Precision, Sky(lux)Illuminance} -> ImportAnalysisGrid.E {cascade}
  ImportAnalysisGrid.(P,Val) -> Tag.L,.T {numeric values tagged directly at each grid point in the viewport}
  ```
- Tree handling notes: n/a beyond the standard GECO cascade convention.
- Failure modes: Eco2DGrid's [W]/[H] domains should both be positive or both negative so the grid lies entirely within ONE quadrant of Rhino's space; when chaining two EcoMeshExport calls into the same scene, the second must set ModelNew=2 to avoid deleting the first export's geometry — but this is only safe when the two mesh sets are genuinely non-overlapping (as with a window/panels partition of one box); sky illuminance (lux) varies systematically with latitude and should be looked up rather than assumed.
- Source: [STATED, AAD pt.6 p.459-464].

### Graphical Statics Funicular Form-Finding [PARTIAL]
- Purpose: A pragmatic, non-simulation alternative to Kangaroo hanging-chain form-finding: construct a reversed catenary/funicular form by classical graphical-statics vector construction (form diagram / force diagram / pole method), then use Goat to minimize axial force and size a vault's thickness.
- Difficulty: advanced
- Chain:
  ```
  === Section: Graphical statics reversed-catenary (conceptual, no GH canvas shown) ===
  [loads] -> initial force diagram {L1,L2,L3} -> tangent-vector construction -> initial pole p1 -> initial form polygon
  -> per-segment loads {L1',L2',L3'} -> trial pole pt -> trial form polygon -> point Y' via centerline intersection
  -> final pole pf -> final force diagram -> final form diagram (through point Y) = the funicular/reversed-catenary shape
  Goat.Objective <- length of vectors in the final force diagram (axial force) [Goat set to Minimize]
  axial force P -> F_allow = P/A -> t = P[lb] / (12in * F_allow[lb/in^2])  {vault thickness}
  ```
- Tree handling notes: n/a.
- Failure modes: **[PARTIAL — conceptual only, no component-level GH canvas shown in source]** the only named Grasshopper-specific element is the Goat solver itself; the full 13-step vector construction is geometric/manual, not diagrammed as GH wiring in the extracted pages (the complete .gh file is stated to be available only via an external link, outside the extraction). The source explicitly cautions this demonstrates "pragmatic data logic only" — it does not account for all real imposed loads and must be reviewed by a qualified engineer; minimum/maximum rise-to-span ratios and minimum thickness must be enforced deliberately via slider ranges and conditional logic, not derived automatically.
- Source: [STATED, AAD pt.6 p.467-471] [NOT IN SOURCE: component-level wiring for the vector construction itself].

---

## Stats

```
TOTAL RECIPES: 96

By category:
  1. Fundamentals — Points, Curves, Vectors ........................ 13
  2. List Operations ................................................ 9
  3. Data-Tree Manipulation & List Matching ........................ 15
  4. Attractor Patterns .............................................. 6
  5. Grids & Paneling ............................................... 10
  6. Surface Subdivision & Morphing .................................. 5
  7. Curvature & Developable-Surface Analysis ........................ 3
  8. Mesh & Subdivision .............................................. 8
  9. Physics / Form-Finding — Kangaroo ............................... 8
  10. Optimization — Goat / Galapagos / Karamba / Millipede .......... 5
  11. Fabrication — Sectioning, Waffling, Printing ................... 4
  12. Recursion / Loops — HoopSnake & Loop Plug-in ................... 4
  13. Environmental Analysis — GECO / Ecotect ........................ 6

MERGED-DUPLICATE RECIPES (same pattern consolidated from 2+ source locations,
both citations preserved): 12
  - Curve Division Family (AAD pt.1/2/3 + Essential pt.1)
  - Robust Curve-Midpoint Evaluation (AAD pt.3 + Essential pt.1)
  - Container Components & Data-Source Precedence (AAD pt.1 + Essential pt.1)
  - Curve-Aligned Circles -> Loft (Essential pt.1 + AAD pt.1)
  - List Item vs Cull Index (AAD pt.1 + Essential pt.1)
  - Dispatch (AAD pt.2 + Essential pt.1)
  - Shift List with Wrap (AAD pt.1 + Essential pt.1)
  - Sort List + Reverse List (AAD pt.2 + Essential pt.1)
  - List/Data Matching: Longest/Shortest/Cross Reference (AAD pt.2 + Essential pt.1)
  - Cartesian-Product Grid via Cross Reference (AAD pt.2 + Essential pt.1)
  - Custom Cyclic-Repeat Matching (AAD pt.2 + Essential pt.1)
  - Grafting for Full Cross-Product Pairing (Essential pt.2 + AAD pt.6)
  - Diagonal Grid / Diagrid Connectivity — 3 methods (AAD pt.1 + AAD pt.3 + Essential pt.2)
  - Image-Sampler-Driven Attractor Pattern (AAD pt.3 + AAD pt.4)
  - Flattening a Tree to a Single List (Essential pt.2 + AAD pt.3 + AAD pt.6)
  [note: 15 merge points listed above across 12 recipe entries; several recipes
   merge 3 source locations rather than 2]

PARTIAL RECIPES (diagram illegible / no GH canvas in source — wiring not invented): 10
  - Voronoi Pattern Projected onto a Freeform Surface (§5)
  - Chebyshev-Net Equal-Edge-Length Grid (§5) — no GH canvas at all
  - Cull-Adjacent-Faces Cleanup for Joined Mesh-Box Aggregations (§8)
  - Faceted Pyramidal Panelization via Delaunay on a Freeform Surface (§8)
  - Shell Force for Bending Resistance — 4-input Merge source (§9)
  - Waffle Joint — Boolean-Difference Interlocking Slots (§11) — component names not given
  - Robotic-Cast Variable-Volume Piece Generation (DRG) (§11) — fully illegible diagram
  - HoopSnake 3D Fractal (§12) — partial wiring illegible
  - Loop Plug-in Sphere-Chain Generator (§12) — partial wiring illegible
  - Graphical Statics Funicular Form-Finding (§13) — conceptual only, no GH canvas
```
