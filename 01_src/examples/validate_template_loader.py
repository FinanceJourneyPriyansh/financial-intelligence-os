"""
Financial Intelligence OS
Template Loader Validation

Purpose
-------
Validate the Financial Intelligence OS Template Loader
and Repository Template Library.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# Make platform_core importable
sys.path.insert(
    0,
    str(ROOT / "01_src"),
)

from platform_core.generators.template_loader import TemplateLoader


def main() -> None:
    """
    Execute Template Loader validation.
    """

    template_directory = (
        ROOT
        / "00_control_center"
        / "05_templates"
        / "02_repository"
    )

    print("=" * 60)
    print("Financial Intelligence OS")
    print("Template Loader Validation")
    print("=" * 60)
    print()

    loader = TemplateLoader(
        template_directory,
    )

    template_name = "00_readme.md.j2"

    exists = loader.exists(
        template_name,
    )

    print(
        f"Template Exists : {exists}"
    )

    print()

    templates = loader.list_templates()

    print(
        f"Templates Found : {len(templates)}"
    )

    print()
    print("Repository Templates")
    print("-" * 60)

    for template in templates:
        print(f"• {template}")

    print()
    print("-" * 60)

    if exists:

        print("Validation Status : SUCCESS")

    else:

        print("Validation Status : FAILED")

    print("=" * 60)


if __name__ == "__main__":
    main()