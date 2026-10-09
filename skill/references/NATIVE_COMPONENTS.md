# Grasshopper Component Reference

Synthesized from AAD (Tedeschi/Wirz/Andreani, *Algorithms-Aided Design*, 2014) and Essential Algorithms and Data Structures for Grasshopper (2nd ed., Rajaa Issa). Every entry is derived strictly from these two sources; nothing has been added from general Grasshopper knowledge unless the source itself flagged a value as [GENERAL]/[INFERRED]. Type GUIDs are attached only where a component's name matches an entry in `guid-map.json` (127 names confirmed present in real .ghx files).

Provenance tags: `[STATED, AAD p.X]` / `[STATED, Essential p.X]` = explicitly stated in that source. `[INFERRED]` = reasoned from a diagram/context by the extraction, not asserted outright by the book. `[GENERAL]` = general Grasshopper knowledge the source itself invoked without claiming it as the book's own statement. `[CONFLICT: ...]` = sources disagree; both positions kept. "Inputs (partial per source)" = the source's own diagrams/text did not fully explain every port.

## Table of Contents

- [Params](#params) — 20 components
- [Maths](#maths) — 28 components
- [Sets](#sets) — 32 components
- [Vector](#vector) — 19 components
- [Curve](#curve) — 33 components
- [Surface](#surface) — 28 components
- [Mesh](#mesh) — 16 components
- [Intersect](#intersect) — 2 components
- [Transform](#transform) — 8 components
- [Display](#display) — 6 components
- [Tab unconfirmed](#tab-unconfirmed) — 3 components
- [Third-party plugins](#third-party-plugins) — ~60 components across 13 plugins (LunchBox, Weaverbird, Kangaroo, Karamba, Millipede, Goat, GECO, HoopSnake, Tree8, Mesh Edit, Generation, Elk/Finches/gHowl)
- [Special / Solver](#special--solver) — 2 components (Galapagos, Gene Pool)
- [Coverage stats](#coverage-stats)

---

## Params

### Number Slider
- Tab: Params > Input | Type GUID: 57da07bd-ecab-415d-9d86-af36d7073abc
- Inputs: none (input component; user-editable)
- Outputs: single number within a domain
- Behavior: Properties dialog (double-click the slider's name) exposes Name, Expression, Grip Style, Rounding (R=float, N=integer, E=even, O=odd), Digits, Numeric domain (Min/Max/Range), Numeric value. Canvas search-box shorthand: bare number → slider at that value with default domain 0-10; `min<value<max` → explicit domain; decimal → Rounding=R, domain 0-1; `min-value` → negative preset, domain 0 to -10 (visually ambiguous with typing a lone `-`, which instead recalls Subtraction).
- Provenance: [STATED, AAD p.44, 46, 73]

### Panel
- Tab: Params > Input | Type GUID: 59e0b89a-e487-49f8-bab8-b5bab16be14c
- Inputs: any data
- Outputs: passthrough/display only
- Behavior: Visualization/inspection tool displaying a component's output as text; for lists shows a path header (e.g. `{0;0}`) and a numbered `index | datum` table. Typing text and pressing Enter does not commit — must confirm via the Panel Properties OK button.
- Provenance: [STATED, AAD p.63, 71, 109, 128; Essential p.9-10, 53]

### Boolean Toggle
- Tab: Params > Input | Type GUID: 2e78987b-9dfb-42a2-8b76-3923ac8bd91a
- Inputs: none (input component)
- Outputs: single Boolean (True/False)
- Behavior: Clickable button toggling True/False by left-clicking; combined into ordered Boolean-pattern lists via Merge.
- Provenance: [STATED, AAD p.78]

### Colour Swatch
- Tab: Params > Input | Type GUID: 9c53bac0-ba66-40bd-8154-ce9829b9db1a
- Alias: Swatch
- Inputs: none (input component)
- Outputs: a color (with alpha/transparency)
- Behavior: Color and transparency set via a context menu opened by left-clicking the swatch; feeds Custom Preview's S-input.
- Provenance: [STATED, AAD p.67]

### Gradient
- Tab: Params > Input
- Inputs: L0, L1 (colors at the two ends of the gradient), t (parameter, 0-1)
- Outputs: color at t
- Behavior: Special input-type component mapping a 0-1 parameter to an interpolated color; right-click to choose a color preset.
- Provenance: [STATED, AAD p.114-115]

### Graph Mapper
- Tab: Params > Input | Type GUID: bc984576-7aa6-491f-a91d-e444c33675a7
- Inputs: a value or list of values (typically 0-1)
- Outputs: same count of values, remapped through a user-editable graph curve
- Behavior: Unlike Remap Numbers (strictly linear), lets the designer draw/control an arbitrary non-linear remapping curve via an internal Graph Editor with TWO independent domains (input domain A, output codomain B — both must be set correctly or the mapping is silently wrong). Graph type chosen from None, Bezier, Conic, Gaussian, Linear, Parabola, Perlin, Power, Sinc, Sine, Sine Summation, Square Root; draggable on-canvas "grip" handles reshape the curve. Right-click also offers Enabled, Runtime warnings, Wire Display, Reverse, Flatten, Graft, Simplify, Locked, Default. GOTCHA: cannot have its internal curve driven by a Number Slider, and therefore cannot itself be wired as a Genome variable into Galapagos — expose the upstream sliders that feed it instead.
- Provenance: [STATED, AAD p.151, 199-202, 323, 483-484; Essential p.51]

### Image Sampler
- Tab: Params > Input | Type GUID: d69a3494-785b-4beb-969b-d2373f65abfd
- Inputs: point(s) with UV coordinates in [0,1]x[0,1] (or per configured X/Y Domain)
- Outputs: list of numbers (intensity values), or colour values for RGB/colour images
- Behavior: Configured via "Image Sampler Settings" dialog: X/Y Domain (default 0-1), Tiling, Channel (R/G/B/A/Hue/Sat/.../grayscale), Interpolate checkbox, File path, Auto update, Save in file, Preview. Treats a raster image as a continuous 2D scalar field; pure-black areas return intensity=0, an invalid Scale factor — must be floored via Maximum against a small nonzero value.
- Provenance: [STATED, AAD p.203-206, 207-209, 288-289]

### MD Slider
- Tab: Params > Input
- Outputs: a 2D (u,v) value pair, default range [0,1]x[0,1]
- Behavior: "Multi dimensional slider" — drag a point within a 2D grid area to set u and v simultaneously; bidimensional extension of Number Slider.
- Provenance: [STATED, AAD p.144]

### Point (container)
- Tab: Params > Geometry | Type GUID: fbac3e32-f100-4292-8692-77240a42fd1a
- Alias: Pt
- Inputs: optional set-from-Rhino data
- Outputs: Pt (stored point)
- Behavior: Black-hexagon container component; right-click offers Set one Point / Set Multiple Points / Manage Point collection. Distinct from the standard "Construct Point" component despite sharing the "Pt" abbreviation on canvas — the container just stores/references, Construct Point computes from X/Y/Z. If the referenced Rhino geometry is deleted, the container turns orange (data lost) unless "Internalise data" was used first.
- Provenance: [STATED, AAD p.49-52; Essential p.12]

### Curve (container)
- Tab: Params > Geometry | Type GUID: d5967b9f-e8ee-436b-a8ad-29fdcecf32d5
- Alias: Crv
- Outputs: Crv (stored curve)
- Behavior: Collects curve geometry only; cannot collect points (container components expect their own specific geometry type).
- Provenance: [STATED, AAD p.51]

### Geometry (container)
- Tab: Params > Geometry | Type GUID: ac2bc2cb-70fb-4dd5-9c78-7e1ea97fe278
- Alias: Geo
- Outputs: Geo (stored geometry, any type)
- Behavior: Versatile catch-all container storing any geometry type (points, curves, solids, etc.); right-click offers Set one Geometry / Set Multiple Geometries.
- Provenance: [STATED, AAD p.51-52]

### Boolean (parameter)
- Tab: Params > Primitive | Type GUID: cb95db89-6165-43b6-9c41-5702bc5bf137
- Alias: Bool
- Outputs: Bool (True/False)
- Provenance: [STATED, Essential p.13]

### Text (parameter)
- Tab: Params > Primitive | Type GUID: 3ede854e-c753-40eb-84cb-b48008f14fd4
- Alias: Txt
- Outputs: Txt (string)
- Provenance: [STATED, Essential p.13]

### Number (parameter)
- Tab: Params > Primitive | Type GUID: 3e8ca6be-fda8-4aaf-b5c0-3c54c8bb7312
- Alias: Num
- Inputs: internal numeric value or cast input (e.g. text)
- Outputs: Num
- Behavior: Shows error "Data conversion failed from Text to Number" when input can't cast (e.g. "12AB" fails, "12" succeeds).
- Provenance: [STATED, Essential p.13, 15]

### Domain (parameter)
- Tab: Params > Primitive | Type GUID: 15b7afe5-d0d0-43e1-b894-34fcfe3be384
- Outputs: Domain (e.g. "0 To 15")
- Provenance: [STATED, Essential p.14]

### Vector (parameter)
- Tab: Params > Primitive | Type GUID: 16ef3e75-e315-4899-b531-d3166b42dac9
- Alias: Vec
- Outputs: Vec
- Provenance: [STATED, Essential p.14]

### Transform (matrix parameter)
- Tab: Params > Primitive | Type GUID: 28f40e48-e739-4211-91bd-f4aefa5965f8
- Inputs: internal, or from Move's X output
- Outputs: 4x4 transformation matrix display
- Provenance: [STATED, Essential p.14]

### Param Viewer / Parameter Viewer
- Tab: Params > Util | Type GUID: 72a29b54-2e48-474b-a400-d2124c4edf79
- Inputs: any data
- Outputs: none (double-click opens a graphical Data Tree structure visualizer)
- Behavior: Two display modes recorded across sources: a text/list summary ("Data with N branches, {0} N=5") and a graphical radial-tree diagram (branches drawn as a radial tree with leaf/root dots). Used as a debugging tool to confirm a tree-restructuring operation (e.g. Flip Matrix) had the intended effect.
- Provenance: [STATED, AAD p.18, 225; Essential p.18, 30, 33, 53-54] — AAD's "Param Viewer" and Essential's "Parameter Viewer" are treated as the same component (identical behavior described).

### Quick Graph
- Tab: Params > Display (grouped as an "analysis" tool)
- Inputs: numeric list
- Outputs: visual plotted graph of values
- Provenance: [STATED, Essential p.18, 30]

### File Path
- Tab: Params > Primitive
- Behavior: Right-click "Set One File Path" to load a file (e.g. a .WEA weather file for GECO); renamed "weather file" in the book's examples.
- Provenance: [STATED, AAD p.445, 448]

---

## Maths

### Addition
- Tab: Maths > Operators | Type GUID: a0d62394-a118-422d-abb3-6af115c75b25
- Alias: A+B
- Inputs: A, B (numbers or lists)
- Outputs: R (sum)
- Behavior: Adds two numbers or lists item-by-item; used to sum two attractor distance fields, and repeatedly as the generic "combine two branch/tree values" operator throughout the data-tree tutorials.
- Provenance: [STATED, AAD p.6, 9-10, 116; Essential p.6, 9-10]

### Subtraction (A-B)
- Tab: Maths > Operators
- Alias: A-B
- Inputs: A, B (numbers)
- Outputs: R (A minus B)
- Behavior: Used to compute (Fitness − target) ahead of Absolute Value for goal-seeking optimization, and to compute relative angles/counts elsewhere.
- Provenance: [STATED, AAD p.191, 193, 323, 439]

### Multiplication
- Tab: Maths > Operators | Type GUID: ce46b74e-00c9-43c4-805a-193b69ea4a11
- Alias: AxB
- Inputs: A, B (numbers)
- Outputs: R (product)
- Behavior: Used e.g. to visually exaggerate a tiny displacement value for deformed-shape preview without altering the real value; also as the Rest-Length-Factor multiplier in Kangaroo recipes.
- Provenance: [STATED, AAD p.187, 289, 425; Essential p.16]

### Division
- Tab: Maths > Operators
- Alias: A/B
- Inputs: A, B (numbers or lists)
- Outputs: R (quotient)
- Behavior: Used to normalize a distance field by an "operating range" constant, and generically for radius = length/2 calculations.
- Provenance: [STATED, AAD p.117; Essential p.52]

### Larger Than
- Tab: Maths > Operators
- Alias: Larger (canvas nickname)
- Inputs: A (number), B (number)
- Outputs: `>` (bool, A>B), `>=` (bool, A>=B)
- Behavior: RESOLVED — real, standing GH1 component. Essential documents it (as "Larger"); AAD has no dedicated entry for it, which is a coverage gap in that source rather than a factual error to reconcile.
- Provenance: [STATED, Essential p.15, 17-18, 21-22] [VERIFIED https://grasshopperdocs.com/components/grasshoppermaths/largerThan.html]

### Smaller
- Tab: Maths > Operators
- Inputs: A (number), B (number)
- Outputs: `<` (bool), `<=` (bool)
- Provenance: [STATED, Essential p.18]

### And
- Tab: Maths > Logic
- Inputs: A (bool), B (bool)
- Outputs: R (bool)
- Provenance: [STATED, Essential p.18]

### Not
- Tab: Maths > Logic
- Inputs: A (bool)
- Outputs: R (bool, negated)
- Provenance: [STATED, Essential p.21-22]

### Xnor
- Tab: Maths > Logic
- Inputs: A (bool), B (bool)
- Outputs: R (bool — true when A and B match)
- Behavior: Used to build a "within range" flag, true only when neither below-min nor above-max is true.
- Provenance: [STATED, Essential p.25, 29-31]

### Equals
- Tab: Maths > Operators
- Inputs: A, B
- Outputs: `=` (bool)
- Provenance: [STATED, Essential p.25, 30-31]

### Mod (Modulus / Remainder)
- Tab: Math > Operators | Type GUID: 431bc610-8ae1-4090-b217-1a9d9c519fe2
- Inputs: A (number), B (number)
- Outputs: R (remainder of A/B)
- Behavior: Used in generic arithmetic chains and to test even/odd (remainder of dividing by 2, compared to 0 via Equals).
- Provenance: [STATED, Essential p.25, 31]

### Mass Addition
- Tab: Maths (exact sub-tab not stated in any source) [NOT IN SOURCE: sub-tab placement] | Type GUID: 5b850221-b527-4bd6-8c62-e94168cd6efa
- Alias: MA
- Inputs: I (Numbers, list)
- Outputs: R (Result, sum), Pr (Partial Results, running accumulation)
- Behavior: Sums a list of numbers; behavior depends entirely on input structure — a single item returns itself (R = the item, identity sum), a flat list returns one number (the grand-total sum of the whole list), and a tree returns one sum PER BRANCH, never a single grand total across the whole tree (canonical demo: item `1` -> R=1; list `[1,2,3,4]` -> R=10; tree `[1,2,3,4]/[5,6,7]/[8,9]` -> R=[10,18,17]) — item/list/tree behavior per data-trees.md's Mass Addition demo. Pr exposes the running/partial accumulation alongside the final R.
- Provenance: [STATED, Essential p.24, p.33 via data-trees.md/patterns.md]

### Minimum
- Tab: Maths > Util
- Alias: Min
- Inputs: A (list of numbers), B (comparison number)
- Outputs: R (list)
- Behavior: Element-wise clamps each value in A exceeding B down to B — NOT a list-reduction "smallest value" statistic; caps e.g. scale factors at a maximum.
- Provenance: [STATED, AAD p.117-118, 178]

### Maximum
- Tab: Math > Operators
- Alias: Max
- Inputs: A, B (numbers)
- Outputs: R (larger of A,B)
- Behavior: Used to floor near-zero/zero values, e.g. clamping Image-Sampler-derived scale factors up to a minimum (like 0.1) to avoid Scale's "F cannot be 0" error.
- Provenance: [STATED, AAD p.205]

### Absolute
- Tab: Math > Operators | Alias: Abs
- Inputs: x (number)
- Outputs: y (absolute value)
- Behavior: Used after Subtraction so a Fitness magnitude (not sign) is minimized toward a target; also used to make Mean Curvature values usable as a physical radius (curvature can be negative by sign convention).
- Provenance: [STATED, AAD p.178, 439]

### Negative
- Tab: Math > Operators | Alias: Neg
- Inputs: x (number)
- Outputs: y (= -x)
- Provenance: [STATED, AAD p.194, 303]

### Negate (vector) — MERGED into Reverse (vector)
- Status: CORRECTED — no standalone "Negate" vector component exists in GH1. This AAD p.376 usage (turning a +Z Unit vector into a gravity-pointing -Z direction for the Catenary component's G input) is the same real component as **Reverse (vector)** under the Vector tab below (identical V→V port shape, identical sign-flip behavior). Merged into that entry; see Vector > Vector > Reverse for the full spec. The alias "Neg" recorded here is likely a conflation with the Maths **Negative** component's real alias "Neg" (a scalar, not vector, operation).
- Provenance: [STATED, AAD p.376] [CORRECTED, VERIFIED https://grasshopperdocs.com/components/grasshoppervector/reverse.html] [see also https://grasshopperdocs.com/components/grasshoppermaths/negative.html]

### Factorial
- Tab: Math > Operators
- Alias: Fac
- Inputs: N (number)
- Outputs: F (factorial)
- Provenance: [STATED, Essential p.16]

### Sine
- Tab: Math > Trig
- Alias: Sin
- Inputs: x (angle in radians)
- Outputs: y (sine value)
- Provenance: [STATED, Essential p.16]

### Radians
- Tab: Math > Trig | Type GUID: a4cd2751-414d-42ec-8916-476ebf62d7fe
- Alias: Rad
- Inputs: D (degrees)
- Outputs: R (radians)
- Behavior: GH math/trig components only accept radians — degree inputs must always be converted first (e.g. before Rotate/Rotate Axis).
- Provenance: [STATED, AAD p.189; Essential p.16, 20]

### Angle
- Tab: Vector > Vector
- Inputs: A (vector 1), B (vector 2), P (optional plane)
- Outputs: A (angle in radians), R (reflex angle)
- Behavior: Measures incidence angle between two vectors (e.g. solar ray and face normal) to drive a dependent parameter such as facade aperture size.
- Provenance: [STATED, AAD p.451]

### Expression
- Tab: Maths > Script | Type GUID: 9df5e896-552d-4c8c-b9ca-4fc147ffa022
- Inputs: user-named variables (e.g. x, y, n)
- Outputs: R (result of typed expression, e.g. "(x+y)*y", "n! + Sin(Rad(n))", "((a+b)*c)%d")
- Behavior: Variable "x" always represents "the supplied input" when set inline on a component's own input (right-click > Expression). Preferred consolidation technique once several chained numeric ops are involved, versus a verbose component chain. Confirmed a real, distinct component from Evaluate F(X) (Maths > Script, above) — both ship in current GH1 and do almost the same thing, differing in whether the formula is a pin (Evaluate) or typed inline (Expression).
- Provenance: [STATED, Essential p.16-17, 25] [VERIFIED https://grasshopperdocs.com/components/grasshoppermaths/expression.html]

### Evaluate F(X) [DISAMBIGUATION 1 of 3 — see Evaluate Curve, Evaluate Length under Curve tab; all three render as an identical plain "Eval" box]
- Tab: Maths > Script
- Alias: Evaluate / Eval
- Inputs: F (function/expression text), x (and other variables as needed, e.g. y)
- Outputs: r (result/codomain values)
- Behavior: Evaluates a mathematical function/expression (authored via "Expression Designer," double-click, or via a Panel wired into F) against input numeric values; supports arithmetic, comparisons (=,<,>,<=,!=), `if(test,A,B)` conditional syntax (dynamically typed), and `Contains(s,p)` membership/substring testing. Distinguish from the other two "Eval" components by its F/x/y ports and its Maths > Script tab. RESOLVED — Essential's "Expression" component (above) is a separate, real component (both ship in current GH1); they behave almost identically but Expression has the formula authored inline (no separate F pin) while Evaluate takes the formula as its own input pin. Correctly kept as distinct entries, not merged.
- Provenance: [STATED, AAD p.101-102, 107-111, 178-179, 198, 292, 303, 375] [VERIFIED https://grasshopperdocs.com/components/grasshoppermaths/evaluate.html] [VERIFIED https://discourse.mcneel.com/t/expression-vs-evaluate-component/51839]

### Construct Domain
- Tab: Maths > Domain
- Alias: Dom
- Inputs: A (start), B (end)
- Outputs: I (domain)
- Behavior: Builds a numeric domain [A,B] from two numbers; also used for EcoSolCal's day-of-year and time-of-day domain inputs.
- Provenance: [STATED, AAD p.100, 198, 309, 323, 375, 452]

### Deconstruct Domain (DeDomain)
- Tab: Maths > Domain | Type GUID: 825ea536-aebb-41e9-af32-8baeb2ecb590
- Inputs: I (domain)
- Outputs: S (start value), E (end value)
- Behavior: Used to deconstruct a curve's domain into numeric start/end (e.g. to compute a custom midpoint via Expression), and to extract "the length of the longest list" from a Bounds-computed domain of list-lengths (E = max).
- Provenance: [STATED, Essential p.24, 48]

### Bounds
- Tab: Maths > Domain | Type GUID: f44b92b0-3b5b-493a-86f4-fd7408c3daf3
- Alias: Bnd
- Inputs: N (numbers)
- Outputs: I (interval/domain spanning min-max)
- Behavior: Automatically computes the min/max domain of a list of numbers; commonly paired with Remap Numbers as the auto-derived source domain instead of hardcoding it.
- Provenance: [STATED, AAD p.112, 233, 287, 452; Essential p.18, 20, 22-23, 30-31, 48]

### Remap Numbers
- Tab: Maths > Domain | Type GUID: 2fcc2743-8339-4cdf-a046-a1f17439191d
- Alias: ReMap
- Inputs: V (value(s) to remap), S (source domain), T (target domain)
- Outputs: R ("Mapped", Number — remapped value, may exceed the target domain if the input V fell outside the source domain S), C ("Clipped", Number — remapped value clamped/constrained to stay within the target domain's min/max bounds)
- Behavior: Rescales a list of numbers proportionally from a source domain to a target domain (strictly linear — contrast Graph Mapper's non-linear remap). Core of the "attractor" recipe (Distance → Bounds → Remap Numbers → apply to transform parameter). Inverting the target domain's start/end inverts which end of the effect is near/far. CONFIRMED — the KB's own inferred description of C (GH's clamping-to-target-domain behavior) was accurate.
- Provenance: [STATED, AAD p.112, 117, 233, 287, 451-452; Essential p.20, 22-23, 30-31] [VERIFIED https://grasshopperdocs.com/components/grasshoppermaths/remapNumbers.html]

### Divide Domain²
- Tab: Maths > Domain
- Alias: Divide
- Inputs: I (2D domain), U (U count), V (V count)
- Outputs: S (list of uv sub-domains)
- Behavior: Evenly divides a bidimensional domain into a grid of sub-domains for Isotrim to cut along.
- Provenance: [STATED, AAD p.149, 178]

### Deconstruct Domain²
- Tab: Maths > Domain
- Alias: DeDom2
- Inputs: I (2D domain)
- Outputs: U (1D u-domain), V (1D v-domain)
- Provenance: [STATED, AAD p.151]

### Construct Domain²
- Tab: Maths > Domain
- Alias: Dom²
- Inputs: U (1D u-domain), V (1D v-domain)
- Outputs: I² (2D domain)
- Behavior: Reassembles two 1D domains into one 2D domain (inverse of Deconstruct Domain²).
- Provenance: [STATED, AAD p.151]

---

## Sets

### List Item
- Tab: Sets > List | Type GUID: 59daf374-bc21-4a5e-8282-5504fb7ae9ae
- Alias: Item
- Inputs: L (list), i (index or list of indices), W (Wrap, Boolean)
- Outputs: i (item(s) at specified index/indices)
- Behavior: First "filter" component many of the tutorials build on — extracts datum/data at numeric position(s); if i is a list, returns a filtered sub-list. On a tree, selecting a fixed index per branch operates per-branch. A "zoomed" variant adds extra output params (+1..+6), an alternative to wiring several List Item components.
- Provenance: [STATED, AAD p.72-75, 189, 232, 242; Essential p.19, 37, 65, 68]

### Cull Index
- Tab: Sets > Sequence (RESOLVED — AAD p.179's "Sets > List" citation is an internal inconsistency in the source, mixing this up with the neighboring List panel; Sequence is correct)
- Alias: Cull i
- Inputs: L (list), I (index or indices to remove), W (Wrap, Boolean)
- Outputs: L (list with specified index/indices deleted)
- Behavior: The "reverse function" of List Item — deletes specified item(s), keeps everything else.
- Provenance: [STATED, AAD p.76-77, 82, 179, 292] [VERIFIED https://grasshopperdocs.com/components/grasshoppersets/cullIndex.html]

### Cull Pattern
- Tab: Sets > Sequence (RESOLVED — AAD p.107-108/178's "Sets > List" citation is an internal inconsistency in the source; Sequence is correct) | Type GUID: 008e9a6f-478a-4813-8c8a-546273bc3a6b
- Alias: Cull
- Inputs: L (list), P (repeating Boolean pattern — has a built-in "Invert" toggle to select the complementary subset from the same pattern list)
- Outputs: L (filtered list)
- Behavior: Keeps items aligned with True in the pattern, removes items aligned with False; the pattern automatically tiles/repeats across the entire input list (or, on a tree, across each branch independently). Discards the unwanted subset entirely — contrast Dispatch, which preserves both subsets as separate outputs.
- Provenance: [STATED, AAD p.78-80, 107-108, 178; Essential p.19, 22-23, 38, 40, 50, 69, 96] [VERIFIED https://grasshopperdocs.com/components/grasshoppersets/cullPattern.html]

### Shift List
- Tab: Sets > List | Type GUID: 4fdfe351-6c07-47ce-9fb9-be027fb62186
- Alias: Shift
- Inputs: L (list), S (shift offset, integer), W (Wrap, Boolean)
- Outputs: L (shifted list)
- Behavior: Re-indexes list items by an integer offset; negative S shifts the tail toward the front, positive shifts the head toward the back. W=true re-appends items that fall off one end (count unchanged, circular); W=false discards them (list shortens). On a tree, shifts elements within each branch independently. Changing which of two matched point lists is Shifted before Line-connecting them changes the resulting geometric pattern entirely (radial/spoke twist demo).
- Provenance: [STATED, AAD p.80-82; Essential p.38-40, 68, 96]

### Sort List
- Tab: Sets > List | Type GUID: 6f93d366-919f-4dda-a35e-ba03dd62799b
- Alias: Sort
- Inputs: K (sort keys), A (optional parallel list to carry along in sorted order)
- Outputs: K (sorted keys), A (sorted list — a single flattened trunk, not automatically branched even when the new order clusters into logical groups)
- Behavior: Randomly-generated curve parameters must be Sorted before evaluating a curve at each and lofting/connecting the results in sequence, or the profile curves are visited out of order, producing a twisted/self-intersecting surface. Also used with Deconstruct(point)'s coordinate output as sort key to recover grid order from geometry when list order is scrambled.
- Provenance: [STATED, AAD p.249-250, 252; Essential p.19, 30-31, 37]

### Reverse List
- Tab: Sets > List | Type GUID: 6ec97ea8-c559-47a2-8d0f-ce80c794d1f4
- Alias: Rev
- Inputs: L (list)
- Outputs: L (reversed list)
- Behavior: Reverses item order (index 0 becomes last). Also available as right-click "Reverse" on any input slot (no separate component needed).
- Provenance: [STATED, AAD p.85-86; Essential p.19, 37]

### Split List
- Tab: Sets > List | Type GUID: 9ab93e1a-ebdf-4090-9296-b000cff7b202 [ambiguous — see also Split Tree below, distinct GUID d8b1e7ac]
- Alias: Split
- Inputs: L (list), i (Index, integer)
- Outputs: A (list [0..i-1]), B (list [i..end])
- Behavior: Splits one list at index i into two lists. Edge case: i = list length → A = full list, B = empty. On a tree, splits EACH branch at the specified index (each output branch gets a new trailing sub-index appended).
- Provenance: [STATED, AAD p.83-84; Essential p.68]

### Subset
- Tab: Sets > List
- Alias: SubSet
- Inputs: L (list), D (domain of indices to keep), W (wrap?)
- Outputs: L (sub-list), I (the sub-indices actually used)
- Behavior: Selects a contiguous range of a list by an index domain (e.g. domain "1 to 3" keeps indices 1,2,3).
- Provenance: [STATED, Essential p.38]

### List Length
- Tab: Sets > List | Type GUID: 1817fd29-20ae-4503-b542-f0fb651e67d7
- Alias: Lng / L
- Inputs: L (list)
- Outputs: L (integer count)
- Behavior: Typically wired to a Panel to display; recommended check on both inputs before wiring two lists into the same component, to detect length mismatches before they silently trigger default list-matching.
- Provenance: [STATED, AAD p.83; Essential p.26, 37, 41, 48]

### Dispatch
- Tab: Sets > List | Type GUID: d8332545-21b2-4716-96e3-8559a9876e17
- Inputs: L (list), P (boolean pattern)
- Outputs: A (items where pattern True), B (items where pattern False)
- Behavior: Splits one list into two based on a boolean pattern in a single step — contrasted with needing two separate Cull Pattern operations (one per boolean state) to capture both outcomes. Idiomatic GH way to do conditional/clamping logic: build a candidate-value list + a parallel boolean selection list (from comparisons), feed both into Dispatch so the True branch is the "selected" value used downstream.
- Provenance: [STATED, AAD p.18, 21-23, 29-31, 38, 108-109]

### Jitter
- Tab: Sets > List | Type GUID: f02a20f6-bb49-4e3d-b155-8ed5d3c6b000
- Inputs: L (list), J (jitter factor, 0-1), S (seed)
- Outputs: V (list with randomized/shuffled order), I (the new index order applied)
- Behavior: Randomly reorders a list's items (not their values) — e.g. to connect points in scrambled order for a chaotic linework pattern.
- Provenance: [STATED, Essential p.40]

### Long ("Repeat Last")
- Tab: Sets > List (List Matching mode; also invocable as an explicit component)
- Alias: Long
- Inputs: A (list), B (list)
- Outputs: A, B — both padded to the same (longer) length by repeating the shorter list's LAST item
- Behavior: Explicit component form of Grasshopper's own DEFAULT list-matching behavior — confirmed stated: "GH defaults to Long List matching."
- Provenance: [STATED, Essential p.41-42]

### Shortest List
- Tab: Sets > List
- Alias: Short / SL / "Trim End" (all informal aliases — RESOLVED: "Shortest List" is the official ribbon-listed name, already standard as of GH 0.9, i.e. current in AAD's own 2014 era too)
- Inputs: A (List (A), generic data), B (List (B), generic data)
- Outputs: A, B — both truncated to the same (shorter) length; extra trailing items of the longer list discarded
- Provenance: [STATED, Essential p.42, 375] [STATED, AAD p.92, 375 as "Shortest List"/"Short" — CONSISTENT across both] [VERIFIED https://grasshopperdocs.com/components/grasshoppersets/shortestList.html] [VERIFIED https://www.grasshopper3d.com/page/new-data-matching-in-0-9]

### Longest List
- Tab: Sets > List | Type GUID: 8440fd1b-b6e0-4bdb-aa93-4ec295c213e9
- Alias: LL
- Inputs: A (List (A), generic data), B (List (B), generic data) — expandable to more list inputs
- Outputs: A, B (same names — both lists grown/padded to match the longest input's length, by repeating the shorter list's last item)
- Behavior: Forces two lists to be matched using longest-list logic explicitly as a component (GH's default: once the shorter list is exhausted, its last item repeats to pair with remaining longer-list items). Functionally the same as "Long."
- Provenance: [STATED, AAD p.92] [VERIFIED https://grasshopperdocs.com/components/grasshoppersets/longestList.html]

### Cross Reference
- Tab: Sets > List | Type GUID: 36947590-f0cb-4807-a8f9-9c90c9b20621
- Alias: CrossRef / "Holistic"
- Inputs: A, B (and additional C, D... — generalizes to N inputs)
- Outputs: A, B, (C...) each expanded so every item of one list pairs with every item of the other(s) — full Cartesian product; result length = PRODUCT of all input lengths
- Behavior: Recommended "when trying to produce all possible combinations of input data" — the book's standard technique for turning two independent 1D sequences into a 2D/3D grid. Order of inputs affects the ORDER of the result (though not the underlying value-set) — explicitly flagged "Order of input matters." Generalizes beyond 2 inputs (a 3-way CrossRef of a 6-item list into X/Y/Z produces a 6x6x6=216-point cube). Result length grows multiplicatively — worth checking list lengths first to avoid combinatorial explosion.
- Provenance: [STATED, AAD p.90-94, 305; Essential p.42-45]

### Repeat / Repeat Data
- Tab: Sets > Sequence (RESOLVED — Essential p.43,48 and AAD p.243,245's "Sets > List" citations are imprecise; Sequence is the standing GH1 panel)
- Alias: Repeat
- Inputs: D (Data, generic data — the list/pattern to repeat), L (Length, Integer — target length)
- Outputs: D (Data, generic data — input cyclically tiled until it reaches length L)
- Behavior: Used to build "custom" matching that cyclically repeats an entire short list's pattern, differing from GH's default Long (repeat-last-item) matching — identical raw inputs produce DIFFERENT results under the two strategies (e.g. `[1,2]+[1,2,3,4,5]`: Long→`[2,4,5,6,7]` vs. cyclic Repeat→`[2,4,4,6,6]`).
- Provenance: [STATED, AAD p.95, 99, 243, 245; Essential p.43, 48] [VERIFIED https://grasshopperdocs.com/components/grasshoppersets/repeatData.html]

### Merge
- Tab: Sets > Tree (RESOLVED — GUID confirms current Merge, not a legacy List component; Essential's "List/Util" grouping is imprecise)
- Type GUID: 3cadddef-1e2b-4c09-9390-0e8f78f7609f
- Inputs: D1, D2 (dynamically grows a new empty D-input, e.g. D3, once the previous one receives a wire; expandable further via the Zoomable User Interface's "+" control)
- Outputs: R
- Behavior: Concatenates multiple lists into ONE single bigger flat list, in input order — contrast Entwine, which keeps N inputs as N separate branches. Explicitly set to "simplify" mode in some recipes so pieces collapse into a single flat branch per group before Join.
- Provenance: [STATED, AAD p.64, 74, 78, 95, 223-224, 269, 436, 452; Essential p.71] [VERIFIED https://grasshopperdocs.com/components/grasshoppersets/merge.html]

### Entwine
- Tab: Sets > Tree | Type GUID: c9785b8e-2f30-4f90-8ee3-cca710f82402
- Inputs: variable number of generic inputs shown as branch labels (renamed from D1,D2... in the UI); has a "Flatten" toggle/label per input
- Outputs: R (Result tree)
- Behavior: Combines any number of separate lists into one NEW tree, one branch per input list — no values are combined, just organized into parallel branches.
- Provenance: [STATED, Essential p.59-60, 71]

### Weave
- Tab: Sets > List (RESOLVED — AAD wins; Essential's implied Tree placement, p.92-99, does not match current docs)
- Inputs: P (Pattern, Integer — list of stream-index integers, e.g. 0,1,0,1..., naming which numbered stream to pull the next item from), plus one Generic Data input per stream, auto-labeled "0", "1", "2"... as more are wired in
- Outputs: W (Weave, Generic Data — single interleaved list built by walking the pattern and pulling the next unused item from the named stream each time)
- Behavior: The inverse of splitting (Cull Pattern/Dispatch take one list and filter/split it; Weave takes multiple separate streams and interleaves them back into one list) — used to recombine separately-culled "top"/"bottom" point subsets into original alternating order, and to interleave 3 corner-point sets (A,B,C) for triangular plates. When the pattern and streams don't match perfectly, mismatched lengths produce nulls in the output or silently skip depleted streams. The Pattern input's exact authoring grammar (literal typed string vs. wired from Series/other integer-list components) remains undocumented in every source checked — genuinely unverifiable beyond "list of stream-index integers."
- Provenance: [STATED, AAD p.50; Essential p.50, 92-99] [VERIFIED https://grasshopperdocs.com/components/grasshoppersets/weave.html] [VERIFIED https://modelab.gitbooks.io/grasshopper-primer/content/1-foundations/1-4/6_list-management.html]

### Graft Tree
- Tab: Sets > Tree | Type GUID: 87e1d9ef-088b-4d30-9dda-8a7448a17329
- Alias: Graft
- Inputs: T (Tree/list)
- Outputs: T (grafted tree — one branch created per item)
- Behavior: The most extreme possible un-flattening — turns a flat list into a tree with one branch per item. "Unintuitive" (complicates structure) but essential for full cross-product matching: grafting two independent lists (each item → own branch) before Merging causes per-branch components (e.g. Loft) to process matched pairs instead of one giant flattened concatenation. Works even on variable-depth trees — every leaf item gets its own NEW deepest branch level regardless of starting depth (e.g. a 4-branch variable-depth tree becomes 8 branches, each N=1). Also available as a right-click menu option on any parameter/input.
- Provenance: [STATED, AAD p.222-224, 328; Essential p.69, 75]

### Flatten Tree
- Tab: Sets > Tree | Type GUID: f80cfe18-9510-4b89-8301-8e58faf423bb
- Alias: Flatten
- Inputs: T (tree), P (optional path parameter)
- Outputs: T (flattened tree — all data under a single branch/trunk {0}, preserving original branch-by-branch/item-by-item order)
- Behavior: Removes ALL branching info. Converts a dashed (tree-structured) wire into a solid (flat-list) wire. Branches are read "in order starting with the lowest-index trunk." Per-pin "Flatten" also available via right-click on any individual input/output. Critical requirement in the GECO workflow: MUST flatten Mesh Explode's F output before EcoMeshExport.M, else Ecotect imports only the faces in the tree's LAST branch, silently dropping the rest.
- Provenance: [STATED, AAD p.220-221, 453-454; Essential p.70]

### Unflatten Tree
- Tab: Sets > Tree [INFERRED]
- Alias: Unflatten
- Inputs: T (flat list), G (guide tree — the desired branching pattern)
- Outputs: T (restructured tree, matching G's branch/item shape)
- Behavior: Flatten's inverse — re-splits a flat list into branches matching a separately-supplied guide tree's structure. Strict precondition [STATED]: the flat list must contain exactly the same number of items as the guide tree, or the component does not operate. Canonical worked case [STATED] ("4 triangles -> 12 vertices"): a 4-branch x 3-item vertex tree is Flattened to {1x12}, then Unflattened using the ORIGINAL pre-flatten tree as guide, restoring the exact 4x3 structure. Also the closing step of the "flatten -> transform -> unflatten" idiom [STATED]: applying an alternating +/- pattern to still-tree-structured data makes the pattern silently restart at the beginning of every branch, so the fix is to Flatten first, apply the transform, then Unflatten Tree with the ORIGINAL pre-flatten tree as guide (G) to restore per-branch grouping before the next per-branch operation (e.g. Interpolate, one curve per thread) — skipping this restoration produces one tangled curve through the entire point set instead of separate per-thread curves.
- Provenance: [STATED, Essential p.70; AAD p.222, 245-247]

### Flip Matrix
- Tab: Sets > Tree | Type GUID: 41aa4112-9c9b-42f4-847e-503b9d90e4c7
- Alias: Flip
- Inputs: D (tree/matrix-like data)
- Outputs: D (flipped tree — rows/columns swapped: items become branches, branches become items)
- Behavior: Transposes an M-branch x N-item tree into an N-branch x M-item tree (matrix transpose) — used to regroup "corresponding" items (e.g. same point-index across several curves/threads) that started out grouped by source object. Requires uniform branch depth: variable-LENGTH branches get padded with literal `<null>` values to remain rectangular; variable-DEPTH branches (nested at different levels) make Flip fail entirely — component turns red/errors, "there is no logical solution to flip." NOTE: shares the on-canvas nickname "Flip" with the unrelated Flip Curve component (Curve > Util) — disambiguate by pins (Flip Matrix: D in/out; Flip Curve: C in/out) and tab.
- Provenance: [STATED, AAD p.224-225, 242, 280; Essential p.71-72, 94]

### Split Tree
- Tab: Sets > Tree | Type GUID: d8b1e7ac-cd31-4748-b262-e07e53068afc
- Alias: Split
- Inputs: D (Data tree), M (split Mask string)
- Outputs: P (Positive tree — items matching mask), N (Negative tree — items not matching)
- Behavior: Mask-string grammar: `{;;}` enclose the branch-selection mask, `[]` enclose the element/leaf-selection mask (omitted = select all, `[*]`); `()` for grouping. Wildcards: `*` matches any number of integers in a path; `?` matches any single integer; a bare integer matches that value; `!` negates a rule; comma-list `(2,6,7)` matches any listed value (negatable); range `(2 to 20)` matches an inclusive range (negatable); open arithmetic sequence `(0,2,...)` matches integers in that ascending sequence, optionally bounded `(0,2,...,48)` — a negated infinite sequence `!(3,5,...)` does NOT extend leftward, so it also matches everything below the sequence start; rules combine with and/or, e.g. `{*}[(0 to 4) or (6,11,41)]`. BOTH outputs retain the EXACT original tree structure (same branch paths/item counts) — excluded elements are replaced with null, not removed — enabling lossless recombination via Combine Data after independently transforming one side. Also demonstrated splitting by whole alternating BRANCH indices (mask at the branch level, e.g. `{0,2,...}`) rather than within-branch elements, for "treat whole columns differently" cases.
- Provenance: [STATED, Essential p.81-86, 96]

### Simplify Tree
- Tab: Sets > Tree | Type GUID: 1303da7b-e339-4e65-a051-82c4dce8224d
- Alias: Simplify
- Inputs: T (Tree, generic data), F ("Front", boolean — optional; when True, restricts path-collapsing to indices at the start/front of each path only, rather than collapsing overlap anywhere in the path)
- Outputs: T (simplified tree)
- Behavior: Removes redundant/overlapping nested branch levels (e.g. `{0;0;0;0;0;0}` → `{0}`) without changing item counts or values. Needed in addition to (not instead of) Graft when repeated Explode/Graft chains accumulate over-nested branches, before Merge+Loft will pair curves correctly. Related but separately-named cleanup tools mentioned only in body text: Clean Tree and Trim Tree (remove null elements/empty branches), Explode Tree (splits all branches into separate list outputs). CORRECTED: the KB's prior guess of "mask or 'L' for levels" for the second input was wrong — it is "Front" (F), a boolean.
- Provenance: [STATED, AAD p.228-229; Essential p.72] [VERIFIED https://grasshopperdocs.com/components/grasshoppersets/simplifyTree.html]

### Relative Item
- Tab: Sets > Tree | Type GUID: fac0d5be-e3ff-4bbb-9742-ec9a54900d41 (single-tree variant); a distinct "Relative Items" GUID (2653b135-4df1-4a6b-820c-55e2ad3bc1e0) also appears in guid-map, likely the two-tree/"RelItem2" variant
- Alias: RelItem (also "RelItem2" for the two-tree/repeated-instance variant)
- Inputs: T (Tree, source; or A/B for the two-tree variant), O (Offset mask string, e.g. "{+1}[+1]"), Wp (Wrap Paths, boolean), Wi (Wrap Items, boolean)
- Outputs: A (tree A), B (tree B)
- Behavior: Offset-string grammar "{branch offset}[index offset]" describes how to connect an item at one address to another item at a relative address in the SAME or a DIFFERENT tree — e.g. `{+1}[+1]` connects branch B/index I to branch B+1/index I+1 (diagonal grid connectivity). Internally builds two NEW correlated trees (A tree, B tree) whose corresponding branches/items are exactly the described pairs, so a simple 2-point Line A→B draws all offset connections at once. Necessarily produces OUTPUT trees SMALLER than the input whenever the offset references an out-of-bounds branch/index (e.g. the last branch/item has no +1 neighbor) — both outputs trim to only addresses where both base and offset target exist.
- Provenance: [STATED, Essential p.76-80, 95]

### Combine Data
- Tab: Sets > Tree | Type GUID: e7c80ff6-0299-4303-be36-3080977c14a1
- Alias: Combine
- Inputs: 0 (first data set), 1 (second data set)
- Outputs: R (Result)
- Behavior: Recombines a Split Tree's Positive/Negative outputs (or any two same-structure trees with complementary nulls) back into one complete tree — lossless as long as structure/paths were preserved.
- Provenance: [STATED, Essential p.83-91]

### Clean Tree
- Tab: Sets > Tree | Type GUID: 071c3940-a12d-4b77-bb23-42b5d3314a0d
- Alias: Clean
- Inputs: T (Tree, generic data — tree to clean), N ("Null" removal, boolean — True strips `<null>` items, False retains them), X ("Invalid" removal, boolean — True strips invalid/malformed data items in addition to nulls), E ("Empty" branch removal, boolean — True removes branches left empty after cleanup while preserving overall tree structure)
- Outputs: T (cleaned Tree)
- Behavior: Strips `<null>` placeholder items (e.g. inserted by Flip Matrix for unequal branch lengths) before feeding into geometry components that can't handle nulls. Input ordering is non-standard (options mixed in with the T data input rather than data-first).
- Provenance: [STATED, Essential p.86, 96] [VERIFIED https://grasshopperdocs.com/components/grasshoppersets/cleanTree.html] [VERIFIED https://iarchway.com/en/clean_tree/]

### Path Mapper
- Tab: Sets > Tree (also filed under Params in some GH versions) | Type GUID: f9b89a46-bc5d-4f7a-9a6f-134f93ac3af9
- Inputs: one data tree (source paths fixed/read-only, taken from input)
- Outputs: remapped data tree per a user-authored target-path expression
- Behavior: "Perhaps the least intuitive to use and can cause a loss of data," but "the only way to find a solution in some cases." Three named constants for expressions: item_count (items in current branch), path_count (branches in whole tree), path_index (index of current branch). Typical expressions use tuple notation `{A;B;C}` for a 3-level path and `(i)`/`[i]` for item index, e.g. regroup `{A;B;C}->{A;C;B}`, or flip (promote item index into path, demote a path level into item index) `{A;B;C}[i]->{A;B;i}[C]`; composable into one expression, e.g. `{A;B;C}[i]->{A;C;i}[B]` (saves processing vs. chaining two Path Mappers — "not always possible"). Right-click presets: Mapping Editor, Create Null Mapping (no-op template), Create Flatten Mapping, Create Graft Mapping, Create Trim Mapping, Create Reverse Mapping (reverses item order per branch, structure unchanged), Create Renumber Mapping (strips nested path structure to flat sequential top-level branch numbers), Enabled, Help.
- Provenance: [STATED, Essential p.86-91]

### Branch
- Tab: Sets > Tree
- Inputs: T (Tree), P (Path, as text or Path parameter)
- Outputs: B (Branch)
- Behavior: Extracts a single branch from a tree given its explicit path address (e.g. "{0;0;0}"); can also be fed a dynamically-derived path (e.g. from Tree Statistics + List Item, using -1 wrap-around indexing for "last branch") instead of hardcoding.
- Provenance: [STATED, Essential p.65] (has a "Maintain" mode label per source)

### Tree Statistics
- Tab: Sets > Tree | Type GUID: 99bee19d-588c-41a0-b9b9-1d00fb03ea1a
- Alias: TStat
- Inputs: T (Tree)
- Outputs: P (Paths — list of all branch path addresses), L (branch element counts, one number per branch), C (branch Count, total number of branches)
- Behavior: Used to dynamically extract path addresses (e.g. for feeding Branch) instead of typing them, and to reconstruct a point list from an XYZ-organized tree.
- Provenance: [STATED, Essential p.65-67]

### Concatenate
- Tab: Sets > Text (RESOLVED — AAD wins; Essential's "near Maths" grouping is a thematic/teaching grouping, not the component's actual ribbon tab)
- Type GUID: 2013e425-8713-42e2-a661-b57e78840337
- Alias: Concat
- Inputs: A, B (text fragments; expandable to more)
- Outputs: R (joined text)
- Behavior: Joins text fragments into one string; used for literal sentences and for assembling parametric condition expressions (e.g. a slider value concatenated after "x>").
- Provenance: [STATED, AAD p.109-110; Essential p.17]

### Cull Duplicates
- Tab: Sets > Point
- Alias: CullPt
- Inputs: P (points), T (tolerance)
- Outputs: P (culled/averaged points), I (index info), V (valence)
- Behavior: Mode option "Average" used to detect coincident/duplicate points (e.g. face centroids of touching mesh-box faces) within tolerance — a -1 index entry marks a point with no duplicate (genuine boundary), paired index entries mark coincident/overlapping points to be culled. Used in a "cull adjacent/internal faces" cleanup strategy for joined mesh-box aggregations.
- Provenance: [STATED, AAD p.292]

### Series
- Tab: Sets > Sequence | Type GUID: e64c5fb1-845c-4ab1-8911-5f338516ba67
- Inputs: S (start number), N (step size), C (count of steps)
- Outputs: S (list of numbers)
- Behavior: Generates an arithmetic numeric sequence; default S=0,N=1,C=10 → (0..9); negative N gives a decreasing sequence. Setting Start=0 makes the first generated element coincide with the un-translated original object.
- Provenance: [STATED, AAD p.87, 188; Essential p.35, 93]

### Random
- Tab: Sets > Sequence / Maths > Domain | Type GUID: 2ab17f9a-d852-4405-80e1-938c5e57e78d
- Inputs: R (domain), N (number of values), S (seed)
- Outputs: R (list of random numbers)
- Behavior: Generates N random real numbers within domain R; deterministic given a fixed seed — same seed always reproduces the same list. Right-click "Integer Numbers" switches output to integers.
- Provenance: [STATED, AAD p.100, 214; Essential p.28-30, 35]

### Range
- Tab: Sets > Sequence | Type GUID: 9445ca40-cc73-4861-a455-146308676855
- Inputs: D (domain), N (number of steps)
- Outputs: R (list of N+1 numbers spanning domain D)
- Behavior: Divides a numeric domain into N equal parts, returning N+1 values inclusive of both ends — contrast Series, which is not domain-bound. GOTCHA: to get exactly one value per existing object, subtract 1 from the object count (via Subtraction) before feeding Range's N-input, or lists are off-by-one.
- Provenance: [STATED, AAD p.101, 198; Essential p.17, 34-35, 36, 51]

---

## Vector

### Unit X
- Tab: Vector > Vector | Type GUID: 79f9fbb3-8f1d-4d9a-88a9-f7961b1012cd
- Inputs: F (Factor)
- Outputs: V (vector)
- Behavior: Default unit vector along the world X-axis, scalable via F (embedded scalar multiplication).
- Provenance: [STATED, AAD p.66, 88-94, 187]

### Unit Y
- Tab: Vector > Vector | Type GUID: d3d195ea-2d59-4ffa-90b1-8b7ff3369f69
- Inputs: F (Factor)
- Outputs: V (vector)
- Provenance: [STATED, AAD p.66, 88-94, 187]

### Unit Z
- Tab: Vector > Vector | Type GUID: 9103c240-a6a9-4223-9b42-dbd19bf38e2b
- Inputs: F (Factor, default 1.0)
- Outputs: V (vector)
- Behavior: Default unit vector along world Z-axis, magnitude 1 unless scaled via F; used pervasively for gravity/self-weight loads and "move up by height" translations.
- Provenance: [STATED, AAD p.35, 66, 76, 88-94, 187, 283, 323, 366, 370, 372, 379, 383, 392; Essential p.50]

### Vector XYZ
- Tab: Vector > Vector
- Inputs: X ("X component", Number), Y ("Y component", Number), Z ("Z component", Number)
- Outputs: V ("Vector", Vector), L ("Length", Number — magnitude of the constructed vector)
- Behavior: Alternative to Unit X/Y/Z shortcuts — builds a vector from three explicit numeric components.
- Provenance: [STATED, AAD p.66] [VERIFIED https://grasshopperdocs.com/components/grasshoppervector/vectorXYZ.html]

### Vector 2Pt
- Tab: Vector > Vector
- Alias: Vec2Pt
- Inputs: A (point, start), B (point, end), U (boolean, optional unitize toggle)
- Outputs: V (vector), L (number, magnitude/length)
- Behavior: A single boundary edge can supply both plane-origin points (via Divide Distance) and a single constant slicing direction (via Vector 2Pt) for a family of parallel cutting planes.
- Provenance: [STATED, AAD p.185, 332]

### Unit Vector
- Tab: Vector > Vector
- Alias: Unit
- Inputs: V (vector)
- Outputs: V (unit vector, length 1, same direction/sense)
- Provenance: [STATED, AAD p.185-186]

### Vector Length
- Tab: Vector > Vector
- Alias: VLen
- Inputs: V (vector)
- Outputs: L (magnitude)
- Behavior: One of two equivalent ways to get a curvature value (the other: 1/osculating-circle-radius via Deconstruct Arc + Division).
- Provenance: [STATED, AAD p.137, 186]

### Amplitude
- Tab: Vector > Vector | Type GUID: 6ec39468-dae7-4ffa-a766-f2ab22a2c62e
- Alias: Amp
- Inputs: V (vector), A (amplitude/target length, number)
- Outputs: V (rescaled vector)
- Behavior: Rescales a vector to a target length while preserving direction/sense. In the surface-conforming Weaving tutorial, driven by the LOCAL surface normal (from Divide Surface) rather than a fixed world direction, so a woven pattern can conform to any surface — explicit warning: "make sure the data structure of normals and points match."
- Provenance: [STATED, AAD p.169, 186, 309; Essential p.101]

### Distance
- Tab: Vector > Point
- Alias: Dist
- Inputs: A (point), B (point)
- Outputs: D (distance)
- Behavior: Computes the distance between two points; used to measure attractor-to-geometry distance, and (with a target value) as the Fitness basis for goal-seeking optimization.
- Provenance: [STATED, AAD p.113, 233, 433]

### Construct Point
- Tab: Vector > Point | Type GUID: 3581f42a-9592-4549-bd6b-1c0fc39d067b
- Alias: Pt
- Inputs: X, Y, Z (numbers, default 0,0,0)
- Outputs: Pt (Point)
- Behavior: Computes a point from x/y/z; distinct from the container "Point" component despite sharing the "Pt" abbreviation on canvas. Default input data 0,0,0 places a point at the world origin.
- Provenance: [STATED, AAD p.38, 41-42, 103, 287, 375, 436; Essential p.11-12]

### Deconstruct (point) / Point Decompose
- Tab: Vector > Point
- Alias: pDecon
- Inputs: P (point)
- Outputs: X, Y, Z (coordinate values)
- Behavior: Used as a sort-key source (feed X or Y output into Sort List's K) to recover grid order from geometry when list order is scrambled.
- Provenance: [STATED, AAD p.249, 251, 252; Essential p.60]

### DePlane
- Tab: Vector > Plane
- Inputs: P (plane)
- Outputs: O (origin), X, Y, Z (axis vectors)
- Behavior: Deconstructs a plane into origin + 3 axis vectors; used as an intermediate step to extract a circle's plane/origin so Scale can use it as the scale center.
- Provenance: [STATED, Essential p.7]

### Plane Origin
- Tab: Vector > Plane | Type GUID: 75eec078-a905-47a1-b0d2-0934182b1e3d
- Alias: Pl Origin
- Inputs: B (base plane), O (new origin point)
- Outputs: Pl (a new plane with B's orientation relocated to origin O)
- Provenance: [STATED, Essential p.28-30]

### Plane Normal
- Tab: Vector > Plane
- Alias: Pl
- Inputs: O (origin point), Z (z-axis direction vector)
- Outputs: P (plane)
- Behavior: Builds a plane from an origin + a normal vector (e.g. a surface normal from Evaluate Surface), used to derive a rotation plane from geometry, or a panel's local offset direction for non-coplanar panel arrays.
- Provenance: [STATED, AAD p.189-190, 289-290, 332]

### Construct Plane
- Tab: Vector > Plane
- Alias: Pl
- Inputs: O ("Origin", Point), X ("X-Axis", Vector — X-axis direction of the plane), Y ("Y-Axis", Vector — Y-axis direction of the plane)
- Outputs: Pl ("Plane", Plane)
- Behavior: CORRECTED — a real, distinct component from Plane Normal (above), not a probable duplicate. It builds a plane from an origin plus explicit X- and Y-axis vectors (3 inputs), not from an origin plus a single Z/normal vector as previously guessed by analogy. If AAD p.269's partly-illegible diagram genuinely showed only two inputs (O and one vector), that diagram was more likely depicting Plane Normal (or another 2-input plane constructor) rather than this 3-input component.
- Provenance: [STATED, AAD p.269] [VERIFIED https://grasshopperdocs.com/components/grasshoppervector/constructPlane.html]

### XY Plane
- Tab: Plane > Plane (Vector tab per book) | Type GUID: 17b7152b-d30d-4d50-b9ef-c9fe25576fc2
- Alias: XY
- Inputs: O (origin point)
- Outputs: P (plane, world-XY-aligned at O)
- Provenance: [STATED, AAD p.193-194]

### Square Grid
- Tab: Vector > Grid
- Alias: SqGrid
- Inputs: P (Plane, default XY), S (Size, cell size), Ex (Extent X = branch span), Ey (Extent Y = element span)
- Outputs: C (Cells, closed polylines), P (Points, tree — one branch per row/column)
- Behavior: Ex controls the number of tree branches in the output point tree; Ey controls the number of items per branch.
- Provenance: [STATED, Essential p.77-78]

### Reverse (vector)
- Tab: Vector > Vector
- Alias: Rev
- Inputs: V ("Vector", Vector — base vector)
- Outputs: V ("Vector", Vector — reversed vector, i.e. multiplied by -1)
- Behavior: Used to invert a face-normal direction when it does not match the required sense relative to another vector (e.g. a solar-ray vector) — direction requirement is context-dependent (e.g. must point inward for one recipe, outward for another); always verify with Vector Display first. CORRECTED/MERGED: this is the same real component as the KB's separate "Negate (vector)" entry (AAD p.376, gravity-vector usage feeding Catenary's G input) — both describe a Vector > Vector sign-flip with identical V→V ports. No standalone "Negate" component exists in GH1; the two AAD citations (p.376 and p.451/454) are merged into this one entry.
- Provenance: [STATED, AAD p.451, 454] [STATED, AAD p.376 as "Negate"/alias "Neg" — merged, same component] [VERIFIED https://grasshopperdocs.com/components/grasshoppervector/reverse.html]

---

## Curve

### Circle (plane + radius)
- Tab: Curve > Primitive | Type GUID: 807b86e3-be8d-4970-92b5-f8cdcb45b06b or d1028c72-ff86-4057-9eb0-36c687a4d98c [ambiguous — guid-map contains two distinct entries both named "Circle"; likely one is this standard component and the other a generic Circle parameter/container]
- Alias: Cir
- Inputs: P/C (Plane, default WorldXY), R (Radius)
- Outputs: C (Circle)
- Behavior: Constructs a circle from a plane and radius — the first Grasshopper component shown in AAD, wired to a Radius slider.
- Provenance: [STATED, AAD p.35, 112; Essential p.6, 10-11]

### Circle CNR (center + normal + radius)
- Tab: Curve > Primitive | Type GUID: d114323a-e6ee-4164-946b-e4ca0ce15efa
- Alias: Circle
- Inputs: C (center point), N (normal vector), R (radius, number)
- Outputs: C (circle curve)
- Behavior: Builds the circle's plane implicitly from a point+normal instead of a full Plane — convenient when normals come from curve/surface evaluation (e.g. Eval.T or Evaluate Surface.N). AAD explicitly names "Circle CNR"; Essential shows the identical port shape (center, normal, radius) simply labeled "Circle" — treated as the same component.
- Provenance: [STATED, AAD p.112 (used unnamed as "Circle"), 178 (formally named), 204; Essential p.32, 46]

### Arc 3Pt
- Tab: Curve > Primitive
- Alias: Arc
- Inputs: A ("Point A", Point — start), B ("Point B", Point — point the arc passes through), C ("Point C", Point — end)
- Outputs: A ("Arc", Arc/Geometry — the arc curve), P ("Plane", Plane — the plane containing the arc), R ("Radius", Number — arc radius)
- Behavior: Creates an arc through three points; A and C are endpoints, B is a point the arc passes through. Used to build a pre-set arc-length (e.g. forcing a 10-unit-span arc to have arc-length exactly 20) as the starting geometry for a near-inextensible catenary approximation.
- Provenance: [STATED, AAD p.97-98, 377-378] [VERIFIED https://grasshopperdocs.com/components/grasshoppercurve/arc3Pt.html]

### Line (2-point)
- Tab: Curve > Primitive | Type GUID: 4c4e56eb-2f04-43f9-95a3-cc46a14f495a or 8529dbdf-9b6f-42e9-8e1f-c7a2bde56a70 [ambiguous — two distinct guid-map entries both named "Line"]
- Alias: Ln / Ls
- Inputs: A (point or points list, start), B (point or points list, end)
- Outputs: L (line or lines)
- Behavior: Builds a line from two points; shows orange/warning if A/B unconnected, red/error if a wrong type is wired (e.g. a raw Number into a Point input — "Data conversion failed from Number to Point"). With two point lists (e.g. from dividing concentric circles), connects corresponding points; combining with Shift List on one list changes which points pair up, producing different radial/spoke patterns.
- Provenance: [STATED, AAD p.46-49, 96-99, 176, 303, 388; Essential p.11-12, 39-40, 77]

### Line SDL
- Tab: Curve > Primitive | Type GUID: 4c619bc9-39fd-4717-82a6-1e07ea237bbe
- Alias: Line
- Inputs: S (start point), D (direction vector), L (length)
- Outputs: L (line)
- Behavior: Builds a line from a start point + direction + length — distinct from the two-point Line component (A/B inputs); used e.g. to offset an "apex" point above a sub-surface center along its normal.
- Provenance: [STATED, AAD p.160, 190, 324]

### Rectangle
- Tab: Curve > Primitive | Type GUID: d93100b6-d50b-40b2-831a-814659dc38e3
- Alias: Rec / Rectangle
- Inputs: P (Plane), X (Dimensions of rectangle in plane X direction, domain or number), Y (Dimensions of rectangle in plane Y direction, domain or number), R (Rectangle corner fillet radius)
- Outputs: R (Rectangle — Rectangle3d / GH_Rectangle), L (Length — perimeter of rectangle curve)
- Behavior: Creates a rectangle on a plane with optional corner fillets. Outputs Rectangle3d on R, directly feeding components requiring Param_Rectangle (e.g. Heteroptera GridInRectangle) or Param_Curve, and perimeter Length on L. Disambiguation: d93100b6-d50b-40b2-831a-814659dc38e3 is the active Grasshopper component; 0ca0a214-396c-44ea-b22f-d3a1757c32d6 is the obsolete version (which only output Curve); abf9c670-5462-4cd8-acb3-f1ab0256dbf3 is the Param_Rectangle parameter container.
- Provenance: [VERIFIED Rhino 8 Live ComponentServer]

### Rectangle 2Pt
- Tab: Curve > Primitive | Type GUID: 575660b1-8c79-4b8d-9222-7ab4a6ddb359
- Alias: Rec 2Pt
- Inputs: P (Plane), A (corner point A), B (corner point B), R (corner Radius)
- Outputs: R (Rectangle), L (Length)
- Provenance: [STATED, Essential p.75]

### Point on Curve
- Tab: Curve > Analysis
- Inputs: curve (implicit) + value 0-1 (rendered as a slider-bar on the component's face)
- Outputs: a point on the curve / CurvePoint
- Behavior: Finds a point via fractional ARC LENGTH (not domain parameter t) — 0.5 is always the true geometric midpoint; does not require reparameterization. Right-click named snaps: 0.0(start)/1/4(quarter)/1/3(third)/1/2(mid)/2/3(two thirds)/3/4(three quarters)/1.0(end). CONTRASTS with Evaluate Curve (domain-parameter-based, not arc-length-based) — a Grasshopper-native substitute for CAD Osnap "midpoint" picking.
- Provenance: [STATED, AAD p.61, 96, 132]

### End Points
- Tab: Curve > Analysis (RESOLVED — AAD p.160's "Endpoint"/Curve > Util reference is an internal inconsistency, likely mislabeling of an in-context screenshot; "End Points"/Curve > Analysis is correct) | Type GUID: 11bbd48b-bb0a-4f1b-8167-fa297590390d
- Alias: End
- Inputs: C (Curve)
- Outputs: S (start point), E (end point)
- Behavior: Extracts a curve's two endpoints — a Grasshopper-native substitute for CAD Osnap "endpoint" picking.
- Provenance: [STATED, AAD p.62, 160, 303, 366; Essential p.19 general list mention] [VERIFIED https://grasshopperdocs.com/components/grasshoppercurve/endPoints.html]

### Evaluate Curve [DISAMBIGUATION 2 of 3 — see Evaluate F(X) under Maths, Evaluate Length below]
- Tab: Curve > Analysis | Type GUID: fc6979e4-7e91-4508-8e05-37c680779751
- Alias: Eval
- Inputs: C (curve — should be Reparameterized first), t (parameter, 0-1 domain)
- Outputs: P (point in WCS), T (tangent vector), A ("Angle", Number — angle in radians between the incoming vs. outgoing curve direction at t; a discontinuity measure, not curvature)
- Behavior: Finds point + tangent vector at DOMAIN parameter t — NOT arc-length (t=0.5 is generally NOT the true midpoint unless the curve is reparameterized AND happens to be uniform). Renders as a plain "Eval" box identical to Evaluate F(X) and Evaluate Length; distinguish by its C/t ports and Curve > Analysis tab. Combined with Random + Sort: Random generates unordered curve parameters, which MUST be Sorted (ascending) before feeding to Eval, else resulting points/circles are visited out of curve order, producing a twisted/self-intersecting Loft.
- Provenance: [STATED, AAD p.126-127, 325, 433; Essential p.24, 46] [VERIFIED https://grasshopperdocs.com/components/grasshoppercurve/evaluateCurve.html]

### Evaluate Length [DISAMBIGUATION 3 of 3 — see Evaluate F(X) under Maths, Evaluate Curve above]
- Tab: Curve > Analysis | Type GUID: 6b021f56-b194-4210-b9a1-6cef3b7d0848
- Alias: Eval
- Inputs: C (curve), L ("Length", Number — length factor), N ("Normalized", Boolean — if True, L is read as a normalized 0.0-1.0 fraction of total curve length; if False, L is read as an absolute length in curve/model units; AAD's example implicitly uses N=False/absolute-length mode)
- Outputs: P (point, WCS), T (tangent), t (parameter, LCS)
- Behavior: Finds the point located a given arc-length distance L from the curve's start (t=0). Renders as a plain "Eval" box identical to Evaluate F(X) and Evaluate Curve; distinguish by its C/L/N ports and Curve > Analysis tab.
- Provenance: [STATED, AAD p.132] [VERIFIED https://grasshopperdocs.com/components/grasshoppercurve/evaluateLength.html]

### Curve Length
- Tab: Curve > Analysis | Type GUID: c75b62fa-0a33-4da7-a5bd-03fd0068fd93
- Alias: Len
- Inputs: C (curve)
- Outputs: L (total arc length)
- Provenance: [STATED, AAD p.132, 303, 370, 372; Essential p.52]

### Divide Curve
- Tab: Curve > Division | Type GUID: 2162e72e-72fc-4bf8-9459-d4d82fa8aa14
- Alias: Divide
- Inputs: C (Curve), N (Count, number of segments), K ("Kinks", Boolean — when True, adds extra split points at the curve's discontinuities/direction changes)
- Outputs: P (points), T ("Tangents", Vector — tangent direction at each point), t ("Parameters", Number — the curve parameter at each point)
- Behavior: Divides an open or closed curve into equal arc-length segments: N+1 points for an open curve, exactly N points for a closed curve (e.g. dividing a circle into 5 gives 5 points, since start/end coincide). Output points ordered by the curve's parametric start-to-end direction. Dividing a SINGLE curve gives a flat list; dividing a LIST of curves gives a tree (one branch per curve) — a key example of components that add tree nesting.
- Provenance: [STATED, AAD p.64-65, 85, 96, 225, 326, 365; Essential p.35, 59, 72-73] [VERIFIED https://grasshopperdocs.com/components/grasshoppercurve/divideCurve.html]

### Divide Length
- Tab: Curve > Division
- Alias: DivLength
- Inputs: C (curve), L (arc-length per segment)
- Outputs: P (points), T (tangents), t (parameters)
- Behavior: Divides a curve into fixed absolute-length segments; leaves a "leftover-arc" of different length at the end if the curve's total length isn't an exact multiple of L.
- Provenance: [STATED, AAD p.133]

### Divide Distance
- Tab: Curve > Division
- Alias: DivDist
- Inputs: C (curve), D (radial distance)
- Outputs: P (points), T (tangents), t (parameters)
- Behavior: Divides a curve via sequential intersections of circles of radius D (centered at each successively-found point) with the curve — geometrically distinct from Divide Length. Leaves a leftover-arc if D doesn't evenly divide the curve. A single boundary edge can supply both plane-origin points (via Divide Distance) and a constant slicing direction (via Vector 2Pt) for parallel cutting planes.
- Provenance: [STATED, AAD p.134, 332]

### Contour
- Tab: Curve > Division
- Inputs: C (Curve), P (Point — start point), N (Direction, Vector), D (Distance, Number — spacing between cutting planes)
- Outputs: C ("Contours", Point — intersection points, grouped by section), t ("Parameters", Number — curve parameter of each contour point)
- Behavior: Intersects a curve with a family of parallel cutting lines/planes spaced D apart along direction N, starting from point P.
- Provenance: [STATED, AAD p.134] [VERIFIED https://grasshopperdocs.com/components/grasshoppercurve/contour.html]

### Shatter
- Tab: Curve > Division
- Inputs: C (curve), t (list of split parameters, LCS [0,1] domain)
- Outputs: S (curve segments)
- Behavior: Splits a curve into segments AT given t-parameters — returns curve pieces, not points (unlike other Division-family components). The t-input can be a slider, Curve CP's t-output, or Divide Curve's t-output. RESOLVED: this is a real, distinct component from Explode Curve (Curve > Util, below). AAD p.378's diagram labeled "Explode" with ports C,R → S,V is NOT a mislabeled Shatter — its ports exactly match the real, separate Explode component's spec (Shatter has no R input and no V output), so it is the book's own surrounding text (still calling it "Shatter" in context on that page) that is wrong, not the diagram label.
- Provenance: [STATED, AAD p.135, 365] [VERIFIED https://grasshopperdocs.com/components/grasshoppercurve/shatter.html] [VERIFIED https://discourse.mcneel.com/t/shatter-component-whats-it-about/101884]

### Curvature
- Tab: Curve > Analysis
- Inputs: C (curve), t (parameter)
- Outputs: P (point), K (curvature vector), C (osculating circle)
- Behavior: Returns the curvature vector and osculating circle (best-fit circle) at a point on a curve; k = |K| = 1/r (osculating circle radius).
- Provenance: [STATED, AAD p.136-137]

### Curvature Graph
- Tab: Curve > Analysis
- Inputs: a curve
- Outputs: graphical comb display (no discussed data ports)
- Behavior: Visually displays curvature along a curve as a comb of perpendicular hairlines, length proportional to curvature magnitude, +/- signs marking curvature-sign regions.
- Provenance: [STATED, AAD p.138]

### Flip Curve [shares nickname "Flip" with the unrelated Flip Matrix (Sets > Tree) — see that entry's disambiguation note]
- Tab: Curve > Util
- Alias: Flip
- Inputs: C (curve or list of curves), G (optional guide/reference curve)
- Outputs: C (flipped curve(s)), F (flipped indicator)
- Behavior: Reverses a curve's parametric direction (swaps t=0/t=1 ends). With G supplied plus a list of mixed-direction curves at C, flips only curves not already matching G's direction, in one operation. Does NOT fix curve direction via Reparameterize — these are independent operations (direction is set by original control-point order).
- Provenance: [STATED, AAD p.128-130, 242]

### Curve Closest Point
- Tab: Curve > Analysis
- Alias: Crv CP
- Inputs: P (point), C (curve)
- Outputs: P (closest point on curve), t (parameter), D (distance)
- Behavior: World-to-Local conversion for curves — finds closest point on curve to a given point, returns the distance; if P lies exactly on the curve, P=P' and D=0. Implements curve-based attractors.
- Provenance: [STATED, AAD p.115, 130-131]

### Deconstruct Arc
- Tab: Curve > Analysis
- Alias: DArc
- Inputs: A (arc)
- Outputs: B (base plane), R (radius), A (angle domain)
- Behavior: Breaks an arc (incl. a circle, a closed arc) into base plane, radius, and angle domain.
- Provenance: [STATED, AAD p.107]

### Interpolate Curve (official GH1 name: "Interpolate")
- Tab: Curve > Spline | Type GUID: 2b2a4145-3dff-41d4-a8de-1ea9d29eef33
- Alias: IntCrv
- Inputs: V ("Vertices", Point — interpolation points), D ("Degree", Integer), P ("Periodic", Boolean), K ("KnotStyle", Integer — 0=uniform, 1=chord, 2=sqrt-chord)
- Outputs: C ("Curve", Curve — resulting NURBS curve), L ("Length", Number — curve length), D ("Domain", Domain — curve domain)
- Behavior: Draws a curve interpolated through a list of points. Used repeatedly to fit a smooth curve through Kangaroo particle positions for visual continuity — a caveat applies: this can look smooth but is physically incorrect at multi-anchor junctions since it implies bending stiffness a hinge-particle simulation cannot have. CORRECTED (naming): the current GH1 component's official name is "Interpolate" (nickname "IntCrv"), not "Interpolate Curve" — a naming nuance, not a factual error in the port data. COMPLETED: the extra L/D outputs are real (Length, Domain), not an over-guess — the source's own hedge undersold what AAD/Essential correctly showed as 3 outputs.
- Provenance: [STATED, AAD p.103, 245, 369, 400-401, 433; Essential p.100-101] [VERIFIED https://grasshopperdocs.com/components/grasshoppercurve/interpolate.html]

### Nurbs Curve
- Tab: Curve > Spline
- Alias: Nurbs
- Inputs: V ("Vertices", Point — control points), D ("Degree", Integer), P ("Periodic", Boolean)
- Outputs: C ("Curve", Curve), L ("Length", Number), D ("Domain", Domain)
- Behavior: Rebuilds a smooth freeform curve through a point list — used to fix sharp-corner discontinuities introduced by a raw Offset, and to rebuild a smooth silhouette from a twisted-loft isocurve extraction. Confirmed to share the same L/D output pattern as Interpolate Curve, exactly as previously guessed by analogy.
- Provenance: [STATED, AAD p.326, 332-333] [VERIFIED https://grasshopperdocs.com/components/grasshoppercurve/nurbsCurve.html]

### Polyline
- Tab: Curve > Spline | Type GUID: 71b5b089-500a-4ea6-81c5-2f960441a0e8
- Alias: PLine
- Inputs: V (vertices, points), C (Closed, boolean)
- Outputs: Pl (polyline curve)
- Behavior: Operates PER BRANCH on tree-structured input — a component fed N branches produces N separate polylines, not one continuous one (core illustration of "branches are watertight").
- Provenance: [STATED, AAD p.218-220, 287, 378; Essential p.49-50, 52]

### Isocurve
- Tab: Curve > Spline
- Alias: Iso
- Inputs: S (surface), uv (2D coordinate)
- Outputs: U (isocurve along u), V (isocurve along v)
- Behavior: Extracts the two isocurves passing through a given uv point.
- Provenance: [STATED, AAD p.147-148, 325]

### Curve on Surface
- Tab: Curve > Spline
- Alias: CrvSrf
- Inputs: S ("Surface", Surface — base surface), uv ("UV coordinates", Point — list/tree of uv interpolation points, from Merge), C ("Closed", Boolean — whether the resulting curve is closed)
- Outputs: C ("Curve", Curve — resulting NURBS curve coincident to the surface), L ("Length", Number — curve length), D ("Domain", Domain — curve parameter domain)
- Behavior: Creates an interpolated curve on a surface through an arbitrary set of uv points in the surface's Local Coordinate System — used to build a Galapagos-optimized shortest path across a freeform surface. Note the component reuses nickname "C" for both an input (Closed) and an output (Curve).
- Provenance: [STATED, AAD p.436] [VERIFIED https://grasshopperdocs.com/components/grasshoppercurve/curveOnSurface.html]

### Region Union
- Tab: Curve > Region | Type GUID: 1222394f-0d33-4f31-9101-7281bde89fe5
- Alias: RUnion
- Inputs: C (curves), P (plane)
- Outputs: R (unioned closed curve/region)
- Provenance: [STATED, AAD p.28-30 (as Essential); Essential p.28-30, 75]

### Offset (curve)
- Tab: Curve > Util
- Inputs: C (curve), D (distance), P (plane), C (corners/corner style)
- Outputs: C (offset curve)
- Behavior: Generic planar/3D curve offset (not surface-constrained — contrast Offset on Srf below). Offsetting a curve with sharp corners can introduce discontinuities/kinks at those corners — fix: divide the offset into many points and rebuild via Nurbs Curve.
- Provenance: [STATED, AAD p.303, 332-333; Essential p.99]

### Offset on Srf
- Tab: Curve > Util
- Alias: OffsetS
- Inputs: C (curves to offset), D (offset distance, number), S (surface(s) to keep the offset coincident to)
- Outputs: C (offset curves)
- Behavior: Unlike a generic curve offset, keeps the result coincident with a host surface — required so an inward-offset "frame" curve of a curved panel stays flush with the panel sub-surface rather than drifting off it in 3D.
- Provenance: [STATED, AAD p.227]

### Explode Curve [3-WAY NAME CONFLICT: "Explode" is shared by this component (Curve > Util), by a Mesh > Util component that explodes a mesh into faces, and by a Mesh > Analysis "Mesh Explode" — disambiguate by tab and by whether the input is a curve or a mesh]
- Tab: Curve > Util
- Alias: Explode
- Inputs: C (Curve), R (Recurse, boolean)
- Outputs: S (Segments), V (Vertices)
- Behavior: Breaks a polyline/polycurve into its constituent segments and vertices.
- Provenance: [STATED, AAD p.228, 235, 242, 378; Essential p.52]

### Discontinuity
- Tab: Curve > Analysis
- Alias: Disc
- Inputs: C (curve), L (continuity level)
- Outputs: P (discontinuity/vertex points), t (parameters)
- Behavior: Returns one branch of points per input curve (e.g. turns each Voronoi cell — a single closed curve — into its own branch of boundary vertex points).
- Provenance: [STATED, AAD p.284]

### Join Curves
- Tab: Curve > Util
- Alias: Join
- Inputs: C (curves)
- Outputs: C (joined curve)
- Provenance: [STATED, AAD p.326, 333, 370]

### Project
- Tab: Curve > Util
- Inputs: C (curve), B (target brep/surface), D (direction, optional)
- Outputs: C (projected curve)
- Behavior: Projects a curve onto a target surface, replacing straight segments with true surface-coincident curves — essential post-step for diagrid construction (a diagrid floats off a curved surface except at corners; Project snaps it back).
- Provenance: [STATED, AAD p.157-158]

---

## Surface

### Extrude
- Tab: Surface > Freeform
- Alias: Extr
- Inputs: B (Base curve/Brep), D (Direction, vector)
- Outputs: E (Extrusion)
- Behavior: Extrudes a base curve/brep along a direction vector — "the easiest way to create a surface."
- Provenance: [STATED, AAD p.35, 75-76, 141]

### Loft
- Tab: Surface > Freeform | Type GUID: a7a41d0a-2188-4f7a-82cc-1a2c4e4ec850
- Inputs: C (curves/sections), O (options)
- Outputs: L (lofted surface)
- Behavior: Generates a surface through a set of section curves.
- Provenance: [STATED, AAD p.98, 141, 223-224, 324, 452; Essential p.32, 45-47, 73]

### Loft Options
- Tab: Surface > Freeform
- Inputs: Rbd (rebuild, int/bool), Cl (closed, bool), type (integer 0-5: 0=Normal,1=Loose,2=Tight,3=Straight,4=Developable,5=Uniform)
- Outputs: feeds Loft's O-input
- Behavior: Sets loft behavior; rebuild needed when too few section curves exist for a smooth surface.
- Provenance: [STATED, AAD p.98]

### Boundary Surfaces
- Tab: Surface > Freeform | Type GUID: d51e9b65-aa4e-4fd6-976c-cef35d421d05
- Alias: Boundary
- Inputs: E (closed, planar, continuous curve(s)/edges)
- Outputs: S (planar surface, trimmed or untrimmed)
- Behavior: Creates a flat planar surface bounded by closed curve(s); also usable as an implicit planarity test (only produces a surface if the boundary curves are planar).
- Provenance: [STATED, AAD p.114, 141, 270, 449; Essential p.75]

### Surface from Points
- Tab: Surface > Freeform
- Alias: SrfGrid
- Inputs: P (Points — grid of points, must be pre-ordered row-by-row/column-by-column and set to flatten mode), U (U Count — number of points in u-direction, integer), I (Interpolate — boolean, interpolate a surface through the points vs. use them as control points)
- Outputs: S (Surface)
- Behavior: Builds a surface from a rectangular grid of points; needs an explicit U count to know how many points lie in one direction (obtained e.g. via List Length on a Range output). WARNING: assumes the input list is already sequenced in row/column grid order — a geometrically-correct but list-order-scrambled point set produces a severely malformed, self-intersecting surface with NO error raised.
- Provenance: [STATED, AAD p.105, 142, 248-249, 252] [VERIFIED https://grasshopperdocs.com/components/grasshoppersurface/surfaceFromPoints.html]

### Edge Surface
- Tab: Surface > Freeform
- Alias: EdgeSrf
- Inputs: 2, 3, or 4 ordered edge curves (E1-E4)
- Outputs: interpolated surface
- Behavior: Creates a surface interpolating between 2-4 ordered boundary/edge curves. Can only cap boundaries of exactly 4 edges — N-sided openings (e.g. hexagons) require a different capping strategy (two Lofts between opposite edge pairs, or Patch as a general alternative).
- Provenance: [STATED, AAD p.142, 155, 232, 239, 241]

### Patch
- Tab: Surface > Freeform | Type GUID: 57b2184c-8931-4e70-9220-612ec5b3809a
- Inputs: points and/or open/closed curves
- Outputs: trimmed or untrimmed surface
- Behavior: Fits a surface using perpendicular "span" curves generated from the input; spans rarely align with the output surface's edges — a fallback when other surfacing methods aren't feasible (e.g. general-purpose N-sided capping).
- Provenance: [STATED, AAD p.143, 239, 241]

### Network Surface
- Tab: Surface > Freeform
- Alias: NetSurf
- Inputs: U (curve network, direction 1), V (curve network, direction 2), C (continuity: 0=Loose,1=Position,2=Tangency,3=Curvature)
- Outputs: S (surface fit through the two curve families)
- Behavior: Builds one surface from two ordered curve sets — more edge control than Loft. Also usable as an alternative weave finish: if warp/weft threads are allowed to touch (skip the Negative-vector step), the resulting curve network can be fed directly into Network Surface for one continuous quilted surface instead of discrete piped tubes.
- Provenance: [STATED, AAD p.143-144, 246-247]

### Sweep1
- Tab: Surface > Freeform
- Inputs: section curve, one rail curve
- Outputs: surface
- Provenance: [STATED, AAD p.143]

### Sweep2
- Tab: Surface > Freeform
- Inputs: section curve, two rail curves
- Outputs: surface
- Provenance: [STATED, AAD p.143]

### Revolution
- Tab: Surface > Freeform
- Inputs: P (profile curve), A (axis), D (angle domain)
- Outputs: surface
- Behavior: Revolves a profile curve around a fixed axis.
- Provenance: [STATED, AAD p.144]

### Rail Revolution
- Tab: Surface > Freeform
- Alias: RailRev
- Inputs: P (profile curve), R (rail curve), A (revolution axis line, per one usage)
- Outputs: surface (has a visible "Seam")
- Behavior: Revolves a profile using a rail curve instead of a fixed axis, letting the axis itself vary along the rail — used to rebuild a smooth-edged surface of revolution replacing a sharp-edged twisted Loft.
- Provenance: [STATED, AAD p.144, 326]

### Pipe
- Tab: Surface > Freeform
- Inputs: C (Curve — base/rail curve), R (Radius, number), E (Caps — integer 0=None, 1=Flat, 2=Round)
- Outputs: P (Pipe, Brep)
- Behavior: Sweeps a circular cross-section of given radius along one or more rail curves — e.g. turns a wireframe diagrid into a tubular 3D structure, or a woven thread curve into a solid member.
- Provenance: [STATED, AAD p.159, 245; Essential p.96-99] [VERIFIED https://grasshopperdocs.com/components/grasshoppersurface/pipe.html]

### Evaluate Surface
- Tab: Surface > Analysis
- Alias: EvalSrf
- Inputs: S (surface, should be Reparameterized), uv (2D coordinate)
- Outputs: P (point, WCS), N (normal vector), F (tangent plane)
- Behavior: Surface analog of Evaluate Curve.
- Provenance: [STATED, AAD p.144-146, 178, 269]

### Surface CP
- Tab: Surface > Analysis
- Alias: Srf CP
- Inputs: P (point, WCS), S (surface)
- Outputs: P (closest point P' on surface), uvP (local uv coordinate), D (displacement distance)
- Behavior: World-to-Local conversion for surfaces (surface analog of Curve CP); if the input point lies on the surface, P=P' and D=0.
- Provenance: [STATED, AAD p.146, 204, 269, 436]

### Divide Surface
- Tab: Surface > Util
- Alias: SDivide
- Inputs: S (surface), U (U count), V (V count)
- Outputs: P (grid points), N (normal vectors), uv (local coordinates)
- Behavior: Generates a grid of points at isocurve intersections dividing u/v evenly by the given integer counts. Dividing a single surface produces a TREE of points (a grid), one branch per row/column. Its natural U+1-branches x V-items output tree is exploited directly as the "warp" direction of a weave, and Flip-Matrix-transposed to get the "weft" direction for free.
- Provenance: [STATED, AAD p.148, 176, 245-246, 248; Essential p.58, 101]

### Isotrim
- Tab: Surface > Util
- Alias: SubSrf
- Inputs: S (surface), D (list of uv sub-domains)
- Outputs: S (list of untrimmed sub-surfaces)
- Behavior: Splits a surface into contiguous untrimmed sub-surfaces per a supplied grid of sub-domains (typically from Divide Domain²). Output sub-surfaces KEEP the original parent surface's domain (not reset to [0,1]) unless explicitly Reparameterized.
- Provenance: [STATED, AAD p.149-150, 178-179, 271]

### Deconstruct Brep
- Tab: Surface > Analysis
- Alias: DeBrep
- Inputs: B (Brep: surface, polysurface, or solid)
- Outputs: F (faces), E (edges), V (vertices)
- Behavior: Extracts all constituent faces, edges, vertices of any Brep. When fed a list of N sub-surfaces at once, each downstream List Item(i=k) extracts "vertex slot k of every sub-surface" as one flat parallel list (implicit grouping, not explicit tree manipulation) — key to scaling single-item recipes (e.g. a diagrid) to whole-surface recipes.
- Provenance: [STATED, AAD p.152-153, 156-157, 189, 218, 269, 328]

### Center Box
- Tab: Surface > Primitive
- Alias: Box
- Inputs: B (base plane), X (x-domain), Y (y-domain), Z (z-domain)
- Outputs: B (box, a 6-face Brep)
- Behavior: Builds a box primitive; output is a Brep not a single Surface — wiring directly into a Surface-typed parameter causes a red type-mismatch error; fix: Deconstruct Brep first.
- Provenance: [STATED, AAD p.153, 187-188]

### Bounding Box
- Tab: Surface > Primitive
- Alias: BBox
- Inputs: C (geometry/content), P (plane, optional)
- Outputs: B (box), B (second box output — e.g. axis-aligned vs. plane-aligned)
- Behavior: Right-click mode toggle: "Per Object" (one bbox per input geometry) vs. "Union Box" (one box enclosing all input geometries together).
- Provenance: [STATED, AAD p.210-211, 327-328]

### Geodesic
- Tab: Surface > Analysis (implied)
- Inputs: S (surface), S (start point on surface), E (end point on surface)
- Outputs: G (geodesic curve)
- Behavior: Constructs the shortest-path curve ("straight line in curved space") between two points on a surface — used as a natural cutting curve for Surface Split, and (per a guest project) as the basis of a gridshell panelization pattern.
- Provenance: [STATED, AAD p.154, 489-490]

### Surface Split
- Tab: Intersect > Physical (RESOLVED — AAD p.178-179's "Surface > Util" citation is an internal inconsistency, that page range discusses Surface-tab material generally; Intersect > Physical is the component's actual/only tab)
- Alias: SrfSplit
- Inputs: S (surface), C (splitting curve(s), coincident with the surface)
- Outputs: F (trimmed surface fragments — index 0 = the split "main" surface, indices 1..N = "scrap" surfaces in one worked example)
- Behavior: Splits a surface along curve(s) lying on it into separate trimmed pieces.
- Provenance: [STATED, AAD p.155, 178-179] [VERIFIED https://grasshopperdocs.com/components/grasshopperintersect/surfaceSplit.html]

### Area
- Tab: Surface > Analysis (per book's own label, applied even to a planar closed curve)
- Inputs: G (closed planar curve, or surface)
- Outputs: A (area), C (centroid)
- Behavior: Computes area and centroid; used in attractor recipes purely for the centroid output ("center of each circle").
- Provenance: [STATED, AAD p.62-63, 113, 269]

### Volume
- Tab: Surface/Mesh > Analysis
- Inputs: G (closed 3D geometry/brep)
- Outputs: V (volume), C (centroid)
- Provenance: [STATED, AAD p.63, 191, 197]

### Principal Curvature [NAME CONFLICT: nicknamed "Curvature" on canvas — same nickname as Surface Curvature below, disambiguate by outputs]
- Tab: Surface > Analysis
- Alias: Curvature
- Inputs: S (surface), uv (point in UV domain, e.g. MD Slider)
- Outputs: F (frame/point), C1 (curve, principal direction 1), C2 (curve, principal direction 2), K1 (vector, min principal curvature direction), K2 (vector, max principal curvature direction)
- Behavior: At point P on a surface, C1 = curve of minimum curvature K1, C2 = curve of maximum curvature K2 through P; directions always perpendicular.
- Provenance: [STATED, AAD p.167, 169]

### Surface Curvature [NAME CONFLICT: nicknamed "Curvature" — see Principal Curvature above]
- Tab: Surface > Analysis
- Alias: Curvature
- Inputs: S (surface), uv (point)
- Outputs: F (frame/point), G (Gaussian Curvature), M (Mean Curvature)
- Behavior: G = K1·K2 (product of principal curvatures; G=0 developable, G>0 synclastic/dome, G<0 anticlastic/saddle); M = (K1+K2)/2 (M=0 defines minimal surfaces, e.g. catenoids/soap films). Signed-curvature convention: circles are defined as negative curvature, so e.g. a cylinder's M comes out negative — must Absolute-value before using as a physical quantity like radius.
- Provenance: [STATED, AAD p.167, 169, 173-174, 178]

### Osculating Circles
- Tab: Surface > Analysis
- Alias: Osc
- Inputs: S (Surface), uv (Point — {u,v} coordinate to evaluate)
- Outputs: P (Point — surface point at that uv), C1 (First circle, Curve — first principal osculating circle), C2 (Second circle, Curve — second principal osculating circle)
- Behavior: Developability test: if the surface is developable at P, at least one of C1/C2 degenerates to a straight line (very-large-radius circle); test by piping into a Line-cast component — cast succeeds (valid) = line-like = developable there; cast fails (red/error) = genuine arc = not developable there via that direction. CORRECTED/MERGED: this is the same component previously also listed under "Tab unconfirmed" as "Oscillator" (AAD p.309, identical S,uv → P,C1,C2 shape) — "Oscillator" is not a real Grasshopper component name; that entry was a mistranscription/mislabeling of this one and is merged in here.
- Provenance: [STATED, AAD p.175-176] [STATED, AAD p.309 as "Oscillator" — merged, same component] [VERIFIED https://grasshopperdocs.com/components/grasshoppersurface/osculatingCircles.html]

---

## Mesh

### Mesh Triangle
- Tab: Mesh > Primitive
- Alias: Triangle
- Inputs: A, B, C (corner point-list indices)
- Outputs: F (mesh face)
- Behavior: Builds one triangular mesh face by topology (index references into a separate vertex list, not raw points); winding order (CCW) determines front/back orientation. "Creating meshes by topology" strategy — suited to small point counts or repeating logics.
- Provenance: [STATED, AAD p.263-265]

### Construct Mesh
- Tab: Mesh > Primitive
- Alias: ConMesh
- Inputs: V (vertices/points), F (faces), C (colors, optional)
- Outputs: M (mesh)
- Behavior: Assembles a mesh from a vertex list + face-index list (+ optional colors).
- Provenance: [STATED, AAD p.263]

### Mesh Quad
- Tab: Mesh > Primitive
- Alias: Quad
- Inputs: A, B, C, D (corner point-list indices)
- Outputs: F (mesh face)
- Provenance: [STATED, AAD p.265-266]

### Delaunay Mesh
- Tab: Mesh > Triangulation
- Alias: Del
- Inputs: P (points), Pl (plane/planes)
- Outputs: M (mesh)
- Behavior: Triangulates an arbitrary point set maximizing minimum angle (avoids skinny/thin triangles that produce inaccurate FEM/particle-spring simulation results); formal rule: for each triangulated face, its circumscribed "Delaunay circle" must not contain any other point of the set. Operates per-branch on grafted/tree-structured input (one discrete disconnected mesh per branch — requires join+weld afterward to fuse).
- Provenance: [STATED, AAD p.266-268, 283-285, 305]

### Mesh Surface / Mesh UV
- Tab: Mesh > Util (RESOLVED — AAD p.450/456's "Mesh > Triangulation" citation is an internal inconsistency; Util is correct. Mesh > Triangulation is a real, separate panel too, home to Delaunay Mesh/Voronoi/TriRemesh — AAD appears to have conflated the two panels for this entry)
- Alias: Mesh UV
- Inputs: S (Surface), U (U Count), V (V Count), H (Overhang — allow faces to overhang trims, boolean), Q (Equalize — equalize span length, boolean)
- Outputs: M (Mesh, quadrangular)
- Behavior: NURBS-to-mesh conversion — reliable only for UNTRIMMED surfaces (clean rectangular isogrid maps directly to quad grid); trimmed surfaces only approximate their boundary via this component (Mesh Brep preserves exact boundary but risks skinny triangles near it). U/V counts must match numerically across adjoining surfaces converted independently, or mismatched vertex counts ("T-nodes") prevent correct welding.
- Provenance: [STATED, AAD p.269-272, 278-279, 382, 450, 456] [VERIFIED https://grasshopperdocs.com/components/grasshoppermesh/meshSurface.html]

### Face Boundaries
- Tab: Mesh > Analysis
- Inputs: M (Mesh)
- Outputs: B (Boundary — polyline per face)
- Behavior: Used with Planar to test whether a converted mesh's faces are planar (PQ-mesh check).
- Provenance: [STATED, AAD p.270] [VERIFIED https://grasshopperdocs.com/components/grasshoppermesh/faceBoundaries.html]

### Planar
- Tab: Curve > Analysis (CORRECTED from "Analysis > Curve" — note: this component is physically listed here under the Mesh section of this document because AAD introduces it alongside mesh-planarity checking, but its actual GH tab is Curve > Analysis, not a Mesh tab)
- Inputs: C (Curve)
- Outputs: p (Planar, boolean), P (Plane — best-fit plane), D (Deviation, number)
- Behavior: AAD's own text/diagram recorded only the single boolean output; two more outputs (Plane, Deviation) exist on the real component.
- Provenance: [STATED, AAD p.270] [VERIFIED https://grasshopperdocs.com/components/grasshoppercurve/planar.html]

### Mesh Join
- Tab: Mesh > Util
- Alias: MJoin
- Inputs: M (list of meshes)
- Outputs: M (single merged mesh, vertices NOT welded)
- Behavior: Contrast with Weaverbird's Join Meshes and Weld (Third-party plugins) — MJoin keeps duplicate/unshared vertices at shared edges (e.g. 100 quad faces x 4 unshared vertices = 400 total vertices vs. welded 121 for a 10x10 grid).
- Provenance: [STATED, AAD p.271]

### Mesh Flip
- Tab: Mesh > Util
- Alias: Flip
- Inputs: M (mesh)
- Outputs: M (mesh with reversed face direction/winding)
- Behavior: Fixes face-orientation incompatibility between adjoining meshes converted from different surfaces (visible as a shading/shadow artifact along the shared edge) before joining/welding/subdividing.
- Provenance: [STATED, AAD p.280]

### Voronoi
- Tab: Mesh > Triangulation
- Inputs: P (points), R (radius, optional), B (containment boundary curve), Pl (plane)
- Outputs: C (Voronoi cells)
- Behavior: Decomposes space into cells, one per seed point, such that every location in a cell is closer to its seed than any other. No R input → defaults to infinite radius (full tessellation, cells share edges). Finite R → clips each cell to a circle of that radius (may overlap/leave gaps, not a clean tiling).
- Provenance: [STATED, AAD p.281-283]

### Explode (mesh) [3-WAY NAME CONFLICT — see Explode Curve (Curve tab) and Mesh Explode below]
- Tab: Mesh > Util
- Inputs: M (mesh)
- Outputs: F (list of individual single-face mesh pieces)
- Provenance: [STATED, AAD p.292]

### Mesh Explode [3-WAY NAME CONFLICT: nicknamed "Explode," distinct from the Mesh > Util "Explode" above and from Curve > Util "Explode Curve" — three different "Explode"-family components; disambiguate by tab and input type]
- Tab: Analysis (MeshEdit plugin) — CORRECTED: no native/core Grasshopper "Mesh Explode" component was found in any current documentation; the best-attested match is the MeshEdit plugin's "Mesh Explode" (by Ursula Frick & Thomas Grabner, the "uto" authors — see Mesh Edit plugin section). Recommend re-filing this entry under Third-party plugins > Mesh Edit rather than native Mesh > Analysis.
- Alias: Explode
- Inputs: M (Mesh), I (Interpolate — interpolate vertex colours, boolean; the book's "J (Join?)" is not attested anywhere and is likely a misread of "I")
- Outputs: F (Faces, Mesh type)
- Behavior: Breaks a mesh into its constituent faces.
- Provenance: [STATED, AAD p.388, 391-392, 453-455] [VERIFIED https://discourse.mcneel.com/t/mesh-explode/198247] [VERIFIED https://grasshopperdocs.com/components/meshedit/meshExplode.html]

### Deconstruct Mesh
- Tab: Mesh > Analysis
- Alias: DeMesh
- Inputs: M (mesh)
- Outputs: V (Vertices), F (Faces), C (Colors), N (Normals)
- Provenance: [STATED, AAD p.391-392]

### Face Normals
- Tab: Mesh > Analysis
- Alias: FaceN
- Inputs: M (Mesh)
- Outputs: C (Centers — center point of each face), N (Normals — normal vector per face)
- Behavior: Used to derive per-panel local offset directions (via Plane Normal) so that non-coplanar panel arrays displace correctly along their OWN normal rather than one global direction.
- Provenance: [STATED, AAD p.305, 450] [VERIFIED https://grasshopperdocs.com/components/grasshoppermesh/faceNormals.html]

### Mesh Colours
- Tab: Mesh > Primitive
- Alias: MCol
- Inputs: M (mesh, grafted), C (colours, grafted — e.g. from an Object Request RGB output)
- Outputs: M (mesh with per-face vertex colours applied)
- Behavior: Visualizes an analysis-value colour gradient directly on the mesh.
- Provenance: [STATED, AAD p.458]

---

## Intersect

### Surface Split
- Tab: Intersect > Physical (RESOLVED — see full entry under Surface tab above; cross-referenced here per its confirmed Intersect tab)
- Alias: SrfSplit
- Inputs: S (surface), C (splitting curve(s))
- Outputs: F (trimmed surface fragments)
- Provenance: [STATED, AAD p.155, 178-179] [VERIFIED https://grasshopperdocs.com/components/grasshopperintersect/surfaceSplit.html] (see Surface tab for full entry)

### Intersect (Brep|Plane)
- Tab: Intersect > Mathematical
- Alias: Sec
- Inputs: B (brep), P (plane)
- Outputs: C (curves), P (points)
- Behavior: Intersects a brep with a plane to compute section/contour curves — core of a unidirectional-sectioning fabrication recipe (waffling/CNC).
- Provenance: [STATED, AAD p.332]

---

## Transform

### Move
- Tab: Transform > Euclidean (RESOLVED — "Euclidian" is simply a misspelling found across these sources' citations; the panel is spelled "Euclidean" in current GH1) | Type GUID: e9eb1dcf-92f6-4d4d-84ae-96222d60f56b
- Inputs: G (Geometry), T (Translation, vector)
- Outputs: G (moved Geometry), X (Transform data)
- Behavior: Moves geometry by a translation vector. Feeding T with a LIST of vectors (e.g. an increasing Series through Unit Z) produces one translated copy per vector via default list matching — the book's standard technique for stacking/arraying copies of a single base object "for free."
- Provenance: [STATED, AAD p.57-58, 66, 88, 187, 269, 366-397 (Kangaroo recipes); Essential p.75, 79-101] [VERIFIED https://grasshopperdocs.com/components/grasshoppertransform/move.html]

### Scale
- Tab: Transform > Affine (RESOLVED — AAD p.113-114/451-452's "Transform > Euclidean" citation is an internal inconsistency within the same book; p.196/323, Affine, is correct)
- Inputs: G (geometry), C (center of scaling), F (scale factor)
- Outputs: G (scaled geometry), X (transform, in some usages)
- Behavior: Scales geometry by factor F about center point C (any point, not necessarily the object's own centroid). F must be a positive number and can never be exactly 0 ("a null scale factor is a mathematical error"); 0<F<1 shrinks, F=1 unchanged, F>1 enlarges. Supplying a LIST of factors (one per object, matched against a list of geometries and a list of per-object centers) lets each object scale independently.
- Provenance: [STATED, AAD p.113-114, 196-198, 323, 451-452; Essential p.6-7] [VERIFIED https://grasshopperdocs.com/components/grasshoppertransform/scale.html]

### Rotate
- Tab: Transform > Euclidean
- Inputs: G (geometry), A (angle, radians), P (plane to rotate in)
- Outputs: G (rotated geometry), X (transform)
- Behavior: Rotation around a fixed point/rotation plane (in-plane/2D-style case); angle must be radians (convert a Degrees slider via Radians first).
- Provenance: [STATED, AAD p.189-190; Essential p.75]

### Rotate Axis
- Tab: Transform > Euclidean
- Alias: RotAx
- Inputs: G (geometry), A (angle, radians), X (rotation axis, line)
- Outputs: G (rotated geometry), X (transform)
- Behavior: Rotates around an explicit 3D axis line directly (vs. Rotate's plane-based in-plane rotation); same radians requirement. Used with a per-floor incrementing angle (Series) for a "twisted tower" progressive-rotation recipe.
- Provenance: [STATED, AAD p.189-193, 324]

### Orient
- Tab: Transform > Euclidean
- Inputs: G (geometry), A (initial/reference plane), B (final/target plane)
- Outputs: G (oriented geometry), X (transform)
- Behavior: Maps geometry from plane A to plane B in one step = translation + rotation combined, replacing separate Move+Rotate chains — e.g. flattening arbitrarily-oriented rib surfaces onto XY, or laying closed planar section curves flat for CNC output.
- Provenance: [STATED, AAD p.193-194, 334]

### Box Morph
- Tab: Transform > Morph
- Alias: Morph
- Inputs: G (geometry to morph), R (reference/"pliable" box enclosing G), T (target box)
- Outputs: G' (morphed geometry)
- Behavior: Cage-style deformation, likened to Rhino's Cage/CageEdit — maps every point of G from R's local box-coordinates to T's box-coordinates, so irregular/twisted target boxes produce correspondingly deformed copies (e.g. re-imposing a twisted-tower silhouette onto a plain surface of revolution).
- Provenance: [STATED, AAD p.210-211, 327-328]

### Twisted Box
- Tab: Transform > Morph
- Alias: TBox
- Inputs: A, B, C, D, E, F, G, H (eight corner points defining a twisted hexahedron)
- Outputs: B (twisted box brep)
- Provenance: [STATED, AAD p.211, 328]

### Surface Box
- Tab: Transform > Morph
- Alias: SBox
- Inputs: S (surface), D (bidimensional domain), H (height, number or list)
- Outputs: B (twisted box(es) conforming to the surface)
- Behavior: Auto-generates a grid of surface-conforming (potentially twisted) target boxes from a surface's UV subdivision; used with Box Morph for paneling. Non-constant H (e.g. random, incl. negative) per cell produces varying/inverted-height panels.
- Provenance: [STATED, AAD p.212-214]

---

## Display

### Vector Display
- Tab: Display > Vector
- Alias: VDis
- Inputs: A (anchor/start point), V (vector to display)
- Outputs: none (display-only)
- Behavior: Visualizes a vector as an arrow in the Rhino viewport (vectors have no default preview). Used pervasively to verify vector direction (solar rays, face normals) before further processing.
- Provenance: [STATED, AAD p.66-67, 96-99, 169, 185, 448-454]

### Custom Preview
- Tab: Display > Preview | Type GUID: 537b0419-bbc2-4ff4-bf08-afe526367b2c
- Alias: Preview
- Inputs: G (Geometry), S (Swatch/color)
- Outputs: none (display-only)
- Behavior: Overrides GH's default red preview color for specific geometry using a custom color sourced from Colour Swatch or a computed Gradient.
- Provenance: [STATED, AAD p.67, 114, 309]

### Point List
- Tab: Display > Vector
- Inputs: P (Points), T (Tags — boolean, show index numbers), L (Lines — boolean, show connecting lines), S (Size — number, font size)
- Outputs: none (display-only)
- Behavior: Overlays each point's list-index number in the Rhino viewport; S controls displayed text size. AAD's own diagram was missing the T and L boolean toggle inputs, now filled in. [POSSIBLE MERGE: Essential's "Points" component (p.78, 97) describes the identical index-tagging behavior under a shortened name — likely the same component.]
- Provenance: [STATED, AAD p.65; Essential p.78, 97 as "Points"] [VERIFIED https://grasshopperdocs.com/components/grasshopperdisplay/pointList.html]

### ARGB
- Tab: Display > Colour
- Inputs: C (colour, e.g. from Image Sampler output)
- Outputs: A (alpha), R (red), G (green), B (blue)
- Behavior: Default output range 0-1 (fractional); right-click "Integer Channels" switches to 0-255.
- Provenance: [STATED, AAD p.208]

### Text Tag 3D
- Tab: Display > Dimensions
- Alias: Tag
- Inputs: L (location points), T (text/values to display), S (text Size), C, J
- Outputs: displays numeric analysis result at each location point in the Rhino viewport
- Provenance: [STATED, AAD p.464]

### Colour (RGB)
- Tab: Params > Colour or Display (ambiguous per source)
- Alias: RGB
- Inputs: R, G, B, A
- Outputs: C (colour)
- Provenance: [STATED, AAD p.309]

---

## Tab unconfirmed

### Oscillator — CORRECTED, MERGED into Osculating Circles
- Status: CORRECTED. "Oscillator" is not a real Grasshopper component name (no such component exists in current or legacy GH1 documentation). This AAD p.309 diagram (S,uv → P,C1,C2) is the real **Osculating Circles** component (Surface > Analysis) — see the full merged entry there. No native or plugin component named "Oscillator" with this port shape was found anywhere searched (the only unrelated "Oscillator"-named component found, Heteroptera's "Noise Oscillator," has a different tab and shape).
- Provenance: [NOT IN SOURCE: purpose not explained, AAD p.309] [CORRECTED, VERIFIED https://grasshopperdocs.com/components/grasshoppersurface/osculatingCircles.html]

### Draw Arc
- Tab: "probable Curve > Primitive" per source, but flagged as an inferred guess rather than confirmed — placed here per the "don't guess a tab" instruction
- Alias: DArc
- Inputs: A, R
- Outputs: B
- Behavior: Not elaborated in source; the alias "DArc" also risks confusion with the distinct, better-documented "Deconstruct Arc" component (Curve > Analysis, in: A(arc), out: B/R/A) — these are almost certainly NOT the same component given the different input/output shapes, but the shared abbreviation is a source of ambiguity worth flagging. Checked against current docs: no Grasshopper component (native or plugin) named "Draw Arc" was found; its (A,R)→(B) shape matches no real arc-related component found (Arc, Arc 3Pt, Arc SED, Deconstruct Arc). May be a genuinely obscure/legacy GH 0.9-era component, a custom user cluster in the book's example file, or a mistranscription of Deconstruct Arc's ports.
- Provenance: [INFERRED, AAD p.309 diagram] [UNVERIFIED — no documentation found 2026-07]

### Delete Consecutive (DCon) — CORRECTED identity
- Tab: Sets (sub-panel not independently confirmed beyond "Sets"; likely Sets > List by analogy with neighboring list-filtering components)
- Inputs: S (Set, Generic Data), W (Wrap, Boolean — if True, treats the last and first items as adjacent for consecutive-duplicate comparison, i.e. wraps around)
- Outputs: S (Set, Generic Data — set with consecutive identical members removed), N (Count, Integer — number of members removed)
- Behavior: Diagram-stated purpose: "remove consecutive duplicates" / "weave points and remove duplicates" (used right after a Weave operation in a Zigzag-tutorial recipe, to strip points where a mesh/grid's diagonals coincide with real edges). CORRECTED: the abbreviation "DCon" stands for **Delete Consecutive**, not Deconstruct/Deconstruct Point — neither of which removes duplicates. The source recorded N as a third INPUT as well as an output; the real component has only 2 inputs (S,W) and 2 outputs (S,N) — N is a Count OUTPUT only, likely a transcription slip reading a 2-in/2-out diagram as 3-in/2-out.
- Provenance: [NOT IN SOURCE: authoritative component identity/tab not confirmed, Essential p.96] [CORRECTED, VERIFIED https://grasshopperdocs.com/components/grasshoppersets/deleteConsecutive.html]

---

## Third-party plugins

Plugin components are kept separate from core Grasshopper per instructions. Grouped by plugin.

### LunchBox (by Nathan Miller, CASE)

#### Surface Direction
- Tab: LunchBox > Util
- Alias: RevSrf
- Inputs: Srf (surface), R (Reverse Option, integer 0-3)
- Outputs: RevSrf (surface with inverted uv)
- Behavior: R=0 no change, R=1 inverts u, R=2 inverts v, R=3 inverts both. Output often needs Reparameterize applied afterward. The first non-native component shown in AAD, signaling the plugin ecosystem fills gaps in the native toolset.
- Provenance: [STATED, AAD p.147]

#### Hexagon Cells
- Tab: LunchBox > Panels
- Alias: Hex
- Inputs: Srf (target surface), U (U divisions), V (V divisions)
- Outputs: Cells (hexagonal closed polylines; border cells are 4- or 5-sided instead of 6-sided), Centers (center point of each cell)
- Behavior: Applying a hex grid to a rectangular surface leaves border row/column cells as 4-/5-sided rather than true hexagons — must cull via an edge-count=6 test before further per-cell operations.
- Provenance: [STATED, AAD p.235-236]

#### Triangle Panels B
- Tab: LunchBox plugin
- Alias: TriB
- Inputs: Srf (surface), U (U divisions), V (V divisions)
- Outputs: Panels (triangular panel surfaces)
- Provenance: [STATED, AAD p.268-269]

#### Diamond Panels
- Tab: LunchBox > Panels
- Alias: Diamond
- Inputs: Srf (surface), U (U divisions), V (V divisions)
- Outputs: Diamonds (quad/diamond sub-surfaces), Triangles (triangular infill sub-surfaces)
- Provenance: [STATED, AAD p.288, 290]

#### Lunchbox (urban-data import context)
- Behavior: Also used, in a different chapter, to import tables/databases (geo-referenced population, commercial hubs, schools, libraries data published by public administrations) into Grasshopper — same plugin family as the paneling components above.
- Provenance: [STATED, AAD p.479]

### Weaverbird (by Giulio Piacentino)

#### Join Meshes and Weld
- Tab: Weaverbird > Extract (Wb tab)
- Alias: wbJoin
- Inputs: M+ (meshes, set to flatten), W (boolean: weld coincident vertices)
- Outputs: M (single welded mesh)
- Behavior: Grasshopper has no native Subdivision Surface (SubD) support — it comes entirely from Weaverbird, which adds mesh creation, extraction, smoothing, SubD, and transform components under a new "Wb" tab.
- Provenance: [STATED, AAD p.271, 273]

#### Naked/Mesh Edges (wbEdges)
- Tab: Wb Extract (CORRECTED from "Weaverbird > Extract" naming)
- Inputs: G (Mesh or Polylines — open/closed mesh, or closed polyline group)
- Outputs: L (Lines — the wires/edge lines)
- Behavior: Extracts a mesh's edges as lines, e.g. to become Kangaroo springs in a cable-net membrane recipe. CORRECTED: current "Mesh Edges" has only ONE input (G) — no second "O" input is attested. Weaverbird separately ships a "Naked boundary" component (M → C) that extracts only the open/naked boundary — a distinct component, not a second input on Mesh Edges — possibly the source of the book's "O". Plugin still actively maintained (v0.9.0.1 for Rhino 7/8 as of Jan 2026, distributed via Rhino Package Manager), by Giulio Piacentino.
- Provenance: [STATED, AAD p.305, 382] [CORRECTED, VERIFIED https://grasshopperdocs.com/components/weaverbird/meshEdges.html]

#### wbVertices
- Tab: Weaverbird > Extract
- Inputs: G (Mesh), W
- Outputs: P (Points)
- Behavior: Extracts a mesh's vertices as points, e.g. to become Kangaroo particles.
- Provenance: [STATED, AAD p.382]

#### Loop Subdivision
- Tab: Weaverbird > SubD (Wb tab)
- Alias: wbLoop
- Inputs: M (mesh to subdivide, must be TRIANGULAR), L (iteration level, 1-3), S (naked-edge treatment: 0=Fixed, 1=Smooth, 2=Corner Fixed)
- Outputs: O (subdivided mesh)
- Behavior: Charles Loop's 1987 algorithm — new vertex at every edge midpoint, splitting each triangle into 4; converges to a "limit surface" with diminishing change per iteration; a simple/schematic input mesh produces more refined output than an already-dense one. Works on meshes with holes (rounds the hole boundary).
- Provenance: [STATED, AAD p.274-276]

#### Catmull-Clark Subdivision
- Tab: Weaverbird > SubD (Wb tab)
- Alias: wbCatmullClark
- Inputs: M (mesh to subdivide, quad or triangular), L (iteration level), S (naked-edge treatment)
- Outputs: O (subdivided mesh)
- Behavior: Catmull & Clark's 1978 algorithm — the quad/triangle-mesh analogue of Loop subdivision.
- Provenance: [STATED, AAD p.277, 280]

#### Mesh Thicken
- Tab: Weaverbird > Transform (Wb tab)
- Alias: wbThicken
- Inputs: M (mesh), D (distance), T
- Outputs: O (thickened, watertight mesh)
- Behavior: Final step in making a mesh genuinely 3D-printable — gives it real wall thickness.
- Provenance: [STATED, AAD p.328]

### Kangaroo (physics engine, by Daniel Piker et al.)

#### Springs From Line
- Tab: Kangaroo > Forces
- Alias: Springs
- Inputs: Connection (lines only — other geometry yields null), Stiffness (k value, N/cm), Damping (default 10; affects only deformation velocity, not final length), Rest length (target unloaded length), UpperCutoff (default 0), LowerCutoff (default 0), Plasticity (max elastic deformation vs. rest length)
- Outputs: S (Springs)
- Behavior: Converts lines into elastic linear springs per Hooke's law F=k·X. Rest Length = Start Length → "perfectly elastic"; Rest Length < Start Length (via Length × Factor 0-1) → pre-tensioned; Rest Length > Start Length (Factor 1-N) → relaxed/slack. The Connection input accepts lines only; the "Line" container component is recommended because it visibly turns red if non-line geometry is piped in.
- Provenance: [STATED, AAD p.366, 373-374, 379, 383, 388-389, 392]

#### Unary Force
- Tab: Kangaroo > Forces
- Alias: UForce
- Inputs: Point, Force
- Outputs: U
- Behavior: Applies a force vector to every input point/particle (e.g. self-weight via a negative Unit-Z vector). Calibration rule: force magnitude should equal total load divided by particle count.
- Provenance: [STATED, AAD p.366, 381]

#### KangarooPhysics
- Tab: Kangaroo (Kangaroo tab)
- Alias: Kangaroo
- Inputs: Force objects (flattened list of Springs+Forces outputs — MUST be set to flatten), AnchorPoints, Settings, Geometry (visualization geometry for live preview), SimulationReset
- Outputs: Out, Iterations, ParticlesOut, GeometryOut
- Behavior: The physics solver "engine" — iterates particle positions/velocities toward equilibrium each solver tick. Does not auto-recompute like standard GH; driven by a Timer (dotted wire) + Boolean Toggle (False=running, True=stopped — inverted from intuition; double-clicking the component gives an alternative stop/play/pause panel). Anchor points must coincide exactly with a particle or they have no effect. Dragging anchors live then stopping/restarting without returning them to original position breaks the solver's restraint recognition. Cannot process NURBS curves/surfaces directly — must discretize to lines/meshes first.
- Provenance: [STATED, AAD p.363-369, 393]

#### Kangaroo Settings
- Tab: Kangaroo (Kangaroo tab)
- Inputs: Tolerance, TimeStep, SubIterations, Floor (Boolean — enables virtual ground-plane collision), Drag, Restitution, StaticFriction, KineticFriction, Settle, Tumble, Sound, Solver
- Outputs: Settings
- Provenance: [STATED, AAD p.393]

#### MeshCorners
- Tab: Kangaroo > Utility
- Inputs: Mesh, AngleTolerance
- Outputs: L (corner points list)
- Behavior: Auto-extracts the corner points of a typically 4-sided/UV mesh, e.g. for a simple corner-anchored membrane simulation.
- Provenance: [STATED, AAD p.383]

#### Naked Vertices
- Tab: Kangaroo > Utility
- Alias: NV
- Inputs: M (Mesh)
- Outputs: ClothedI, NakedI (indices), ClothedPts, NakedPts
- Behavior: Separates mesh vertices into "clothed" (bordered by faces on all sides) vs. "naked" (boundary/free-edge) — used to anchor an entire mesh boundary instead of just corners (edge-supported tent shape).
- Provenance: [STATED, AAD p.386]

#### WarpWeft
- Tab: Kangaroo > Mesh
- Inputs: M (Mesh)
- Outputs: A (Warp, lines), B (Weft, lines), NA (NakedA — per-edge naked-boundary boolean), NB (NakedB, same for Weft)
- Behavior: Separates a mesh's edges into two orthogonal direction groups for anisotropic (direction-dependent) spring behavior.
- Provenance: [STATED, AAD p.389] [VERIFIED https://grasshopperdocs.com/components/kangaroo2/warpWeft.html]
- Version note: AAD (2014) teaches Kangaroo-1-era components (e.g. Springs From Line, above). Kangaroo 1 was fully rewritten as Kangaroo 2 (~2015-16) with most components renamed/restructured (e.g. Springs From Line → a generic Length goal). WarpWeft is unusual in having kept the same name, tab, and role across both versions — still current in Kangaroo 2.

#### removeDuplicateLines
- Tab: Kangaroo > Utility
- Alias: dupLn
- Inputs: L (Lines), t (Tolerance)
- Outputs: Q (deduplicated lines)
- Behavior: Removes coincident/overlapping lines within tolerance — needed e.g. because a triangulated mesh-sphere's diagonals coincide with real edges near the poles, which would otherwise double-spring those regions.
- Provenance: [STATED, AAD p.391-392]

#### Shell
- Tab: Kangaroo > Utility
- Inputs: Mesh, Strength (e.g. 500), AngleFactor (e.g. 1)
- Outputs: ShellForce
- Behavior: Generates a bending-resistance force, giving discretized particle-spring surfaces moment/rigidity capacity that plain hinge-particles otherwise lack — without it, a mesh-sphere crumples irreversibly on hitting a rigid floor even at high Stiffness + diagonal bracing, since nothing resists local bending/folding at the particles.
- Provenance: [STATED, AAD p.391-393]

#### Kangaroo Hinge force / Spring force (conceptual force types, no dedicated component diagram in this range)
- Behavior: Hinge force — points move in space constrained by a rest angle; when anchor points move but the rest angle wants to stay at zero, resistance appears (used for fold lines). Spring force with rest length set to zero pulls two points together ("pinch") — used to fold/pinch a flat fabric sheet into a smocking pattern (The Magic Garden dress installation).
- Provenance: [STATED, AAD p.485]

### Karamba (structural analysis, by Clemens Presinger)

#### LineToBeam
- Tab: Karamba plugin
- Inputs: Pts, Line, New, Remove, LDist, Id
- Outputs: Pts, Elem, Info
- Behavior: Converts a Rhino line into a structural beam finite element for analysis.
- Provenance: [STATED, AAD p.408]

#### Supp
- Tab: Karamba plugin
- Inputs: Pos|Ind (node position/index), Plane, Conditions (Tx,Ty,Tz,Rx,Ry,Rz toggle buttons)
- Outputs: Supp
- Behavior: Defines a nodal support/restraint with six independently-toggleable restraint conditions (e.g. cantilever fixed end = all 6 enabled).
- Provenance: [STATED, AAD p.408]

#### PLoad
- Tab: Karamba plugin
- Inputs: Vec (force vector), Pos|Ind (application point/index), LCase (load case)
- Outputs: PLoad
- Provenance: [STATED, AAD p.408]

#### ReadMatTable
- Tab: Karamba plugin
- Inputs: Path
- Outputs: Mat
- Behavior: Reads a built-in or external material properties table.
- Provenance: [STATED, AAD p.408]

#### MatSelect
- Tab: Karamba plugin
- Inputs: ElemId, Name|Ind, Mat
- Outputs: Mat
- Behavior: Assigns a specific material (by name/index) to specific elements.
- Provenance: [STATED, AAD p.408]

#### ReadCSTable
- Tab: Karamba plugin
- Inputs: Path
- Outputs: CroSec, Info
- Behavior: Reads a built-in or external cross-section properties table (e.g. UNI5397-78/UNI5398-78, or Karamba's IPE/HE section families).
- Provenance: [STATED, AAD p.408]

#### CroSecSelect
- Tab: Karamba plugin
- Inputs: ElemIds, Name|Ind, CroSecs
- Outputs: CroSec, Info
- Behavior: Assigns a specific cross-section (by name/index) to specific elements — this is the parameter a genetic solver (Galapagos) mutates for shape optimization in AAD's worked example (index slider 29 "HEAA320" → Galapagos-optimized to index 89, ~38x displacement reduction, same topology throughout).
- Provenance: [STATED, AAD p.408, 410]

#### Assemble
- Tab: Karamba plugin
- Inputs: Pt, Elem, Support, Load, CroSec, Material, Set, LDist
- Outputs: Model, Info, Mass
- Behavior: Assembles all model inputs into one analyzable structural model.
- Provenance: [STATED, AAD p.409]

#### Analyze
- Tab: Karamba plugin
- Inputs: Model
- Outputs: Model, Disp (Displacement), G, Energy
- Behavior: Runs finite-element structural analysis (FEA) on an assembled model.
- Provenance: [STATED, AAD p.409]

#### ModelView
- Tab: Karamba plugin
- Inputs: Model, LCFactor, LCIndex, Colors, Ids
- Outputs: Model, def.Mesh, def.Curves, def.Model
- Behavior: Visualizes the deformed structural model.
- Provenance: [STATED, AAD p.409]

#### BeamView
- Tab: Karamba plugin
- Inputs: Model
- Outputs: Model, Mesh, Curves, Legend C, Legend T
- Behavior: Visualizes per-beam analysis results (section forces, stresses, utilization); configurable Display Scales (Deformation, Reactions, Loads, Supports, Local axes, Joints) and Render Settings (Length/Segment, Upper/Lower Result Threshold) and a Section Forces panel (Mx,My,Mz,Nx,Vy,Vz).
- Provenance: [STATED, AAD p.409]

### Millipede (topology optimization)

#### 2DBoundaryRegion
- Tab: Millipede plugin (2D topology optimization)
- Inputs: Boundary (Crv), IsVoid (bool, marks region as void)
- Outputs: BReg (Boundary Region)
- Provenance: [STATED, AAD p.422-424]

#### 2DSupportRegion
- Tab: Millipede plugin
- Inputs: Boundary (Geo), SUP (support-type data from StockSupportType), AM, Displacement
- Outputs: SReg (Support Region)
- Provenance: [STATED, AAD p.424]

#### StockSupportType
- Tab: Millipede plugin (Stock section)
- Inputs: X, Y, Z, RX, RY, RZ (Boolean toggles per DOF; True = restrained)
- Outputs: SUP
- Provenance: [STATED, AAD p.424]

#### 2DBoundaryLoad
- Tab: Millipede plugin
- Inputs: Boundary (Geo, load-application region), L (load vector/intensity)
- Outputs: LReg (Load Region)
- Behavior: Load intensity value has NO relationship with the topology-optimization result — safe to use a fictitious load; only geometry/regions matter.
- Provenance: [STATED, AAD p.424]

#### Topostruct2DModel
- Tab: Millipede plugin
- Inputs: M (merged region input — accepts multiple simultaneous wires: BReg+SReg+LReg), XR (XResolution, preset default 12 — book calls this "too low for every type of application")
- Outputs: FE (finite element model), P, Size
- Provenance: [STATED, AAD p.424]

#### Topostruct2DSolver
- Tab: Millipede plugin (core solver)
- Inputs (10 total, 4 used in worked examples): FE (from Topostruct2DModel — connect LAST, auto-starts analysis), SWC (Self Weight Coefficient: 0=none,1=computed once), O (Optimization Iterations — practice suggests O=1 to keep process controllable), T (Target Density 0..1 — near 0 = excessive discard, near 1 = inadequate decrease); unused-in-example inputs: MD, DTH, PerX, PerY, Load Case, All Cases, Compliant Mechanism
- Outputs: FE (pass-through for visualization), maxu (maximum displacement — typically tiny; scaling it for preview via Multiplication does NOT change the real displacement)
- Behavior: Embedded right-click/dropdown tool menu: Step, Analyze, Reset, Smooth, Elastic, Subdivide.
- Provenance: [STATED, AAD p.424-426]

#### 2DMeshResult
- Tab: Millipede plugin (visualization)
- Inputs: FE-output of solver
- Outputs: colored mesh visualizing VonMisesStresses, Principal tension, Deflection
- Provenance: [STATED, AAD p.425]

#### 3DDensityRegion
- Tab: Millipede plugin (3D topology optimization)
- Inputs: geometry (parallelepiped) defining a non-design-space volume excluded from optimization (kept as constant "framework")
- Outputs: region for 3D model assembly
- Provenance: [STATED, AAD p.429]

#### 3DIsoMesh
- Tab: Topostruct3D (Millipede plugin; printed in the book as "3DisoMesh")
- Inputs: FE (FE Model), D (Deflection), Iso (Iso Contour Value)
- Outputs: Mesh
- Behavior: Renders 3D result geometry, displays internal stresses and maximum displacements. Author confirmed as Panagiotis Michalatos (AAD omits this attribution). Plugin's current maintenance status is unclear — no explicit "discontinued" notice found, but community mentions describe it as no longer actively developed.
- Provenance: [STATED, AAD p.430] [VERIFIED https://grasshopperdocs.com/components/millipede/3DIsoMesh.html]

### Goat (exact/local optimization, by Simon Flöry)

#### Goat
- Tab: Special > Util
- Inputs: Variables (one or more Number Sliders), Objective (exactly one numeric value to minimize/maximize)
- Behavior: Double-click opens "goat - Optimization Settings" dialog: "Optimize for" (Minimum/Maximum), "Optimization algorithm" dropdown (e.g. "Local, linear approximations (COBYLA)"), "Stop optimization if" checkboxes (relative change in objective/variables below threshold, objective below value, running time exceeds limit). Exact solver: always finds the single best solution, same result every run — contrast Galapagos (heuristic, varies run to run). Local algorithms can get stuck at local optima; for complex problems run Global first then refine Local. Used in AAD's worked examples to minimize point-to-curve distance and (in a guest essay) to minimize axial force in a graphical-statics funicular form.
- Provenance: [STATED, AAD p.432-434, 467-471]

### GECO (bridge to Autodesk Ecotect Analysis, by Ursula Frick & Thomas Grabner)

#### Link Ecotect
- Tab: Extra > GECO
- Alias: EcoLink
- Inputs: E (Boolean, from Toggle — establishes/disconnects link)
- Outputs: out (text log of connectivity test), D (Boolean done-flag)
- Behavior: Must always remain an ISOLATED component connected only to a Panel, never chained to other GECO components. Color signals state: normal=OK; orange=warning (connection to Ecotect failed — fix by toggling E False then True); red=error (Ecotect/GECO not installed properly, re-toggle won't fix).
- Provenance: [STATED, AAD p.443-447]

#### Export Mesh to Ecotect
- Tab: Extra > GECO
- Alias: EcoMeshExport
- Inputs: E (bool, True=export now), M (mesh — must be Exploded+Flattened first, or Ecotect only imports faces in the tree's LAST branch), [C] (scale factor: 0=default/mm, 1000=use if Rhino doc is in meters), [N] (delete-mode: 0=delete ALL existing Ecotect geometry, 1=delete only meshes from latest export, 2=keep all existing geometry — "may lead to overlapping errors"), [F] (bool, fit analysis grid to exported mesh), [T] (ElementType index 0-15: 0_Void,1_Roof,2_Floor,3_Ceiling,4_Wall,5_Partition,6_Window,7_Panel,8_Door,9_Point,10_Speaker,11_Light,12_Appliance,13_Line,14_Solarcollector,15_Camera), [M] (material), [Z] (zone name text — same value reused across multiple export components places different meshes in one shared zone)
- Outputs: out, D (Boolean done — feeds cascade), I (face indices, feeds downstream Object Request)
- Behavior: Ecotect works EXCLUSIVELY on mesh geometry — never NURBS/breps directly.
- Provenance: [STATED, AAD p.453-457]

#### Object Request
- Tab: Extra > GECO
- Alias: EcoObjectRequest
- Inputs: E (cascade, from upstream D output), [A] (AttributeIndex — selects analysis result to retrieve), I (face indices, from EcoMeshExport.I)
- Outputs: out, RGB (colour gradient per value, feeds Mesh Colours), Min, Max, Val (numeric analysis result at each mesh-face center)
- Behavior: Used for analysis performed directly on mesh faces (vs. AnalysisGrid for point-sensor analysis).
- Provenance: [STATED, AAD p.446-448, 457-460]

#### AnalysisGrid (Import)
- Tab: Extra > GECO
- Alias: EcoGridRequest / "ImportAnalysisGrid"
- Inputs: E, [A] (AttributeIndex — e.g. daylight analysis A=0 Daylight Factor, A=1 Daylighting Levels), F
- Outputs: out, RGB, Min, Max, Val, P (grid point locations), U, V, H
- Behavior: Imports results calculated on an Analysis Grid (point-sensor based) rather than mesh faces.
- Provenance: [STATED, AAD p.444, 457, 459-460, 464]

#### EcoSunPath
- Tab: Extra > GECO
- Inputs: E (bool trigger), [D] (day, slider 1-31), [M] (month, slider 1-12), [W] (Weather File), [N], [S] (scale of output curves)
- Outputs: out, C (sundial curve), S (sun path curve), T (sunrise & sunset time), D (Boolean done, feeds cascade to EcoSunRays.E)
- Provenance: [STATED, AAD p.448-451]

#### EcoSunRays
- Tab: Extra > GECO
- Inputs: E (cascade, from EcoSunPath.D), [D], [M] (same as EcoSunPath), [T] (time of day, e.g. 8.00-18.00), [S]
- Outputs: out, F, P (vector start-point), V (solar ray vector — feed to Vector Display or MShadow.L), W
- Provenance: [STATED, AAD p.448-451]

#### Lighting Calculations
- Tab: Extra > GECO
- Alias: EcoLightCal / LightingCalculations
- Inputs: E (cascade, from FitGrid.D or similar), [T] (0=analysis grid default,1=point objects), [G], [C] (selects calculation/attribute), [P] (Precision, e.g. 2=High), [S], [L] (Sky(lux)Illuminance, e.g. 7300), [W]
- Outputs: out, D (cascade to ImportAnalysisGrid.E)
- Behavior: Calculates Daylight factor, Daylight levels, Sky component. Sky illuminance value derived from latitude (peaks ~10,100 lux at equator, decreases toward poles).
- Provenance: [STATED, AAD p.445-446, 461, 464]

#### Insolation Calculations
- Tab: Extra > GECO
- Alias: EcoSolCal
- Inputs: E (cascade, from EcoMeshExport.D), W (Weather File), [T] (Terrain Type: 0=wind-exposed,1=rural,2=suburban,3=dense urban), [C] (Calculation type: 1=incident solar radiation,2=solar absorption-transmission,3=sky factor & PAR), [M], [A], [S] (Sky Subdivision 1-15, smaller=more accurate/slower; 50=fast/approximate), [O], [G] (Object vs Grid analysis, default Object), [3D], [DP] (start/end Julian day-of-year domain, default [1,365]), [TP] (start/end time-of-day domain, 0.00-23.99)
- Outputs: out, D (cascade to Object Request.E)
- Behavior: Computes insolation (Wh/m²) via Lambert's cosine law; design intent typically maximize winter/minimize summer insolation for passive solar gain; also informs solar-collector/PV sizing.
- Provenance: [STATED, AAD p.444, 456-459]

#### MShadow (MeshShadow)
- Tab: Mesh > Util (stated as core GH tab, but used exclusively in GECO recipes)
- Inputs: M (mesh geometry to cast shadow), L (light/solar-ray vector, from EcoSunRays.V), P (arbitrary receiving plane)
- Outputs: O (shadow contour data projected onto plane P)
- Provenance: [STATED, AAD p.448-449]

#### EcoFitGrid (FitGrid)
- Tab: Extra > GECO
- Inputs: E (cascade, from EcoMeshExport.D), [A] (GridAxis: 0=XY,1=YZ,2=XZ), [T] (fit type: 0=within mesh,1=around,2=adapted,3=larger than object), [Cx],[Cy],[Cz] (face count per direction), [O] (offset from reference plane)
- Outputs: out, D (cascade)
- Behavior: Fits an analysis grid to the extents of an object already exported to Ecotect.
- Provenance: [STATED, AAD p.459]

#### MeshGrid (EcoMeshGrid)
- Tab: Extra > GECO
- Inputs: P (points), U, V, C (colours), H
- Outputs: M (colored mesh representation of the grid)
- Provenance: [STATED, AAD p.459, 464]

#### 2dAnalysisGrid (Eco2DGrid)
- Tab: Extra > GECO
- Inputs: E, [A] (GridAxis/reference plane), [W] (domain width via Construct Domain), [H] (domain height via Construct Domain), [Cw],[Ch] (face counts), [O] (offset)
- Outputs: out, D
- Behavior: Manually defines a grid's plane/size/resolution (vs. auto-fit FitGrid). Recommendation: W and H domains should both be positive or both negative (grid must lie within one quadrant).
- Provenance: [STATED, AAD p.460]

#### Geco (reused reference, Eco-Resort project)
- Behavior: Imports a real-time sun-angle value computed in Ecotect directly into HoopSnake's recursion parameters, so recursive roof geometry grows while automatically keeping summer sun out and letting winter sun in.
- Provenance: [STATED, AAD p.488]

### HoopSnake (recursion, by Yannis Chatzikonstantinou)

#### HoopSnake
- Tab: Extra tab (Logic/Code Flow) (plugin; food4rhino / yconst.com / GitHub)
- Alias: HS
- Inputs: S (Starting Data), D (Data — feedback data closing the loop), B (Termination Condition — boolean or number; stops the loop when false, or when the iteration count is reached), T (Trigger — fires one HS iteration when its content changes)
- Outputs: F (Feedback), C/H (Cumulative Feedback / Feedback History — one branch per iteration; grasshopperdocs calls it "C", the plugin's own source comments call it "H" — same output functionally), L (Loops Counter), I (Iterations Counter)
- Behavior: Emulates a loop despite GH's left-to-right-only solver logic (a true feedback wire is otherwise forbidden and would need to route a downstream output back into an upstream input). Edge-condition geometry → S-input, passes through unchanged as F; loop body's final output → D-input closes the loop; B sets iteration count. Does NOT run within GH's normal automatic solver — must be manually started via its own floating control panel (double-click to open): Step (one iteration), Auto Loop All (runs until iteration counter I = B), Reset All. Used to generate a 3D Koch-snowflake fractal (recursive triangle subdivision) and a spiral "galaxy-like" roof mesh (recursive vector move+rotate, driven by a live Ecotect sun-angle imported via Geco).
- Provenance: [STATED, AAD p.298-301, 303, 305, 486, 488-490] [VERIFIED https://grasshopperdocs.com/components/hoopsnake/hoopSnake.html]
- Version/status note: HoopSnake still works and is still distributed, but the current de-facto standard plugin for loops/recursion in Grasshopper is now **Anemone** (Loop Start/Loop End) — most present-day tutorials recommend Anemone over HoopSnake.

### Tree8 (structural toolset add-on, by Jissi Choi)

#### Allocate N
- Tab: Mesh/Tree8 plug-in (part of STRAUTO structural toolset for SAP2000/MIDAS)
- Alias: AllocN
- Inputs: Data (flat list), N (number of items per branch)
- Outputs: Data (tree, split into branches of N items each)
- Behavior: Restructures a flat list into a tree — e.g. a flat 24-point list + N=6 → 4 branches of 6 points, paths {0;0}..{0;3}. AAD initially discusses this component without naming its plugin origin (aad-part3), then explicitly identifies it as the third-party Tree8 plugin (aad-part4) — NOT a native GH component as might first appear.
- Status: deprecated/superseded by native Grasshopper's **Partition List** component per https://discourse.mcneel.com/t/tree-8-narrowly-c/101676 — Tree8 is hard to find today: not on Food4Rhino, not documented on grasshopperdocs.com, and forum users (2021+) report its original host (tree8.chang-soft.co.kr) is gone and it has compatibility problems in Rhino 7. Partition List now covers Allocate N's core function (splitting a flat list into a tree of N-item branches), making Tree8 unnecessary for this task in current Grasshopper.
- Provenance: [STATED, AAD p.250-252, 251] [VERIFIED https://www.grasshopper3d.com/profiles/blogs/tree8-list-management-components] [VERIFIED https://discourse.mcneel.com/t/tree-8-narrowly-c/101676]

### Mesh Edit (by Ursula Frick & Thomas Grabner, "uto")

#### Triangulate
- Tab: Mesh > Util — CORRECTED: a **native** Grasshopper component named "Triangulate" now exists here and does NOT require the Mesh Edit plugin, as AAD's own claim states; that claim is outdated/imprecise for current GH1.
- Alias: Tri
- Inputs: M (Mesh)
- Outputs: M (Mesh, triangulated), N (Integer — number of quads that were triangulated)
- Behavior: Converts a quad mesh to triangular (same vertex count, double face count — each quad split into 2 triangles); triangular faces are always planar even where the source quad mesh might not be. This native component's M-in/M,N-out shape matches the book's own diagram exactly. Separately, the MeshEdit plugin ships its OWN "Mesh Triangulate" (Tab: Analysis; Inputs: M, S=ShortDiagonal boolean; Outputs: M only, no count output) — a distinct component with no N output; the AAD source is likely describing what is now the native component, not (only) the plugin.
- Provenance: [STATED, AAD p.270] [CORRECTED, VERIFIED https://grasshopperdocs.com/components/grasshoppermesh/triangulate.html] [VERIFIED https://grasshopperdocs.com/components/meshedit/meshTriangulate.html]

### "Generation" add-on (by Antonio Turiello)

#### Random (Rnd) [DISTINCT from the native Random component under Sets — same concept, different plugin implementation]
- Tab: "Generation" plugin add-on (food4rhino/project/generation)
- Alias: Rnd
- Inputs: D (domain), N (count), I (interpolate/seed)
- Outputs: R (list of pseudo-random numbers, refreshed by a Timer or the Recompute command — NOT auto-refreshed like typical GH components)
- Provenance: [STATED, AAD p.306]

#### Store
- Tab: "Generation" plugin add-on
- Inputs: B (data to store), E (enable/expire trigger)
- Outputs: T (held/stored data)
- Behavior: Holds/persists data between successive Loop-plugin updates.
- Provenance: [STATED, AAD p.306, 309]

#### Loop
- Tab: separate, standalone plugin by Antonio Turiello (CORRECTED — same author as "Generation," but a distinct, independently-listed plugin, not a component bundled inside it; food4rhino/app/loop)
- Inputs/Outputs: vary by use (example diagram labels: C, O, I, N, P, R) — no structured input/output documentation could be found for it anywhere (not indexed on grasshopperdocs.com; author's own blog post carries no technical detail either)
- Behavior: Iterates a procedure by substituting an output parameter of the procedure's FINAL component into an input parameter of the procedure's INITIAL component — closes a loop "by reference" rather than a direct feedback wire; typically paired with a Timer for continuous refresh. Alternative to HoopSnake. The modern standard alternative for loops/iteration in Grasshopper is **Anemone** (Loop Start/Loop End), not this "loop" plugin or HoopSnake.
- Provenance: [STATED, AAD p.306-307, 309] [CORRECTED, VERIFIED https://www.food4rhino.com/en/app/loop]

### Urban-data plugins

#### Elk
- Tab: third-party plugin (by Timothy Logan)
- Behavior: Imports an OpenStreetMap .osm file directly into Grasshopper, generating map/topographical surfaces using OSM data + Shuttle Radar Topography Mission elevation data. Imported geometry carries metadata tags (minor/major roads, waterways, railways, railway:station, highway:bus stop, highway:pedestrian, parking, buildings, amenity, leisure:park, leisure:garden, landuse:industrial, area, etc.).
- Provenance: [STATED, AAD p.479]

#### Finches
- Tab: third-party plugin (developed by Nicholas De Monchaux)
- Behavior: Imports, exports, and batch-processes Esri shapefiles (points/lines/polygons GIS vector data, e.g. water wells, rivers, lakes).
- Provenance: [STATED, AAD p.479]

#### gHowl
- Tab: third-party plugin
- Behavior: Used to achieve exact geolocation overlap between different imported datasets, exploiting its correspondence with OpenStreetMap's coordinate system.
- Provenance: [STATED, AAD p.479]

---

## Special / Solver

### Galapagos (Genome / Fitness)
- Tab: Params > Util (native Grasshopper genetic solver, by David Rutten)
- Inputs (Genome): the arbitrary set of sliders embedded in Gene Pool component(s), or any slider(s) directly
- Inputs (Fitness): one numeric value
- Behavior: Double-click opens the "Galapagos Editor" (tabs Options/Solvers/Record): Options — Fitness Minimize/Maximize dropdown, Threshold, Runtime Limit; Evolutionary Solver settings (Max Stagnant, Population, Initial Boost); Solvers tab — Start/Stop Solver, live fitness-range graph, ranked candidate list. Heuristic solver: a population of candidates evolves via mutation/crossover/selection; NO run-to-run guarantee of an identical result (unlike the exact solver Goat). Best suited for large variable counts where no exact solver applies. Cannot be driven by a Graph Mapper (its internal curve is not slider-drivable, so it cannot itself be a Genome input — expose the sliders that feed it instead). Runs indefinitely; must be manually stopped once the top candidate's fitness stabilizes. Worked example: cantilever cross-section shape optimization (Karamba) — topology fixed, only CroSecSelect's index varies — reduced tip displacement from 0.009703 (index 29) to 0.000253 (index 89 optimum), ~38x improvement. Also used to find the shortest interpolated path between two fixed points on a freeform surface via Gene Pool-driven uv control points, and (per a guest essay) to re-solve a fabrication-constrained panelization for a smaller laser-cutter bed without redesigning the geometry.
- Provenance: [STATED, AAD p.407, 409-410, 432, 435-438, 483-484]

### Gene Pool
- Tab: Params > Util (native GH component supporting Galapagos)
- Behavior: Embeds a configurable collection of Number Sliders in one component; double-click sets Gene Count, slider range (min/max), significant digits. More sliders = higher accuracy of the resulting optimized curve/geometry.
- Provenance: [STATED, AAD p.436]

---

## Coverage stats

- **Total components documented:** 197 — 2 entries added post-audit (Phase 3 KB gaps): Mass Addition, Unflatten Tree
- **Per-tab counts:**
  - Params: 20
  - Maths: 29
  - Sets: 36
  - Vector: 18
  - Curve: 33
  - Surface: 27
  - Mesh: 15
  - Intersect: 2
  - Transform: 8
  - Display: 6
  - Tab unconfirmed: 3
  - Third-party plugins: ~53 (LunchBox 5, Weaverbird 6, Kangaroo 9, Karamba 11, Millipede 9, Goat 1, GECO 15, HoopSnake 1, Tree8 1, Mesh Edit 1, Generation 3, Elk/Finches/gHowl 3)
  - Special/Solver: 2
- **[CONFLICT] flags:** 0 remaining (was 15). All 15 resolved during Phase 2b web verification against current grasshopperdocs.com/docs.mcneel.com/discourse.mcneel.com sources — see `knowledge/validation/verify-1-conflicts.md` for full verdicts. Resolved: Larger's cross-source naming (→ Larger Than, Essential correct); Cull Index tab (→ Sets > Sequence); Cull Pattern tab (→ Sets > Sequence); Repeat/Repeat Data tab (→ Sets > Sequence); Merge tab (→ Sets > Tree); Weave tab (→ Sets > List); Concatenate tab (→ Sets > Text); Short vs. Shortest List cross-reference (→ same component, "Shortest List" official); Scale tab (→ Transform > Affine); Move tab spelling (→ "Euclidean"); Mesh Surface/Mesh UV tab (→ Mesh > Util); Surface Split tab (→ Intersect > Physical); End Points/Endpoint name+tab (→ "End Points", Curve > Analysis); Shatter vs. "Explode" diagram/text naming (→ two distinct real components, AAD p.378 diagram is genuinely Explode, book's surrounding text is what's wrong); Evaluate F(X) vs. Expression port-shape note (→ both real, distinct components, correctly kept separate).
- **Verified entries: 49 [VERIFIED]** — components/notes now carrying at least one `[VERIFIED <url>]` or `[CORRECTED, VERIFIED <url>]` provenance tag from Phase 2b web verification (verify-1-conflicts.md, verify-2-core.md, verify-3-surface-plugins.md), on top of their original `[STATED]`/other tags.
- **Unverifiable: 1** — Draw Arc (Tab unconfirmed): no Grasshopper component (native or plugin, current or legacy) matching its recorded (A,R)→(B) shape and "Draw Arc"/"DArc" name could be found in any source checked; tagged `[UNVERIFIED — no documentation found 2026-07]`.
- **Entries with partial/incomplete specs remaining (all others resolved via Phase 2b verification):** Weave's Pattern-input authoring grammar (exact typed syntax still undocumented in every source checked, though the rest of the spec is now complete); Loop ("Generation" plugin, Third-party plugins) — no structured I/O documentation exists anywhere for this plugin; Colour (RGB) — Params/Display tab ambiguity not addressed by any Phase 2b finding, left as originally recorded; Draw Arc — see Unverifiable, above.
- **Three-way "Eval" naming collision disambiguated:** Evaluate F(X)/Expression (Maths > Script), Evaluate Curve (Curve > Analysis), Evaluate Length (Curve > Analysis) — see cross-referenced disambiguation notes on each entry.
- **Other multi-way name collisions disambiguated:** "Explode" (3-way: Explode Curve / Mesh > Util Explode / Mesh Explode), "Flip" (Flip Matrix vs. Flip Curve), "Circle" (plane+radius vs. Circle CNR center+normal+radius vs. Circle 3Pt — only the first two documented from sources), "Curvature" (Principal Curvature vs. Surface Curvature).
- **Phase 2b identity corrections/merges:** "Oscillator" (Tab unconfirmed, AAD p.309) merged into **Osculating Circles** (Surface > Analysis) — not a real, separate component name. "DCon" (Tab unconfirmed) renamed to **Delete Consecutive**, port count corrected (N is output-only). "Negate (vector)" (Maths-adjacent, AAD p.376) merged into **Reverse (vector)** (Vector > Vector) — same component, not a separate "Negate."






