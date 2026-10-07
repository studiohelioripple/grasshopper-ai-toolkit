"""
Tests for Heteroptera catalog loading, component schema validation, and recipes.
"""

import os
import unittest
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from gh_toolkit.heteroptera import (
    load_heteroptera_catalog,
    find_heteroptera_component,
    list_heteroptera_components,
    get_canonical_recipes,
    find_yak,
    get_heteroptera_status,
)


class TestHeteropteraCatalog(unittest.TestCase):
    def setUp(self):
        self.catalog = load_heteroptera_catalog()

    def test_catalog_size_and_categories(self):
        self.assertGreaterEqual(self.catalog.get("total_components", 0), 150)
        subcats = self.catalog.get("subcategories", {})
        self.assertIn("Networks", subcats)
        self.assertIn("Vectors", subcats)
        self.assertIn("Uncertainty", subcats)
        self.assertIn("Streaming", subcats)
        self.assertIn("Geometry", subcats)
        self.assertIn("Maths", subcats)
        self.assertIn("Utilities", subcats)

    def test_space_syntax_schema(self):
        comp = find_heteroptera_component("Space Syntax")
        self.assertIsNotNone(comp)
        self.assertEqual(comp["guid"].lower(), "d4077291-8c30-4313-8bb3-45a86138c521")
        inp_names = [i["name"] for i in comp["inputs"]]
        self.assertIn("Node→Node", inp_names)
        self.assertIn("Source", inp_names)
        self.assertIn("Depth", inp_names)
        out_names = [o["name"] for o in comp["outputs"]]
        self.assertIn("Node SpaceSyntax", out_names)

    def test_recipes(self):
        recipes = get_canonical_recipes()
        self.assertGreaterEqual(len(recipes), 3)
        recipe_ids = [r["id"] for r in recipes]
        self.assertIn("space_syntax", recipe_ids)
        self.assertIn("shortest_walk", recipe_ids)
        self.assertIn("stochastic_masonry", recipe_ids)

    def test_heteroptera_status(self):
        status = get_heteroptera_status()
        self.assertIsInstance(status, dict)
        self.assertIn("yak_found", status)
        self.assertIn("installed", status)
        self.assertIn("is_latest", status)


if __name__ == "__main__":
    unittest.main()

