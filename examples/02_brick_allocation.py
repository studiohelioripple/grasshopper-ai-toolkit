#!/usr/bin/env python3
"""
Example 02: Synthesize a Stochastic Brick Masonry Variation Definition.

Demonstrates assembling custom Heteroptera components for parametric
brick layout and stochastic rotation offset pairing.
"""

import os
import sys

# Ensure local package is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from gh_toolkit import GHBuilder


def main():
    print("Synthesizing Stochastic Masonry Definition...")
    builder = GHBuilder(name="StochasticBrickMasonry")

    # 1. Sliders for grid dimensions
    builder.add_slider("s_cols", "Columns", 5, 50, 20, (100, 100))
    builder.add_slider("s_rows", "Rows", 2, 30, 10, (100, 180))
    builder.add_slider("s_jitter", "Jitter", 0.0, 1.0, 0.25, (100, 260))

    # 2. Heteroptera Stochastic Allocator Components
    builder.add_heteroptera_component("Careless Range", "careless", (340, 180))
    builder.add_heteroptera_component("Slingshot Allocator", "slingshot", (560, 180))
    builder.add_heteroptera_component("Symmetric Domain", "sym_dom", (780, 180))

    # 3. Add GhPython Brick Solver Component
    brick_python = """
# Inputs: cols, rows, jitter_vals
# Outputs: brick_boxes, centers
import Rhino.Geometry as rg

brick_boxes = []
centers = []
w, h, d = 200.0, 65.0, 100.0

for r in range(int(rows)):
    offset = (w * 0.5) if (r % 2 == 1) else 0.0
    for c in range(int(cols)):
        idx = (r * int(cols) + c) % len(jitter_vals) if jitter_vals else 0
        rot = jitter_vals[idx] if jitter_vals else 0.0
        pt = rg.Point3d(c * (w + 10.0) + offset, 0, r * (h + 10.0))
        box = rg.Box(rg.Plane.WorldXY, rg.Interval(pt.X - w/2, pt.X + w/2),
                     rg.Interval(pt.Y - d/2, pt.Y + d/2),
                     rg.Interval(pt.Z, pt.Z + h))
        brick_boxes.append(box)
        centers.append(pt)
"""
    builder.add_python_script(
        alias="py_bricks",
        code=brick_python,
        inputs=["cols", "rows", "jitter_vals"],
        outputs=["brick_boxes", "centers"],
        pivot=(1000, 150),
    )

    # 4. Connect Wires
    builder.connect("s_cols.out", "py_bricks.cols")
    builder.connect("s_rows.out", "py_bricks.rows")
    builder.connect("s_jitter.out", "careless.Errancy")
    builder.connect("careless.Range", "slingshot.Data")
    builder.connect("slingshot.Data Tree", "sym_dom.Length")
    builder.connect("sym_dom.Interval", "py_bricks.jitter_vals")

    output_dir = os.path.join(os.path.dirname(__file__), "outputs")
    os.makedirs(output_dir, exist_ok=True)

    ghx_path = os.path.join(output_dir, "brick_masonry.ghx")
    gh_path = os.path.join(output_dir, "brick_masonry.gh")

    builder.save_ghx(ghx_path)
    builder.save_gh(gh_path)

    print(f"\nGenerated files:")
    print(f"  - XML Definition:    {ghx_path}")
    print(f"  - Binary Definition: {gh_path}")


if __name__ == "__main__":
    main()
