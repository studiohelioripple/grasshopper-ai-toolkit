"""
Live Attractor Script — linked to a GhPython Script component on the canvas.

Inputs  (add as Grasshopper input params on the script component):
  x    — attractor point X  (Number Slider)
  y    — attractor point Y  (Number Slider)
  r    — influence radius   (Number Slider, default ~10)
  pts  — input point grid   (Point3d list)

Outputs:
  a    — normalised per-point scalar attraction values (0..1)
  col  — System.Drawing.Color list for Custom Preview

Hot-reload:
  gh-toolkit live watch MyAttractor examples/live_attractor.py
"""

import Rhino.Geometry as rg
import math

# ─── safe defaults (GH injects x/y/r/pts automatically) ─────────────────────
try:
    attractor_x = float(x)
    attractor_y = float(y)
    radius      = float(r) if r else 10.0
    input_pts   = list(pts) if pts else []
except Exception:
    attractor_x, attractor_y, radius = 0.0, 0.0, 10.0
    input_pts = [rg.Point3d(i, j, 0) for i in range(-5, 6) for j in range(-5, 6)]

# ─── attractor falloff per point ──────────────────────────────────────────────
attractor_pt = rg.Point3d(attractor_x, attractor_y, 0.0)
raw = []

for pt in input_pts:
    d   = pt.DistanceTo(attractor_pt)
    val = max(0.0, 1.0 - (d / radius) ** 2) if radius > 0 else 0.0
    raw.append(val)

# ─── normalise 0..1 ──────────────────────────────────────────────────────────
mn, mx = (min(raw), max(raw)) if raw else (0.0, 1.0)
span   = mx - mn if mx != mn else 1.0
a      = [(v - mn) / span for v in raw]

# ─── colour gradient  blue (far) → red (close) ───────────────────────────────
import System.Drawing as sd

def lerp_color(t):
    r_ = min(255, int(30  + 200 * t))
    g_ = max(0,   int(120 * (1 - t)))
    b_ = max(0,   int(220 * (1 - t)))
    return sd.Color.FromArgb(255, r_, g_, b_)

col = [lerp_color(v) for v in a]
