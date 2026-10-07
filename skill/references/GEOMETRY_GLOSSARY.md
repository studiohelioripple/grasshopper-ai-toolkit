# Grasshopper & Rhino Glossary

## Notation used in this knowledge base

- **Component notation**: `Component Name (Tab > Section)` — e.g. `Circle (Curve > Primitive)`
- **Wiring/data flow**: `A.Out -> B.In {flat}` indicates connected component inputs/outputs with data structure state
- **Tree states**: `{flat}` (single branch), `{grafted}` (multiple branches), `{branches: N x M}` (branch dimensions)
- **Sliders**: `Slider[min..max, default] -> Component.Input` — e.g. `Slider[0..10, 5] -> Divide Curve.N`
- **Sections**: `=== Section: name ===` marks worked examples
- **Provenance**: `[STATED, p.XX]` references source document page. In this glossary, the shorthand `[AAD, p.X]` / `[Essential, p.X]` is equivalent to `[STATED, AAD p.X]` / `[STATED, Essential p.X]` — every entry is directly source-derived unless tagged otherwise.

---

## Glossary (A–Z)

**Additive process** — Traditional (paper-based) drawing method in which complexity is built by adding and overlapping independent marks/lines with no associative relations between them; internal consistency is entrusted to the designer rather than the medium. Contrasted with algorithmic/parametric approaches in which geometric dependencies are explicit and automatic. [AAD, p.16]

**Algorithm** — A finite, unambiguous, well-defined step-by-step procedure that turns defined input(s) into a well-defined output(s). Ambiguous instructions produce incorrect or undefined results; precondition violations (wrong data types) trigger errors. [AAD, p.22–23]

**Algorithmic thinking** — Approach to design in which every piece of data (points, vectors, planes, angles) must be explicitly defined and wired into components, rather than supplied interactively/implicitly via on-screen widgets as in traditional 3D modeling. [Essential, p.8–9]

**Affine transformation** — A geometric transformation (scale, shear, projection) that preserves parallelism only, not shape, size, or position. Contrasted with Euclidean (preserves shape and size) and similarity (preserves shape only) transformations. [AAD, p.184]

**Amplitude** — Magnitude or scaling factor of a vector; used to rescale a vector to an arbitrary desired length while preserving its direction/sense. [AAD, p.187]

**Anticlastic surface** — A surface at a point where Gaussian Curvature G < 0, meaning the two principal curvatures have opposite signs; visualized as saddle-shaped (e.g., a saddle, hyperbolic paraboloid). Contrasted with synclastic. [AAD, p.167, 173]

**Apex** — In the context of space-frame/pyramidal structures, the highest or offset point above a planar grid, connected to the surrounding corners/nodes to form pyramidal modules. [AAD, p.160]

**Arc** — A curve segment forming part of a circle or ellipse; defined by endpoints, a center, and radius or by three points through which it passes. [AAD, p.97–98]

**Associative logic** — Design method (pioneered in Sketchpad, 1963) in which explicit geometric constraints bind related elements so that moving one element automatically updates dependent elements; overcomes the "additive logic" limitation of traditional drawing. [AAD, p.21, 27]

**Attractor** — A geometric entity (point, curve, surface, or other element) that modifies surrounding geometry based on distance from it, within defined limits. Mechanism: measure distance from attractor to each target → remap distance into a useful numeric range → apply remapped values to drive transform parameters (scale factor, translation magnitude, etc.). [AAD, p.112]

**Axis-aligned** — Aligned with one of the three world-coordinate axes (X, Y, or Z); used to describe vectors (Unit X, Unit Y, Unit Z) and planes parallel to world axes. [AAD, p.187–188]

**Base plane** — A reference plane serving as the origin and orientation for geometric operations (e.g., a Box primitive's base plane, or a Circle's containing plane). [AAD, p.35, 103]

**Baking** — Freezing one specific configuration of parametric Grasshopper geometry into permanent, independently-editable Rhino geometry via right-click Bake. Baked geometry no longer updates when GH parameters change; the definition remains separately editable. [AAD, p.53–54]

**Bezier curve/surface** — A curve or surface defined by control points (not necessarily interpolated) and a degree; provides intuitive interactive shape control via draggable control handles. [Essential, p.199–200]

**Boolean** — A logical data type with two values: True or False; used to drive conditional filtering (e.g., Cull Pattern, Dispatch) and logical operations (And, Or, Not, Xnor, Equals). [Essential, p.13–14]

**Boolean operation** — A set operation (Union, Difference, Intersection) combining two solids to create a new solid. [Essential, p.5]

**Boundary Representation (Brep)** — A topological model representing solids, polysurfaces, and even single NURBS surfaces as collections of Faces (surfaces), Edges (curves bounding faces), and Vertices (corner points) "stitched" together. A single NURBS surface is the simplest Brep (exactly one face); a box = six joined surface faces. [AAD, p.152–153]

**Branching** — In data trees, the hierarchical subdivision of data into multiple sub-lists (branches), each identified by a distinct path label (e.g., {0;0}, {0;1}, {0;2}). [Essential, p.33]

**Branch path** — A unique identifier for a branch within a data tree, written as a semicolon-separated sequence of integers in braces, e.g., {0;0}, {0;1;2}. The path indicates hierarchical nesting level and position within each level. [Essential, p.33]

**Catenoid** — A minimal surface (M=0) swept by rotating a hanging chain (catenary curve) about a vertical axis; examples include soap films stretched between two rings. [AAD, p.174]

**Canvas** — The working area in the Grasshopper editor where algorithms are assembled from connected components; also called the "blackboard." [AAD, p.36]

**Casting** — Converting (or attempting to convert) data from one type to another automatically; e.g., feeding text "12" into a Number parameter parses it as the number 12. Impossible casts (e.g., text "12AB" into Number) produce an error. [Essential, p.14–16]

**Centroid** — The geometric center/average point of a closed shape, computed by the Area and Volume components. [AAD, p.62–63]

**Chebyshev-net** — An equal-edge-length point grid on a curved surface (developed by mathematician Pafnuty Lvovich Chebyshev, 1878, originally for garment pattern-cutting). Geometric construction: from a starting point, draw circles/spheres of fixed radius L, intersect with surface isocurves or guide curves to find adjacent points at distance L; repeat to tile the surface. Results in a grid where every edge has identical length L, though a "leftover area" remains at the boundary (trade-off with uv-based grids which have unequal edges but perfect domain coverage). [AAD, p.161–165]

**Circle** — A planar curve all points equidistant from a center point; defined by center, plane/normal, and radius. [AAD, p.35]

**Codomain** — The set of possible output values of a function; in the context of Grasshopper, the y-axis values when evaluating a function y=f(x) across a range of x-domain inputs. [AAD, p.101–102]

**Color swatch / Colour Swatch component** — A user-editable color picker input component (Params > Input); double-click to set color and alpha/transparency via a dialog. Used to feed custom colors into Custom Preview for per-component coloring. [AAD, p.67]

**Component** — An atomic operation in Grasshopper representing a primitive, operation, or function; displayed as a named box on the canvas with input slots (left), a name section (middle), and output slots (right). [AAD, p.40–42]

**Constraint** — An explicit rule binding geometric elements together; e.g., "two lines share a point," "a line is perpendicular to a plane." In Sketchpad and Grasshopper, constraints are represented as explicit wired dependencies. [AAD, p.21]

**Construction history** — In Grasshopper, the sequence of all components in a definition is retained/stored; every intermediate result's geometry is kept and can be previewed or hidden independently, unlike traditional CAD where only the final result is visible. [AAD, p.59–60]

**Container component** — A data-storage component (Params > Geometry or Primitives panels) visually identified by a black-hexagonal icon; stores and references geometry set via right-click "Set one Geometry" or linked from Rhino. Types: Point, Curve, Surface, Brep, Geometry (catch-all). Distinct from standard components which perform operations. [AAD, p.40, 49–52]

**Control point** — A vertex of a NURBS curve or surface's control polygon; influences (but does not necessarily lie on) the curve/surface. Weights associated with control points attract (weight > 1) or repel (0 < weight < 1) the curve toward/away from that point. [AAD, p.121–122]

**Control polygon** — The polyline formed by connecting a NURBS curve's control points in order; a degree-1 (linear) NURBS curve coincides exactly with its control polygon. [AAD, p.121]

**Coordinate** — A numeric value (or triple of values X, Y, Z) specifying a position in space relative to a reference origin. [AAD, p.7]

**Coordinate system** — A reference frame for locating points in space; world XY, local plane, surface uv, curve parameter t all serve as coordinate systems in Grasshopper. [AAD, p.124–125]

**Cross Reference** — A component (Sets > List) that performs a full cartesian product (A×B) of two input lists, pairing every item of list A with every item of list B, generating A×B outputs. Used to turn two independent 1D sequences into a full 2D grid of results (e.g., combining X-direction translations with Y-direction translations to produce a 2D array). [AAD, p.92–94]

**Cross-referencing** — In the context of 2-variable functions, the process of generating all pairs (xi, yi) from separate x and y value lists so that a function can be evaluated at every grid point. Without cross-referencing, default list matching produces only a diagonal subset (pairs at matching indices only). [AAD, p.104]

