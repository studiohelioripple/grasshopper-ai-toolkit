"""
gh_toolkit.heteroptera - Heteroptera plugin bindings, component lookup, and recipes.

Covers all 152 components across 7 primary subcategories:
Networks, Vectors, Uncertainty, Streaming, Geometry, Maths, Utilities.
"""

import os
import json
from typing import Dict, Any, Optional, List, Tuple

_CACHED_CATALOG: Optional[Dict[str, Any]] = None


def load_heteroptera_catalog() -> Dict[str, Any]:
    """Load the 152-component Heteroptera catalog from package data or known locations."""
    global _CACHED_CATALOG
    if _CACHED_CATALOG is not None:
        return _CACHED_CATALOG

    base_dir = os.path.dirname(__file__)
    candidates = [
        os.path.join(base_dir, "data", "heteroptera_catalog.json"),
        os.path.join(base_dir, "..", "data", "heteroptera_catalog.json"),
        os.path.join(base_dir, "..", "skill", "resources", "heteroptera_catalog.json"),
        os.path.join(base_dir, "..", "..", "tools", "heteroptera_catalog.json"),
        os.path.join(os.getcwd(), "tools", "heteroptera_catalog.json"),
    ]

    for p in candidates:
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    _CACHED_CATALOG = json.load(f)
                    return _CACHED_CATALOG
            except Exception:
                pass

    return {"by_guid": {}, "by_name": {}, "subcategories": {}, "total_components": 0}


def find_heteroptera_component(name_or_guid: str) -> Optional[Dict[str, Any]]:
    """Look up a Heteroptera component by GUID, Name, or Nickname."""
    catalog = load_heteroptera_catalog()
    query = name_or_guid.lower().strip()

    if query in catalog.get("by_guid", {}):
        return catalog["by_guid"][query]

    if name_or_guid in catalog.get("by_name", {}):
        return catalog["by_name"][name_or_guid]

    for k, v in catalog.get("by_name", {}).items():
        if k.lower() == query:
            return v

    return None


def list_heteroptera_components(subcategory: Optional[str] = None) -> List[Dict[str, Any]]:
    """List components, optionally filtered by subcategory."""
    catalog = load_heteroptera_catalog()
    subcats = catalog.get("subcategories", {})

    results = []
    for sub, names in subcats.items():
        if subcategory and subcategory.lower() not in (sub.lower(), "all"):
            continue
        for n in names:
            comp = catalog.get("by_name", {}).get(n)
            if comp:
                results.append(comp)
    return results


def get_canonical_recipes() -> List[Dict[str, Any]]:
    """Return the canonical wiring recipes discovered across repository definitions."""
    return [
        {
            "id": "space_syntax",
            "name": "Space Syntax Architectural Plan Analysis",
            "domain": "Spatial Networks",
            "description": "Calculates topological mean depth and integration across floorplan rooms.",
            "pipeline": [
                "Floorplan Polylines -> Heteroptera: Center (Centroids)",
                "Floorplan Polylines -> Heteroptera: Topology Of Adjacencies (Cell→Cell)",
                "Cell→Cell + Centroids -> Heteroptera: Reconstruct Topology (Node→Node)",
                "Node→Node + Source Node Slider -> Heteroptera: Space Syntax (Node SpaceSyntax)",
                "Node SpaceSyntax -> Heteroptera: Normalizer -> Color Gradient -> Visual Heatmap",
            ],
            "invariants": [
                "Always pipe Topology Of Adjacencies through Reconstruct Topology before Space Syntax.",
                "Always normalize raw depth values using Normalizer [0.0, 1.0] before color gradients.",
            ],
        },
        {
            "id": "shortest_walk",
            "name": "Shortest Route Navigation on Proximity Network",
            "domain": "Spatial Networks",
            "description": "Calculates shortest metric/topological paths across point clouds.",
            "pipeline": [
                "Spatial Points -> Heteroptera: Proximity Network (Node→Node)",
                "Node→Node + Start + End -> Heteroptera: Shortest Route (Route)",
                "Route + Points -> Heteroptera: Topology Embody -> Shortest Path Curve",
            ],
            "invariants": [
                "Proximity Network requires valid distance threshold to avoid disconnected graphs.",
            ],
        },
        {
            "id": "stochastic_masonry",
            "name": "Attractor-Driven Stochastic Facade & Masonry Allocation",
            "domain": "Parametric Masonry",
            "description": "Applies controlled jitter and varied brick rotation states using probabilistic allocators.",
            "pipeline": [
                "Grid Points -> Attractor Point/Curve -> Distance -> Domain Remap",
                "Mapped Values -> Heteroptera: Careless Range / Weighted Allocator",
                "Weights -> Heteroptera: Slingshot Allocator -> Brick State Index",
                "State Index -> Heteroptera: Symmetric Domain [-θ, +θ] -> Block Rotation",
                "Geometry Stream -> Heteroptera: Stream Freeze / Gate (Execution Lock)",
            ],
            "invariants": [
                "Use Symmetric Domain around 0 to ensure mortar gaps remain structurally stable.",
            ],
        },
    ]
