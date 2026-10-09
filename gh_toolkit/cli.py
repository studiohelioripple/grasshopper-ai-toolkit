"""
gh_toolkit.cli - Command-line interface for the Grasshopper AI Toolkit.
"""

import os
import sys
import argparse

from .core import read_gh_binary, write_gh_binary, read_ghx, write_ghx, GHGraph
from .heteroptera import (
    load_heteroptera_catalog,
    find_heteroptera_component,
    list_heteroptera_components,
    get_canonical_recipes,
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
    live_inject_script,
    live_watch_script,
)
from .builder import GHBuilder



def main():
    parser = argparse.ArgumentParser(
        prog="gh-toolkit",
        description="Grasshopper AI Toolkit - Inspect, convert, and synthesize Grasshopper definitions.",
    )
    subparsers = parser.add_subparsers(dest="cmd", help="Sub-command to execute")

    p_info = subparsers.add_parser("info", help="Inspect file metadata, component list, and canvas parameters")
    p_info.add_argument("file", help="Path to .gh or .ghx file")

    p_to_ghx = subparsers.add_parser("to-ghx", help="Convert .gh binary to human-readable .ghx XML")
    p_to_ghx.add_argument("input", help="Input .gh file")
    p_to_ghx.add_argument("output", help="Output .ghx file")

    p_to_gh = subparsers.add_parser("to-gh", help="Convert .ghx XML to compressed .gh binary")
    p_to_gh.add_argument("input", help="Input .ghx file")
    p_to_gh.add_argument("output", help="Output .gh file")

    p_to_json = subparsers.add_parser("to-json", help="Convert .gh/.ghx to lightweight JSON Graph IR")
    p_to_json.add_argument("input", help="Input file")
    p_to_json.add_argument("output", help="Output .json file")

    p_scripts = subparsers.add_parser("extract-scripts", help="Batch extract embedded Python and C# scripts")
    p_scripts.add_argument("target", help="File or directory of .gh/.ghx files")
    p_scripts.add_argument("--out", "-o", default="./extracted_scripts", help="Output directory")

    p_het = subparsers.add_parser("heteroptera", help="Inspect and audit Heteroptera plugin components & pipelines")
    p_het.add_argument("--list", nargs="?", const="all", help="List components (optional subcategory filter)")
    p_het.add_argument("--info", help="Get detailed input/output schema for a component name or GUID")
    p_het.add_argument("--audit", help="Audit a .gh/.ghx file for Heteroptera components and pipelines")
    p_het.add_argument("--recipes", action="store_true", help="Display canonical Heteroptera wiring recipes")
    p_het.add_argument("--status", action="store_true", help="Check Heteroptera installation status & latest version")
    p_het.add_argument("--install", action="store_true", help="Install or upgrade Heteroptera to latest release via Yak")
    p_het.add_argument("--force", action="store_true", help="Force reinstall even if up to date")

    p_nat = subparsers.add_parser("native", help="Inspect verified native Grasshopper components (212 cataloged)")
    p_nat.add_argument("--list", nargs="?", const="all", help="List native components (optional category filter, e.g. Curve, Surface, Vector, Sets)")
    p_nat.add_argument("--info", help="Get input/output schema for a component name or GUID")

    p_lego = subparsers.add_parser("legopod", help="Inspect verified LegoPod plugin components (42 cataloged)")
    p_lego.add_argument("--list", nargs="?", const="all", help="List LegoPod components (optional subcategory filter)")
    p_lego.add_argument("--info", help="Get input/output schema for a LegoPod component name or GUID")

    p_mag = subparsers.add_parser("magpie", help="Inspect verified Magpie machine-learning components (14 cataloged)")
    p_mag.add_argument("--list", nargs="?", const="all", help="List Magpie components (optional subcategory filter)")
    p_mag.add_argument("--info", help="Get input/output schema for a Magpie component name or GUID")

    p_audit = subparsers.add_parser("audit", help="Audit a .gh/.ghx file across Native, Heteroptera, LegoPod, and Magpie with optimization advice")
    p_audit.add_argument("file", help="Path to .gh or .ghx file")

    p_synth = subparsers.add_parser("synthesize", help="Synthesize ready-to-run canonical definitions and tri-plugin pipelines")
    p_synth.add_argument("template", choices=["spatial-ml", "field-blocks", "space-syntax"], help="Template pipeline to synthesize")
    p_synth.add_argument("--out", "-o", required=True, help="Output path (.gh or .ghx)")
    p_synth.add_argument("--clusters", type=int, default=4, help="Number of clusters for spatial-ml (default: 4)")
    p_synth.add_argument("--source", type=int, default=0, help="Source node index for space syntax (default: 0)")
    p_synth.add_argument("--depth", type=int, default=6, help="Topological search depth for space syntax (default: 6)")

    # Live Rhino / Grasshopper Canvas Integration
    p_live = subparsers.add_parser("live", help="Interact directly with running Rhino 8 and active Grasshopper canvas")
    live_subs = p_live.add_subparsers(dest="live_cmd", help="Live action to execute")

    p_ls = live_subs.add_parser("status", help="Inspect connection to Rhino 8 and active Grasshopper document")

    p_ll = live_subs.add_parser("list", help="List all components, pins, and coordinates on active canvas")
    p_ll.add_argument("--json", action="store_true", help="Output full JSON DAG")

    p_la = live_subs.add_parser("add", help="Add component to active canvas")
    p_la.add_argument("name", help="Component Name or GUID")
    p_la.add_argument("--x", type=float, default=100.0, help="Canvas X coordinate (default: 100)")
    p_la.add_argument("--y", type=float, default=100.0, help="Canvas Y coordinate (default: 100)")
    p_la.add_argument("--name", "-n", dest="nickname", help="Custom NickName")

    p_lr = live_subs.add_parser("remove", help="Remove component from active canvas")
    p_lr.add_argument("target", help="Component Instance GUID, NickName, or Name")

    p_lw = live_subs.add_parser("wire", help="Connect source component output to target component input")
    p_lw.add_argument("source", help="Source component (GUID, NickName, or Name)")
    p_lw.add_argument("target", help="Target component (GUID, NickName, or Name)")
    p_lw.add_argument("--source-pin", "-s", default=0, help="Source output pin (index or name, default: 0)")
    p_lw.add_argument("--target-pin", "-t", default=0, help="Target input pin (index or name, default: 0)")

    p_lu = live_subs.add_parser("unwire", help="Disconnect input wires from target component")
    p_lu.add_argument("target", help="Target component (GUID, NickName, or Name)")
    p_lu.add_argument("--target-pin", "-t", default=0, help="Target input pin (index or name, default: 0)")
    p_lu.add_argument("--source", "-s", help="Optional specific source to disconnect")

    p_lset = live_subs.add_parser("set", help="Set value of Number Slider, Panel, or Boolean Toggle")
    p_lset.add_argument("target", help="Component (GUID, NickName, or Name)")
    p_lset.add_argument("value", help="Value to set")

    p_lsol = live_subs.add_parser("solve", help="Force recomputation of active Grasshopper document and refresh canvas")

    p_lsave = live_subs.add_parser("save", help="Save active Grasshopper document quietly")
    p_lsave.add_argument("path", nargs="?", help="Destination file path (.gh or .ghx)")

    p_lopen = live_subs.add_parser("open", help="Open definition into active Grasshopper canvas")
    p_lopen.add_argument("file", help="Path to .gh or .ghx file")

    p_linj = live_subs.add_parser("inject", help="Inject a Python or C# script file into a script component on the active canvas")
    p_linj.add_argument("target", help="Nickname, name, or instance GUID of script component. Use 'new' to always create.")
    p_linj.add_argument("file", help="Path to the .py or .cs source file to inject")
    p_linj.add_argument("--lang", default="auto", choices=["auto", "python", "csharp"], help="Script language (default: auto-detect)")
    p_linj.add_argument("--x", type=float, default=400.0, help="Canvas X pivot if creating new component")
    p_linj.add_argument("--y", type=float, default=300.0, help="Canvas Y pivot if creating new component")
    p_linj.add_argument("--no-create", action="store_true", help="Error instead of creating if component not found")

    p_lwatch = live_subs.add_parser("watch", help="Watch a script file and hot-reload it into a Grasshopper script component on every save")
    p_lwatch.add_argument("target", help="Nickname, name, or instance GUID of script component. Use 'new' to always create.")
    p_lwatch.add_argument("file", help="Path to the .py or .cs source file to watch")
    p_lwatch.add_argument("--lang", default="auto", choices=["auto", "python", "csharp"], help="Script language (default: auto-detect)")
    p_lwatch.add_argument("--interval", type=float, default=0.5, help="Polling interval in seconds (default: 0.5)")
    p_lwatch.add_argument("--x", type=float, default=400.0, help="Canvas X pivot if creating new component")
    p_lwatch.add_argument("--y", type=float, default=300.0, help="Canvas Y pivot if creating new component")
    p_lwatch.add_argument("--no-create", action="store_true", help="Error instead of creating if component not found")

    args = parser.parse_args()


    if not args.cmd:
        parser.print_help()
        sys.exit(1)

    if args.cmd == "info":
        ext = os.path.splitext(args.file)[1].lower()
        archive = read_ghx(args.file) if ext == ".ghx" else read_gh_binary(args.file)
        graph = GHGraph.from_archive(archive)
        print(f"File:                  {args.file}")
        print(f"Definition Name:       {graph.name}")
        print(f"Total Components:      {len(graph.components)}")
        print(f"Total Wires:           {len(graph.wires)}")
        print("\nCanvas Components Sample:")
        for c in graph.components[:15]:
            print(f"  [{c.comp_id}] {c.name} ('{c.nickname}') - {len(c.inputs)} in, {len(c.outputs)} out")
            if c.script_source:
                print(f"      [Embedded Script: {len(c.script_source)} characters]")

    elif args.cmd == "to-ghx":
        archive = read_gh_binary(args.input)
        write_ghx(archive, args.output)
        print(f"Wrote XML Grasshopper definition to: {args.output}")

    elif args.cmd == "to-gh":
        archive = read_ghx(args.input)
        write_gh_binary(archive, args.output, compress=True)
        print(f"Wrote binary Grasshopper definition to: {args.output}")

    elif args.cmd == "to-json":
        ext = os.path.splitext(args.input)[1].lower()
        archive = read_ghx(args.input) if ext == ".ghx" else read_gh_binary(args.input)
        graph = GHGraph.from_archive(archive)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(graph.to_json())
        print(f"Wrote JSON Graph IR to: {args.output}")

    elif args.cmd == "extract-scripts":
        os.makedirs(args.out, exist_ok=True)
        files = []
        if os.path.isdir(args.target):
            for root, _, fnames in os.walk(args.target):
                for fn in fnames:
                    if fn.lower().endswith((".gh", ".ghx")):
                        files.append(os.path.join(root, fn))
        else:
            files.append(args.target)

        count = 0
        for fpath in files:
            try:
                ext = os.path.splitext(fpath)[1].lower()
                archive = read_ghx(fpath) if ext == ".ghx" else read_gh_binary(fpath)
                graph = GHGraph.from_archive(archive)
                base = os.path.splitext(os.path.basename(fpath))[0]
                for idx, c in enumerate(graph.components):
                    if c.script_source:
                        script_ext = ".cs" if ("using " in c.script_source or "public class" in c.script_source) else ".py"
                        out_name = f"{base}_{c.nickname or c.name}_{idx}{script_ext}"
                        out_name = "".join(ch if ch.isalnum() or ch in "._- " else "_" for ch in out_name)
                        out_path = os.path.join(args.out, out_name)
                        with open(out_path, "w", encoding="utf-8") as sf:
                            sf.write(c.script_source)
                        count += 1
                        print(f"Extracted: {out_name}")
            except Exception as e:
                print(f"Error reading {fpath}: {e}")
        print(f"Done! Extracted {count} script(s) to {args.out}")

    elif args.cmd == "heteroptera":
        if args.status:
            stat = get_heteroptera_status()
            print("=== Heteroptera Plugin Installation Status ===")
            print(f"Yak Package Manager: {'Found (' + str(stat['yak_path']) + ')' if stat['yak_found'] else 'Not Found'}")
            print(f"Installed in Rhino:  {'Yes (version ' + str(stat['installed_version']) + ')' if stat['installed'] else 'No'}")
            print(f"Latest on Yak:       {stat['latest_version'] or 'Unknown / Network error'}")
            print(f"Status:              {'Up to date' if stat['is_latest'] else ('Update Available' if stat['installed'] else 'Missing')}")
            if stat.get("packages_dir"):
                print(f"Package Directory:   {stat['packages_dir']}")
            return

        if args.install:
            print("Checking and installing Heteroptera via McNeel Yak...")
            ok, msg = install_heteroptera(force=args.force)
            print(msg)
            if not ok:
                sys.exit(1)
            return

        catalog = load_heteroptera_catalog()
        if not catalog.get("by_name"):
            print("Error: Heteroptera catalog not found. Please ensure heteroptera_catalog.json exists.")
            sys.exit(1)

        if args.recipes:
            print("=== Canonical Heteroptera Wiring Recipes ===\n")
            recipes = get_canonical_recipes()
            for r in recipes:
                print(f"[{r['name']}] ({r['domain']})")
                print(f"Description: {r['description']}")
                print("Pipeline:")
                for step in r["pipeline"]:
                    print(f"  * {step}")
                print("Invariants:")
                for inv in r["invariants"]:
                    print(f"  ! {inv}")
                print()

        elif args.info:
            comp = find_heteroptera_component(args.info)
            if not comp:
                print(f"Component '{args.info}' not found in Heteroptera catalog.")
                sys.exit(1)
            print(f"Component:    {comp['name']} [{comp.get('nickname', '')}]")
            print(f"GUID:         {comp['guid']}")
            print(f"Subcategory:  {comp.get('subcategory', 'General')}")
            print(f"Type Name:    {comp.get('type_name', '')}")
            print(f"Description:  {comp.get('description', '')}")
            print("\nInputs:")
            for inp in comp.get("inputs", []):
                print(f"  - {inp['name']} ({inp.get('nickname', '')}): {inp.get('type', '')} [{inp.get('access', 'item')}] - {inp.get('description', '')}")
            print("\nOutputs:")
            for outp in comp.get("outputs", []):
                print(f"  - {outp['name']} ({outp.get('nickname', '')}): {outp.get('type', '')} - {outp.get('description', '')}")

        elif args.audit:
            ext = os.path.splitext(args.audit)[1].lower()
            archive = read_ghx(args.audit) if ext == ".ghx" else read_gh_binary(args.audit)
            graph = GHGraph.from_archive(archive)
            guids = {c['guid'].lower(): c for c in catalog.get("by_guid", {}).values()}
            found_het = []
            for c in graph.components:
                cid = c.guid.lower()
                if cid in guids:
                    found_het.append((c, guids[cid]))
            print(f"Audit Results for:          {args.audit}")
            print(f"Total Definition Components: {len(graph.components)}")
            print(f"Heteroptera Components:     {len(found_het)}")
            if found_het:
                by_sub = {}
                for c, meta in found_het:
                    by_sub.setdefault(meta.get('subcategory', 'General'), []).append(c.name)
                for sub, names in sorted(by_sub.items()):
                    print(f"  [{sub}] ({len(names)}): {', '.join(names[:6])}{'...' if len(names) > 6 else ''}")

        elif args.list:
            subcats = catalog.get("subcategories", {})
            filt = args.list.lower()
            print(f"Heteroptera Plugin Catalog ({catalog.get('total_components', 0)} components):\n")
            for sub, names in sorted(subcats.items()):
                if filt != "all" and filt != sub.lower():
                    continue
                print(f"=== {sub} ({len(names)} components) ===")
                for n in sorted(names):
                    meta = catalog.get("by_name", {}).get(n, {})
                    print(f"  * {n} [{meta.get('nickname', '')}] - GUID: {meta.get('guid', '')}")
                print()

    elif args.cmd == "native":
        catalog = load_native_catalog()
        if not catalog.get("by_name"):
            print("Error: Native catalog not found. Please ensure native_catalog.json exists.")
            sys.exit(1)

        if args.info:
            comp = find_native_component(args.info)
            if not comp:
                print(f"Component '{args.info}' not found in native catalog.")
                sys.exit(1)
            print(f"Component:    {comp['name']} [{comp.get('nickname', '')}]")
            print(f"GUID:         {comp['guid']}")
            print(f"Tab:          {comp.get('tab', 'Core')}")
            print(f"Category:     {comp.get('category', 'General')}")
            print(f"Behavior:     {comp.get('behavior', '')}")
            if comp.get("obsolete"):
                print(f"Status:       [OBSOLETE] (Preserved for legacy definitions)")
                if comp.get("superseded_by"):
                    print(f"Replaced By:  {comp['superseded_by']}")
            else:
                print(f"Status:       [ACTIVE] (Generation ready)")
            if comp.get("provenance"):
                print(f"Provenance:   {comp['provenance']}")
            print("\nInputs:")
            for inp in comp.get("inputs", []):
                print(f"  - {inp['name']}")
            print("\nOutputs:")
            for outp in comp.get("outputs", []):
                print(f"  - {outp['name']}")

        elif args.list:
            cats = catalog.get("categories", {})
            filt = args.list.lower() if args.list else "all"
            print(f"Native Grasshopper Catalog ({catalog.get('total_components', 0)} components):\n")
            for cat, names in sorted(cats.items()):
                if filt != "all" and filt != cat.lower():
                    continue
                print(f"=== {cat} ({len(names)} components) ===")
                for n in sorted(names):
                    meta = catalog.get("by_name", {}).get(n, {})
                    print(f"  * {n} [{meta.get('nickname', '')}] - GUID: {meta.get('guid', '')}")
                print()

    elif args.cmd == "legopod":
        catalog = load_legopod_catalog()
        if not catalog.get("by_name"):
            print("Error: LegoPod catalog not found. Please ensure legopod_catalog.json exists.")
            sys.exit(1)

        if args.info:
            comp = find_legopod_component(args.info)
            if not comp:
                print(f"Component '{args.info}' not found in LegoPod catalog.")
                sys.exit(1)
            print(f"Component:    {comp['name']} [{comp.get('nickname', '')}]")
            print(f"GUID:         {comp['guid']}")
            print(f"Category:     {comp.get('category', 'LegoPod')}")
            print(f"Subcategory:  {comp.get('subcategory', 'General')}")
            print(f"Description:  {comp.get('description', '')}")
            print("\nInputs:")
            for inp in comp.get("inputs", []):
                pdesc = f" - {inp['description']}" if inp.get("description") else ""
                print(f"  - {inp['name']} ({inp.get('nickname', '')}): {inp.get('type', 'Generic')} [{inp.get('access', 'item')}]{pdesc}")
            print("\nOutputs:")
            for outp in comp.get("outputs", []):
                pdesc = f" - {outp['description']}" if outp.get("description") else ""
                print(f"  - {outp['name']} ({outp.get('nickname', '')}): {outp.get('type', 'Generic')} [{outp.get('access', 'item')}]{pdesc}")

        elif args.list:
            subcats = catalog.get("subcategories", {})
            filt = args.list.lower() if args.list else "all"
            print(f"LegoPod Plugin Catalog ({catalog.get('total_components', 0)} components):\n")
            for sub, names in sorted(subcats.items()):
                if filt != "all" and filt != sub.lower():
                    continue
                print(f"=== {sub} ({len(names)} components) ===")
                for n in sorted(names):
                    meta = catalog.get("by_name", {}).get(n, {})
                    print(f"  * {n} [{meta.get('nickname', '')}] - GUID: {meta.get('guid', '')}")
                print()

    elif args.cmd == "magpie":
        catalog = load_magpie_catalog()
        if not catalog.get("by_name"):
            print("Error: Magpie catalog not found. Please ensure magpie_catalog.json exists.")
            sys.exit(1)

        if args.info:
            comp = find_magpie_component(args.info)
            if not comp:
                print(f"Component '{args.info}' not found in Magpie catalog.")
                sys.exit(1)
            print(f"Component:    {comp['name']} [{comp.get('nickname', '')}]")
            print(f"GUID:         {comp['guid']}")
            print(f"Category:     {comp.get('category', 'Magpie')}")
            print(f"Subcategory:  {comp.get('subcategory', 'General')}")
            print(f"Description:  {comp.get('description', '')}")
            print("\nInputs:")
            for inp in comp.get("inputs", []):
                pdesc = f" - {inp['description']}" if inp.get("description") else ""
                print(f"  - {inp['name']} ({inp.get('nickname', '')}): {inp.get('type', 'Generic')} [{inp.get('access', 'item')}]{pdesc}")
            print("\nOutputs:")
            for outp in comp.get("outputs", []):
                pdesc = f" - {outp['description']}" if outp.get("description") else ""
                print(f"  - {outp['name']} ({outp.get('nickname', '')}): {outp.get('type', 'Generic')} [{outp.get('access', 'item')}]{pdesc}")

        elif args.list:
            subcats = catalog.get("subcategories", {})
            filt = args.list.lower() if args.list else "all"
            print(f"Magpie Plugin Catalog ({catalog.get('total_components', 0)} components):\n")
            for sub, names in sorted(subcats.items()):
                if filt != "all" and filt != sub.lower():
                    continue
                print(f"=== {sub} ({len(names)} components) ===")
                for n in sorted(names):
                    meta = catalog.get("by_name", {}).get(n, {})
                    print(f"  * {n} [{meta.get('nickname', '')}] - GUID: {meta.get('guid', '')}")
                print()

    elif args.cmd == "audit":
        ext = os.path.splitext(args.file)[1].lower()
        archive = read_ghx(args.file) if ext == ".ghx" else read_gh_binary(args.file)
        graph = GHGraph.from_archive(archive)

        nat_cat = load_native_catalog()
        het_cat = load_heteroptera_catalog()
        lego_cat = load_legopod_catalog()
        mag_cat = load_magpie_catalog()

        nat_guids = {c["guid"].lower(): c for c in nat_cat.get("by_guid", {}).values()}
        het_guids = {c["guid"].lower(): c for c in het_cat.get("by_guid", {}).values()}
        lego_guids = {c["guid"].lower(): c for c in lego_cat.get("by_guid", {}).values()}
        mag_guids = {c["guid"].lower(): c for c in mag_cat.get("by_guid", {}).values()}

        found_nat = []
        found_het = []
        found_lego = []
        found_mag = []
        found_other = []

        for c in graph.components:
            cid = c.guid.lower()
            if cid in nat_guids:
                found_nat.append((c, nat_guids[cid]))
            elif cid in het_guids:
                found_het.append((c, het_guids[cid]))
            elif cid in lego_guids:
                found_lego.append((c, lego_guids[cid]))
            elif cid in mag_guids:
                found_mag.append((c, mag_guids[cid]))
            else:
                found_other.append(c)

        print(f"===============================================================")
        print(f"Comprehensive Audit Report: {os.path.basename(args.file)}")
        print(f"===============================================================")
        print(f"Total Components:           {len(graph.components)}")
        print(f"Total Wires:                {len(graph.wires)}")
        print(f"Embedded Script Components: {sum(1 for c in graph.components if c.script_source)}")
        print(f"\nComponent Ecosystem Breakdown:")
        print(f"  * Native Grasshopper:     {len(found_nat):3d} components")
        print(f"  * Heteroptera:            {len(found_het):3d} components")
        print(f"  * LegoPod:                {len(found_lego):3d} components")
        print(f"  * Magpie ML:              {len(found_mag):3d} components")
        print(f"  * Third-Party / Unknown:  {len(found_other):3d} components")

        if found_het:
            print("\nHeteroptera Components Present:")
            for c, m in found_het:
                print(f"  - {m['name']} ({m.get('subcategory', 'General')})")

        if found_lego:
            print("\nLegoPod Components Present:")
            for c, m in found_lego:
                print(f"  - {m['name']} ({m.get('subcategory', 'General')})")

        if found_mag:
            print("\nMagpie Machine Learning Components Present:")
            for c, m in found_mag:
                print(f"  - {m['name']} ({m.get('subcategory', 'General')})")

        found_obsolete = [pair for pair in found_nat if pair[1].get("obsolete")]
        if found_obsolete:
            print(f"\nLegacy / Obsolete Components Detected ({len(found_obsolete)}):")
            for c, m in found_obsolete:
                rep = m.get("superseded_by", "N/A")
                print(f"  [OBSOLETE] {m['name']} (GUID: {m['guid']}) -> Active Replacement: {rep}")

        print("\nOptimization & Architectural Advice:")
        advice_count = 0
        names = [c.name.lower() for c in graph.components]

        if found_obsolete:
            print(f"  [!] Obsolete components detected: Upgrade {len(found_obsolete)} legacy component(s) to modern Grasshopper 8 active GUIDs for future-proof definitions.")
            advice_count += 1

        # Heteroptera advice
        if "distance" in names and not any("adjacen" in n or "topology" in n for n in names):
            print("  [!] Distance-matrix network detected: Consider replacing bulky native Distance/SmallerThan chains with Heteroptera 'Topology Of Adjacencies' + 'Reconstruct Topology'.")
            advice_count += 1
        if any("space syntax" in n for n in names) and not any("normaliz" in n for n in names):
            print("  [!] Space Syntax detected without Normalizer: Pipe Space Syntax scores through Heteroptera 'Normalizer' [0.0, 1.0] before color gradients or scaling.")
            advice_count += 1

        # LegoPod advice
        if len(graph.components) > 10 and not found_lego:
            print("  [!] No LegoPod metadata packaging detected: Consider using LegoPod 'User Dictionary' and 'Build Attribute' to attach analytical results to Rhino geometry.")
            advice_count += 1

        # Magpie advice
        if any(c.script_source and ("cluster" in c.script_source.lower() or "pca" in c.script_source.lower() or "kmeans" in c.script_source.lower()) for c in graph.components):
            print("  [!] Custom script clustering detected: Consider replacing custom Python scripts with Magpie 'Clustering Machine' or 'PCA Machine' for zero-dependency native execution.")
            advice_count += 1

        if advice_count == 0:
            print("  [+] Graph structure adheres to clean architectural and algorithmic invariants.")
        print()

    elif args.cmd == "synthesize":
        builder = GHBuilder(name=f"Synthesized_{args.template.title().replace('-', '')}")
        if args.template == "spatial-ml":
            builder.add_spatial_ml_metadata_pipeline(
                cluster_count=args.clusters,
                source_node=args.source,
                depth=args.depth
            )
        elif args.template == "field-blocks":
            builder.add_generative_field_block_pipeline()
        elif args.template == "space-syntax":
            builder.add_space_syntax_pipeline()

        out_ext = os.path.splitext(args.out)[1].lower()
        if out_ext == ".gh":
            builder.save_gh(args.out)
        else:
            builder.save_ghx(args.out)
        print(f"Synthesized '{args.template}' definition with {builder.object_count} components -> {args.out}")

    elif args.cmd == "live":
        if not args.live_cmd:
            print("Usage: gh-toolkit live {status,list,add,remove,wire,unwire,set,solve,save,open,inject,watch} ...")
            sys.exit(1)

        if args.live_cmd == "status":
            st = live_status()
            if not st.get("rhino_running"):
                print("❌ Rhino 8 is NOT connected.")
                print(f"   Reason: {st.get('error', 'Unknown error')}")
                print("   Tip: In Rhino 8 command line, run 'StartScriptServer' to enable external scripting.")
                sys.exit(1)
            print("⚡ Rhino 8 Live Connection Active:")
            print(f"   Rhino Version:     {st.get('rhino_version')}")
            print(f"   Rhino Active Doc:  {st.get('rhino_doc')}")
            act = st.get("active_document")
            if act:
                print(f"   Grasshopper Doc:   {act.get('name')} ({'Modified' if act.get('modified') else 'Clean'})")
                print(f"   Object Count:      {act.get('object_count')} canvas objects")
                if act.get('file_path'):
                    print(f"   Saved Path:        {act.get('file_path')}")
            else:
                print("   Grasshopper Doc:   No document open on canvas.")

        elif args.live_cmd == "list":
            res = live_list_objects()
            if "error" in res:
                print(f"❌ Error: {res['error']}")
                sys.exit(1)
            if getattr(args, "json", False):
                import json
                print(json.dumps(res, indent=2))
            else:
                print(f"📋 Live Canvas: {res.get('doc_name')} ({res.get('total_objects')} objects)\n")
                print(f"{'GUID (Prefix)':<16} {'Name':<24} {'NickName':<14} {'Pivot (X, Y)':<18} {'Inputs':<8} {'Outputs':<8}")
                print("-" * 90)
                for o in res.get("objects", []):
                    short_id = o['instance_guid'][:8]
                    inputs_count = len(o.get('inputs', []))
                    outputs_count = len(o.get('outputs', []))
                    pivot_str = f"({o['pivot'][0]}, {o['pivot'][1]})"
                    print(f"{short_id:<16} {o['name'][:23]:<24} {o['nickname'][:13]:<14} {pivot_str:<18} {inputs_count:<8} {outputs_count:<8}")
                    if "value" in o:
                        print(f"    ↳ Value: {o['value']}")

        elif args.live_cmd == "add":
            res = live_add_component(args.name, x=args.x, y=args.y, nickname=args.nickname)
            if not res.get("success"):
                print(f"❌ Failed to add component: {res.get('error')}")
                sys.exit(1)
            print(f"✅ Added '{res.get('name')}' to canvas at ({args.x}, {args.y})")
            print(f"   Instance GUID: {res.get('instance_guid')}")

        elif args.live_cmd == "remove":
            res = live_remove_object(args.target)
            if not res.get("success"):
                print(f"❌ Failed to remove component: {res.get('error')}")
                sys.exit(1)
            print(f"✅ Removed {res.get('removed_count')} component(s) from canvas.")

        elif args.live_cmd == "wire":
            # Allow integer pin or string pin
            s_pin = int(args.source_pin) if str(args.source_pin).isdigit() else args.source_pin
            t_pin = int(args.target_pin) if str(args.target_pin).isdigit() else args.target_pin
            res = live_wire(args.source, args.target, source_pin=s_pin, target_pin=t_pin)
            if not res.get("success"):
                print(f"❌ Failed to connect wire: {res.get('error')}")
                sys.exit(1)
            src = res.get("source", {})
            dst = res.get("target", {})
            print(f"✅ Connected: {src.get('name')}[{src.get('output')}] ──▶ {dst.get('name')}[{dst.get('input')}]")

        elif args.live_cmd == "unwire":
            t_pin = int(args.target_pin) if str(args.target_pin).isdigit() else args.target_pin
            res = live_unwire(args.target, target_pin=t_pin, source_id_or_name=args.source)
            if not res.get("success"):
                print(f"❌ Failed to disconnect wire: {res.get('error')}")
                sys.exit(1)
            print(f"✅ Disconnected {res.get('disconnected_count')} wire(s) from {res.get('target')}[{res.get('input')}].")

        elif args.live_cmd == "set":
            res = live_set_value(args.target, args.value)
            if not res.get("success"):
                print(f"❌ Failed to set value: {res.get('error')}")
                sys.exit(1)
            print(f"✅ Updated {res.get('type')} '{res.get('object')}' value to: {res.get('new_value')}")

        elif args.live_cmd == "solve":
            res = live_solve()
            if not res.get("success"):
                print(f"❌ Failed to solve canvas: {res.get('error')}")
                sys.exit(1)
            print(f"✅ Solved document '{res.get('doc_name')}' ({res.get('objects_count')} objects) and refreshed canvas.")

        elif args.live_cmd == "save":
            res = live_save(filepath=args.path)
            if not res.get("success"):
                print(f"❌ Failed to save document: {res.get('error')}")
                sys.exit(1)
            print(f"✅ Saved live Grasshopper definition to: {res.get('file_path')}")

        elif args.live_cmd == "open":
            res = live_open(args.file)
            if not res.get("success"):
                print(f"❌ Failed to open document: {res.get('error')}")
                sys.exit(1)
            print(f"✅ Opened '{res.get('doc_name')}' ({res.get('objects_count')} objects) on live canvas.")

        elif args.live_cmd == "inject":
            if not os.path.exists(args.file):
                print(f"❌ Script file not found: {args.file}")
                sys.exit(1)
            with open(args.file, "r", encoding="utf-8") as f:
                code = f.read()
            res = live_inject_script(
                target=args.target,
                code=code,
                lang=args.lang,
                add_if_missing=not args.no_create,
                pivot=(args.x, args.y),
            )
            if not res.get("success"):
                print(f"❌ Inject failed: {res.get('error')}")
                sys.exit(1)
            action = res.get("action", "updated")
            guid = res.get("instance_guid", "?")
            lang_used = res.get("lang", args.lang)
            print(f"✅ Script {action} on canvas  [{lang_used}]  GUID: {guid}")
            print(f"   Source: {os.path.abspath(args.file)}")

        elif args.live_cmd == "watch":
            live_watch_script(
                target=args.target,
                filepath=args.file,
                lang=args.lang,
                add_if_missing=not args.no_create,
                pivot=(args.x, args.y),
                interval=args.interval,
            )


if __name__ == "__main__":
    main()

