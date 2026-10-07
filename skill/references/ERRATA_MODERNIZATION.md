# Errata — Phase 2b Web Verification

This file records corrections found while verifying the two 2014-era source books behind `components.md` — Tedeschi/Wirz/Andreani, *Algorithms-Aided Design* (AAD, reflecting Grasshopper ~0.9.0076 for Rhino 5) and Rajaa Issa, *Essential Algorithms and Data Structures for Grasshopper* (Essential) — against current, official Grasshopper 1.0 documentation (grasshopperdocs.com component pages, docs.mcneel.com, developer.rhino3d.com, McNeel Discourse/YouTrack, rhino3d.education). It is the errata companion to `components.md`; every entry below corresponds to a `[VERIFIED <url>]`-tagged finding in `knowledge/validation/verify-1-conflicts.md`, `verify-2-core.md`, or `verify-3-surface-plugins.md`.

Two kinds of note are recorded here:
1. **Errata** — a case where a source book's own citation, diagram, or claim is wrong, imprecise, or internally inconsistent, verified against current docs.
2. **Version notes** — not errors at all, just genuine 2014-vs-2026 differences (plugin rewrites, renames, deprecations) that a reader moving between the book and current Grasshopper should know about.

Nothing below adds facts beyond what the three verification findings files already established; see those files for full source-URL citations and reasoning.

---

## AAD errata (Tedeschi et al., *Algorithms-Aided Design*, 2014)

**AAD p.179** — cites Cull Index as Sets > List -> the component's actual tab is Sets > Sequence; p.179 mixes it up with the neighboring List panel — [https://grasshopperdocs.com/components/grasshoppersets/cullIndex.html](https://grasshopperdocs.com/components/grasshoppersets/cullIndex.html)

**AAD p.107-108, 178** — cites Cull Pattern as Sets > List -> the component's actual tab is Sets > Sequence — [https://grasshopperdocs.com/components/grasshoppersets/cullPattern.html](https://grasshopperdocs.com/components/grasshoppersets/cullPattern.html)

**AAD p.243, 245** (also Essential p.43, 48 — see Essential section) — cites Repeat/Repeat Data as Sets > List -> the component's actual tab is Sets > Sequence — [https://grasshopperdocs.com/components/grasshoppersets/repeatData.html](https://grasshopperdocs.com/components/grasshoppersets/repeatData.html)

**AAD p.113-114, 451-452** — cites Scale as Transform > Euclidean -> the component's actual tab is Transform > Affine (an internal citation inconsistency within the same book — p.196/323 correctly say Affine) — [https://grasshopperdocs.com/components/grasshoppertransform/scale.html](https://grasshopperdocs.com/components/grasshoppertransform/scale.html)

**AAD/Essential (Move entry)** — one source's citation spells the tab "Euclidian" -> the panel is spelled "Euclidean" in current GH1; a simple misspelling, not a real alternate name — [https://grasshopperdocs.com/components/grasshoppertransform/move.html](https://grasshopperdocs.com/components/grasshoppertransform/move.html)

**AAD p.450, 456** — cites Mesh Surface / Mesh UV as Mesh > Triangulation -> the component's actual tab is Mesh > Util; Mesh > Triangulation is a real, separate panel (home to Delaunay Mesh/Voronoi/TriRemesh) that AAD appears to have conflated with Util for this entry — [https://grasshopperdocs.com/components/grasshoppermesh/meshSurface.html](https://grasshopperdocs.com/components/grasshoppermesh/meshSurface.html)

**AAD p.178-179** — cites Surface Split as Surface > Util -> the component's actual (and only) tab is Intersect > Physical; that page range discusses Surface-tab material generally rather than this component specifically — [https://grasshopperdocs.com/components/grasshopperintersect/surfaceSplit.html](https://grasshopperdocs.com/components/grasshopperintersect/surfaceSplit.html)

