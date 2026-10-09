#!/usr/bin/env python3
"""
Example 03: Synthesize a Complete Viewport Controller Definition.

Generates a fully wired Grasshopper definition containing:
- Parameter Sliders (Azimuth, Elevation, Distance, Lens)
- View Name & Display Mode Panels
- Native GhPython Viewport Controller component
- Output Status Panel & Visual Wireframe Frustum Preview
"""

import os
import sys

# Ensure local package is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from gh_toolkit import GHBuilder


def main():
    print("Synthesizing Viewport Controller Definition...")
    builder = GHBuilder(name="RhinoViewportController")

    # Load Python script source
    script_file = os.path.join(os.path.dirname(__file__), "viewport_controller.py")
    with open(script_file, "r", encoding="utf-8") as f:
        viewport_code = f.read()

    # 1. Sliders & Inputs (Column 1)
    builder.add_slider("s_azim", "Azimuth", 0.0, 360.0, 45.0, (100, 100))
    builder.add_slider("s_elev", "Elevation", -89.0, 89.0, 30.0, (100, 180))
    builder.add_slider("s_dist", "Distance", 10.0, 1000.0, 150.0, (100, 260))
    builder.add_slider("s_lens", "Lens Focal Length", 14.0, 200.0, 50.0, (100, 340))
    builder.add_panel("p_view", "Perspective", (100, 420))
    builder.add_panel("p_mode", "Shaded", (100, 500))

    # 2. Add GhPython Viewport Controller Component (Column 2)
    builder.add_python_script(
        alias="py_viewport",
        code=viewport_code,
        inputs=["run", "view_name", "target", "camera", "azim", "elev", "dist", "lens", "up", "display_mode", "projection", "bbox", "redraw"],
        outputs=["cam_pt", "target_pt", "cam_dir", "cam_plane", "frustum", "status"],
        pivot=(380, 220),
    )

    # 3. Output Panels (Column 3)
    builder.add_panel("p_status", "Status Output", (620, 260))

    # 4. Wire Connections
    builder.connect("s_azim.out", "py_viewport.azim")
    builder.connect("s_elev.out", "py_viewport.elev")
    builder.connect("s_dist.out", "py_viewport.dist")
    builder.connect("s_lens.out", "py_viewport.lens")
    builder.connect("p_view.out", "py_viewport.view_name")
    builder.connect("p_mode.out", "py_viewport.display_mode")
    builder.connect("py_viewport.status", "p_status.in")

    output_dir = os.path.join(os.path.dirname(__file__), "outputs")
    os.makedirs(output_dir, exist_ok=True)

    ghx_path = os.path.join(output_dir, "viewport_controller.ghx")
    gh_path = os.path.join(output_dir, "viewport_controller.gh")

    builder.save_ghx(ghx_path)
    builder.save_gh(gh_path)

    print(f"\nGenerated files successfully:")
    print(f"  - XML Definition:    {ghx_path}")
    print(f"  - Binary Definition: {gh_path}")
    print("\nDouble-click either file to open directly in Rhino 8!")


if __name__ == "__main__":
    main()
