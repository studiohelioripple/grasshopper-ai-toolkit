# Curated GhPython & C# Script Library
> Extracted, refactored, and annotated from 128 production scripts across 193 Grasshopper definitions.

---

## 1. DataTree Hierarchy Mapping (`ghpythonlib.treehelpers`)
*Origin: `Final Approach Product.gh` & `StructureTree Mapper Product.gh`*

Convert nested Python data structures (lists of lists) into native Grasshopper `DataTree` instances and vice-versa.

```python
import ghpythonlib.treehelpers as th
import Grasshopper.DataTree as datatree
from Grasshopper.Kernel.Data import GH_Path

# Convert nested Python list to Grasshopper DataTree
# nested_list = [[pt1, pt2], [pt3, pt4, pt5]]
tree = th.list_to_tree(nested_data)

# Convert Grasshopper DataTree to nested Python list
py_list = th.tree_to_list(tree_input)
```

---

## 2. Parametric Genome Hexadecimal Codec (Sliders & Toggles)
*Origin: `Bricks Agged Catalog.gh`*

Compresses all number sliders and boolean toggles ending with `:` on the canvas into a compact hexadecimal string (and unpacks them on demand). Ideal for state presets and variant libraries.

### Encoder (Pack Canvas State to Hex String):
```csharp
var objects = GrasshopperDocument.Objects.Where(i => i.NickName.EndsWith(":")).ToList();
var sliders = objects.OfType<GH_NumberSlider>().ToList();
var toggles = objects.OfType<GH_BooleanToggle>().ToList();

var hex = "";
for (int s = 0; s < sliders.Count; s++) {
    int val = (int)Math.Round((double)sliders[s].TickValue / sliders[s].TickCount * 255.0);
    hex += val.ToString("X2");
}

byte toggleByte = 0;
for (int t = 0; t < Math.Min(toggles.Count, 8); t++) {
    if (toggles[t].Value) toggleByte |= (byte)(1 << t);
}
hex += toggleByte.ToString("X2");

A = hex; // Outputs compact genome string e.g. 'FA30C805'
```

### Decoder (Restore Canvas State from Hex String):
```csharp
if (string.IsNullOrEmpty(CODE)) return;

var objects = GrasshopperDocument.Objects.Where(i => i.NickName.EndsWith(":")).ToList();
var sliders = objects.OfType<GH_NumberSlider>().ToList();
var toggles = objects.OfType<GH_BooleanToggle>().ToList();

for (int s = 0; s < sliders.Count; s++) {
    int byteVal = Convert.ToInt32(CODE.Substring(s * 2, 2), 16);
    sliders[s].TickValue = (int)Math.Round(byteVal / 255.0 * sliders[s].TickCount);
}

if (CODE.Length >= (sliders.Count + 1) * 2) {
    byte toggleByte = Convert.ToByte(CODE.Substring(sliders.Count * 2, 2), 16);
    for (int t = 0; t < Math.Min(toggles.Count, 8); t++) {
        toggles[t].Value = (toggleByte & (1 << t)) != 0;
    }
}
```

---

## 3. Dynamic Section Slicing & Dimensional Extraction
*Origin: `Dimension.gh`*

Intersects complex curves with an array of section planes to dynamically extract local frame profiles and dimensions.

```csharp
using System.Linq;
using Rhino.Geometry;
using Rhino.Geometry.Intersect;

var dimensions = new List<double>();
var polyCurves = Curves.Select(c => new PolylineCurve(c)).ToList();

foreach (Plane plane in Planes) {
    foreach (var pc in polyCurves) {
        var events = Intersection.CurvePlane(pc, plane, 0.001);
        if (events == null || !events.Any()) continue;
        
        foreach (var ev in events) {
            plane.ClosestParameter(ev.PointA, out double u, out double v);
            dimensions.Add(Math.Abs(u));
        }
    }
}
A = dimensions;
```

---

## 4. Non-Overlapping Facade Opening Intervals
*Origin: `conduit ramsar.gh`*

Merges overlapping linear opening domains along a facade wall into unified, non-conflicting bounding rectangles.

```python
import ghpythonlib.components as gh
import Rhino.Geometry as rh

# Input: curves (lines on wall base), t (wall height)
intervals = []
for crv in curves:
    pt_start, pt_end = gh.EndPoints(crv)
    intervals.append(gh.ConstructDomain(pt_start.X, pt_end.X))

# Merge collinear overlapping segments via Heteroptera
merged_intervals = gh.Heteroptera.IntervalsUnion(intervals)

base_y = curves[0].PointAtStart.Y
height_interval = rh.Interval(base_y, base_y + t)
plane_xy = rh.Plane.WorldXY

if isinstance(merged_intervals, float):
    rectangles = rh.Rectangle3d(plane_xy, merged_intervals, height_interval)
else:
    rectangles = [rh.Rectangle3d(plane_xy, iv, height_interval) for iv in merged_intervals]

a = rectangles
```

---

## 5. Direct Rhino Document Object Attribute Extractor (BIM Keys)
*Origin: `Att Hatches2.gh` & `Rasht Attribute farsi.gh`*

Extracts user strings, keys, and layer metadata directly from Rhino Document without baking.

```csharp
using System.Linq;
using Rhino.DocObjects;

var docObjects = RhinoDocument.Objects.FindByObjectType(ObjectType.Curve).ToList();
var metadata = new List<string>();

foreach (var obj in docObjects) {
    var userStrings = obj.Attributes.GetUserStrings();
    foreach (string key in userStrings.AllKeys) {
        metadata.Add($"{obj.Id}|{key}|{userStrings[key]}");
    }
}
A = metadata;
```

---

## 6. Recursive N-Queens Constraint Solver
*Origin: `8Queens All possible states.gh` & `8vazir.gh`*

Recursive spatial constraint backtracking engine in GhPython.

```python
def solve_n_queens(n=8):
    solutions = []
    board = [-1] * n

    def is_safe(row, col):
        for r in range(row):
            c = board[r]
            if c == col or abs(c - col) == abs(r - row):
                return False
        return True

    def place_queen(row):
        if row == n:
            solutions.append(list(board))
            return
        for col in range(n):
            if is_safe(row, col):
                board[row] = col
                place_queen(row + 1)
                board[row] = -1

    place_queen(0)
    return solutions

# Input: count
# Output: all_boards (list of row column positions)
all_boards = solve_n_queens(int(count) if 'count' in globals() else 8)
```