**AAD p.160** — names the curve-endpoints component "Endpoint" in Curve > Util -> the correct name is "End Points" in Curve > Analysis (p.62's citation is correct; p.160 is likely a mislabeled in-context screenshot) — [https://grasshopperdocs.com/components/grasshoppercurve/endPoints.html](https://grasshopperdocs.com/components/grasshoppercurve/endPoints.html)

**AAD p.378** — a canvas diagram is labeled "Explode" (ports C, R -> S, V) while the surrounding body text still calls it "Shatter" -> the diagram is genuinely the separate **Explode** component (Curve > Util); the real **Shatter** (Curve > Division) takes C, t -> S only, with no R input or V output, so it is the book's own surrounding text that is wrong on that page, not the diagram — [https://grasshopperdocs.com/components/grasshoppercurve/shatter.html](https://grasshopperdocs.com/components/grasshoppercurve/shatter.html) / [https://grasshopperdocs.com/components/grasshoppercurve/explode.html](https://grasshopperdocs.com/components/grasshoppercurve/explode.html)

**AAD p.269** — Construct Plane's diagram is only partly legible and appears to show 2 inputs (O, one vector) -> the real Construct Plane takes 3 inputs (O, X-Axis, Y-Axis); a 2-input O+vector diagram more likely depicts the separate **Plane Normal** component instead — [https://grasshopperdocs.com/components/grasshoppervector/constructPlane.html](https://grasshopperdocs.com/components/grasshoppervector/constructPlane.html)

**AAD p.309** — a diagram (S, uv -> P, C1, C2) is labeled/transcribed as "Oscillator" -> no such component exists; this is the real **Osculating Circles** component (Surface > Analysis) — [https://grasshopperdocs.com/components/grasshoppersurface/osculatingCircles.html](https://grasshopperdocs.com/components/grasshoppersurface/osculatingCircles.html)

**AAD p.270** — Planar is recorded with only a single Boolean output -> the real component also outputs Plane (best-fit plane) and Deviation (number); tab is confirmed as Curve > Analysis — [https://grasshopperdocs.com/components/grasshoppercurve/planar.html](https://grasshopperdocs.com/components/grasshoppercurve/planar.html)

**AAD p.388, 391-392, 453-455** — presents Mesh Explode as if it were a native Mesh > Analysis component with a "J (Join?)" input -> no native "Mesh Explode" exists in current Grasshopper; the real match is the MeshEdit plugin's "Mesh Explode" (Analysis tab; inputs M, I=Interpolate -> output F); "J" is unattested anywhere and is likely a misread of "I" — [https://grasshopperdocs.com/components/meshedit/meshExplode.html](https://grasshopperdocs.com/components/meshedit/meshExplode.html)

**AAD p.65** — Point List is shown with only P (points) and S (text size) inputs -> the real component also has T (Tags, boolean) and L (Lines, boolean) toggle inputs that the book omits — [https://grasshopperdocs.com/components/grasshopperdisplay/pointList.html](https://grasshopperdocs.com/components/grasshopperdisplay/pointList.html)

**AAD p.305, 382** — Weaverbird's "Mesh Edges" (wbEdges) is shown with a second input "O" -> the real component has only ONE input (G); "O" is likely a confusion with Weaverbird's separate "Naked boundary" component (M -> C), which extracts only the open/naked boundary — [https://grasshopperdocs.com/components/weaverbird/meshEdges.html](https://grasshopperdocs.com/components/weaverbird/meshEdges.html)

**AAD p.430** — presents 3DIsoMesh (Millipede) without naming a plugin author -> the confirmed author is Panagiotis Michalatos — [https://grasshopperdocs.com/components/millipede/3DIsoMesh.html](https://grasshopperdocs.com/components/millipede/3DIsoMesh.html)

**AAD p.306-307, 309** — frames "Loop" as part of/bundled inside the "Generation" plugin -> "Loop" is a separate, standalone plugin (food4rhino/app/loop) by the same author, Antonio Turiello, not a component inside Generation — [https://www.food4rhino.com/en/app/loop](https://www.food4rhino.com/en/app/loop)

---

## Essential errata (Issa, *Essential Algorithms and Data Structures for Grasshopper*, 2nd ed.)

**Essential p.71** — groups Merge under "Sets > List/Util" -> the component's actual tab is Sets > Tree (confirmed by its Type GUID); AAD's own p.64 citation of Tree is the one that matches current docs — [https://grasshopperdocs.com/components/grasshoppersets/merge.html](https://grasshopperdocs.com/components/grasshoppersets/merge.html)

**Essential p.92-99** — implies Weave belongs under Sets > Tree -> the component's actual tab is Sets > List (AAD's p.50 citation is correct) — [https://grasshopperdocs.com/components/grasshoppersets/weave.html](https://grasshopperdocs.com/components/grasshoppersets/weave.html)

**Essential (Concatenate entry)** — groups Concatenate near the Maths tab -> the component's actual tab is Sets > Text; the "near Maths" grouping is a thematic/teaching grouping in the book, not the component's ribbon tab — [https://grasshopperdocs.com/components/grasshoppersets/concatenate.html](https://grasshopperdocs.com/components/grasshoppersets/concatenate.html)

**Essential p.43, 48** — cites Repeat/Repeat Data as Sets > List -> the component's actual tab is Sets > Sequence (same correction as the AAD p.243,245 entry above) — [https://grasshopperdocs.com/components/grasshoppersets/repeatData.html](https://grasshopperdocs.com/components/grasshoppersets/repeatData.html)

**Essential p.96** — records "DCon"'s N as both an input AND an output -> the real component (**Delete Consecutive**) has N only as an OUTPUT (count of members removed); it has just 2 inputs (S, W) and 2 outputs (S, N), not 3 inputs — [https://grasshopperdocs.com/components/grasshoppersets/deleteConsecutive.html](https://grasshopperdocs.com/components/grasshoppersets/deleteConsecutive.html)

---

## Version notes (not errors)

2014-era vs. current (2026) Grasshopper 1.0 differences that a reader moving between these books and today's software should know about. None of these reflect a mistake in either book — they are genuine ecosystem changes since 2014.

- **Kangaroo 1 -> Kangaroo 2.** AAD (2014) teaches Kangaroo-1-era components (e.g. Springs From Line, KangarooPhysics, Kangaroo Settings). Kangaroo 1 was fully rewritten as Kangaroo 2 (~2015-16) with most components renamed/restructured (e.g. Springs From Line -> a generic Length goal). WarpWeft is unusual in having kept the same name, tab, and role across both versions — still current in Kangaroo 2.

- **HoopSnake -> Anemone.** HoopSnake (AAD's loop/recursion plugin) still works and is still distributed (food4rhino, GitHub), but the current de-facto standard plugin for loops/recursion in Grasshopper is now **Anemone** (Loop Start/Loop End) — most present-day tutorials recommend Anemone over HoopSnake.

- **"Generation" plugin's Loop -> Anemone.** The same modern-standard shift applies to Antonio Turiello's standalone "loop" plugin (distinct from his "Generation" plugin, see errata above): Anemone is now the standard tool for loops/iteration, not this "loop" plugin or HoopSnake.

- **Tree8's Allocate N -> native Partition List.** Tree8 (AAD's structural list-management add-on, part of the STRAUTO toolset) is hard to find today: not on Food4Rhino, not documented on grasshopperdocs.com, and forum users (2021+) report its original host (tree8.chang-soft.co.kr) is gone with compatibility problems in Rhino 7. Native Grasshopper's built-in **Partition List** component now covers Allocate N's core function (splitting a flat list into a tree of N-item branches), making Tree8 unnecessary for this task in current Grasshopper.

- **Mesh Edit's Triangulate -> native Triangulate.** AAD-era Grasshopper required the Mesh Edit plugin (Ursula Frick & Thomas Grabner) for mesh triangulation. Grasshopper now ships a **native** Mesh > Util "Triangulate" component (M -> M, N) that matches the book's own M-in/M,N-out diagram better than the plugin's own "Mesh Triangulate" (which lacks the N/count output entirely).

- **Interpolate Curve naming.** The current official GH1 component name is "**Interpolate**" (nickname "IntCrv"), not "Interpolate Curve" — a naming nuance, not a factual error in the recorded port data (the L/D outputs the KB flagged as uncertain are both real).

- **List-matching components already standard by 2014.** Shortest List, Longest List, and Cross Reference were already standardized by GH 0.9 (per McNeel's "New Data Matching in 0.9+" page) — i.e., already current in AAD's own 2014-era Grasshopper, not a later rename. Only the KB's own naming/aliasing was uncertain, not the components' vintage.

- **Larger Than: a 2014 coverage gap, not a version difference.** Essential documents this component (as "Larger"); AAD has no dedicated entry for it. The component itself was already a real, standing part of GH1 in 2014 — AAD simply never covered it.

- **Weaverbird: still current.** The plugin AAD documents for mesh SubD/extraction (Join Meshes and Weld, Mesh Edges, Loop/Catmull-Clark Subdivision, Mesh Thicken) remains actively maintained — v0.9.0.1 for Rhino 7/8 as of January 2026, distributed via the Rhino Package Manager.

- **Millipede: maintenance status uncertain.** No explicit "discontinued" notice was found for Millipede (AAD's topology-optimization plugin), but community mentions describe it as no longer actively developed as of this verification pass.