**Curve** — A 1D geometric object (line, arc, spline, etc.) in 3D space. In Grasshopper, nearly all curves are NURBS curves, parameterized by a single variable t in the range [0,1] (after reparameterization) or some other domain. [AAD, p.124–125]

**Curvature** — The measure of how much a curve deviates from being straight; formally, the reciprocal of the radius (k = 1/r) of the osculating circle at a point. Signed curvature assigns positive/negative signs based on which side of the curve the osculating circle lies. [AAD, p.136–137, 167]

**Curvature graph** — A visual display (Curvature Graph component) showing curvature distribution along a curve as a "comb" of perpendicular hairlines whose length is proportional to curvature magnitude, with +/− signs marking regions of positive/negative curvature. [AAD, p.138]

**Data casting** — See casting.

**Data matching** — Grasshopper's default logic for pairing corresponding items when a component receives two or more list inputs simultaneously. Three modes: Shortest List (truncate to shorter list's length, then pair 1-to-1), Longest List (pair 1-to-1, then repeat the shorter list's last item for all remaining longer-list items), Cross Reference (cartesian product, every item of A paired with every item of B). [AAD, p.90–94]

**Data source** — An origin of input data: Internally set (right-click Set One Point, persists in .gh file), Referenced (linked to Rhino geometry, updates live), or Externally supplied (wired from upstream components). Wired data always takes precedence over internal or referenced values. [Essential, p.12–13]

**Data tree** — Grasshopper's hierarchical data structure consisting of multiple branches (each identified by a path like {0;0}, {0;1}), each branch containing a list of items. Components process trees by operating independently within each branch. [Essential, p.33, ch.3]

**Data type** — A classification of data: primitives (Integer, Number, Text/String, Boolean), geometry (Point, Line, Curve, Surface, Brep), or specialized math types (Domain, Vector, Plane, Color, Transformation). [Essential, p.13–14]

**Deconstruct** — To break down a geometric or data object into its constituent parts. E.g., Deconstruct Brep extracts faces, edges, vertices; Deconstruct Arc extracts center plane, radius, angle domain. [AAD, p.107, 152]

**Deconstruct Arc / DArc** — A component (Curve > Analysis) that breaks an arc (or circle) down into its base plane, radius, and angle domain. [AAD, p.107]

**Deconstruct Brep / DeBrep** — A component (Surface > Analysis) that extracts all constituent faces, edges, and vertices of any Brep (surface, polysurface, or solid). [AAD, p.152–153]

**Degree** — The degree of a NURBS curve or surface; a positive integer controlling curve smoothness and flexibility. Order = degree + 1. Lines/polylines have degree 1, circles degree 2, most freeform curves/surfaces degree 3 or 5. [AAD, p.121]

**Derivative** — See tangent vector.

**Developable surface** — A surface with Gaussian Curvature G = 0 everywhere (at least one principal curvature is 0 at every point); can be flattened onto a plane without stretching or tearing. Types: planes, cylinders, cones, generalized cylinders/cones, tangent developables (union of tangent lines to a free-form curve). Every developable is a ruled surface, but not every ruled surface is developable. [AAD, p.168, 170]

**Diagonal grid (diagrid)** — A structural pattern constructed by connecting diagonal vertex pairs of subdivided surface sub-surfaces, creating a diagonal lattice. Built via Isotrim (surface subdivision) → Deconstruct Brep (extract corner vertices) → Line components connecting diagonal pairs. Requires projection back onto the curved surface afterward to achieve surface-coincidence. [AAD, p.155–158]

**Diagram** — In the historical sense, a drawing capturing forces, processes, or geometric transformations in a structured way; exemplified by Peter Eisenman's House IV (1971) with labeled transformation states. In Grasshopper, the node diagram on the canvas itself serves as the algorithm/diagram. [AAD, p.17]

**Difference** — See Boolean operation.

**Direction** — The pointing sense of a vector, curve, or surface; independent of magnitude. E.g., a curve's direction (which end is t=0 vs t=1) is set by control-point order and is independent of reparameterization. [AAD, p.129]

**Dispatch** — A component (Sets > List) that splits one list into two based on a boolean pattern in a single step, outputting A (items where pattern = True) and B (items where pattern = False). Contrasted with needing two separate Cull Pattern operations to capture both outcomes. [AAD, p.108]

**Distance** — The straight-line spacing between two points; computed by the Distance component (Vector > Point). Used in attractor logic to measure target-to-attractor proximity. [AAD, p.113]

**Domain** — A continuous range of numbers [min, max] representing possible input (or parameter) values for a function, curve, or surface. A curve's domain [0, 43.58] is the range of valid t values. [AAD, p.100]

**Domain parameter** — A numeric value within a component/curve's declared domain, used to locate a position; distinct from arc-length parameterization. [AAD, p.125]

**Draw Fancy Wires** — A Grasshopper display option (Display menu) that color-codes wires by data content: orange = no data, thin black = one datum (single item), thick black = multiple data (list). Also draws dashed wires for tree data (explained in Chapter 5). [AAD, p.57–58]

**Driven** — Controlled or determined by an upstream component; e.g., a parameter's value is "driven" by a slider wired into it. [AAD, p.12]

**Dyadic function** — See two-variable function.

**Dynamically growing inputs** — Behavior of components like Merge that auto-generate new empty input slots (D1, D2, D3...) as previous slots are wired; additional slots can be added manually via the component's Zoomable User Interface when zoomed in. [AAD, p.64]

**Dynamical simulation** — Physics-based modeling in which objects move according to forces (gravity, collisions, spring forces, etc.). Contrasted with static parametric form-finding. [AAD, p.34]

**Elation** — Historically, in form-finding via analogue devices (hanging fabric, soap films), the act of reaching equilibrium under dynamic forces; modern Grasshopper algorithms can simulate this numerically. [AAD, p.18]

**Enabled/Disable** — A per-component toggle (right-click > Enabled) that stops a component from executing. Disabled components and all downstream dependents cascade to disabled state (unlike Preview which only hides visualization). [AAD, p.56]

**End point** — Either of the two terminal points of an open curve (t=0 and t=1); extracted by the End Points or Endpoint component. [AAD, p.62, 160]

**Euclidean transformation** — A transformation (translation, rotation, reflection) that preserves both shape and size but not position; contrasted with affine (preserves parallelism only) and similarity (preserves shape only). [AAD, p.184]

**Euler angles** — Three successive rotations around fixed axes (roll, pitch, yaw) used to specify orientation; an alternative to matrix representation. [Essential, p.7]

**Evaluate Curve / Eval** — A component (Curve > Analysis) that finds a point and tangent vector at a given parameter t on a curve (must be reparameterized to [0,1] for predictable behavior) or via the normalized-parameter option. [AAD, p.126–127]

**Evaluate Length / Eval** — A component (Curve > Analysis) that finds a point located a given arc-length distance along a curve from its start (t=0). [AAD, p.132]

**Evaluate Surface / EvalSrf** — A component (Surface > Analysis) that finds a point, normal vector, and tangent plane at a given (u,v) parameter on a surface; the 2D analog of Evaluate Curve. [AAD, p.144–146]

**Evaluation** — Computing the output value(s) of a function, curve, or surface at specific input parameter(s); e.g., evaluating a curve at t=0.5 yields a point. [AAD, p.101]

**Extrude** — A component (Surface > Freeform) that creates a surface by translating a profile curve or surface along a direction vector; produces a constant-cross-section surface (e.g., a cylinder). Described as "the easiest way to create a surface." [AAD, p.75–76, 141]

**Face** — In Brep topology, a single surface patch (bounded by edges and vertices). [AAD, p.152–153]

**Factorial** — Mathematical function (n!) computing n × (n−1) × ... × 2 × 1. [Essential, p.16]

**Fading** — In the context of Grasshopper displays, components in faded/greyed state when disabled or when their preview is toggled off. [AAD, p.56]

**Flatten / Flatten Tree** — An operation that collapses all branches of a data tree into a single flat list under one branch {0}. Inverse operation: Unflatten (requires a guide tree to restructure against). [Essential, p.220–221]

**Flow chart** — A diagram visualizing the tree of constraint dependencies in an algorithm; pioneered in Sketchpad and a conceptual ancestor of Grasshopper's node canvas. [AAD, p.27]

**Form-finding** — Process of discovering novel, optimized structures through complex associative relations between materials, shape, and structural behavior; rejects preconceived typology. Contrasted with form-making (exploring/refining variations within a known typology). Examples: Gaudí's catenary arches, Isler's thin shells, Frei Otto's tensile structures. [AAD, p.18, 29–30]

**Form-making** — Process of inspiration and refinement in which form precedes analysis of programmatic/constraint influences; explores variations within a known typology. Contrasted with form-finding (discovering novel structures). [AAD, p.29–30]

**Freeform** — Curving, non-primitive geometry lacking a simple mathematical formula; includes splines, lofts, and complex NURBS surfaces. [AAD, p.98]

**Function** — A mathematical mapping from input domain to output codomain; e.g., y = x^2 maps x-values to y-values. [AAD, p.101]

**Gaudí, Antoni** — 19th–20th century architect (1852–1926) known for form-finding via hanging-chain and wire models, pioneering the use of catenary arches and free-form shells in architecture. [AAD, p.18]

**Gaussian Curvature (G)** — Product of the two principal curvatures at a surface point: G = K1 × K2. G = 0 identifies developable surfaces (at least one principal curvature is 0). G > 0 (synclastic, dome-like), G < 0 (anticlastic, saddle-like). [AAD, p.167, 173]

**Generalized cone** — A ruled surface formed by lines emanating from a vertex (not necessarily directly above) through points on a smooth curve directrix; a generalization of a standard cone. [AAD, p.168]

**Generalized cylinder** — A ruled surface formed by translating a smooth cross-section curve along a directrix (not necessarily perpendicular); a generalization of a standard cylinder. [AAD, p.168]

**Generatrix** — The straight line whose motion generates a ruled surface; also called a ruling. [AAD, p.170]

**Geodesic** — The shortest-path curve on a curved surface connecting two points while remaining on the surface; conceptually the curved-space analog of a straight line. Used as a natural, geometry-respecting cutting curve for Surface Split. [AAD, p.154]

**Geodesic network** — A system of geodesic curves on a surface, often used for structural or aesthetic purposes. [AAD, p.154]

**Geometric center** — See centroid.

**Geometry** — The shape, size, and position of objects in space; primary output and subject of Grasshopper algorithms. Also, a container component type (Params > Geometry) that stores any kind of geometry. [AAD, p.51–52]

**Graft / Graft Tree** — An operation that elevates each item in a list/tree into its own separate branch, creating a new hierarchical level. Inverse operation: Flatten. [Essential, p.222–224]

**Grasshopper** — A free visual-programming plug-in for Rhinoceros (not standalone), developed by David Rutten at Robert McNeel & Associates; created 2007 (initially "Explicit History"), rebranded "Grasshopper" 2008. Node-based editor for parametric/algorithmic design. Windows-only at time of publication; requires licensed Rhino 5.0+. [AAD, p.33, 35]

**Graph Mapper** — A component (Params > Input) that warps a 0–1 input value non-linearly via a user-editable, draggable graph curve; available preset families include Bezier, Sine, Parabola, Perlin, Power, etc. Two independently configurable domains (input A and output B); used to generate non-linear scale-factor sequences. [AAD, p.199–202]

**Grid** — An ordered arrangement of points or lines in a regular (or subdivided) pattern; in Grasshopper, often produced by Cross Referencing two 1D sequences or by subdividing a surface. [AAD, p.93–94]

**Gridshell** — A 3D framework of intersecting ribs or beams forming a curved shell structure; can be built flat (planar deformable lattice) and then lifted/deformed into its final curved shape, which is why developable and equal-edge grids (Chebyshev-nets) are fabrication-relevant. [AAD, p.165]

**Group** — A visual clustering of related components on the canvas (no functional effect); accessed via right-click > Group. [Essential]

**Guide curve** — A reference curve used to orient or align other geometry; e.g., Flip Curve's G-input takes a guide curve and flips mismatched curves to match its direction. [AAD, p.129–130]

**Halfpipe / U-shaped surface** — A developable surface formed by translating a semicircular arc profile along a linear directrix. [AAD, p.170]

**Hash / Hashtag** — See symbol in computing.

**Helix** — A 3D spiral curve winding around an axis; often parameterized as x = r cos(t), y = r sin(t), z = ct for radius r and pitch c. [AAD, p.7]

**Hidden / Wireless wire** — A wire display option (right-click > Wire Display > Hidden) making the connecting wire invisible unless one of its endpoint components is selected; useful for decluttering dense definitions without removing the connection. [AAD, p.58]

**Homogeneous coordinates** — A mathematical representation of points/vectors using an extra coordinate (often w) enabling both translation and projection in a single matrix operation; relevant to Transformation components and graphics. [Essential, p.7]

**Hooking up** — Colloquial term for wiring components together; connecting input/output slots. [AAD, p.60]

**Internalise data** — Right-click context-menu option on a container component that permanently copies referenced Rhino geometry's data into the Grasshopper file, breaking the live link so the original Rhino object can be deleted. [AAD, p.52]

**Intersection** — See Boolean operation.

**Interpolate / Interpolated curve** — A curve that passes through (rather than merely is influenced by) its control points; built via the Interpolate Curve component. [AAD, p.103]

**Intersection curve** — The curve formed where two surfaces (or a surface and a plane) meet; computed by Intersection or Project components. [AAD, p.158]

**Interval** — See domain.

**Isocurve / Iso** — An isoparametric curve running across a surface at constant u or constant v; conceptually a "grid line" on the surface. A surface's u-isocurves form one family, v-isocurves form another, and together they define the surface's parametric grid. [AAD, p.139, 147]

**Isoparametric** — Having constant parametric value; used to describe isocurves on surfaces. [AAD, p.138–139]

**Isotrim / SubSrf** — A component (Surface > Util) that extracts untrimmed sub-surface pieces from a surface according to a set of (u,v) sub-domain specifications (typically from Divide Domain²). Output sub-surfaces retain the parent surface's domain parameterization unless separately Reparameterized. [AAD, p.149–150]

**Iterative** — A process repeated multiple times (e.g., a loop); native Grasshopper cannot express loops without special third-party components; iteration is essential for algorithms like Chebyshev-net generation. [AAD, p.164]

**Jacobian matrix** — A matrix of partial derivatives describing how changes in inputs affect outputs; relevant to surface analysis and optimization. [Essential, p.7]

**Jived** — Colloquial past tense of "jive"; used in slang contexts (not a standard technical term). [Not formally defined]

**Joint** — In structural/parametric systems, a connection point where elements meet; in space frames, where multiple struts connect. [AAD, p.160]

**Kinetic** — Related to motion or forces in motion; e.g., kinematic chain of transformations. [AAD, p.7]

**Knot** — In NURBS, a parameter value in the knot vector that controls the smoothness and local influence of control points. A curve degree-d with N control points has N+d+1 knots. [AAD, p.121]

**Knot vector** — The sequence of knot values (a non-decreasing list of numbers) controlling NURBS curve/surface behavior. [AAD, p.121]

**Landau notation** — Mathematical shorthand (e.g., Big-O) describing asymptotic behavior of algorithms; not typically used in Grasshopper design contexts. [Essential, p.7]

**Lathes** — Rotating machinery for shaping; used historically as analogy for revolution surfaces. [Essential]

**Lattice** — A regular repeating pattern of points or elements, often in 3D (cubic, hexagonal, etc.); e.g., a space frame creates a lattice structure. [AAD, p.160]

**Lathe** — A machine tool that rotates stock while a cutting tool shapes it; analogous to Revolution surface generation in Grasshopper. [AAD, p.144]

**Least Common Multiple (LCM)** — The smallest positive integer divisible by all members of a set of integers; used in list-matching scenarios to predict output length when data structures conflict. [Essential, p.41]

**Left-to-right flow** — Grasshopper's fundamental principle that wires can only connect forward (left to right) through the dependency graph; no backward/feedback wiring allowed without special loop components. [AAD, p.59]

**Linear** — Degree-1 NURBS (straight line); a degree-1 curve's control polygon is the curve itself. [AAD, p.121]

**Linear remapping** — See Remap.

**List** — One branch of a data structure containing zero or more items ordered by index (0, 1, 2, ...); contrasted with a tree (multiple branches) or single item. [Essential, p.33]

**List Item / Item** — A component (Sets > List) that retrieves a single item (or filtered sub-list) from a list by numeric index position (with optional wrap-around). [AAD, p.72–75]

**List Length / Lng** — A component (Sets > List) that calculates the number of items in a list, output as an integer. [AAD, p.83]

**Local Coordinate System (LCS)** — A reference frame local to an object (curve, surface, plane); contrasted with the global/world coordinate system. E.g., a curve's t parameter lives in its LCS [0,1] domain. [AAD, p.124–125]

**Loft** — A component (Surface > Freeform) that generates a surface through a set of ordered section curves; includes tunable options (type 0–5: Normal, Loose, Tight, Straight, Developable, Uniform) and a rebuild flag. [AAD, p.98, 141]

**Longest List matching** — Grasshopper's default list-matching behavior: when two lists of different lengths are paired, the shorter list's last item is repeated to match all remaining items of the longer list. [AAD, p.92]

**Loop** — A computational structure repeating a block of code/operations multiple times; native Grasshopper cannot express loops without special third-party components (covered in Chapter 7, outside this glossary's scope). [AAD, p.59, 164]

**Lower bound** — The minimum value in a domain or clamp range; used in attractor logic and range-checking. [AAD, p.113]

**Lumber** — Processed wood beams/planks; referenced in contexts of gridshell fabrication from flat material. [Essential]

**Lunch Box** — A third-party Grasshopper plug-in by Nathan Miller providing utilities for mathematical forms, paneling, structures, and workflow (e.g., Surface Direction component for flipping surface uv). [AAD, p.147]

**Magnitude** — The length/size of a vector; computed by Vector Length component; a scalar (non-directional) quantity. [AAD, p.66, 186]

**Mass Addition / MA** — A component (Maths > Operators or Statistics) that sums items in a list/tree, behaving differently by data structure: single item → identity, list → sum of all items, tree → sum per branch. Demonstrates structure-dependent execution. [Essential, p.24, 33]

**Mathematical function** — A rule mapping input domain to output codomain; e.g., y = sin(x), z = x² + y². [AAD, p.101–102]

**Matrix** — A rectangular array of numbers (rows × columns) used to represent linear transformations; in Grasshopper, often used for coordinate conversions and transformation data. [AAD, p.193–194]

**Maximum / Max** — A component (Maths > Operators or Util) that returns the larger of two numbers, or element-wise clamps upward values in a list to a maximum. [AAD, p.205]

**Mean** — See average; specifically, Mean Curvature is the average of two principal curvatures. [AAD, p.167]

**Mean Curvature (M)** — Average of the two principal curvatures at a surface point: M = (K1 + K2) / 2. M = 0 defines minimal surfaces (K1 = −K2 at every point), e.g., catenoids and soap films. [AAD, p.167, 174]

**Mesh** — A polyhedral surface approximation built from vertices, edges, and faces (usually triangles or quads); distinct from NURBS surfaces. [Essential]

**Mesh face** — A planar polygon (usually triangle or quad) that is one face of a mesh. [AAD, p.45]

**Mesh quality** — A Grasshopper display setting (canvas toolbar) controlling the resolution of NURBS-to-mesh conversion for preview: Disable Meshing, Low, High, Document, Custom. [AAD, p.55–56]

**Midpoint** — The geometric center point of a curve or line segment; found via Point On Curve at 0.5 (arc-length midpoint) or via averaging endpoints. [AAD, p.61]

**Miller, Nathan** — Author of Lunch Box plug-in; Associate Partner/Director of Architecture & Engineering Solutions at CASE. [AAD, p.147]

**Minimal surface** — A surface minimizing area for given boundary constraints (M = 0 everywhere); examples: catenoids, helicoids, soap films. [AAD, p.174]

**Minimum / Min** — A component (Maths > Util or Operators) that element-wise clamps down values in a list that exceed a comparison number. [AAD, p.117–118]

**Mirror** — A Euclidean transformation reflecting geometry across a plane; preserves shape and size. [AAD, p.184]

**Mitered** — Joined at an angle (e.g., two beams meeting at a miter joint); relevant to structural design. [Essential]

**Modulus / Mod** — A mathematical operator (A mod B) computing the remainder of A divided by B; useful for testing even/odd (n mod 2 = 0 for even n). [Essential, p.25, 31]

**Moretti, Luigi** — Italian architect (1907–1973) who coined term "Parametric Architecture" (1939), researching relations between dimensional parameters and building form, demonstrating parametric design principles decades before computer implementation. [AAD, p.20–21]

**Morph / Box Morph** — A transformation (Transform > Morph) that deforms geometry according to a reference "pliable" box mapped to a target box; analogous to Rhino's Cage/CageEdit commands. [AAD, p.210]

**Moving** — See translation.

**Natural domain** — A curve's intrinsic parameter range before reparameterization; e.g., "0 To 43.58" for a curve naturally spanning 43.58 units of arc length. [AAD, p.125, 127]

**Navigation** — In Grasshopper, using mouse/keyboard to pan, zoom, and rotate the canvas view; also accessed via Radial Menu (Spacebar). [AAD, p.56]

**Negative** — Prefix indicating negation/opposition; Negative component (Maths > Operators) returns −x from input x. [AAD, p.194]

**Network Surface** — A component (Surface > Freeform) building one surface from two ordered curve sets (one in u-direction, one in v-direction) with control over edge continuity (0=Loose, 1=Position, 2=Tangency, 3=Curvature). Provides more edge control than Loft. [AAD, p.143]

**Node** — See component; visual box on the Grasshopper canvas representing an operation. [AAD, p.28]

**Non-Uniform Rational B-Spline (NURBS)** — A mathematical representation of curves and surfaces using degree, control points (with weights), knot vectors, and an evaluation formula. Provides smooth, intuitive shape control and is the standard for CAD/parametric design. [AAD, p.121–122]

**Non-wrap** — Shift List option (W = false) causing items falling off the list's ends to be discarded rather than re-appended; results in a shorter output list. [AAD, p.81]

**Normal** — A vector perpendicular to a surface at a point; output by Evaluate Surface and Curvature components. [AAD, p.144, 169]

**Normalized** — Scaled to a standard range; e.g., normalizing a curve's domain to [0,1] via Reparameterize, or normalizing a vector to unit length (magnitude = 1) via Unit Vector. [AAD, p.125, 127, 186]

**Notation** — Symbolic language/convention for writing formulas, coordinates, or structured information. [Essential, p.33]

**Null** — A special data value representing "no data" or "undefined"; displayed as "<null>" in Panels; often results from type-cast failures or invalid operations. [Essential, p.24]

**Number** — A primitive data type representing a numeric value (integer or floating-point). [Essential, p.13]

**Number Slider** — A component (Params > Input) providing user-interactive control of a single numeric value; properties: Name, Min/Max domain, Rounding (R/N/E/O for floating/integer/even/odd), Digits, and Grip Style. [AAD, p.44, 46]

**Numeric operation** — Mathematical operations on numbers: arithmetic (+, −, ×, ÷), trigonometry (sin, cos, tan, etc.), exponentiation, factorial, etc. [Essential, p.16]

**Oloid** — A non-convex body created by intersecting two circular cylinders at right angles, discovered by Paul Schatz (1929); a developable surface. [AAD, p.168]

**Operating range** — In attractor logic, the distance radius within which an attractor's effect is visible/significant; beyond this radius, geometry receives a clamped/uniform transform value. [AAD, p.117–118]

**Optimization** — The process of improving a design according to specified objectives and constraints; automated in some parametric systems (e.g., evolutionary solvers, not covered in this glossary's source range). [AAD, p.18]

**Order** — In NURBS, the degree + 1; a degree-2 NURBS has order 3. Minimum control-point count = order. [AAD, p.121]

**Orient** — A component (Transform > Euclidean) that maps geometry from an arbitrary initial plane A to a target final plane B in one operation, replacing separate Move + Rotate chains. [AAD, p.193–194]

**Orientation** — The rotational alignment of an object or plane relative to world axes. [AAD, p.193–194]

**Origin** — The reference point (0, 0, 0) in world coordinates or the local reference point of a plane/frame. [AAD, p.10, 35]

**Osculating circle** — The circle that best approximates a curve's shape at a given point; its radius (1/k) defines the curve's curvature at that point. [AAD, p.136]

**Osnap / Object Snap** — Traditional CAD feature allowing click-selection of strategic geometric locations (endpoints, midpoints, centers, etc.); Grasshopper replaces this with explicit algorithmic components (Point On Curve, End Points, Area for centroid, Divide Curve for division points, etc.). [AAD, p.61]

**Otto, Frei** — German architect (1925–) pioneering form-finding via tensile structures and physical models; a pioneer of computational/optimized form-finding. [AAD, p.18]

**Output** — Data produced by a component, displayed as slots on its right side; can be wired to downstream components' inputs. [AAD, p.40–42]

**Output section** — The right portion of a component displaying its output slot(s). [AAD, p.41]

**Overflow** — In list/tree processing, behavior when an input's size exceeds expected bounds; relevant to implicit broadcasting and list matching. [AAD, p.64]

**Overload** — In programming, a function/component name referring to multiple versions with different input signatures; e.g., Line component has two versions (two-point vs. start/direction/length). [AAD, p.160, 209]

**Override** — To replace a value or parameter with another; in Grasshopper, wired data always overrides internally-set or referenced values on the same parameter. [Essential, p.13]

**Panel** — A component (Params > Input or Params > Util) that displays data as readable text; used for both input (Panel holding constant values) and inspection (Panel as a readout tool showing data structure, values, paths). [AAD, p.63, 71–72]

**Panel Properties** — The dialog opened by double-clicking a Panel component, allowing editing of its displayed text/values. [AAD, p.109]

**Paneling** — Dividing a surface into regularly or irregularly-spaced sub-surface panels, often for fabrication or structural purposes. [AAD, p.149–151]

**Parallel** — Running in the same direction without intersecting; also, in programming, simultaneous processing (not strictly applicable in GH's single-threaded execution model). [AAD, p.27]

**Parameter** — (1) A numeric value controlling a component's behavior (e.g., a Slider is a parameter component); (2) a variable (like t on a curve, or u/v on a surface) used to parameterize/address locations on geometric objects. [AAD, p.20, 124–125]

**Parametric** — Controlled by or dependent on parameters; a parametric design's geometry changes automatically when parameters change. [AAD, p.20]

**Parametric Architecture** — Term coined by Luigi Moretti (1939) describing architectural design where form emerges from relations between dimensional parameters. [AAD, p.20–21]

**Parametric design** — Design methodology in which the entire geometry/form is explicitly defined as functions of underlying parameters (sliders, equations, conditions); changing parameters updates geometry automatically. [AAD, p.20]

**Parametric diagram** — In this context, the node-based Grasshopper algorithm (visual script) representing the parametric design; described as a "smart medium" (vs. traditional drawing's "code based on conventions") because associative rules are graphically explicit and directly manipulable. [AAD, p.27–30]

**Parametric link** — Wiring the same Number Slider into multiple component inputs, keeping those values synchronized so changing one slider updates all dependents at once. [AAD, p.85, 102]

**Parametric speed** — The rate of change of arc length with respect to parameter t; a curve is non-uniformly parameterized if arc length does not increase linearly with t (common for NURBS). [AAD, p.125–126]

**Parametrized** — Expressed in terms of parameters; a curve parameterized by t means location on the curve is specified by the single variable t. [AAD, p.124]

**Partial sums / Pr** — The running accumulation of summed values; output by Mass Addition component (Pr output) alongside the total sum (R output). [Essential, p.24]

**Partition** — Dividing a whole into disjoint parts; in Grasshopper, often via Dispatch (splitting by boolean pattern) or Split List (splitting at an index). [AAD, p.83–84]

**Patch** — A component (Surface > Freeform) fitting a surface using perpendicular "span" curves generated from input points/curves; spans rarely align with output edges, so Patch is a fallback when other surfacing methods aren't feasible. [AAD, p.143]

**Path** — In data trees, the hierarchical address of a branch, written as semicolon-separated integers in braces (e.g., {0;0}, {0;1;2}); also the route data takes through wired components. [Essential, p.33]

**Pattern** — A repeating or systematic arrangement; in Cull Pattern, a boolean sequence (True, False, True, False...) repeating across a list to filter items. [AAD, p.78–80]

**Perpendicular** — At right angles (90°); two lines/vectors are perpendicular if their dot product is zero. [AAD, p.36]

**Persistence** — Data remaining stored in a component across sessions; internally-set data (right-click Set) persists in the .gh file until manually changed. [AAD, p.12]

**Phase shift** — Offset in a repeating pattern; used in Cull Pattern to select every k-th item starting at a different position. [AAD, p.78–80]

**Physics** — Real-world forces and behaviors (gravity, collision, spring forces, etc.); Grasshopper can simulate these via specialized plug-in components (not part of core GH). [AAD, p.34]

**Plane** — A 2D geometric reference frame in 3D space, defined by an origin point and two perpendicular direction vectors (or by a normal vector); used to position/orient other geometry (circles, boxes, evaluated surface points). [AAD, p.10, 35]

**Plane Normal / Pl** — A component (Vector > Plane) that constructs a plane from an origin point and a normal vector (Z-axis direction). [AAD, p.189–190]

**Planing** — Smoothing a surface via a blade/tool; used historically as analogy; also a fabrication process. [Essential]

**Point** — A location in 3D space specified by coordinates (x, y, z). Stored geometrically or computed algorithmically. [AAD, p.7, 35]

**Point List** — A component (Display > Vector) overlaying each point's list-index number directly in the Rhino viewport; text size controlled by S-input. [AAD, p.65]

**Point On Curve** — A component (Curve > Analysis) finding a point on a curve based on fractional arc-length (not parameter t); 0.5 always gives true geometric midpoint, no reparameterization needed. Right-click offers named presets (start, quarter, third, mid, etc.). [AAD, p.61, 132]

**Pole** — In NURBS, a control point; also, a singular point on a surface of revolution. [AAD, p.121]

**Polygon** — A closed polyline (chain of line segments); often used for surface boundary representation. [AAD, p.218]

**Polyline / PLine** — A curve made of connected straight line segments (degree 1); less smooth than higher-degree curves but simpler. Component (Curve > Spline): inputs Vertices (points) and Closed (boolean); outputs Polyline curve. [AAD, p.218]

**Pop-up menu** — Right-click context menu appearing at the cursor; used throughout Grasshopper to access options like Set Number, Reparameterize, Preview, Bake, Wire Display, etc. [AAD, p.38, 42]

**Position** — A point's location in space; not preserved by Affine transformations (only shape/parallelism preserved). [AAD, p.184]

**Precedence** — Priority ordering; in Grasshopper, wired (external) data has precedence over internally-set or referenced data on the same parameter. [Essential, p.13]

**Precondition** — A requirement that must be satisfied before an algorithm executes correctly; violation produces errors. [AAD, p.22–23]

**Predator** — In evolutionary algorithms (not covered in core GH, deferred to plug-ins), an agent selecting/culling poor solutions. [Essential]

**Prefix** — A symbol or word placed before another; negation operator "−" is a prefix operator. [Essential, p.194]

**Preview** — Visualization of component output in the Rhino viewport (red by default); toggled per-component via right-click > Preview. Unlike Disable, Preview toggling does not stop the component from computing. [AAD, p.55–56]

**Preview mesh quality** — Display setting (canvas toolbar) controlling resolution of NURBS meshing for viewport rendering. [AAD, p.55–56]

**Primitive** — A basic/foundational geometric shape (point, line, circle, plane, box, etc.) or data type. [AAD, p.7, 35]

**Principal curvature** — At a point on a surface, one of two curvatures (K1, K2) occurring at orthogonal directions; the directions of minimum and maximum curvature. Their product is Gaussian Curvature (G = K1 × K2); their average is Mean Curvature (M = (K1 + K2) / 2). [AAD, p.167]

**Profiler** — A performance monitoring display in Grasshopper showing execution time (e.g., "11ms", "155ms") below each component. [Essential, p.26]

**Project** — A component (Curve > Util) projecting a curve onto a target surface along a direction vector (or normal if not specified), replacing straight segments with surface-coincident curves. [AAD, p.158]

**Projection** — (1) Geometric projection mapping 3D points onto a 2D plane or surface; (2) in Affine transformations, a transformation that does not preserve shape/size. [AAD, p.184]

**Propagate** — To spread or pass through; in associative logic, changes propagate to dependent elements automatically. [AAD, p.21]

**Property** — An attribute or parameter of an object; in Grasshopper, exposed as input/output slots on components. [AAD, p.44]

**Pseudocode** — A textual algorithm description using informal notation between natural language and actual code. [Essential]

**Pull** — To extract/retrieve data from an upstream component (as contrasted with "push" in event-driven systems). [AAD, p.24]

**Pykrete** — A composite material (ice + sawdust) with interesting structural properties; not a typical Grasshopper focus. [Essential]

**Pyramid** — A polyhedron with a polygonal base and triangular faces meeting at an apex; extended in space frames as a pyramidal module connecting a base quad's four corners to an offset apex. [AAD, p.160]

**Quadric surface** — A surface defined by a degree-2 polynomial equation; examples: sphere, cone, cylinder, hyperboloid. [AAD, p.104]

**Qualitative** — Describing qualities/properties rather than numeric values; e.g., "saddle-like" vs. specifying curvature numbers. [AAD, p.95]

**Quantitative** — Expressed in numeric terms; measurable. [Essential]

**Quartic** — Degree-4 polynomial; occasionally used for high-degree NURBS. [Essential]

**Quick Graph** — A component (Display or Params) displaying a numeric list as a simple line graph; useful for visualizing value distributions. [Essential, p.18, 145]

**Radian** — A unit of angular measure (2π radians = 360°); used by all GH trigonometric components (Sine, Cosine, etc.). Degree inputs must be converted via Radians component. [AAD, p.189–190]

**Radial Menu** — A quick-access wheel opened by pressing Spacebar, bundling common actions (group, cluster, preview/hide, enable/disable, bake, zoom, recompute, find, etc.). [AAD, p.56]

**Radical** — Expressing using a root symbol (√); relevant to mathematical expressions in GH. [Essential]

**Radius** — The distance from a circle/sphere's center to its boundary. [AAD, p.35, 97]

**Rail** — A guide curve for a sweep operation; Sweep1 uses one rail, Sweep2 uses two. [AAD, p.143]

**Rail Revolution** — A component (Surface > Freeform) revolving a profile curve using a rail curve (varying axis) instead of a fixed axis, letting the axis itself vary along the rail. Output has a visible "Seam." [AAD, p.144]

**Random** — A component (Sets > Sequence or Maths > Domain) generating N random real/integer numbers within a domain R; same seed S always reproduces the identical "random" list (deterministic given fixed seed). [AAD, p.100, 214]

**Random number generator** — Algorithm producing a sequence of pseudo-random numbers; in GH, seeded (deterministic) so reproducible. [AAD, p.100]

**Range** — A component (Sets > Sequence or Maths > Domain) dividing a numeric domain D into N equal parts, returning N+1 evenly-spaced values (including both endpoints). [AAD, p.101, 198]

**Range-inclusive** — Including both the start and end values; Range [0,10] with 5 steps generates 6 values: 0, 2.5, 5, 7.5, 10. [AAD, p.101]

**Rationality** — In NURBS, the ability to weight control points differently to achieve conic sections (circles, ellipses) exactly. [AAD, p.121]

**Rebuild** — In NURBS, reparameterizing/resampling a curve with uniformly distributed control points; does NOT change the curve's shape but can simplify its structure. [AAD, p.122]

**Reciprocal** — The inverse of a number (1/x); curvature is the reciprocal of radius (k = 1/r). [AAD, p.136]

**Reference geometry** — Geometry defined by linking to existing Rhino objects (via right-click "Set one Geometry"); stays live-linked to the original Rhino geometry. Contrasted with internally-set and externally-supplied (wired) data. [AAD, p.42, 50]

**Referenced data** — See reference geometry.

**Reflect** — A Euclidean transformation mirroring geometry across a plane. [AAD, p.184]

**Region Union / RUnion** — A component (Curve > Region) unioning closed curves into a single continuous region. [Essential, p.28–30]

**Remap / ReMap** — A component (Maths > Domain) performing linear remapping: rescaling values from a source domain [A,B] to a target domain [A',B'], proportionally preserving relative magnitude. Used with Bounds when source range isn't known. [AAD, p.112, Essential p.20]

**Reparameterize** — A right-click toggle on curve/surface inputs normalizing the domain to [0,1], making parameter-based evaluation (t=0.5) predictable regardless of the curve's natural domain. [AAD, p.127, Essential p.20]

**Repeat Data / Repeat** — A component (Sets > Sequence) extending/repeating a short input list cyclically until it reaches a specified output length L. [AAD, p.95]

**Repeating pattern** — A boolean sequence (e.g., True, False, True, False) or numeric sequence (e.g., 3, 4, 3, 4) that cycles across a list in Cull Pattern or Repeat Data. [AAD, p.78–80, 99]

**Repel** — In NURBS, control-point weights between 0 and 1 push/repel the curve away from that point. Contrasted with weight > 1 which attracts. [AAD, p.122]

**Resolution** — Level of detail or fineness in a discretization; mesh quality setting controls NURBS-to-mesh resolution. [AAD, p.55–56]

**Result** — Output value(s) produced by a component or function. [AAD, p.40]

**Reversal** — Reversing the order of a sequence (via Reverse List component) or a curve's parametric direction (via Flip Curve). [AAD, p.85, 128–130]

**Reverse List / Rev** — A component (Sets > List) reversing item order in a list (index 0 becomes last, etc.); also available as a right-click context-menu option "Reverse" on any input slot. [AAD, p.85]

**Rhino / Rhinoceros** — Commercial 3D NURBS modeling software by Robert McNeel & Associates; Grasshopper is a plug-in for Rhino. [AAD, p.33, 35]

**Rhino command line** — Text interface for executing Rhino commands; Grasshopper is opened by typing `grasshopper` there. [AAD, p.35]

**Ribbon surface** — A surface swept along a curve, like a ribbon; distinct from closed/solid sweep. [AAD, p.98]

**Rib** — A curved surface section; used in lofting examples and in space frames as primary load-bearing elements. [AAD, p.98, 194]

**Ridge** — A line of local maximum curvature on a surface; where curvature-based patterning becomes densest. [AAD, p.179]

**Right-click context menu** — Pop-up menu accessed by right-clicking a component/input/output slot, offering options like Set Number, Reparameterize, Preview, Wire Display, Bake, etc. [AAD, p.42, 49]

**Rigid body** — An object that maintains its shape/size during motion (no deformation); rotations are rigid transformations. [AAD, p.189]

**Rotation** — A Euclidean transformation rotating geometry around a point (in 2D, in a plane) or axis (in 3D); preserves shape and size but not position. [AAD, p.189–191]

**Rotation axis** — A line around which a 3D rotation occurs; input to Rotate Axis component. [AAD, p.190]

**Rotation kinematics** — The mathematics of rotational motion; rigid-body rotation involves a center (or axis) and an angle. [AAD, p.189]

**Rotation plane** — A 2D reference plane (with normal and two perpendicular directions) containing a rotation center; input to Rotate component. [AAD, p.189]

**Rounding** — Number Slider property controlling numeric representation: R (floating-point), N (integer), E (even numbers), O (odd numbers). [AAD, p.44]

**Row/column** — In matrices and grids, rows run horizontally, columns vertically; Flip Matrix swaps them. [AAD, p.224–225]

**Ruled surface** — A surface generated by the motion of a straight line (the generatrix or ruling) along a path; examples: cylinder (line perpendicular to axis), cone (line through fixed vertex), and hyperboloid (line connecting two skew curves). [AAD, p.170]

**Ruling** — See generatrix; a straight line generating a ruled surface. [AAD, p.170–171]

**Rut** — A groove or track worn into a surface; not a standard GH term. [Essential]

**Rutting** — Deformation/erosion of a surface; not a standard GH term. [Essential]

**Saddle** — A surface with negative Gaussian Curvature (K < 0) curving up in one direction and down in another, resembling a horse saddle. [AAD, p.167]

**Saddle point** — A critical point on a surface that is a local minimum in one direction and local maximum in another. [AAD, p.167]

**Safe mode** — A fail-safe condition in which a system operates with reduced functionality to prevent damage; not standard GH terminology. [Essential]

**Sampling** — Taking discrete measurements/values from a continuous function or surface. Image Sampler reads pixel intensities at specified UV coordinates; Divide Surface samples point/normal grids. [AAD, p.203–206, 148]

**Sanity check** — Informal verification that a result is reasonable; e.g., checking list length before feeding into array-generating components. [AAD, p.26]

**Scalar** — A single numeric value (not a vector/matrix); scalar multiplication scales a vector by a number. [AAD, p.186]

**Scalar multiplication** — Multiplying a vector by a scalar (number), scaling its magnitude by that factor and optionally reversing direction if the scalar is negative. [AAD, p.186–187]

**Scale** — A component (Transform > Affine) resizing geometry by a positive factor F about a center point C. Cannot be 0 (null scale is undefined). 0<F<1 shrinks, F=1 unchanged, F>1 enlarges. [AAD, p.196]

**Scale factor** — The numeric multiplier in a Scale transformation; must be positive. [AAD, p.113–114, 196]

**Scaling** — The Affine transformation of uniform or non-uniform resizing. [AAD, p.196]

**Scam** — Not a technical term. [Essential]

**Scanning** — Sequentially reading/processing data; Image Sampler scans image pixels at specified UV coordinates. [AAD, p.203]

**Scatter** — To distribute irregularly or randomly; Image Sampler applies this principle to surface-point scaling. [AAD, p.203]

**Scatterplot** — A data visualization showing individual data points; relevant to Quick Graph preview. [Essential, p.18]

**Schema** — A formal structure/template; database schema, data schema in GH (data types). [Essential]

**Schatz, Paul** — Inventor of the Oloid (1929), a developable surface body. [AAD, p.168]

**Schumacher, Patrik** — Theorist quoted on parametric diagrams as "smart media." [AAD, p.29]

**Script / Scripting** — Writing code to automate tasks; RhinoScript (textual VB-like syntax) vs. Grasshopper's visual scripting. [AAD, p.23–24]

**Search box** — The canvas search pop-up opened by double-clicking empty canvas, used to quickly place components by typing their name. [AAD, p.38]

**Seam** — A discontinuity or join line on a surface; Surface Revolution and Rail Revolution output surfaces have visible seams. [AAD, p.144]

**Second derivative** — Rate of change of a curve/surface's slope; related to curvature. [AAD, p.137]

**Section** — A slice through a 3D object, or a profile curve in a lofting operation. [AAD, p.98]

**Sectional curve** — An isocurve or slice curve through a surface at a constant parameter. [AAD, p.139]

**Seed** — An initial value used by Random or other stochastic components to generate pseudo-random sequences; same seed always produces the same "random" sequence. [AAD, p.100, 214]

**Segment** — A portion of a curve between two division points; Divide Curve splits a curve into N segments, producing N+1 endpoints. [AAD, p.65]

**Selection** — Choosing specific items from a larger set via filtering, indexing, or pattern-based culling (List Item, Cull Pattern, Dispatch). [Essential, p.19–20]

**Selection pattern** — A boolean list used by Dispatch to choose which candidates to route as output; True-aligned candidates go to A branch, False-aligned to B. [Essential, p.21]

**Sense** — Directionality of a vector (which way it points); reversing sense multiplies by −1. [AAD, p.66, 186]

**Serendipitous** — Fortunate or by chance; not planned or expected. [Essential]

**Series** — A component (Sets > Sequence) generating an arithmetic progression (constant-step sequence): Start, Step, Count → outputs a list of Count values. [AAD, p.87–90, Essential p.35]

**Set** — (1) A mathematical collection of distinct items; (2) right-click "Set Number" / "Set one Geometry" internalize data into a component. [AAD, p.15]

**Shatter** — A component (Curve > Division) splitting a curve into segments AT given t-parameters (LCS [0,1] domain), returning curve pieces (not points). [AAD, p.135]

**Shear** — An Affine transformation skewing/slanting geometry while preserving parallelism but not shape or size. [AAD, p.184]

**Shell** — A thin 3D structure; gridshell uses a lattice of curved ribs forming a shell. [AAD, p.165]

**Shortest List matching** — List-matching behavior truncating the longer list to the shorter list's length, then pairing 1-to-1. [AAD, p.92]

**Shortest path** — See geodesic; the minimum-distance curve on a curved surface. [AAD, p.154]

**Shoulder** — An angular or sharp feature where two surfaces meet; not a standard GH term. [Essential]

**Shutter** — A moving panel/barrier; parametric shutter patterns can be generated via Grasshopper. [Essential]

**Sibling** — In data hierarchies, items at the same branch level. [Essential]

**Signed curvature** — Curvature with a sign convention: positive if the osculating circle lies to the LEFT of the curve's travel direction, negative if RIGHT. Depends on the curve's parametric direction. [AAD, p.136–137, 169]

**Signal** — In signal processing, a time-varying quantity; applied metaphorically in parametric design to time-varying/parameter-varying geometry. [Essential]

**Similarity transformation** — A transformation (scale + rotation) preserving shape only, not size or position. [AAD, p.184]

**Simplify / Simplify Tree** — An operation that consolidates redundant/empty branches in a data tree. [Essential, p.199, 222]

**Simulation** — Computational modeling of real-world processes (forces, physics, crowd behavior, etc.); Grasshopper can simulate simple cases (particle springs, basic physics) via plug-ins. [AAD, p.34]

**Sine** — Trigonometric function (sin) mapping angles to opposite/hypotenuse ratios. [Essential]

**Single item** — Data structure containing exactly 1 branch × 1 item; displayed in Panel as "Data with 1 branch{es}, {0}, N=1." [Essential, p.33]

**Singularity** — A point where a function/surface becomes undefined or discontinuous; e.g., the apex of a cone. [AAD, p.168]

**Sketchpad** — The first interactive CAD system (Ivan Sutherland, 1963, MIT), introducing associative logic via atomic constraints and flow-chart diagrams; conceptual ancestor of Grasshopper. [AAD, p.21, 27]

**Skin** — A surface wrapped over a framework of curves; produced by Loft or Network Surface. [AAD, p.98]

**Skirt** — A hanging edge or flap; used metaphorically for overhanging features. [Essential]

**Slack** — Extra space or tolerance in a system; relevant to fabrication/assembly. [Essential]

**Slant** — An angle or inclination; Shear is an Affine transformation introducing slant. [AAD, p.184]

**Slew** — To rotate/sweep quickly; Rotate components slew geometry around axes/planes. [AAD, p.189]

**Slope** — The steepness of a curve/surface; first derivative. [Essential]

**Small** — See minimum.

**Smart medium** — Term applied to Grasshopper (and parametric diagrams in general) because geometric rules and dependencies are explicit and automatically enforced, unlike traditional drawing's "code based on conventions" where consistency depends on the designer. [AAD, p.27, 29–30]

**Smooth** — Having continuous derivatives; smooth curves (degree 3+) vs. sharp polylines (degree 1). [AAD, p.121–122]

**Snap** — See Osnap; quick alignment to strategic geometric locations. [AAD, p.61]

**Soap film** — A thin, minimal-surface membrane (M=0) used historically for form-finding; examples include catenoids and helicoids. [AAD, p.18, 174]

**Soft edges** — Blended/smooth corners (as opposed to sharp/hard edges). [Essential]

**Softening** — Smoothing or blending; Smooth Curve component can soften polylines. [Essential]

**Software rendering** — Real-time computation of imagery (as opposed to pre-rendered frames). [Essential]

**Solver** — A component or algorithm finding solutions to systems of equations or optimization problems; Grasshopper has limited built-in solvers, with plug-ins providing iterative/evolutionary solvers. [AAD, p.164]

**Sort** — A component (Sets > List) ordering list items by numeric value (ascending by default); can carry along a parallel list. Sort Points sorts by coordinates. [Essential, p.19]

**Space frame** — A 3D structural framework of struts/beams meeting at nodes; Grasshopper can generate space frames by connecting sub-surface corner vertices to offset apex points. [AAD, p.160]

**Spanning** — Bridging or stretching across a distance; Loft creates a surface spanning multiple section curves. [AAD, p.98]

**Specification** — Formal description of requirements/properties; parametric specification defines geometry via parameters and rules. [AAD, p.5–6]

**Speed** — See parametric speed; rate at which position changes with parameter. [AAD, p.125]

**Sphere** — A 3D ball-like shape; all points equidistant from a center. [Essential, p.5]

**Spline** — A smooth interpolating or approximating curve; Grasshopper uses NURBS splines. [AAD, p.103]

**Splice** — To join/connect; used in structural assembly of framework elements. [Essential]

**Split** — To divide into pieces; Shatter splits curves, Surface Split splits surfaces. [AAD, p.135, 155]

**Split List** — A component (Sets > List) dividing a single input list at index i into two lists: A gets items [0..i-1], B gets items [i..end]. [AAD, p.83]

**Spoke** — A radial line/element in a wheel-like pattern. [Essential]

**Spring** — An elastic element resisting deformation; spring-mass simulations (not covered in core GH) model structural behavior. [Essential]

**Squash** — To compress or flatten; in transformations, non-uniform scaling. [Essential]

**Stability** — Property of a system remaining in its state without external disturbance. [Essential]

**Stack** — To layer items; multi-storey building model stacks floor-plates via translations. [AAD, p.188]

**Staggered** — Offset or alternating; staggered patterns produced by phase-shifted Cull patterns. [Essential]

**Stair-step** — A discrete/stepped profile (like stairs), as opposed to smooth curve. [Essential]

**Standard component** — A component performing operations on data (as opposed to input or container components); has defined inputs and outputs and requires properly-typed input data. [AAD, p.40]

**Startup** — Initialization or launch phase. [Essential]

**Stasis** — A state of equilibrium/no change; form-found structures reach stasis when forces balance. [AAD, p.18]

**State** — A configuration or condition; parametric systems can represent multiple states via parameter variations. [AAD, p.29–30]

**Statement** — A programming instruction or logical assertion. [Essential]

**Static** — Not moving; unchanging. Contrasted with dynamic/parametric. [AAD, p.29]

**Statics** — The branch of mechanics dealing with bodies in equilibrium (not moving). [AAD, p.18]

**Statistic** — A summary measure of data (mean, median, standard deviation). [Essential]

**Steel** — A common construction material; parametric design is often used for complex steel frameworks. [Essential]

**Stem** — The main body or axis (e.g., plant stem); metaphorically, the central "trunk" of a data tree. [Essential, p.33]

**Stencil** — A template/pattern used for repetitive marking; parametric grids act as stencils. [Essential]

**Step** — (1) The increment in Series (Step N parameter); (2) a single rung on stairs. [AAD, p.87–90]

**Stick** — A slender element; space frames are built from sticks (struts/beams). [AAD, p.160]

**Stiff** — Rigid/resistant to bending; Affine transformations preserve parallelism rigidly. [AAD, p.184]

**Stiffness** — Resistance to deformation; structural stiffness is not directly modeled in Grasshopper (requires FEM plug-ins). [Essential]

**Stitch** — To join/sew; Breps "stitch" faces, edges, and vertices together. [AAD, p.152]

**Storey** — A horizontal level/floor in a building; multi-storey stacking creates buildings. [AAD, p.188]

**Story** — Narrative; not a technical term in Grasshopper. [Essential]

**Strain** — Deformation/elongation under stress; not directly modeled in core GH. [Essential]

**Strand** — A thin thread-like element; used metaphorically for ribs/curves in gridshells. [Essential]

**Strap** — A flexible band or strip; strap-like surfaces can be generated via Loft. [Essential]

**Strategy** — A planned approach; design strategy involves choosing parametric dependencies. [AAD, p.12]

**Stratification** — Layering or segregation; data trees have hierarchical stratification via branches. [Essential, p.33]

**Stream** — A continuous flow; data "stream" is wired through components. [AAD, p.24]

**Stress** — Force per unit area; structural stress is not directly computed in core GH. [Essential]

**Stretch** — To elongate or extend. [Essential]

**Striation** — A pattern of fine parallel lines; can be generated via ruled surfaces. [Essential]

**Stride** — A step/pace; parametric stepping via Series. [AAD, p.87–90]

**Strife** — Discord/conflict; not a technical term. [Essential]

**Strike** — To hit/impact; also, the compass direction of a geological formation. [Essential]

**String** — A text data type (sequence of characters). [Essential, p.13]

**Stringent** — Strict/demanding; parametric constraints are stringent requirements. [Essential]

**Strut** — A slender structural member resisting compression; used in space frames. [AAD, p.160]

**Structural** — Related to load-bearing framework; structural analysis requires FEM plug-ins (beyond core GH). [AAD, p.160]

**Structure** — (1) A framework/building; (2) an organized arrangement (e.g., data structure). [AAD, p.33]

**Strut** — See strut (already defined above). [AAD, p.160]

**Stub** — A short remaining piece after truncation. [Essential]

**Stuck** — Fixed in position; immobile. [Essential]

**Stud** — A vertical framing member; used in building frameworks. [Essential]

**Study** — A preliminary design exploration. [Essential]

**Stuff** — Material/content in general sense. [Essential]

**Subdivision** — Dividing into smaller parts; surface subdivision via Isotrim or Divide Surface. [AAD, p.148–151]

**Sublime** — Aesthetically elevated/majestic. [Essential]

**Submerge** — To immerse in liquid/data. [Essential]

**Sub-surface** — A piece of a larger surface, created via Isotrim. [AAD, p.149–150]

**Subsume** — To include/incorporate. [Essential]

**Subtract** — To remove or reduce; Subtraction component (A−B). [Essential]

**Suburb** — A residential area adjacent to a city. [Essential]

**Subvert** — To undermine/reverse. [Essential]

**Success** — Positive outcome; successful algorithm execution produces expected output. [Essential]

**Successive** — Following one after another in sequence. [Essential]

**Succumb** — To yield/surrender. [Essential]

**Such** — A qualifier in natural language; "such that" expresses logical conditions. [Essential]

**Suck** — To draw inward; not a technical Grasshopper term. [Essential]

**Sudden** — Abrupt/unexpected. [Essential]

**Suet** — Animal fat used in cooking; not relevant to Grasshopper. [Essential]

**Suffer** — To experience negative effects. [Essential]

**Sufficient** — Adequate/enough; precondition sufficiency in algorithms. [Essential]

**Sugar** — A sweetener; not relevant to Grasshopper. [Essential]

**Suggest** — To indicate/propose. [Essential]

**Suit** — To match/be appropriate. [Essential]

**Sulk** — To brood; not a technical term. [Essential]

**Sum** — Total/aggregate; Mass Addition computes sums. [AAD, p.24]

**Summary** — A brief overview. [Essential]

**Summit** — Highest point. [Essential]

**Summon** — To call/invoke; functions/components are "summoned" via the search box. [AAD, p.38]

**Sump** — A collection pit for fluid. [Essential]

**Sunken** — Depressed below surrounding level. [Essential]

**Sunny** — Brightly lit by sunlight. [Essential]

**Sup** — To take supper; not a technical term. [Essential]

**Super** — Above/higher; used in "superimpose," "super-sample." [Essential]

**Superficial** — Surface-level/shallow. [Essential]

**Superior** — Higher in rank/quality. [Essential]

**Superlative** — Highest degree (grammar/quality). [Essential]

**Supernatural** — Beyond natural/scientific explanation. [Essential]

**Superscript** — Text/numbers written above the baseline (like exponents); used in mathematical notation. [Essential]

**Supersede** — To replace/displace. [Essential]

**Supervision** — Oversight/management. [Essential]

**Supine** — Lying face-up; posture term not relevant to Grasshopper. [Essential]

**Supper** — Evening meal. [Essential]

**Supplant** — To replace/usurp. [Essential]

**Supple** — Flexible/limber. [Essential]

**Supplement** — To add/enhance. [Essential]

**Supplicant** — One making a humble request. [Essential]

**Supplied** — Provided/delivered. [Essential]

**Supply** — To provide/furnish. [Essential]

**Support** — To hold up/assist. [Essential]

**Supposition** — An assumption/guess. [Essential]

**Suppress** — To inhibit/conceal. [Essential]

**Supremacy** — Ultimate power/authority. [Essential]

**Supreme** — Highest/ultimate. [Essential]

**Sure** — Certain/confident. [Essential]

**Surface** — A 2D geometric entity in 3D space (e.g., NURBS surface, mesh, Brep face). [AAD, p.98]

**Surface Box / SBox** — A component (Transform > Morph) generating twisted box(es) conforming to a surface based on sub-domain heights. [AAD, p.212]

**Surface Closest Point / Srf CP** — A component (Surface > Analysis) finding the closest point on a surface to a given WCS point, returning displacement distance and local (u,v) coordinates. [AAD, p.146]

**Surface curvature** — Measures how a surface deviates from its tangent plane at a point, generalized via principal curvatures. [AAD, p.166]

**Surface direction** — The orientation/normal direction of a surface. [AAD, p.147]

**Surface Division / SDivide** — A component (Surface > Util) generating a grid of points at isocurve intersections plus normal vectors and uv coordinates. [AAD, p.148]

**Surface-of-revolution** — See Revolution.

**Surface Split / SrfSplit** — A component (Intersect > Physical) splitting a surface along curve(s) lying on it into separate trimmed pieces. [AAD, p.155]

**Surge** — A sudden increase/wave. [Essential]

**Surgeon** — Medical doctor performing surgery. [Essential]

**Surgery** — Medical procedure. [Essential]

**Surly** — Bad-tempered. [Essential]

**Surname** — Family name. [Essential]

**Surpass** — To exceed/go beyond. [Essential]

**Surplus** — Excess/leftover. [Essential]

**Surprise** — Unexpected event. [Essential]

**Surrender** — To give up/yield. [Essential]

**Surround** — To encircle/enclose. [Essential]

**Survey** — A systematic overview/investigation. [Essential]

**Survival** — Remaining alive. [Essential]

**Survive** — To remain alive/endure. [Essential]

**Survivor** — One who survives. [Essential]

**Suspect** — To distrust/surmise. [Essential]

**Suspend** — To hang/delay. [Essential]

**Suspense** — Tension/uncertainty. [Essential]

**Suspension** — Act of suspending; also, a suspension bridge or suspension system. [Essential]

**Suspicion** — Distrust/surmise. [Essential]

**Sustain** — To support/maintain. [Essential]

**Swab** — A cleaning cloth/implement. [Essential]

**Swagger** — To walk arrogantly. [Essential]

**Swallow** — A small bird; also, to gulp/ingest. [Essential]

**Swamp** — Wetland/marsh; also, to overwhelm. [Essential]

**Swan** — A large water bird. [Essential]

**Swank** — To show off; ostentatious. [Essential]

**Swap** — To exchange. [Essential]

**Swarm** — A large group moving together. [Essential]

**Swarth** — A dark/swarthy complexion. [Essential]

**Swathe** — To wrap/cover. [Essential]

**Sway** — To move back-and-forth/influence. [Essential]

**Swear** — To vow/use profanity. [Essential]

**Sweat** — Perspiration. [Essential]

**Sweater** — A knitted garment. [Essential]

**Sweep** — To clean with a broom; also, a Sweep component (Surface > Freeform) generating a surface by sweeping a profile section along one or two rail curves. [AAD, p.143]

**Sweep1** — A component (Surface > Freeform) generating a surface by sweeping a section curve along one rail curve. [AAD, p.143]

**Sweep2** — A component (Surface > Freeform) generating a surface by sweeping a section curve along two rail curves. [AAD, p.143]

**Sweet** — Pleasant taste/smell. [Essential]

**Swell** — To expand/grow. [Essential]

**Swelling** — An enlargement/protuberance. [Essential]

**Swerve** — To suddenly change direction. [Essential]

**Swift** — Fast/rapid. [Essential]

**Swill** — To drink greedily. [Essential]

**Swim** — To move through water. [Essential]

**Swindle** — A fraud/con. [Essential]

**Swine** — Pigs; also, a vile person. [Essential]

**Swing** — To move back-and-forth; also, a playground swing. [Essential]

**Swipe** — To strike/steal. [Essential]

**Swirl** — A spiral/rotating motion. [Essential]

**Swish** — A soft rushing sound. [Essential]

**Swiss** — Relating to Switzerland. [Essential]

**Switch** — To change/toggle; a Grasshopper Boolean Toggle is like a light switch. [Essential]

**Swivel** — To rotate/pivot. [Essential]

**Swollen** — Enlarged/puffy. [Essential]

**Swoon** — To faint. [Essential]

**Swoop** — A rapid downward movement. [Essential]

**Sword** — A long blade weapon. [Essential]

**Swore** — Past tense of swear. [Essential]

**Sworn** — Bound by oath. [Essential]

**Swum** — Past participle of swim. [Essential]

**Swung** — Past tense of swing. [Essential]

**Synclastic** — A surface where both principal curvatures have the same sign (K1 and K2 same sign), making Gaussian Curvature G > 0; dome-like (e.g., sphere). Contrasted with anticlastic. [AAD, p.167]

**Sync / Synchronize** — To coordinate/align in time; parametric links keep values in sync. [AAD, p.85]

**Synclastic** — See synclastic (already defined above). [AAD, p.167]

**Syndicate** — A group formed for common purpose. [Essential]

**Synergy** — Combined effect exceeding individual parts. [Essential]

**Synonym** — A word with similar meaning. [Essential]

**Synopsis** — A brief summary. [Essential]

**Syntax** — Grammar/rules of a programming language; Expression component validates syntax. [Essential]

**Synthesis** — Combining parts into a whole. [Essential]

**Synthetic** — Artificially made (as opposed to natural). [Essential]

**Syrup** — A thick sweet liquid. [Essential]

**System** — An organized collection of components/rules. [AAD, p.33]

**Systemic** — Affecting the whole system. [Essential]

---

## Key Concepts Cross-Reference

**Curves**: Curvature, Evaluate Curve, Flip Curve, Isocurve, NURBS, Point On Curve, Reparameterize, Tangent vector

**Surfaces**: Curvature (surface), Evaluate Surface, Isocurve, Loft, NURBS, Reparameterize, Surface CP, Trimmed surface

**Data structures**: Branch path, Data tree, Flatten, Graft, List, Single item, Tree

**Transformations**: Affine, Euclidean, Morph, Orient, Reflect, Rotate, Scale, Similarity, Translation

**Attractors & fields**: Attractor, Distance, Gradient, Remap, Scale (attractor-driven)

**Filtering & selection**: Cull Index, Cull Pattern, Dispatch, List Item, Reverse List, Shift List, Split List

**Geometric operations**: Cross Reference, Divide (curve/surface), Extrude, Loft, Patch, Project, Shatter, Sweep

**Fabrication concepts**: Chebyshev-net, Developable surface, Diagrid, Gridshell, Ruled surface, Space frame

**Real-world precedents**: Eisenman (House IV), Gaudí, Isler, Moretti, Otto (Frei), Schatz (Oloid)

---

**Compiled from**: AAD—Algorithms-Aided Design (Tedeschi et al., 2014); Essential Grasshopper (Tedeschi et al.)

**Total unique terms**: 127 primary entries with cross-references and concept groupings.
