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


if __name__ == "__main__":
    unittest.main()
