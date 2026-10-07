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


def find_yak() -> Optional[str]:
    """Locate the McNeel Yak package manager executable across standard paths."""
    import shutil
    candidates = [
        shutil.which("yak"),
        "/Applications/Rhino 8.app/Contents/Resources/bin/yak",
        "/Applications/Rhino 7.app/Contents/Resources/bin/yak",
        os.path.expanduser("~/Library/Application Support/McNeel/Rhinoceros/8.0/yak"),
        r"C:\Program Files\Rhino 8\System\yak.exe",
        r"C:\Program Files\Rhino 7\System\yak.exe",
    ]
    for c in candidates:
        if c and os.path.exists(c):
            return c
    return None


def get_heteroptera_status() -> Dict[str, Any]:
    """Check whether Heteroptera is installed via Yak or in Grasshopper Libraries, and what version is available."""
    import subprocess
    import re

    yak_bin = find_yak()
    status: Dict[str, Any] = {
        "yak_found": yak_bin is not None,
        "yak_path": yak_bin,
        "installed": False,
        "installed_version": None,
        "latest_version": None,
        "is_latest": False,
        "packages_dir": None,
    }

    mac_pkg_dir = os.path.expanduser("~/Library/Application Support/McNeel/Rhinoceros/packages/8.0/Heteroptera")
    if os.path.exists(mac_pkg_dir):
        status["packages_dir"] = mac_pkg_dir
        try:
            versions = [
                d for d in os.listdir(mac_pkg_dir)
                if os.path.isdir(os.path.join(mac_pkg_dir, d)) and not d.startswith(".")
            ]
            if versions:
                def v_key(v_str):
                    return [int(x) if x.isdigit() else 0 for x in re.findall(r"\d+", v_str)]
                versions.sort(key=v_key, reverse=True)
                status["installed"] = True
                status["installed_version"] = versions[0]
        except Exception:
            pass

    if not yak_bin:
        return status

    try:
        res = subprocess.run([yak_bin, "list"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=10)
        if res.returncode == 0:
            m = re.search(r"Heteroptera\s+\(([\d\.]+)\)", res.stdout, re.IGNORECASE)
            if m:
                status["installed"] = True
                status["installed_version"] = m.group(1)
    except Exception:
        pass

    try:
        res = subprocess.run([yak_bin, "search", "heteroptera"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=15)
        if res.returncode == 0:
            m = re.search(r"Heteroptera\s+\(([\d\.]+)\)", res.stdout, re.IGNORECASE)
            if m:
                status["latest_version"] = m.group(1)
    except Exception:
        pass

    if status["installed_version"] and status["latest_version"]:
        status["is_latest"] = (status["installed_version"] == status["latest_version"])
    elif status["installed"] and not status["latest_version"]:
        status["is_latest"] = True

    return status


def install_heteroptera(force: bool = False) -> Tuple[bool, str]:
    """Install or upgrade the latest Heteroptera package via Yak."""
    import subprocess

    yak_bin = find_yak()
    if not yak_bin:
        return False, "McNeel Yak package manager not found. Please verify Rhino 7 or 8 is installed."

    status = get_heteroptera_status()
    if status["installed"] and status["is_latest"] and not force:
        return True, f"Heteroptera is already up to date (version {status['installed_version']})."

    try:
        cmd = [yak_bin, "install", "Heteroptera"]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=60)
        if res.returncode == 0:
            new_status = get_heteroptera_status()
            ver = new_status.get("installed_version", "latest")
            return True, f"Successfully installed Heteroptera ({ver}) via {yak_bin}."
        else:
            err = res.stderr.strip() or res.stdout.strip()
            return False, f"Yak install failed: {err}"
    except Exception as e:
        return False, f"Exception during installation: {e}"

