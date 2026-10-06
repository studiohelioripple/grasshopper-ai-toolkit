"""
Grasshopper AI Toolkit - Zero-dependency Python library for Rhino Grasshopper definitions.
"""

from .core import (
    GHArchive,
    GHChunk,
    GHItem,
    GHGraph,
    GHComponent,
    read_gh_binary,
    write_gh_binary,
    read_ghx,
    write_ghx,
    TYPE_MAP,
    NAME_TO_TYPE,
)
from .builder import GHBuilder
from .heteroptera import (
    load_heteroptera_catalog,
    find_heteroptera_component,
    list_heteroptera_components,
    get_canonical_recipes,
)

__version__ = "0.2.0"
__all__ = [
    "GHArchive",
    "GHChunk",
    "GHItem",
    "GHGraph",
    "GHComponent",
    "read_gh_binary",
    "write_gh_binary",
    "read_ghx",
    "write_ghx",
    "GHBuilder",
    "load_heteroptera_catalog",
    "find_heteroptera_component",
    "list_heteroptera_components",
    "get_canonical_recipes",
    "TYPE_MAP",
    "NAME_TO_TYPE",
]
