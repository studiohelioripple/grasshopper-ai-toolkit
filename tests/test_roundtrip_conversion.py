"""
Tests for .gh binary <-> .ghx XML <-> JSON Graph IR conversions.
"""

import os
import unittest
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from gh_toolkit.core import read_ghx, write_ghx, read_gh_binary, write_gh_binary, GHGraph
from gh_toolkit.builder import GHBuilder


class TestRoundtripConversion(unittest.TestCase):
    def test_xml_and_binary_interop(self):
        builder = GHBuilder(name="InteropTest")
        builder.add_slider("s1", "TestSlider", 0.0, 100.0, 50.0, (100, 100))
        builder.add_panel("p1", "Sample Text Note", (300, 100))

        ghx_path = os.path.join(os.path.dirname(__file__), "interop.ghx")
        gh_path = os.path.join(os.path.dirname(__file__), "interop.gh")

        try:
            builder.save_ghx(ghx_path)
            self.assertTrue(os.path.exists(ghx_path))

            # Load from GHX and save to GH
            arch_from_ghx = read_ghx(ghx_path)
            write_gh_binary(arch_from_ghx, gh_path, compress=True)
            self.assertTrue(os.path.exists(gh_path))

            # Load from GH binary and extract graph
            arch_from_gh = read_gh_binary(gh_path)
            graph = GHGraph.from_archive(arch_from_gh)

            self.assertEqual(graph.name, "InteropTest")
            self.assertEqual(len(graph.components), 2)
            comp_names = [c.name for c in graph.components]
            self.assertIn("Number Slider", comp_names)
            self.assertIn("Panel", comp_names)
        finally:
            for p in (ghx_path, gh_path):
                if os.path.exists(p):
                    os.remove(p)


if __name__ == "__main__":
    unittest.main()
