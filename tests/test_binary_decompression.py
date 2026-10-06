"""
Tests for binary .gh file decompression and chunk tree parsing.
"""

import os
import unittest
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from gh_toolkit.core import read_gh_binary, write_gh_binary, GHArchive, GHChunk


class TestBinaryDecompression(unittest.TestCase):
    def test_synthetic_binary_roundtrip(self):
        archive = GHArchive()
        archive.root.add_item("TestBool", 1, True)
        archive.root.add_item("TestInt", 3, 42)
        archive.root.add_item("TestFloat", 6, 3.14159)
        archive.root.add_item("TestString", 10, "Hello Grasshopper")

        sub = archive.root.create_chunk("SubChunk")
        sub.add_item("SubItem", 10, "Nested Content")

        out_path = os.path.join(os.path.dirname(__file__), "temp_test.gh")
        try:
            write_gh_binary(archive, out_path, compress=True)
            self.assertTrue(os.path.exists(out_path))

            # Read back
            reloaded = read_gh_binary(out_path)
            self.assertEqual(reloaded.root.name, "Root")
            self.assertEqual(reloaded.root.get_value("TestBool"), True)
            self.assertEqual(reloaded.root.get_value("TestInt"), 42)
            self.assertAlmostEqual(reloaded.root.get_value("TestFloat"), 3.14159, places=4)
            self.assertEqual(reloaded.root.get_value("TestString"), "Hello Grasshopper")

            sub_reloaded = reloaded.root.find_chunk("SubChunk")
            self.assertIsNotNone(sub_reloaded)
            self.assertEqual(sub_reloaded.get_value("SubItem"), "Nested Content")
        finally:
            if os.path.exists(out_path):
                os.remove(out_path)


if __name__ == "__main__":
    unittest.main()
