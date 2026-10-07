"""
gh_toolkit.magpie - Magpie plugin bindings, component lookup, and machine learning workflows.

Covers 14 verified components across 4 subcategories:
Machines, Tools, Others, Exteras.
"""

import os
import json
from typing import Dict, Any, Optional, List

_CACHED_MAGPIE_CATALOG: Optional[Dict[str, Any]] = None


def load_magpie_catalog() -> Dict[str, Any]:
    """Load the verified Magpie component catalog."""
    global _CACHED_MAGPIE_CATALOG
    if _CACHED_MAGPIE_CATALOG is not None:
        return _CACHED_MAGPIE_CATALOG

    base_dir = os.path.dirname(__file__)
    candidates = [
        os.path.join(base_dir, "data", "magpie_catalog.json"),
        os.path.join(base_dir, "..", "data", "magpie_catalog.json"),
        os.path.join(base_dir, "..", "skill", "resources", "magpie_catalog.json"),
        os.path.join(os.getcwd(), "skill", "resources", "magpie_catalog.json"),
    ]

    for p in candidates:
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    _CACHED_MAGPIE_CATALOG = json.load(f)
                    return _CACHED_MAGPIE_CATALOG
            except Exception:
                pass

    return {"by_guid": {}, "by_name": {}, "subcategories": {}, "total_components": 0}


def find_magpie_component(name_or_guid: str) -> Optional[Dict[str, Any]]:
    """Look up a Magpie component by GUID, Name, or Nickname/Alias."""
    catalog = load_magpie_catalog()
    query = name_or_guid.lower().strip()

    if query in catalog.get("by_guid", {}):
        return catalog["by_guid"][query]

    if name_or_guid in catalog.get("by_name", {}):
        return catalog["by_name"][name_or_guid]

    for k, v in catalog.get("by_name", {}).items():
        if k.lower() == query:
            return v
        if v.get("nickname") and v["nickname"].lower() == query:
            return v

    return None


def list_magpie_components(subcategory: Optional[str] = None) -> List[Dict[str, Any]]:
    """List Magpie components, optionally filtered by subcategory."""
    catalog = load_magpie_catalog()
    subcats = catalog.get("subcategories", {})

    results = []
    for subcat, names in subcats.items():
        if subcategory and subcategory.lower() not in (subcat.lower(), "all"):
            continue
        for n in names:
            comp = catalog.get("by_name", {}).get(n)
            if comp:
                results.append(comp)
    return results
