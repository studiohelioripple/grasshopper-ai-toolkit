import os
import unittest
from gh_toolkit.native import (
    load_native_catalog,
    find_native_component,
    list_native_components,
    resolve_native_for_generation,
    is_obsolete_native_component,
    get_active_replacement_guid,
)
from gh_toolkit.heteroptera import load_heteroptera_catalog, find_heteroptera_component, list_heteroptera_components
from gh_toolkit.legopod import load_legopod_catalog, find_legopod_component, list_legopod_components
from gh_toolkit.magpie import load_magpie_catalog, find_magpie_component, list_magpie_components
from gh_toolkit.builder import GHBuilder


class TestPluginCatalogs(unittest.TestCase):
    def test_native_catalog(self):
        cat = load_native_catalog()
        self.assertGreaterEqual(cat.get("total_components", 0), 200)
        divide = find_native_component("Divide Curve")
        self.assertIsNotNone(divide)
        self.assertEqual(divide["guid"].lower(), "2162e72e-72fc-4bf8-9459-d4d82fa8aa14")
        crv_comps = list_native_components("Curve")
        self.assertGreater(len(crv_comps), 10)
        # Rectangle component tests
        rect = find_native_component("Rectangle")
        self.assertIsNotNone(rect)
        self.assertEqual(rect["guid"].lower(), "d93100b6-d50b-40b2-831a-814659dc38e3")
        self.assertEqual(len(rect["inputs"]), 4)
        self.assertEqual(len(rect["outputs"]), 2)
        rect_by_guid = find_native_component("d93100b6-d50b-40b2-831a-814659dc38e3")
        self.assertIsNotNone(rect_by_guid)
        self.assertEqual(rect_by_guid["name"], "Rectangle")

    def test_obsolete_component_preservation_and_upgrade(self):
        # Obsolete Multiplication GUID
        obs_mul_guid = "b8963bb1-aa57-476e-a20e-ed6cf635a49c"
        active_mul_guid = "ce46b74e-00c9-43c4-805a-193b69ea4a11"

        # 1. find_native_component must preserve obsolete GUID for old definitions
        comp = find_native_component(obs_mul_guid)
        self.assertIsNotNone(comp)
        self.assertTrue(comp.get("obsolete"))
        self.assertEqual(comp.get("superseded_by"), active_mul_guid)

        # 2. is_obsolete_native_component
        self.assertTrue(is_obsolete_native_component(obs_mul_guid))
        self.assertFalse(is_obsolete_native_component("Multiplication"))

        # 3. get_active_replacement_guid
        self.assertEqual(get_active_replacement_guid(obs_mul_guid), active_mul_guid)

        # 4. resolve_native_for_generation must auto-upgrade to active modern component
        resolved = resolve_native_for_generation(obs_mul_guid)
        self.assertIsNotNone(resolved)
        self.assertEqual(resolved["guid"].lower(), active_mul_guid.lower())
        self.assertFalse(resolved.get("obsolete", False))

        # Obsolete Area GUID
        obs_area_guid = "2e205f24-9279-47b2-b414-d06dcd0b21a7"
        active_area_guid = "86b28a7e-94d9-4791-8306-e13e10d5f8d5"
        self.assertTrue(is_obsolete_native_component(obs_area_guid))
        area_resolved = resolve_native_for_generation(obs_area_guid)
        self.assertEqual(area_resolved["guid"].lower(), active_area_guid.lower())

    def test_builder_obsolete_auto_upgrade(self):
        b = GHBuilder("UpgradeTest")
        obs_mul_guid = "b8963bb1-aa57-476e-a20e-ed6cf635a49c"
        active_mul_guid = "ce46b74e-00c9-43c4-805a-193b69ea4a11"

        obs_rect_guid = "0ca0a214-396c-44ea-b22f-d3a1757c32d6"
        active_rect_guid = "d93100b6-d50b-40b2-831a-814659dc38e3"

        # Add using obsolete GUIDs
        b.add_native_component(obs_mul_guid, "mul", (0, 0))
        b.add_component(obs_rect_guid, "rec", (200, 0))

        out_ghx = "/tmp/test_upgrade_definition.ghx"
        b.save_ghx(out_ghx)
        self.assertTrue(os.path.exists(out_ghx))

        from gh_toolkit.core import read_ghx, GHGraph

        archive = read_ghx(out_ghx)
        graph = GHGraph.from_archive(archive)
        component_guids = [c.guid.lower() for c in graph.components]

        # Must contain active modern GUIDs
        self.assertIn(active_mul_guid.lower(), component_guids)
        self.assertIn(active_rect_guid.lower(), component_guids)

        # Must NOT contain obsolete GUIDs
        self.assertNotIn(obs_mul_guid.lower(), component_guids)
        self.assertNotIn(obs_rect_guid.lower(), component_guids)

        if os.path.exists(out_ghx):
            os.remove(out_ghx)

    def test_catalog_separation_invariants(self):
        cat = load_native_catalog()
        by_name = cat.get("by_name", {})
        by_guid = cat.get("by_guid", {})

        # Primary by_name catalogue used for generation must have ZERO obsolete components
        for name, comp in by_name.items():
            self.assertFalse(comp.get("obsolete", False), f"Component '{name}' in by_name is obsolete!")

        # by_guid preserves obsolete components for reading legacy files
        obsolete_in_guid = [g for g, c in by_guid.items() if c.get("obsolete")]
        self.assertGreater(len(obsolete_in_guid), 100)

    def test_heteroptera_catalog(self):
        cat = load_heteroptera_catalog()
        self.assertGreaterEqual(cat.get("total_components", 0), 150)
        ss = find_heteroptera_component("Space Syntax")
        self.assertIsNotNone(ss)
        self.assertEqual(ss["guid"].lower(), "d4077291-8c30-4313-8bb3-45a86138c521")
        vec_comps = list_heteroptera_components("Vectors")
        self.assertGreater(len(vec_comps), 10)

    def test_legopod_catalog(self):
        cat = load_legopod_catalog()
        self.assertEqual(cat.get("total_components", 0), 42)
        att = find_legopod_component("Build Attribute")
        self.assertIsNotNone(att)
        self.assertEqual(att["guid"].lower(), "3497e94a-b35d-4d20-aae3-9eb2f7d09542")
        self.assertEqual(len(att["inputs"]), 9)
        self.assertEqual(len(att["outputs"]), 1)
        block_comps = list_legopod_components("Blocks")
        self.assertGreater(len(block_comps), 5)

    def test_magpie_catalog(self):
        cat = load_magpie_catalog()
        self.assertEqual(cat.get("total_components", 0), 14)
        corr = find_magpie_component("Correlation Matrix")
        self.assertIsNotNone(corr)
        self.assertEqual(corr["guid"].lower(), "06e60a13-0994-4d55-823d-f2ccc8bec38b")
        self.assertEqual(corr["inputs"][0]["access"], "tree")
        machine_comps = list_magpie_components("Machines")
        self.assertEqual(len(machine_comps), 6)

    def test_ghbuilder_unified_dispatch(self):
        b = GHBuilder("MultiPluginDefinition")
        # Native
        div_id = b.add_component("Divide Curve", "div", (100, 100))
        self.assertIsNotNone(div_id)
        # Heteroptera
        ss_id = b.add_component("Space Syntax", "ss", (300, 100))
        self.assertIsNotNone(ss_id)
        # LegoPod
        att_id = b.add_component("Build Attribute", "att", (500, 100))
        self.assertIsNotNone(att_id)
        # Magpie
        corr_id = b.add_component("Correlation Matrix", "corr", (700, 100))
        self.assertIsNotNone(corr_id)

        self.assertEqual(b.object_count, 4)
        out_ghx = "/tmp/test_multi_plugin.ghx"
        b.save_ghx(out_ghx)
        self.assertTrue(os.path.exists(out_ghx))
        self.assertGreater(os.path.getsize(out_ghx), 1000)
        if os.path.exists(out_ghx):
            os.remove(out_ghx)


if __name__ == "__main__":
    unittest.main()
