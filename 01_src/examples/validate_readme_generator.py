"""
Financial Intelligence OS
README Generator Validation

Purpose
-------
Validate the complete README generation workflow
using the Financial Intelligence OS Blueprint.
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

from platform_core.generators.readme_generator import ReadmeGenerator
from platform_core.generators.yaml_loader import YAMLLoader


def main() -> None:
    """
    Execute README Generator validation.
    """

    core_directory = (
        ROOT
        / "00_control_center"
        / "00_core"
    )

    blueprint_directory = (
        ROOT
        / "00_control_center"
        / "01_blueprint"
    )

    template_directory = (
        ROOT
        / "00_control_center"
        / "05_templates"
        / "02_repository"
    )

    output_directory = (
        ROOT
        / "08_reports"
    )

    print("=" * 60)
    print("Financial Intelligence OS")
    print("README Generator Validation")
    print("=" * 60)
    print()

    print("Loading Blueprint...")

    loader = YAMLLoader()

    context = loader.load_blueprint(
        core_directory,
        blueprint_directory,
    )

    print(
        f"Loaded {len(context)} YAML objects."
    )

    print()

    print("Initializing README Generator...")

    generator = ReadmeGenerator(
        output_directory=output_directory,
        template_directory=template_directory,
    )

    print("Generating README.md...")
    print()

    output_file = generator.generate(
        template_name="00_readme.md.j2",
        context=context,
    )

    print("Generation Successful.")
    print()

    print(f"Generated File : {output_file}")
    print(f"Exists         : {output_file.exists()}")

    if output_file.exists():

        print(
            f"File Size      : "
            f"{output_file.stat().st_size:,} bytes"
        )

    print()
    print("=" * 60)
    print("README Generator Validation Completed")
    print("=" * 60)


if __name__ == "__main__":
    main()