import os
import unittest
from gh_toolkit.builder import GHBuilder
from gh_toolkit.core import read_ghx, GHGraph


class TestTriPluginPipelines(unittest.TestCase):
    def test_spatial_ml_metadata_pipeline(self):
        builder = GHBuilder("TestSpatialML")
        ids = builder.add_spatial_ml_metadata_pipeline(
            start_pivot=(100, 100),
            cluster_count=5,
            source_node=1,
            depth=8
        )

        self.assertIn("center", ids)
        self.assertIn("adj", ids)
        self.assertIn("ss", ids)
        self.assertIn("cluster", ids)
        self.assertIn("dict", ids)
        self.assertIn("att", ids)

        # 7 Heteroptera/Sliders + 3 Magpie/Sliders + 2 LegoPod = 12 objects
        self.assertEqual(builder.object_count, 12)

        out_path = "/tmp/test_spatial_ml.ghx"
        builder.save_ghx(out_path)
        self.assertTrue(os.path.exists(out_path))

        # Validate graph roundtrip
        arch = read_ghx(out_path)
        graph = GHGraph.from_archive(arch)
        comp_names = [c.name for c in graph.components]
        self.assertIn("Space Syntax", comp_names)
        self.assertIn("Clustering Machine", comp_names)
        self.assertIn("User Dictionary", comp_names)
        self.assertIn("Build Attribute", comp_names)

        if os.path.exists(out_path):
            os.remove(out_path)

    def test_generative_field_block_pipeline(self):
        builder = GHBuilder("TestFieldBlock")
        ids = builder.add_generative_field_block_pipeline(start_pivot=(50, 50))

        self.assertIn("curv_field", ids)
        self.assertIn("booster", ids)
        self.assertIn("pca", ids)
        self.assertIn("corr", ids)
        self.assertIn("att", ids)
        self.assertIn("def_block", ids)

        self.assertEqual(builder.object_count, 7)

        out_path = "/tmp/test_field_block.ghx"
        builder.save_ghx(out_path)
        self.assertTrue(os.path.exists(out_path))

        arch = read_ghx(out_path)
        graph = GHGraph.from_archive(arch)
        comp_names = [c.name for c in graph.components]
        self.assertIn("Curvature Field", comp_names)
        self.assertIn("PCA Machine", comp_names)
        self.assertIn("Define Block", comp_names)

        if os.path.exists(out_path):
            os.remove(out_path)


if __name__ == "__main__":
    unittest.main()
