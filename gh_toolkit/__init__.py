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
    find_yak,
    get_heteroptera_status,
    install_heteroptera,
)
from .native import (
    load_native_catalog,
    find_native_component,
    list_native_components,
)
from .legopod import (
    load_legopod_catalog,
    find_legopod_component,
    list_legopod_components,
)
from .magpie import (
    load_magpie_catalog,
    find_magpie_component,
    list_magpie_components,
)
from .live import (
    is_rhino_running,
    get_rhino_instances,
    live_status,
    live_list_objects,
    live_add_component,
    live_remove_object,
    live_wire,
    live_unwire,
    live_set_value,
    live_solve,
    live_save,
    live_open,
)

__version__ = "0.4.0"
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
    "find_yak",
    "get_heteroptera_status",
    "install_heteroptera",
    "load_native_catalog",
    "find_native_component",
    "list_native_components",
    "load_legopod_catalog",
    "find_legopod_component",
    "list_legopod_components",
    "load_magpie_catalog",
    "find_magpie_component",
    "list_magpie_components",
    "is_rhino_running",
    "get_rhino_instances",
    "live_status",
    "live_list_objects",
    "live_add_component",
    "live_remove_object",
    "live_wire",
    "live_unwire",
    "live_set_value",
    "live_solve",
    "live_save",
    "live_open",
    "TYPE_MAP",
    "NAME_TO_TYPE",
]

