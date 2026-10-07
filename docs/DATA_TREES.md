# Grasshopper Data Trees — The Definitive Reference

Synthesized from two primary sources:
- **Essential** = Rajaa Issa, *Essential Algorithms and Data Structures for Grasshopper*, 2nd Edition — `knowledge/raw/essential-part1.md` (printed p.1-52) and `essential-part2.md` (printed p.52-101). This is the book's dedicated data-structures text; Chapter 2 covers list matching, Chapter 3 ("Advanced Data Structures") covers the tree system in full.
- **AAD** = Tedeschi, Wirz, Andreani, *AAD — Algorithms-Aided Design*, 2014 — `knowledge/raw/aad-part3.md` (printed p.167-250, the book's dedicated Chapter 5 "Skins: advanced data management") plus the "Data tree behavior" notes scattered through `aad-part1.md`, `aad-part2.md`, `aad-part4.md`, `aad-part5.md`, `aad-part6.md`.

**Provenance key**: `[STATED, Essential p.X]` / `[STATED, AAD p.X]` = directly asserted in that source at that printed page. `[INFERRED, ...]` = extractor's reasoned inference from a diagram, not a verbatim book statement. `[NOT IN SOURCE: ...]` = a related fact the books name but never diagram/explain within the extracted page ranges. `[GENERAL]` = general Grasshopper knowledge added because the source was silent and the gap would otherwise make the reference unusable; used sparingly and always flagged. `[CONFLICT]` = the two books state genuinely incompatible things (searched for; none found — see §8.4).

---

## Table of Contents

1. [What a Data Tree Is](#1-what-a-data-tree-is)
2. [Single Item vs List vs Tree — Wire-Display Conventions](#2-single-item-vs-list-vs-tree--wire-display-conventions)
3. [Data Matching: Shortest / Longest / Cross-Reference — Worked Proofs](#3-data-matching-shortest--longest--cross-reference--worked-proofs)
4. [Tree Matching (Extending List Matching to Trees)](#4-tree-matching-extending-list-matching-to-trees)
5. [The Tree-Operations Toolkit](#5-the-tree-operations-toolkit)
   - 5.1 [Graft](#51-graft)
   - 5.2 [Flatten / Unflatten](#52-flatten--unflatten)
   - 5.3 [Simplify Tree](#53-simplify-tree)
   - 5.4 [Flip Matrix](#54-flip-matrix)
   - 5.5 [Trim Tree / Clean Tree / Explode Tree](#55-trim-tree--clean-tree--explode-tree)
   - 5.6 [Shift List vs "Shift Paths"](#56-shift-list-vs-shift-paths)
   - 5.7 [Entwine vs Merge](#57-entwine-vs-merge)
   - 5.8 [Split Tree — Full Mask Grammar](#58-split-tree--full-mask-grammar)
   - 5.9 [Path Mapper — Constants, Presets, Expressions](#59-path-mapper--constants-presets-expressions)
   - 5.10 [Allocate N (AAD) — Flat List Back to Grouped Branches](#510-allocate-n-aad--flat-list-back-to-grouped-branches)
6. [Relative Item / Relative Items](#6-relative-item--relative-items)
7. [Decision Logic — When and Why](#7-decision-logic--when-and-why)
8. [Debugging Tree Problems](#8-debugging-tree-problems)
   - 8.1 [Diagnostic tools](#81-diagnostic-tools)
   - 8.2 [Silent-failure gotchas (no error, wrong result)](#82-silent-failure-gotchas-no-error-wrong-result)
   - 8.3 [Structural gotchas, by operation](#83-structural-gotchas-by-operation)
   - 8.4 [Cross-source framing notes and conflict search](#84-cross-source-framing-notes-and-conflict-search)

---

## 1. What a Data Tree Is

Grasshopper has exactly **one** native data structure: the data tree. What earlier, simpler descriptions call a "single item" is really a tree with one branch holding one element, and a "list" is a tree with one branch holding N elements — every wire in Grasshopper ultimately carries a tree. `[STATED, Essential p.53]`

AAD frames the identical idea in parent/child vocabulary rather than list-generalization vocabulary: Grasshopper stores data in a hierarchical Parent-Child structure. The single overall container is the **trunk** (path `{0}`). Grouping data under a parent produces **branches** — watertight subsets identified by a **data path** such as `{0;0}`, `{0;1}`. Within a branch, individual data elements are **items**, indexed `0,1,2,...`. Example: deconstructing 4 triangular breps' vertices naturally produces 4 branches (one per source triangle/parent), each holding 3 items (that triangle's 3 vertices). `[STATED, AAD p.218-219]`

### Path and index notation

- A **branch address (path)** is a sequence of integers separated by semicolons inside curly braces: `{0;0;...;0}`. `[STATED, Essential p.55]`
- The **position of an item within a branch** is an integer in square brackets appended after the path: `{0;0;0}[1]` addresses the 2nd item (index 1) of branch `{0;0;0}`. `[STATED, Essential p.55]`
- Essential names the path segments: the first number is the **main trunk**, the second is the "second trunk out of main," continuing to a **last trunk** that "holds leaves"; the bracketed index is the **leaf index**. Branch/leaf ordering in the book's hand-drawn diagrams runs left-to-right, clockwise. `[STATED, Essential p.55]`
- AAD's simpler three-tier vocabulary — **trunk** `{0}` → **branches** `{0;0}`, `{0;1}` → **items** `0,1,2...` within a branch — describes the same addressing scheme with fewer named tiers; both framings agree on the underlying `{path}[index]` syntax. `[STATED, AAD p.218-219]` — *both framings, not a conflict.*

### Path numbering is a convention, not an absolute

Essential explicitly warns that branch numbering is chosen by whichever component generated the tree — it does not have to start at a fixed value: "The three branches from the main trunk are set here to `0:1`, `0:2`, and `0:3`. They also could have been `0:0`, `0:1` and `0:2`. Both are correct." `[STATED, Essential p.57]`

### Worked tree-construction example (canonical addresses)

A hand-built tree with values `5,10,11,22,100,200,1.1,1.2,1.3,6,7`, solved to addresses:
`{0;1;0}=5`, `{0;1;1}=10`, `{0;1;2}=[11,22]`, `{0;2}=[100,200]`, `{0;3;0}=[1.1,1.2,1.3]`, `{0;3;1}=[6,7]`.
Confirmed: the value "1.2" lives at path `{0;3;0}[1]` (2nd item, index 1). `[STATED, Essential p.56-57]`

### The two fundamental rules of a Data Tree (AAD's framing)

1. **Branches are watertight.** No connection or operation can bridge data across different branches; any operation applied to a tree is applied independently, branch by branch. This is why a Polyline fed 4 branches of 3 points each produces 4 separate 3-point polylines rather than one 12-point polyline — the component has no way to "see across" branches. `[STATED, AAD p.220]`
2. **Trees can be deliberately restructured** via dedicated components to achieve a different, desired grouping of the same underlying data — e.g. flattening 4 branches into 1 to let Polyline draw a single continuous line through all 12 points. `[STATED, AAD p.220]`

Essential states the identical rule as an absolute: "Any operation performed on a Data Tree will affect the data stored in every branch," i.e. there is no way to make a component "reach across" branches without first restructuring the tree (flatten, unflatten, graft, or flip). `[STATED, AAD p.220]` — Essential's Mass Addition example makes the same point from the opposite direction: fed a 3-branch tree `[1,2,3,4]/[5,6,7]/[8,9]`, Mass Addition returns `[10, 18, 17]` — one sum **per branch**, never a single grand total. `[STATED, Essential p.33]`

---

## 2. Single Item vs List vs Tree — Wire-Display Conventions

### The three structures (Essential's exact definitions)

| Structure | Definition | Panel readout |
|---|---|---|
| Single Item | 1 branch × 1 item | `Data with 1 branch(es), {0}, N=1` |
| List | 1 branch × N items | `Data with 1 branch(es), {0}, N=k` (k>1) |
| Tree | M branches, each independently sized | `Data with M branches` + a per-branch `N=` count, e.g. `{0;0} N=4, {0;1} N=3, {0;2} N=2` |

`[STATED, Essential p.33]`

This is presented as the reason Chapter 2 of Essential exists at all: **"GH components execute differently based on input data structures, and hence it is essential to be fully aware of the data structure before using [a component]."** `[STATED, Essential p.33]`

### Canonical worked example (Essential Fig.34/35, p.33)

A Number param wired three ways into a Panel and into Mass Addition (MA):

```
Num[1] -> Panel                          {flat, 1 branch x 1 item}   -> Panel shows "N=1"
Num[1,2,3,4] -> Panel                    {flat, 1 branch x 4 items}  -> Panel shows "N=4"
Num[grafted] -> Panel                    {tree: 3 branches x [4,3,2]} -> {0;0}=1,2,3,4 ; {0;1}=5,6,7 ; {0;2}=8,9
```

Same three inputs into `MassAddition(MA).I -> R`:
- item `1` → `R = 1` (identity — sum of one item is itself)
- list `[1,2,3,4]` → `R = 10` (one number: sum of the whole list)
- tree `[1,2,3,4]/[5,6,7]/[8,9]` → `R = [10, 18, 17]` (a list of 3 numbers, one sum **per branch**)

`[STATED, Essential p.33]`

### Wire-display convention

Grasshopper draws connector wires differently depending on data structure, as a fast visual diagnostic without opening a Panel:

| Data shape | Wire style (Essential's 3-way scheme) |
|---|---|
| Single Item | one simple solid line |
| List | a double (parallel) solid line |
| Tree | a double line that is also **dashed** |

`[STATED, Essential p.34]`

AAD's dedicated data-tree chapter states the same convention with a coarser, 2-way split: a "structured" (branching) data flow is drawn as a **DASHED** wire; once flattened (reduced to a single branch/trunk) the wire becomes **solid/continuous**. `[STATED, AAD p.220-221]` This is the same underlying rule described at different resolution — both books agree dashed = tree-structured, solid/plain = not — Essential additionally distinguishes single-item vs. list within the "not a tree" case via single-vs-double line weight; AAD doesn't re-state that finer distinction in its own tree chapter. *Both framings, not a conflict.*

AAD's earlier chapters (before its dedicated tree chapter) preview this mechanism under the name **"Draw Fancy Wires"** mode and describe a "no data / one datum / many data" 3-way wire scheme, with dashed wires flagged as denoting "some further data condition" to be explained later — i.e. AAD's own vocabulary elsewhere is consistent with Essential's 3-tier scheme, just deferred to its own Chapter 5. `[STATED, AAD p.58, p.71]`

AAD also separately notes: once a Merge operation collapses two single data items into a 2-item list, the resulting output wire visibly **thickens** — an additional wire-weight cue beyond dashed/solid. `[STATED, AAD p.64]`

### Implicit broadcasting preview (before formal list-matching)

Before Essential's formal "list matching" section, its Chapter 1/2 tutorials already show that pairing one internally-set single value against a longer list causes the single value to be broadcast against every list item with no extra wiring: `Plane[internal XY] + Radius-list[5 values from Range] -> Circle` yields 5 circles; `Point[1 supplied] + Radius-list[6 values from Random] -> Circle` yields 6 circles. `[STATED, Essential p.36]`

---

## 3. Data Matching: Shortest / Longest / Cross-Reference — Worked Proofs

Essential's Chapter 2, section 2_4 "List matching," is the book's formal treatment, opened with: "When the input is a single item or has an equal number of elements in a simple list, it is easy to imagine how the data is matched. The matching is based on corresponding indices... There are times when input has variable length lists. In this case, GH reuses the last item on the shorter list and matches it with the next items in the longer list." `[STATED, Essential p.41]`

### Baseline: equal-length / single-item matching (Fig.45)

```
Panel[1] -> Addition.A ; Panel[3.5] -> Addition.B -> R = 4.5              {item}
Panel[1,2] -> Addition.A ; Panel[10,20] -> Addition.B -> R = [11,22]      {flat, N=2, matched by index}
```
`[STATED, Essential p.41]`

### Default matching = "Long List" (repeat the shorter list's LAST item)

**GH defaults to Long List matching.** `[STATED, Essential p.41-42]`

Worked numeric proof (Fig.46, p.41):
```
A = [1,2]  (2 items)
B = [1,2,3,4,5]  (5 items)
Addition(A,B): GH internally treats A as [1,2,2,2,2]  (A's last item "2" repeated 3 more times)
R = [2,4,5,6,7]   {flat, N=5 — matches the LONGER list's length}
```
`[STATED, Essential p.41]`

### Three explicit/forceable matching modes (Figs.47-49, p.42-43)

Right-clicking a component's list input (or wiring the dedicated `Long`, `Short`, `CrossRef` components) forces one of three policies:

| Mode | Nickname | Rule | Result length |
|---|---|---|---|
| **Long** (default) | "Repeat Last" | repeat the shorter list's last item to reach the longer list's length | length of the LONGER list |
| **Short** | "Trim End" | truncate the longer list, discard extra trailing items | length of the SHORTER list |
| **Cross Reference** | "Holistic" | pair every item of one list with every item of the other(s) — full Cartesian product | PRODUCT of all input lengths |

`[STATED, Essential p.42-43]`

Worked numeric proof, same raw inputs `A=[1,2]`, `B=[1,2,3,4,5]`, through all three modes feeding `Addition`:

```
Long:      A(out)=[1,2,2,2,2]                B(out)=[1,2,3,4,5]                          -> R=[2,4,5,6,7]        (N=5)
Short:     A(out)=[1,2]                      B(out)=[1,2]                                -> R=[2,4]              (N=2)
CrossRef:  A(out)=[1,1,1,1,1,2,2,2,2,2]       B(out)=[1,2,3,4,5,1,2,3,4,5]                -> R=[2,3,4,5,6,3,4,5,6,7]  (N=10)
```
`[STATED, Essential p.41-43]`

**Order matters for Cross Reference.** Swapping which list is A vs B changes which items get repeated/tiled and in what order, even though the resulting *values* are the same combinatorial set — explicitly flagged in the book: **"Order of input matters."** Example: `A=[1,2,3,4,5]`, `B=[1,2]` (inputs swapped from above) changes the expansion so A's items each repeat twice consecutively and B tiles 5 times, instead of the reverse. `[STATED, Essential p.42-43]`

### Custom matching: cyclic repeat (beyond the three built-in modes)

If none of Long/Short/Cross-Reference give the desired behavior, a custom rule must be built. Essential's example: repeat a short list's **whole pattern cyclically** (tile it), rather than repeating only its last item — built from `List Length` (to discover the target length generically) + `Repeat` (tiles a list to a specified length). `[STATED, Essential p.43, p.48]`

Worked numeric proof (Fig.50, p.43):
```
A = [1,2]
ListLength(B=[1,2,3,4,5]) = 5
Repeat(D=A, L=5) -> [1,2,1,2,1]        (cyclic tiling, NOT last-item-repeat)
Addition([1,2,1,2,1], [1,2,3,4,5]) -> R = [2,4,4,6,6]
```
Compare against the default Long-matching result for the identical raw inputs: `[2,4,5,6,7]`. **Same inputs, different results** — the book uses this side-by-side specifically to make unmistakably clear that "repeat the last item" (default) and "repeat the whole pattern" (custom) are different, easily-confused behaviors that must be deliberately chosen. `[STATED, Essential p.43]`

### 3-way Cross Reference for full permutation generation ("cube of points" tutorial, 2_4_1)

A single 6-item number list `[0..5]` wired into all three of Cross Reference's `A`, `B`, `C` inputs simultaneously produces three output lists, each of length **216 = 6×6×6**, representing every possible `(x,y,z)` combination — fed into Construct Point to build a 6×6×6 = 216-point cube grid. Confirms Cross Reference generalizes beyond 2 inputs to N inputs, output length = product of all N input lengths. `{flat, N=216, single branch}` `[STATED, Essential p.43-45]`

### Full 3-way comparison on unequal-length lists (Custom List Matching tutorial, 2_5_2)

`A=[1,2]` (len 2), `B=[10,20,30]` (len 3), `C=[0.2,0.4,0.6,0.8,1]` (len 5), fed as X,Y,Z into Construct Point:

| Mode | A (out) | B (out) | C (out) | Resulting points |
|---|---|---|---|---|
| **Long** (default) | `[1,2,2,2,2]` | `[10,20,30,30,30]` | unchanged (already longest) | `{1,10,0.2}, {2,20,0.4}, {2,30,0.6}, {2,30,0.8}, {2,30,1}` |
| **Short** | `[1,2]` | `[10,20]` | `[0.2,0.4]` | `{1,10,0.2}, {2,20,0.4}` |
| **Custom cyclic** (Repeat to length 5, the longest via Bounds+DeDomain) | `[1,2,1,2,1]` | `[10,20,30,10,20]` | unchanged `[0.2,0.4,0.6,0.8,1]` | `{1,10,0.2}, {2,20,0.4}, {1,30,0.6}, {2,10,0.8}, {1,20,1}` |

These are **different point sets** for the identical raw inputs — concrete proof that the choice of matching rule materially changes geometry, not just list bookkeeping. `[STATED, Essential p.46-48]`

### AAD's parallel treatment: Cross Reference for 2D/3D grids, Shortest List for reconciliation

AAD's data-matching chapter (outside its dedicated tree chapter) uses the identical "Holistic"-nicknamed Cross Reference component to build `(xi,yi)` coordinate grids feeding a two-variable function evaluator — e.g. an 11×11 = 121-pair Cartesian grid for a paraboloid. `[STATED, AAD p.104, p.108]` AAD frames this as **list-level pairing logic** for producing 1D→2D/3D dimensional expansion, reaching for Cross Reference rather than Graft for that specific goal in this chunk — a difference in which tool is the default reach for a similar outcome, not a contradiction (AAD's own dedicated tree chapter, §5, teaches Graft extensively for the *branch-per-item pairing before Merge* use case, which is a distinct goal from *pure dimensional-grid generation*). `[INFERRED, AAD p.90-94]` — *both framings.*

AAD separately names a **Shortest List ("Short")** component used specifically to reconcile mismatched list lengths between Range-generated x-values and an Evaluate component's results, before constructing points — trimming both to the shorter length so X/Y pairs match one-to-one. This is the same "Short / Trim End" behavior Essential documents under its `Short` component. `[STATED, AAD p.375]`

AAD also notes: **Split List at an index equal to List Length** yields List A identical to the original full list and List B empty — the boundary condition of Split List. `[STATED, AAD p.84]`

---

## 4. Tree Matching (Extending List Matching to Trees)

Essential states plainly that trees follow the *same* Long/Short/Cross list-matching conventions, just applied recursively: **"if one tree has fewer branches, the last branch is repeated"** to equalize branch count, and within matched branches, the shorter branch's last element is repeated to equalize item count. `[STATED, Essential p.60]`

| Matching case | Rule |
|---|---|
| **Item → Tree** | A single item added to a tree is broadcast: GH builds a matching tree structure and repeats the item into every branch/position needed. `[STATED, Essential p.60-61]` |
| **Short list → Tree** | A list shorter than the tree's branch count is repeated across every branch (its last item repeated as needed). `[STATED, Essential p.61]` |
| **Long list → Tree** | A list longer than a tree's branch count causes branches to expand: each branch's last item is repeated to reach the list's length. **The resulting structure differs from BOTH original inputs** — the book flags this explicitly: "Note that the resulting tree structure will be different than the input tree." `[STATED, Essential p.62]` |
| **Tree → Tree, same branch count** | Corresponding branches matched via standard short-list-repeat-last-item logic; the result's branch structure can end up matching one, both, or neither of the inputs. `[STATED, Essential p.62-63]` |
| **Tree → Tree, different branch count** | GH first inserts new branches into the smaller tree by repeating its LAST branch (to match branch count), THEN expands items within each branch by repeating the last item — a two-stage combination. `[STATED, Essential p.63-64]` |

### Why identical values in different structures give different results (p.55)

Essential demonstrates this with three numbers `{10,20,30}` added via `A+B`, once as a flat 3-item list matched against another 3-item list (giving an item-wise result, `{20,40,60}` per the source's own worked value), and once with `{10,20,30}` split into 3 separate single-item branches matched against a tree, which triggers full tree-to-tree cross-matching and produces a 3×3 grid of 9 results across 3 branches: `{20,30,40}, {30,40,50}, {40,50,60}`. **Note:** the raw extraction of this passage contains the source's own mid-explanation self-correction/hedge language around the exact intermediate values; the final 9-value, 3-branch result is stated cleanly and is reproduced above as the book's clear takeaway: **branch count and depth, not just raw values, determine whether a component treats data as parallel (item-by-item) or as a full combinatorial cross product.** `[STATED, Essential p.55]`

---

## 5. The Tree-Operations Toolkit

### 5.1 Graft

**What it does:** Converts a flat list (or any tree) into a tree with one item per branch — the maximal "un-flattening." `[STATED, Essential p.69-70]` AAD states it identically: Graft Tree takes an (often flat) list of N items and produces a tree with N branches, one item per branch. `[STATED, AAD p.222-224]`

**Depth behavior (worked proof, Essential Fig.68, p.69):** Given an already variable-depth 4-branch input tree (`{0;0;0}` N=2, `{0;0;1}` N=2, `{1;0}` N=2, `{1;1}` N=2 — two branches 3 levels deep, two branches 2 levels deep), Graft produces **8 branches**, each N=1:
`{0;0;0;0}, {0;0;0;1}, {0;0;1;0}, {0;0;1;1}, {1;0;0}, {1;0;1}, {1;1;0}, {1;1;1}`.
This proves Graft adds exactly **one new trailing branch level per existing leaf item**, regardless of the starting depth. `[STATED, Essential p.69]`

**Why it's used (canonical case): forcing correct one-to-one pairing before Merge.** AAD's central worked case study: two lists of 4 corresponding edge curves (top surface edges a'-b'-c'-d', bottom surface edges a-b-c-d) —

```
WRONG:   Srf(top).B -> DeBrep.E {1 branch, 4 curves}
         Srf(bottom).B -> DeBrep.E {1 branch, 4 curves}
         both -> Merge(D1,D2,D3).R  -> {flat: 1 branch x 8 curves, order a'-b'-c'-d'-a-b-c-d}
         -> Loft.L  -> self-intersecting, twisted "bowtie" surface (WRONG)

CORRECT: Srf(top).B -> DeBrep.E --(dashed)--> Graft.T -> {4 branches x 1 item}
         Srf(bottom).B -> DeBrep.E --(dashed)--> Graft.T -> {4 branches x 1 item}
         both grafted -> Merge(D1,D2,D3).R -> {4 branches, each: one top-edge + one bottom-edge}
         -> Loft.L -> simple box-like surface (CORRECT: a-a', b-b', c-c', d-d' each lofted independently)
```
`[STATED, AAD p.223-224]`

Essential's Shutters tutorial teaches the identical lesson with different geometry: to pair 4 rotated rectangles with 4 hinge circles correctly before `RUnion`, **both** lists are independently Grafted first (`{4 branches x 1}` each), specifically so rectangles and hinges pair correctly during the subsequent per-branch RUnion. `[STATED, Essential p.75]`

**Character of the operation:** Essential explicitly calls grafting "unintuitive" because it deliberately *increases* structural complexity (list → tree of singletons) — but this is often required to force full cross-product matching between two lists (e.g. grafting list A before adding it to list B forces every item of A against every item of B). `[STATED, Essential p.69-70]`

### 5.2 Flatten / Unflatten

**Flatten** collapses an entire tree (any depth, any branch count) into one single-branch list. Order is deterministic: branches are read "in order starting with the lowest index trunk," concatenating each branch's items sequentially. `[STATED, Essential p.70]` AAD: Flatten Tree removes ALL branching information, collapsing every item from every branch into one single trunk `{0}`, preserving original branch-by-branch, item-by-item order. `[STATED, AAD p.220-221]`

**Worked proof (Essential Fig.70, p.70):** the same variable-depth 4-branch/8-item tree from the Graft example above, flattened, produces ONE branch `{0}` with N=8, values concatenated strictly in ascending branch-path order: `1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5`. `[STATED, Essential p.70]`

**Canonical worked case (AAD, the "4 triangles → 12 vertices" problem):**
```
Geo(4 triangular breps) -> DeBrep.B -> DeBrep.V  {branches: 4 x 3, vertices grouped per triangle}
-> PLine.V -> PLine.Pl   -> 4 SEPARATE 3-point polylines (WRONG — wanted 1 continuous 12-point line)

FIX: DeBrep.V --(dashed)--> Flatten.T -> Flatten.T  {solid wire, 1 branch x 12}
-> PLine.V -> PLine.Pl   -> ONE 12-point polyline through all vertices (CORRECT)
```
`[STATED, AAD p.218-221]`

**Unflatten Tree** is Flatten's inverse: takes a flat list (T) plus a separate "guide" tree (G) with the desired branching pattern, and re-splits the flat list into branches matching the guide's structure. **Strict precondition: the flat list must contain exactly the same number of items as the guide tree**, or the component does not operate. `[STATED, Essential p.70]` `[STATED, AAD p.222]`

Worked case: `DeBrep.V --(dashed)--> Flatten.T -> Flatten.T {flat, 12 items} -> Unflatten.T ; DeBrep.V (original tree) -> Unflatten.G (guide) -> Unflatten.T (output, restored to 4 branches x 3 items, values identical to the pre-flatten structure)`. `[STATED, AAD p.222]`

**The recurring "flatten → transform → unflatten-with-ORIGINAL-guide" idiom (AAD's weaving tutorial, p.245-247):** if an alternating +/- translation pattern is applied directly to a still-tree-structured (per-branch) point set, the pattern independently **restarts at the beginning of every branch** — every thread's first point gets the same sign instead of alternating (a subtle bug, only visible in the final geometry). The fix: (1) Flatten the point list so the alternating pattern runs continuously across the whole sequence; (2) apply the transform; (3) **Unflatten Tree, using the ORIGINAL pre-flatten tree as the guide (G-input)**, to restore per-branch grouping before the next per-branch operation (e.g. Interpolate, one curve per thread). Interpolating a curve through a still-flat list without this restoration produces one single tangled curve through the entire point set instead of separate per-thread curves. `[STATED, AAD p.245-247]`

**Flatten used to enable a global statistic:** Distance computed between a full per-cell point tree and a single external attractor point is Flattened before being handed to `Bounds` (which needs one flat list to compute a global min/max across the *whole* dataset, not per-branch); the `Remap Numbers` result is then **re-Grafted** to restore per-cell branch alignment before feeding a per-cell input like `Offset on Srf`'s D or `Scale`'s F. `[STATED, AAD p.233, p.235, p.240-241, p.243]`

**Louvers tutorial — when nesting grows vs. doesn't (Essential p.72-73):** step-by-step trace showing that components mapping one-item-in to one-item-out (e.g. Line at each point) preserve tree depth, while components that expand one item into a genuinely new sub-collection (e.g. Divide) add a nesting level:
```
Input curve {0} N=1 -> Divide(Count=10) -> {0} N=11 (still 1 branch, just more items)
-> Line at each point -> {0} N=11 (unchanged — 1-to-1 mapping)
-> Divide each of the 11 lines (Count=5) -> {0;0;0}, {0;0;1}, ... 11 branches x 6 items (nesting ADDED — gained a leading "0" level)
```
`[STATED, Essential p.72-73]`

### 5.3 Simplify Tree

**What it does:** Removes unnecessary leading/trailing zero levels (superfluous nesting) from branch paths, without changing item counts or values. Essential: "Complex data structures are hard to match." Example: `{0;0}...{0;4}` (5 branches nested under a redundant top trunk) → `{0}...{4}` (5 branches, one level). `[STATED, Essential p.72]`

**Why it's needed — chained tree operations accumulate cruft:** AAD's identical warning, applied to repeated Explode/Graft chains: over-nested trees (e.g. a path like `{0;0;0;0;0;0}` that should really be `{0}`) must be collapsed with Simplify Tree (or the per-pin "Simplify" right-click option) **in addition to, not instead of,** grafting, before a Merge + per-branch operation like Loft will pair curves correctly. Demonstrated with before/after Panel screenshots showing path-depth reduction. `[STATED, AAD p.228-229]` **Grafting alone is not always sufficient** — this is stated as an explicit warning. `[STATED, AAD p.228-229]`

### 5.4 Flip Matrix

**What it does:** Regroups elements that share the same index across branches into new branches — a matrix transpose. A tree of 2 branches × 4 items becomes, after Flip, 4 branches × 2 items (branch *i* now holds "column *i*" — the i-th element from each original branch). This "exchanges items with branches and branches with items." `[STATED, Essential p.72]` `[STATED, AAD p.224-225]`

**Worked proof #1 (Essential Fig.72/73, p.71-72):**
- 2 branches × 4 items → flipped → 4 branches × 2 items, where flipped branch *i* = `[branch0[i], branch1[i]]`.
- Same operation on branches of **unequal** length (one N=4, other N=2): flip pads missing slots with the literal placeholder text `<null>` so all resulting branches stay the same count.

**Failure case (Fig.74, p.72):** if the input tree has **variable branch DEPTH** (not just variable length — e.g. some branches at `{0;0;0}`, others at `{1;1}`), Flip **cannot operate at all** — the book states "there is no logical solution to flip," and the component shows red/errors. `[STATED, Essential p.72]`

**Worked proof #2 (AAD, radial spokes across 3 circles, p.224-225):**
```
Crv(3 circles) -> Divide.C ; Slider[Count=10] -> Divide.N -> Divide.P {3 branches x 10 items}
-> PLine.V -> PLine.Pl  -> 3 separate 10-point polylines (one per circle — WRONG, wanted radial spokes)

FIX: Divide.P -> Flip.D -> Flip.D {transposed: 10 branches x 3 items}
-> PLine.V -> PLine.Pl  -> 10 short 3-point "spoke" polylines, each connecting corresponding points A-A'-A'' across the 3 circles (CORRECT)
```
Param Viewer components before/after visually confirm the branch-count change (3 → 10). `[STATED, AAD p.224-225]` AAD's tree chapter doesn't test or mention the variable-DEPTH failure case that Essential documents — a gap in AAD's coverage, not a contradiction between the two.

**Reuse-without-rebuilding pattern:** once a tree exists (e.g. a point grid from Divide Surface, U+1 branches × V items), Flip Matrix lets you derive the perpendicular ("weft") direction's structure for free — transposed to V+1 branches × U items — by transposing the SAME point tree, rather than re-deriving points from the surface a second time. `[STATED, AAD p.245-246, p.248]` Essential's multi-truss tutorial applies the identical trick to link parallel trusses: Top/Bottom point trees (6 branches, one per truss) are each independently Flipped, regrouping "corresponding" points across all 6 trusses (same point-index, different truss) into new branches, so one Polyline per new branch draws each cross-connection. `[STATED, Essential p.94]`

**Null cleanup after Flip:** because unequal-length-branch Flip pads with `<null>`, a `Clean` component ("Remove nulls") is required before feeding the flipped result into geometry components like Polyline. `[STATED, Essential p.86]`

### 5.5 Trim Tree / Clean Tree / Explode Tree

These three cleanup tools are named by Essential in the same breath as Simplify but are **not fully diagrammed** within the extracted page ranges:

- **Clean Tree** — Essential gives partial IO: `Clean | Sets > Tree | inputs: N (remove Nulls, boolean), X (unlabeled), E (unlabeled), T (Tree) -> outputs: T (cleaned Tree)`. Used after Flip to strip `<null>` placeholders, labeled "Remove nulls" in the diagram. `[STATED, Essential p.86]` The exact meaning of the `X` and `E` inputs is **`[NOT IN SOURCE: full Clean component input labels]`**.
- **Trim Tree** — named only, described in prose as removing null elements / empty branches, grouped conceptually with Clean Tree. **`[NOT IN SOURCE: full IO/diagram — named but not diagrammed, Essential p.72]`**
- **Explode Tree** — Essential names it only as "splitting every branch out into its own separate list/output." **`[NOT IN SOURCE: full IO, Essential p.72]`** AAD supplies the missing detail: `Explode Tree` (on-canvas nickname **"BANG!"**) | `inputs: D (data tree)` | `outputs: one output per branch, labeled (0), (1), (2)...` — used in a Box Morph target-box construction where a Bounding Box's 8 corner points are first Grafted (each corner → its own single-item branch) specifically so Explode Tree can split them into 8 individually addressable outputs; only by isolating each corner onto its own wire can 2 of the 8 be selectively re-wired through Move while the other 6 pass through unchanged into Twisted Box's 8 named corner inputs (A-H). `[STATED, AAD p.328]`

### 5.6 Shift List vs "Shift Paths"

The task brief for this document names "Shift Paths" as a tree operation, but **neither source ever names or diagrams a component called "Shift Paths."** **`[NOT IN SOURCE: no "Shift Paths" component appears anywhere in essential-part1/2.md or aad-part1/2/3/4/5/6.md]`**

What both books document extensively is **Shift List** (Sets > List), which shifts **items within a branch** (not branch paths themselves): `inputs: L (List), S (Shift amount/offset, can be negative), W (Wrap toggle)` → `outputs: L (shifted list)`. Shifting by +1 moves every item one position forward; with wrap on, items falling off one end reappear at the other. `[STATED, Essential p.38-40, p.68]` On a tree, Shift List's rotation is applied independently **per branch**, each branch's items cyclically rotated on its own. `[STATED, Essential p.68]`

Right-click "Reverse" is available on every component's input slot by default (not just a dedicated Reverse List component), reversing incoming list order without a separate wired component. `[STATED, AAD p.86]`

### 5.7 Entwine vs Merge

These solve two different-looking-but-often-confused goals `[STATED, Essential p.71]`:

| | Entwine | Merge |
|---|---|---|
| Inputs | N separate lists | N separate data streams (D1, D2, D3, ...) |
| Effect | Creates a **NEW tree with N branches**, one branch per input list — no values combined, just organized into parallel branches | **Concatenates** N inputs into one single bigger flat list (a "list join"), losing separation between the original inputs entirely |
| Example | `pDecon.X -> Entwine.[0;0]`, `.Y -> [0;1]`, `.Z -> [0;2]` → `{branches: 3 x 5}` | `FirstList(4), SecondList(4) -> Merge.D1/.D2 -> {flat: 1 x 8}` |

`[STATED, Essential p.71]` Entwine also carries an internal "Flatten" toggle/label shown under the component. `[STATED, Essential p.59-60]`

**Merge's mechanical behavior:** begins with exactly two visible inputs (D1, D2); as soon as D2 is wired, Grasshopper automatically adds an empty D3 (and so on for D4, D5...), with further manual slots available via the zoomable UI's "+" control. `[STATED, AAD p.64]` Merge arities vary by context in practice — AAD shows 3-input (D1-D3) and 4-input (D1-D4) uses depending on how many streams need combining. `[STATED, AAD p.379, p.388, p.392]` Slot order matters: in a Galapagos worked example, the order of D1/D2/D3 directly controls the resulting point order along an interpolated curve (fixed start point → variable interpolation points → fixed end point). `[STATED, AAD p.436]`

**Merge's right-click modes ("graft"/"simplify") as an alternative to separate Graft/Simplify components:** AAD's chapter 5 rule is invoked by name elsewhere in the book — before merging two parallel per-item streams (original curves + their Scale-transformed counterparts) so Loft can pair them correctly, BOTH streams must first be run through separate Graft components, then combined via Merge (D1=grafted originals, D2=grafted scaled). `[STATED, AAD p.452]` The same graft-before-merge pattern recurs for Mesh Colours (mesh stream + RGB colour stream each individually grafted before wiring into `M`/`C`). `[INFERRED, AAD p.458]` Separately, Merge's own inputs can be set directly to **"graft" mode** (in Voronoi-skin workflows, so each cell's boundary-vertex branch merges with that same cell's single translated-centroid item, keeping one branch per cell) `[STATED, AAD p.284]`, or to **"simplify" mode** (closing each section profile: the section curve, its offset/rebuilt curve, and two connecting line segments collapse into a single flat branch per section, so a subsequent Join only joins pieces belonging to the SAME section) `[STATED, AAD p.333]`.

**Silent-truncation gotcha (high severity):** Mesh Explode's F output (one branch per input mesh) **MUST be explicitly Flattened** before connecting to an export component (EcoMeshExport.M in the worked example). Without flattening, only the faces in the **LAST branch/path of the tree** are exported — the multi-branch structure silently truncates the export with **no error raised**. `[STATED, AAD p.454]`

### 5.8 Split Tree — Full Mask Grammar

`Split (Split Tree) | Sets > Tree | inputs: D (Data tree), M (split Mask, string) | outputs: P (Positive tree), N (Negative tree)`. Split Tree filters a tree per a mask string; **both outputs preserve the original tree structure** (same branch paths, same item counts) — elements that don't match the mask are replaced with `null` in that output rather than removed, so Positive and Negative can later be recombined losslessly via `Combine`. `[STATED, Essential p.81-85]`

**Full mask syntax, reproduced completely as captured from the book (p.81-82):**

| Syntax element | Meaning |
|---|---|
| `{ ; ; }` | curly braces enclose the **branch-selection** mask |
| `[ ]` | square brackets enclose the **element/leaf-selection** mask; may be omitted, meaning "select all" (equivalent to `[*]`) |
| `( )` | round brackets are for **grouping** |
| `*` | wildcard — matches any number of integers in a path; also selects all branches regardless of their paths |
| `?` | matches any **single** integer |
| `6` (a bare integer) | matches that specific integer |
| `!6` | negation prefix — matches anything **EXCEPT** that value |
| `(2,6,7)` | comma-list in parens — matches any ONE of those specific values |
| `!(2,6,7)` | negated comma-list — matches anything EXCEPT those values |
| `(2 to 20)` | inclusive range — matches any integer in that range |
| `!(2 to 20)` | negated range — matches anything OUTSIDE that range |
| `(0,2,...)` | open arithmetic sequence — matches any integer that is part of that infinite ascending sequence; requires at least 2 seed integers, each subsequent bigger than the last |
| `(0,2,...,48)` | bounded arithmetic sequence — same, with a limit after the three dots |
| `!(3,5,...)` | negated infinite sequence — matches any integer NOT part of the sequence. **Important caveat, stated explicitly in the book:** the sequence does not extend to the left, only to the right, so `!(3,5,...)` actually selects `0, 1, 2, 4, 6, 8, 10, 12,` and all remaining even numbers — i.e. everything below the sequence start is automatically included as "not part of it." |
| `!(7,10,21,...,425)` | negated finite/bounded sequence — matches any integer not part of that finite sequence |
| `... or ...` / `... and ...` | rules can be combined with boolean and/or, e.g. `{*}[(0 to 4) or (6,11,41)]` selects "the first five items in every list of a tree and also the items 7, 12 and 42" *(verbatim from the book's own prose — note the prose's item numbers 7/12/42 do not match the mask literal integers 6/11/41 printed just above it; transcribed exactly as printed in the source rather than silently corrected, since the source itself is internally inconsistent)* |

`[STATED, Essential p.81-82]`

**Worked examples:**
- `{*}[(2 to 6)]` on a 6-branch × 10-item grid → Positive = middle rows (indices 2-6), Negative = indices 0,1,7,8,9 — both retain all 6 original branches at their original addresses. `[STATED, Essential p.83-85]`
- `{*;(0,1,2)}[*]` → "Left tree" (Positive) / "Right tree" (Negative), splitting by branch sub-index rather than by item index. `[STATED, Essential p.84]`
- `{0,2,...}` applied **at the branch level** (not the item level) → Positive = even-indexed whole branches, Negative = odd-indexed whole branches — used in the Zigzag tutorial because "the zigzags alternate directions from one row to the next," requiring an entire column/branch to be treated differently from its neighbor, not just alternating points within one branch. `[STATED, Essential p.96]`
- `{*}[1,3,...]` → odd-index items across every branch. `[STATED, Essential p.85-86]`
- `{*;(0,2,...)}[0,2,...]` combined with `{*;(1,3,...)}[1,3,...]` (two masks together) → alternating-element split **within each branch**, used in the Weaving tutorial. `[STATED, Essential p.100]`

**Lossless round-trip confirmed:** Split → (transform Positive only) → `Combine.[0]/.[1] -> Combine.R` → a Polyline per branch reconstructs a single connected pattern per branch, proving the split-transform-recombine cycle is lossless as long as paths are preserved. `[STATED, Essential p.82-85]`

### 5.9 Path Mapper — Constants, Presets, Expressions

**Mechanics:** Path Mapper maps data from a SOURCE path (fixed, taken directly from the input tree — cannot be edited) to a user-defined TARGET path (the only thing you set). `[STATED, Essential p.86-91]`

**The three named constants** for building target-path expressions:

| Constant | Meaning |
|---|---|
| `item_count` | number of items in the current branch |
| `path_count` | number of paths (branches) in the whole tree |
| `path_index` | index of the current path (branch) being mapped |

`[STATED, Essential p.86-91]`

**Notation:** target-path expressions use tuple notation `{A;B;C}` for a 3-level path and `(i)` / `[i]` for the item index, written as `source -> target`. Examples:
- Swap the last two path integers: `{A;B;C} -> {A;C;B}`
- Promote the item index into the path while demoting a path level into the item index (a flip): `{A;B;C}[i] -> {A;B;i}[C]`
- Composed (regroup + flip in one expression): `{A;B;C}[i] -> {A;C;i}[B]` — can save processing time/size versus chaining two separate Path Mapper components, "but also states combining is not always possible" (no further criteria given for when combination fails). `[STATED, Essential p.86-91]`

**Right-click built-in presets** (worked on a fixed 10-branch × 11-item source tree):

| Preset | Effect | Worked result |
|---|---|---|
| **Null Mapping** | no-op — starting template | unchanged: 10 branches × 11 items |
| **Flatten Mapping** | collapses everything into one branch | `Data with 1 branches {0} N=110` |
| **Graft Mapping** | turns every leaf into its own branch | `Data with 110 branches`, each N=1 |
| **Trim Mapping** | *(named, no worked example diagrammed in this chunk)* — **`[NOT IN SOURCE: no worked example]`** |
| **Reverse Mapping** | reverses item order within branches, structure unchanged | still `Data with 10 branches`, each N=11, item order reversed |
| **Renumber(ing) Mapping** | strips nested path structure to flat sequential top-level branch numbers | 10 branches nested as `{0;0}..{0;1;4}` become flat `{0}` through `{9}`, still N=11 each |

`[STATED, Essential p.87-88]`

Right-click context menu also exposes: "Mapping Editor...", "Create Null Mapping", "Create Flatten Mapping", "Create Graft Mapping", "Create Trim Mapping", "Create Reverse Mapping", "Create Renumber Mapping", "Enabled", "Help...". `[STATED, Essential p.86-91]`

**Partitions tutorial — connecting corresponding branches/items across multiple trees (2-step, then combined):**
```
Step 1 (regroup branches across trees):  Tree -> PathMapper1[{A;B;C} -> {A;C;B}] -> {10 branches, reordered so tree-index and branch-index swap, grouping same-branch-different-tree pairs adjacently}
Step 2 (flip each pair into item-pairs): PathMapper1(out) -> PathMapper2[{A;B;C}(i) -> {A;B;i}(C)] -> {55 branches x 2 items — one branch per corresponding point-pair, since 5 branch-pairs x 11 items = 55}
Combined single-step alternative:        Tree -> PathMapper[{A;B;C}(i) -> {A;C;i}(B)] -> same result in one component ("not always possible, but it can save processing time and size")
```
`[STATED, Essential p.88-91]`

**Character of the tool:** Path Mapper is explicitly called out as **"perhaps the least intuitive to use and can cause a loss of data,"** but **"the only way to find a solution in some cases."** `[STATED, Essential p.86]` The clear implication is that misconfigured target-path expressions can silently drop elements rather than error — reach for it only when Flatten/Graft/Flip/Split are insufficient. `[STATED, Essential p.86]`

**Param Viewer as the companion debugging tool for Path Mapper (and any tree op):** double-clicking a Param Viewer wired to any data stream opens a graphical preview of that data's tree/branch structure (radiating-line diagrams whose branch count/arrangement visibly change before vs. after an operation like Flip Matrix) — used to confirm a restructuring had the intended effect. `[STATED, AAD p.225]`

### 5.10 Allocate N (AAD) — Flat List Back to Grouped Branches

Named only in AAD's Chapter 5 (extraction ends mid-explanation at p.252, continues into the next part): **Allocate N** explicitly restructures a flat list into a tree given a target group size N — e.g. a flat 24-point list with N=6 becomes 4 branches (columns) of 6 points (rows) each, with resulting paths `{0;0}, {0;1}, {0;2}, ...`. `[STATED, AAD p.251]`

**Why it's needed — Sort List never creates branches.** `Sort List`'s rearranged output is always a single flat trunk (`{0}`), even when the new order happens to cluster items into logical row/column-sized groups — sorting only reorders items, it never introduces branching. This reframes "recover grid neighbors from a scrambled list" as a pure sorting problem: (1) sort the whole flat list by one axis coordinate (e.g. x, via `Deconstruct(point).X` as sort key) to cluster it into contiguous column-sized runs; (2) `Allocate N` splits that flat, pre-clustered list into real branches; (3) sort each resulting branch again by the other axis coordinate (y) to resolve row order within each column. Step 3's own diagram falls outside the extracted page range. `[STATED, AAD p.249-250, p.252]` `[NOT IN SOURCE: step 3's diagram and Allocate N's own full IO — both fall on pages after the extraction's p.252 cutoff]`

**Why this matters downstream:** `Surface From Points` (and similar grid-building components) assume the input point list is already sequenced in row/column grid order — feeding it a geometrically-correct but list-order-scrambled point set produces a severely malformed, self-intersecting surface **with no error or warning raised**; the problem is only detectable by visually inspecting the output. `[STATED, AAD p.248-249]`

---

## 6. Relative Item / Relative Items

`RelItem (Relative Item) | Sets > Tree | inputs: T (Tree, source), O (Offset mask string), Wp (Wrap Paths, boolean), Wi (Wrap Items, boolean) | outputs: A (tree A), B (tree B)`. `[STATED, Essential p.76-80]`

**Offset-mask grammar:** `{branch offset}[index offset]`. Describes, in relative terms, how to connect an item at some address to another item in the SAME (or a different) tree by adding fixed offsets to the branch number and to the index. Example: `{+1}[+1]` means connect the item at branch B, index I to the item at branch B+1, index I+1 — diagonal connectivity in a grid. The component internally builds **two NEW correlated trees** ("A tree" and "B tree") whose corresponding branches/items are exactly the pairs described by the offset, so a simple 2-point Line component wired A→B draws all the offset connections at once. `[STATED, Essential p.76-77]`

**Worked mechanism (Fig.77, p.76-77):** an "Original tree" with branches `{0},{1},{2},{3}` (4 branches, 3 items each). Applying offset `{+1}[+1]` produces two output trees, each with **3 branches** (reduced from 4 — the last branch and last item in each branch have no `+1` neighbor and are dropped): A-tree items are the base addresses, B-tree items are each base address's diagonal neighbor (branch+1, index+1).

```
Slider[Branch spans=3] -> SqGrid.Ex ; Slider[Element spans=2] -> SqGrid.Ey -> SqGrid.P {branches: 4 x 3}
SqGrid.P -> RelItem.T ; "{+1}[+1]" -> RelItem.O -> RelItem.A {3x2, "Original tree (smaller)"}, RelItem.B {3x2, "Offset tree"}
RelItem.A -> Ln.A ; RelItem.B -> Ln.B -> Ln.L  = diagonal connector lines
```
`[STATED, Essential p.77]`

**Across 2 different trees:** the same offset mechanism works when the two endpoints of each connection come from two DIFFERENT trees rather than one — e.g. offset `{+1}[0]` connects point `[branch B, index I]` of tree 1 to point `[branch B+1, index I]` of tree 2 (same index, next branch over). `[STATED, Essential p.79]`

**Truss tutorial (compound use, 3_6_1_B, p.80-81):** to build a full truss connectivity pattern from one flat grid of points: (1) `Cull Pattern` twice with complementary patterns (`[True,False]` / `[False,True]`) to get "bottom" and "top" interleaved sub-grids; (2) apply `RelItem` twice on EACH sub-grid with complementary masks `{0}[+1]` (horizontal, within a branch) and `{+1}[0]` (vertical, across branches) to build in-plane chord members; (3) apply `RelItem` again between the full (unculled) bottom and top grids with a diagonal offset mask `{0}[0]` / `{0}[-1]` to generate diagonal web members connecting bottom chord to top chord. `[STATED, Essential p.80-81]`

**Output-size gotcha (recurs at every use):** Relative Item necessarily produces output trees **smaller than the input** whenever the offset would reference an out-of-bounds branch/index — reconfirmed with concrete numbers in the Diagonal Triangles tutorial: a 7-branch × 9-item input grid, offset `{+1}[+1]`, produces 6-branch × 8-item A and B trees (branch count 7→6, item count 9→8). `[STATED, Essential p.76-77, p.95]`

---

## 7. Decision Logic — When and Why

The books teach tree operations not as isolated commands but as answers to specific structural problems. Collected here with canonical notation (`Wire: A.Output -> B.Input`, `tree state {flat | grafted | branches: N x M}`, `Slider[min..max, default]`).

| Problem | Operation | Why | Worked example |
|---|---|---|---|
| Two independent lists need to combine **item-by-item**, not as one giant merged sequence | **Graft** both lists first, then Merge | Merging flat lists concatenates them into one branch; a per-branch component (Loft) then processes the whole concatenation as one continuous sequence, not as pairs | `Srf(top).B -> DeBrep.E {1x4}` and `Srf(bottom).B -> DeBrep.E {1x4}` → both Graft → `{4x1}` each → `Merge -> {4 branches, 1 top-edge + 1 bottom-edge each}` → `Loft.L` = correct box, not a bowtie `[STATED, AAD p.223-224]` |
| A component (Polyline) needs to see ALL points as one continuous sequence, ignoring source grouping | **Flatten** | Branches are watertight — Polyline fed 4 branches of 3 points draws 4 separate triangles, not 1 dodecagon | `DeBrep.V {4x3} -> Flatten.T -> {1x12} -> PLine.Pl` = one 12-point polyline `[STATED, AAD p.220-221]` |
| A global statistic (min/max, Bounds) is needed across a whole per-cell tree, but the result must then drive each cell individually again | **Flatten → compute → re-Graft** | Bounds/ReMap need one flat list to find a TRUE global min/max, not per-branch mins; the per-cell driving value then needs branch alignment restored | Distance-to-attractor tree flattened → `Bounds.I` → `ReMap.R` re-Grafted → feeds `OffsetS.D` per cell `[STATED, AAD p.232-235]` |
| An alternating/cyclic value pattern must run continuously across an entire multi-branch dataset, not restart every branch | **Flatten → apply pattern → Unflatten with the ORIGINAL (pre-flatten) tree as guide** | Applying the pattern to still-branched data resets it at every branch start (bug); flattening lets it run continuously; Unflatten restores per-branch grouping needed by the next per-branch step (Interpolate) | Weaving tutorial's warp threads: flatten → alternate ±0.3 → move → `Unflatten.G = original SDivide.P tree` → `IntCrv` one curve per thread `[STATED, AAD p.245-247]` |
| Chained tree-generating steps have left redundant nesting (e.g. `{0;0;0;0;0;0}`) that breaks matching | **Simplify Tree** (in addition to Graft, not instead of) | "Complex data structures are hard to match" — redundant depth must be collapsed before Merge/Loft pairs correctly | 5-branch tree `{0;0}...{0;4}` → Simplify → `{0}...{4}`, same values, matchable depth `[STATED, Essential p.72]` `[STATED, AAD p.228-229]` |
| Data is grouped "by source object" (e.g. one branch per circle) but the goal needs it grouped "by corresponding position across objects" | **Flip Matrix** | Transposes which axis is branch vs. item — the only way to regroup "the Nth item of every branch" into its own branch | 3 circles, 10 pts each `{3x10}` → Flip → `{10x3}` → radial spokes across corresponding points `[STATED, AAD p.224-225]`; also used to derive a "weft" tree from a "warp" tree for free without re-deriving points `[STATED, AAD p.245-246, p.248]` |
| A subset of a tree needs an independent transform, then must be losslessly recombined with the untouched rest | **Split Tree (mask) → transform Positive (or Negative) → Combine** | Both Split outputs retain the ORIGINAL branch paths (excluded items become null, not removed), so Combine can losslessly reassemble | `{*}[(2 to 6)]` splits middle rows; `Move` the Positive; `Combine.[0]/.[1]` restores full structure `[STATED, Essential p.82-85]` |
| Corresponding branches/items across MULTIPLE separate trees (not just within one) need to become adjacent for connection | **Path Mapper** — regroup (`{A;B;C}->{A;C;B}`) then flip index into path (`{A;B;C}(i)->{A;B;i}(C)`) | No simpler tool promotes an item index into the branch structure while also reordering which tree/branch pairs are adjacent | Partitions tutorial: 2 trees × 5 branches × 11 items → regroup → flip → 55 branches × 2 items, one branch per point-pair `[STATED, Essential p.88-91]` |
| N separate lists must stay individually addressable (not combined) as parallel branches | **Entwine** | Unlike Merge, Entwine creates one branch per input list — no value combination | `pDecon.X/.Y/.Z -> Entwine.[0;0]/[0;1]/[0;2] -> {3 branches x 5}` `[STATED, Essential p.71]` |
| N separate lists should become one bigger flat sequence | **Merge** | Concatenation, not organization — used when downstream truly wants one list, e.g. after Grafting for pairing, or to build one continuous curve network | `FirstList(4), SecondList(4) -> Merge.D1/.D2 -> {flat 1x8}` `[STATED, Essential p.71]` |
| Diagonal / offset connectivity is needed between grid neighbors (or between two grids) without manual per-item Shift/Item juggling | **Relative Item** with an offset mask `{db}[di]` | Builds two correlated output trees whose paired branches/items are exactly the desired connections, in one component | `{+1}[+1]` on a 4x3 grid → diagonal connector pairs, reduced to 3x2 at the trimmed edges `[STATED, Essential p.76-77]` |
| A whole algorithm solved for ONE object needs to scale to MANY objects | **Feed a list where a single item used to go — no logic changes** | GH's automatic list-to-tree propagation upgrades every downstream list into a tree "for free," as long as every intermediate step is a per-item (1-to-1 or consistent 1-to-many) operation | Sloped Roof: single Line → single-truss graph; swap in a LIST of 6 lines (via Move+Series) → the same unmodified graph now outputs 6-branch trees for Bottom/Top/Middle points `[STATED, Essential p.92-94]` |

**Cull Pattern vs. Dispatch — a related, non-tree-restructuring decision that recurs alongside these:** Cull Pattern **discards** the unwanted subset entirely; Dispatch **preserves both** the wanted and unwanted subsets as two separate outputs (A and B) — an important distinction when the discarded data might still be needed later in the definition. `[STATED, Essential p.38]`

---

## 8. Debugging Tree Problems

### 8.1 Diagnostic tools

| Tool | What it shows | Source |
|---|---|---|
| **Panel** | Full data values AND structure — path header (e.g. `{0}`) printed above each branch's items, plus a structure summary line (`Data with M branches, {path} N=k...`) | `[STATED, Essential p.18, p.33, p.53]` |
| **Parameter Viewer** | Structure only (no values) — same `Data with M branches...` summary as Panel, without the actual values | `[STATED, Essential p.18, p.33, p.53-54]` |
| **Param Viewer, graphical mode** | Double-click opens a small graphical preview of tree/branch structure — radiating-line diagrams whose branch count/arrangement visibly change before/after an operation | `[STATED, AAD p.225]` |
| **Tree Statistics (TStat)** | `inputs: T (Tree) -> outputs: P (all Paths), L (item counts per branch), C (branch Count)` — used to dynamically extract path addresses instead of hardcoding them | `[STATED, Essential p.67]` |
| **List Length (Lng)** | Item count of a flat list — recommended check on both inputs before wiring two lists into the same component | `[STATED, Essential p.26, p.37]` |
| **Wire display** (dashed vs. solid, single vs. double line) | At-a-glance structure cue without opening any inspector — see §2 | `[STATED, Essential p.34]` `[STATED, AAD p.220-221]` |
| **Profiler** | Per-component elapsed processing time readout (e.g. "11ms", "1.2s") shown directly under a component on canvas | `[STATED, Essential p.26]` |

**Recommended general practice:** always verify the output of each component before relying on it downstream, since GH sometimes ignores invalid input (nulls, wrong/uncastable types) silently rather than erroring loudly. `[STATED, Essential p.15]` For large-scale operations: prototype on a small data subset first, break the solution into stages so slow parts can be isolated, use the Profiler to measure per-component time, and disable/disconnect the offending input if a solution crashes or hangs. `[STATED, Essential p.26]`

### 8.2 Silent-failure gotchas (no error, wrong result)

These are the highest-severity gotchas because Grasshopper gives **no visual indication anything is wrong** — the definition runs, geometry is produced, and it is simply incorrect:

- **Mismatched list lengths or mismatched data structures** (list vs. tree) fed into the same component: GH does not error, it silently applies its default matching/pairing behavior, which "has the potential to spiral the solution out of memory" if not checked. `[STATED, Essential p.25-26]`
- **Long-list-to-tree and tree-to-tree matching** can silently produce an output tree structure that matches **NEITHER** of the original inputs — explicitly flagged as something to verify, never assume. `[STATED, Essential p.62-64]`
- **Merging two lists WITHOUT first Grafting them** silently produces one flat concatenated branch instead of paired branches — a per-branch component (Loft) then processes the entire concatenation as one continuous operation (e.g. a self-intersecting twisted "bowtie" surface) instead of the intended per-pair result. `[STATED, AAD p.223-224]`
- **Surface From Points / any "surface from an ordered point list" component** assumes pre-ordered row/column input; feeding it a geometrically-correct but list-order-scrambled point set produces a severely malformed, self-intersecting surface with **no error or warning** — detectable only by visually inspecting the output. `[STATED, AAD p.248-249]`
- **Mesh Explode's F output fed unflattened into an export component**: Ecotect silently imports only the faces of the LAST branch/path — the multi-branch structure truncates the export with no error. `[STATED, AAD p.454]`
- **Applying an alternating/repeating pattern to still-tree-structured (branched) data**: the pattern resets at the start of every branch instead of continuing — every thread starts with the same sign/value instead of alternating; only visible once the actual geometry is inspected, not from the wiring. `[STATED, AAD p.245-246]`
- **Sort List never creates branches**, even when its new order clusters data into logical row/column-sized groups — a separate restructuring step (Allocate N) is required, or downstream per-group operations will silently operate on the wrong (still-flat) grouping. `[STATED, AAD p.250, p.252]`
- **A curve's Domain is not guaranteed to be 0-to-1** — assuming so and evaluating at `t=0.5` expecting the midpoint is a common, silent bug (the book explicitly marks the wrong result "Wrong output!"). `[STATED, Essential p.20, p.24]`
- **Text-to-Number cast and wrong-type input** can fail totally silently (result `<null>`) rather than showing a red error. `[STATED, Essential p.15, p.24]`
- **KangarooPhysics' Force objects input "must be set to flatten"** (a bolded warning in the source) — two separate branch/streams (Springs output, Unary Force output) must be merged into one flat list before the single Force-objects input will accept them correctly. `[STATED, AAD p.366]`

### 8.3 Structural gotchas, by operation

- **Grafting** feels "unintuitive" because it deliberately increases structural complexity — expect it, don't fight it, when the goal is forcing one-to-one pairing. `[STATED, Essential p.69]`
- **Grafting alone is not always sufficient** after repeated Explode/Graft chains — over-nested trees also need Simplify Tree, or downstream per-branch components still misbehave. `[STATED, AAD p.228-229]`
- **Flip Matrix**: works on unequal-LENGTH branches by padding with literal `<null>` values (a real gotcha for downstream math/geometry components that can't handle nulls — clean with `Clean`/`Trim` first) `[STATED, Essential p.72]`, but **fails entirely** (red error, "there is no logical solution to flip") on trees with variable branch **DEPTH**. `[STATED, Essential p.72]`
- **Unflatten Tree** only works if the flat input list and the guide tree have EXACTLY the same total item count — mismatched counts mean the component will not restructure the data. `[STATED, AAD p.222]`
- **Relative Item** necessarily produces output trees SMALLER than the input whenever an offset mask references an out-of-bounds branch/index (edge branches/items have no `+N` neighbor) — reconfirmed with concrete shrinking numbers (7→6 branches, 9→8 items) across multiple tutorials. `[STATED, Essential p.76-77, p.95]`
- **Split Tree's negated-infinite-sequence rule has an asymmetry**: `!(3,5,...)` also matches everything to the LEFT of the sequence start, since the sequence does not extend leftward — do not assume a negated sequence behaves like a simple complement across all integers. `[STATED, Essential p.82]`
- **Split Tree's own worked example has an internal inconsistency** in the source book: the mask literal `{*}[(0 to 4) or (6,11,41)]` is described in the accompanying prose as selecting "items 7, 12 and 42" — numbers that don't match the mask's own literals (6,11,41). Transcribed here exactly as printed rather than silently corrected. `[STATED, Essential p.82]`
- **Path Mapper** is explicitly the "least intuitive" tool and "can cause a loss of data" — misconfigured target-path expressions can silently drop elements. Combining two mapping operations into one expression is "not always possible," with no further criteria given for when it fails. `[STATED, Essential p.86-91]`
- **Cull Pattern's L and P inputs must share the same flat/tree structure** — a boolean pattern computed via a tree-structured intermediate route must be explicitly Flattened before it will correctly pair with a flat list. `[STATED, AAD p.236]`
- **Cross Reference's result length grows multiplicatively** (product of all input lengths) — a 3-way Cross Reference on three 6-item lists already produces 216 combinations; check list lengths first to avoid combinatorial blow-up. `[STATED, Essential p.43-45]` (general slow/large-data risk also noted `[STATED, Essential p.26]`)
- **Cross Reference's result ORDER depends on input ORDER** (which list is A vs. B) even though the underlying value-set is the same — not a no-op to swap if downstream logic relies on result order. `[STATED, Essential p.42-43]`
- **Randomly-generated curve parameters must be sorted before evaluating/lofting** in sequence, or the resulting cross-section profiles are visited out of the curve's natural order, producing a twisted/self-intersecting Loft. `[STATED, Essential p.46]`
- **Interpolating through a flattened point list without restoring tree structure** (Unflatten with the original tree as guide) produces one tangled curve through the entire point set instead of separate per-thread curves. `[STATED, AAD p.246-247]`
- **Edge Surface only caps exactly 4-edge boundaries**; N-sided openings (e.g. hexagons) need a different strategy (two separate Lofts between opposite edge pairs, using Flip Curve first since consistent winding leaves opposite edges pointing in opposite directions). `[STATED, AAD p.239, p.241-242]`
- **Isotrim's untrimmed sub-surface outputs keep the ORIGINAL parent surface's domain** internally (not reset to [0,1]) until Reparameterize is explicitly applied — a domain-carrying gotcha, not a tree-shape one, but easy to conflate with tree bugs when EvalSrf/uv correspondence looks wrong. `[STATED, AAD p.150]`
- **Length on a list of curves returns one value per item**; Join+Length first merges the list into one curve, then returns a single aggregated total — easy to conflate the two if not watching branch/item counts. `[STATED, AAD p.370, p.372]`
- **"Solve for one instance, then feed a list" scaling strategy** (§7's last row) only works cleanly if every intermediate step in the single-instance graph is a per-item (1-to-1 or consistent 1-to-many) operation — no additional safety net is described beyond the worked example. `[STATED, Essential p.93]`
- **Split by whole branches vs. split within branches are different tools for different symmetry needs**: the Zigzag tutorial's whole-column split (`{0,2,...}` at the branch level) additionally requires reordering item ORDER within the negative branches (not just membership) before the two halves can be woven back together correctly — a structurally valid split is not sufficient by itself if internal order also needs correcting. `[STATED, Essential p.96]`
- **Weaving/normal-driven patterns require the normals tree and points tree to share IDENTICAL structure** — both derived from the same source (e.g. SDivide) and split/flipped with identical masks in parallel, or the per-point normal-direction offset pairs the wrong normal with the wrong point. `[STATED, Essential p.101]`
- **Mesh UV/Surface subdivision counts (U,V) must be numerically identical** across independently-converted adjoining surfaces, so mesh boundary vertices land at coincident positions (avoiding T-nodes) and weld into one continuous mesh. `[STATED, AAD p.278]`
- **Setting a data tree directly inside a parameter** (right-click "Set Multiple Booleans" etc.) is possible but "once set, it is relatively hard to change" — reserve for constant/fixed inputs, not values expected to update. `[STATED, Essential p.58]`
- **HoopSnake's C-output accumulates every loop iteration as a separate branch** of one tree, not just the final result — a recursive/looping definition's full iteration history is exposed downstream this way, easy to misread as "extra unwanted branches" if not expected. `[STATED, AAD p.301, p.303]`

### 8.4 Cross-source framing notes and conflict search

A deliberate search for genuine contradictions between Essential and AAD on data-tree semantics found **none** — the two books are consistent everywhere they overlap. What differs is framing and vocabulary, noted throughout this document at point of use and summarized here:

1. **Vocabulary depth for path/branch/item.** Essential names 3+ tiers (main trunk, second trunk, last trunk holding leaves, leaf index); AAD uses a flatter trunk/branch/item vocabulary. Both describe the identical `{path}[index]` addressing scheme. `[STATED, Essential p.55]` `[STATED, AAD p.218-219]`
2. **Wire-display granularity.** Essential documents a 3-way scheme (single line = item, double solid = list, double dashed = tree). AAD's dedicated tree chapter documents a 2-way scheme (dashed = tree, solid = flat) but its own earlier chapters independently preview an equivalent "no data / one datum / many data" 3-way scheme under a named "Draw Fancy Wires" display mode — consistent with, not contradicting, Essential's granularity. `[STATED, Essential p.34]` `[STATED, AAD p.58, p.71, p.220-221]`
3. **Default tool for dimensional expansion (1D list → 2D/3D grid).** Essential's Chapter 2 (list matching) and Chapter 3 (trees) both reach for Cross Reference for pure Cartesian-grid generation (e.g. the 216-point cube) and for Graft+Merge for per-branch pairing before Loft. AAD's own list-matching chapter also defaults to Cross Reference for coordinate-grid generation, while AAD's dedicated tree chapter (§5) teaches Graft extensively for the pairing use case — the two AAD chapters and Essential all agree Cross Reference and Graft serve different specific goals; no source claims they're interchangeable. `[STATED, Essential p.43-45]` `[STATED, AAD p.104, p.108]` `[INFERRED, AAD p.90-94]`
4. **Coverage gaps, not disagreements.** AAD's Flip Matrix worked example never tests the variable-branch-DEPTH failure case that Essential documents (§5.4) — an omission, not a contradiction. Conversely, Essential never diagrams Explode Tree's actual I/O (only names it), which AAD supplies (§5.5).

No claim in this document required a `[GENERAL]` tag — every operation's semantics, every worked number, and every gotcha above trace to an explicit `[STATED]` or clearly-flagged `[INFERRED]`/`[NOT IN SOURCE]` line in the source extractions.
