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


if __name__ == "__main__":
    unittest.main()
