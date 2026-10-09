"""
gh_toolkit.native - Native Grasshopper component catalog and lookup.

Covers 212 verified native Grasshopper components across standard categories:
Params, Maths, Sets, Vector, Curve, Surface, Mesh, Intersect, Transform, Display.
"""

import os
import json
from typing import Dict, Any, Optional, List

_CACHED_NATIVE_CATALOG: Optional[Dict[str, Any]] = None


def load_native_catalog() -> Dict[str, Any]:
    """Load the verified native Grasshopper component catalog."""
    global _CACHED_NATIVE_CATALOG
    if _CACHED_NATIVE_CATALOG is not None:
        return _CACHED_NATIVE_CATALOG

    base_dir = os.path.dirname(__file__)
    candidates = [
        os.path.join(base_dir, "data", "native_catalog.json"),
        os.path.join(base_dir, "..", "data", "native_catalog.json"),
        os.path.join(base_dir, "..", "skill", "resources", "native_catalog.json"),
        os.path.join(os.getcwd(), "skill", "resources", "native_catalog.json"),
    ]

    for p in candidates:
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    _CACHED_NATIVE_CATALOG = json.load(f)
                    return _CACHED_NATIVE_CATALOG
            except Exception:
                pass

    return {"by_guid": {}, "by_name": {}, "categories": {}, "total_components": 0}


def find_native_component(name_or_guid: str) -> Optional[Dict[str, Any]]:
    """Look up a native Grasshopper component by GUID, Name, or Nickname/Alias."""
    catalog = load_native_catalog()
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


def list_native_components(category: Optional[str] = None) -> List[Dict[str, Any]]:
    """List native components, optionally filtered by category."""
    catalog = load_native_catalog()
    cats = catalog.get("categories", {})

    results = []
    for cat, names in cats.items():
        if category and category.lower() not in (cat.lower(), "all"):
            continue
        for n in names:
            comp = catalog.get("by_name", {}).get(n)
            if comp:
                results.append(comp)
    return results
