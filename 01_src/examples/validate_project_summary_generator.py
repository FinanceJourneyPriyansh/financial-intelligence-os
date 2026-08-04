"""
Financial Intelligence OS
Project Summary Generator Validation

Purpose
-------
Validate the Project Summary Generator by
generating the Project_Summary.md artifact.
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

from platform_core.generators.project_summary_generator import (
    ProjectSummaryGenerator,
)
from platform_core.generators.yaml_loader import YAMLLoader


def main() -> None:
    """
    Execute Project Summary Generator validation.
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
    print("Project Summary Generator Validation")
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

    print(
        "Initializing Project Summary Generator..."
    )

    generator = ProjectSummaryGenerator(
        output_directory=output_directory,
        template_directory=template_directory,
    )

    print("Generating Project_Summary.md...")
    print()

    output_file = generator.generate(
        template_name="03_project_summary.md.j2",
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
    print(
        "Project Summary Generator Validation Completed"
    )
    print("=" * 60)


if __name__ == "__main__":
    main()