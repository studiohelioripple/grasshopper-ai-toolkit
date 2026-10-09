"""
Tests for GHBuilder programmatic definition synthesis and port wiring.
"""

import os
import unittest
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from gh_toolkit.builder import GHBuilder
from gh_toolkit.core import read_gh_binary, read_ghx, GHGraph


class TestGHBuilder(unittest.TestCase):
    def test_space_syntax_pipeline_synthesis(self):
        builder = GHBuilder(name="PipelineTest")
        pipeline_ids = builder.add_space_syntax_pipeline(start_pivot=(100, 100))

        self.assertIn("center", pipeline_ids)
        self.assertIn("adj", pipeline_ids)
        self.assertIn("recon", pipeline_ids)
        self.assertIn("ss", pipeline_ids)
        self.assertIn("norm", pipeline_ids)

        out_path = os.path.join(os.path.dirname(__file__), "test_pipeline.ghx")
        try:
            builder.save_ghx(out_path)
            self.assertTrue(os.path.exists(out_path))

            arch = read_ghx(out_path)
            graph = GHGraph.from_archive(arch)
            self.assertEqual(len(graph.components), 7)
            self.assertGreaterEqual(len(graph.wires), 4)
        finally:
            if os.path.exists(out_path):
                os.remove(out_path)

    def test_native_component_synthesis(self):
        builder = GHBuilder(name="NativeTest")
        builder.add_slider("s_rad", "Radius", 1.0, 10.0, 5.0, (100, 100))
        builder.add_component("Circle (plane + radius)", "c1", (300, 100))
        builder.add_component("Divide Curve", "div", (500, 100))
        builder.connect("s_rad.out", "c1.R")
        builder.connect("c1.C", "div.C")

        out_path = os.path.join(os.path.dirname(__file__), "test_native.gh")
        try:
            builder.save_gh(out_path)
            self.assertTrue(os.path.exists(out_path))

            arch = read_gh_binary(out_path)
            graph = GHGraph.from_archive(arch)
            self.assertEqual(len(graph.components), 3)
            self.assertEqual(len(graph.wires), 2)
        finally:
            if os.path.exists(out_path):
                os.remove(out_path)

    def test_python_script_and_panel_wiring(self):
        builder = GHBuilder(name="ScriptPanelTest")
        builder.add_slider("s_val", "Val", 0.0, 100.0, 50.0, (100, 100))
        builder.add_python_script(
            alias="py_comp",
            code="a = x * 2",
            inputs=["x"],
            outputs=["a"],
            pivot=(300, 100),
        )
        builder.add_panel("p_out", "Output", (500, 100))
        builder.connect("s_val.out", "py_comp.x")
        builder.connect("py_comp.a", "p_out.in")

        out_path = os.path.join(os.path.dirname(__file__), "test_script_panel.ghx")
        try:
            builder.save_ghx(out_path)
            self.assertTrue(os.path.exists(out_path))

            arch = read_ghx(out_path)
            graph = GHGraph.from_archive(arch)
            self.assertEqual(len(graph.components), 3)
            self.assertEqual(len(graph.wires), 2)
        finally:
            if os.path.exists(out_path):
                os.remove(out_path)


    def test_csharp_script_synthesis(self):
        builder = GHBuilder(name="CSharpTest")
        builder.add_slider("s_val", "Val", 0.0, 100.0, 50.0, (100, 100))
        builder.add_csharp_script(
            alias="cs_comp",
            code="A = (double)x * 2.0;",
            inputs=["x"],
            outputs=["A"],
            pivot=(300, 100),
        )
        builder.add_panel("p_out", "Output", (500, 100))
        builder.connect("s_val.out", "cs_comp.x")
        builder.connect("cs_comp.A", "p_out.in")

        out_path = os.path.join(os.path.dirname(__file__), "test_csharp_synthesis.gh")
        try:
            builder.save_gh(out_path)
            self.assertTrue(os.path.exists(out_path))

            arch = read_gh_binary(out_path)
            graph = GHGraph.from_archive(arch)
            self.assertEqual(len(graph.components), 3)
            self.assertEqual(len(graph.wires), 2)
            csharp_comp = [c for c in graph.components if "C#" in c.name or c.guid == "a9a8ebd2-fff5-4c44-a8f5-739736d129ba"]
            self.assertEqual(len(csharp_comp), 1)
        finally:
            if os.path.exists(out_path):
                os.remove(out_path)

    def test_viewport_pip_synthesis(self):
        builder = GHBuilder(name="ViewportPiPTest")
        builder.add_slider("s_fps", "FPS", 1.0, 60.0, 15.0, (150, 540))
        builder.add_panel("p_view", "Perspective", (150, 380))
        builder.add_csharp_script(
            alias="cs_pip",
            code="// Viewport PiP Test",
            inputs=["run", "view_name", "width", "height", "fps", "display_mode"],
            outputs=["is_open", "active_view", "resolution", "status"],
            pivot=(420, 480),
        )
        builder.add_panel("p_status", "PiP Telemetry", (720, 480))
        builder.connect("p_view.out", "cs_pip.view_name")
        builder.connect("s_fps.out", "cs_pip.fps")
        builder.connect("cs_pip.status", "p_status.in")

        out_path = os.path.join(os.path.dirname(__file__), "test_viewport_pip.gh")
        try:
            builder.save_gh(out_path)
            self.assertTrue(os.path.exists(out_path))

            arch = read_gh_binary(out_path)
            graph = GHGraph.from_archive(arch)
            self.assertEqual(len(graph.components), 4)
            self.assertEqual(len(graph.wires), 3)
            csharp_comp = [c for c in graph.components if c.guid == "a9a8ebd2-fff5-4c44-a8f5-739736d129ba"]
            self.assertEqual(len(csharp_comp), 1)
        finally:
            if os.path.exists(out_path):
                os.remove(out_path)


if __name__ == "__main__":
    unittest.main()

