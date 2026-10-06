#!/usr/bin/env python3
"""
Example 01: Synthesize a Complete Space Syntax Analysis Pipeline.

Demonstrates programmatic Grasshopper definition synthesis using gh_toolkit
and the Heteroptera plugin.
"""

import os
import sys

# Ensure local package is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from gh_toolkit import GHBuilder


def main():
    print("Synthesizing Space Syntax Analysis Pipeline...")
    builder = GHBuilder(name="SpaceSyntaxAnalysis")

    # Add the canonical pipeline
    pipeline_ids = builder.add_space_syntax_pipeline(start_pivot=(100, 100))
    print(f"Added {len(pipeline_ids)} pipeline components:")
    for role, comp_id in pipeline_ids.items():
        print(f"  * {role:12} -> {comp_id}")

    output_dir = os.path.join(os.path.dirname(__file__), "outputs")
    os.makedirs(output_dir, exist_ok=True)

    ghx_path = os.path.join(output_dir, "spacesyntax.ghx")
    gh_path = os.path.join(output_dir, "spacesyntax.gh")

    builder.save_ghx(ghx_path)
    builder.save_gh(gh_path)

    print(f"\nGenerated files:")
    print(f"  - XML Definition:    {ghx_path}")
    print(f"  - Binary Definition: {gh_path}")
    print("\nDouble-click either file to open directly in Rhino 8!")


if __name__ == "__main__":
    main()
