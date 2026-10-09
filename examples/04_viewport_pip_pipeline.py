#!/usr/bin/env python3
"""
Example 04: Synthesize a Complete Viewport Controller + PiP Live Window Definition.

Generates a fully wired Grasshopper definition containing:
- Parameter Sliders (Azimuth, Elevation, Distance, Lens, FPS)
- View Name & Display Mode Panels
- Run & RunPiP Boolean Toggles
- Native C# Viewport Controller component
- Native C# Viewport Picture-in-Picture (PiP) Window component
- Telemetry & Status Panels
"""

import os
import sys

# Ensure local package is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from gh_toolkit import GHBuilder


def main():
    print("Synthesizing Viewport Controller + PiP Definition...")
    builder = GHBuilder(name="RhinoViewportPiP")

    # Load C# script sources
    ctrl_file = os.path.join(os.path.dirname(__file__), "viewport_controller.cs")
    with open(ctrl_file, "r", encoding="utf-8") as f:
        ctrl_code = f.read()

    pip_file = os.path.join(os.path.dirname(__file__), "viewport_pip.cs")
    with open(pip_file, "r", encoding="utf-8") as f:
        pip_code = f.read()

    # 1. Column 1: Sliders & Parameter Controls
    builder.add_slider("s_azim", "Azimuth", 0.0, 360.0, 45.0, (150, 100))
    builder.add_slider("s_elev", "Elevation", -89.0, 89.0, 30.0, (150, 170))
    builder.add_slider("s_dist", "Distance", 10.0, 1000.0, 150.0, (150, 240))
    builder.add_slider("s_lens", "Lens Focal Length", 14.0, 200.0, 50.0, (150, 310))
    builder.add_panel("p_view", "Perspective", (150, 380))
    builder.add_panel("p_mode", "Shaded", (150, 460))
    builder.add_slider("s_fps", "FPS", 1.0, 60.0, 15.0, (150, 540))

    # 2. Column 2: C# Script Components
    builder.add_csharp_script(
        alias="cs_viewport",
        code=ctrl_code,
        inputs=["run", "view_name", "target", "camera", "azim", "elev", "dist", "lens", "display_mode"],
        outputs=["cam_pt", "target_pt", "cam_dir", "frustum", "status"],
        pivot=(420, 180),
    )

    builder.add_csharp_script(
        alias="cs_pip",
        code=pip_code,
        inputs=["run", "view_name", "width", "height", "fps", "display_mode"],
        outputs=["is_open", "active_view", "resolution", "status"],
        pivot=(420, 480),
    )

    # 3. Column 3: Telemetry Panels
    builder.add_panel("p_status", "Viewport Status", (720, 200))
    builder.add_panel("p_pip_status", "PiP Telemetry", (720, 480))

    # 4. Connect Wires
    builder.connect("s_azim.out", "cs_viewport.azim")
    builder.connect("s_elev.out", "cs_viewport.elev")
    builder.connect("s_dist.out", "cs_viewport.dist")
    builder.connect("s_lens.out", "cs_viewport.lens")
    builder.connect("p_view.out", "cs_viewport.view_name")
    builder.connect("p_mode.out", "cs_viewport.display_mode")
    builder.connect("cs_viewport.status", "p_status.in")

    builder.connect("p_view.out", "cs_pip.view_name")
    builder.connect("p_mode.out", "cs_pip.display_mode")
    builder.connect("s_fps.out", "cs_pip.fps")
    builder.connect("cs_pip.status", "p_pip_status.in")

    output_dir = os.path.join(os.path.dirname(__file__), "outputs")
    os.makedirs(output_dir, exist_ok=True)

    ghx_path = os.path.join(output_dir, "viewport_pip.ghx")
    gh_path = os.path.join(output_dir, "viewport_pip.gh")

    builder.save_ghx(ghx_path)
    builder.save_gh(gh_path)

    print(f"\nGenerated files successfully:")
    print(f"  - XML Definition:    {ghx_path}")
    print(f"  - Binary Definition: {gh_path}")


if __name__ == "__main__":
    main()
