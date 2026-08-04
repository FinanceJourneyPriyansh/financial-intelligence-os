"""
Financial Intelligence OS
Generator Manager Validation

Purpose
-------
Validate the complete Financial Intelligence OS
Generator Engine by generating every repository
artifact through the Generator Manager.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

sys.path.insert(
    0,
    str(ROOT / "01_src"),
)

from platform_core.generators.generator_manager import (
    GeneratorManager,
)


def main() -> None:

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
    print("Generator Manager Validation")
    print("=" * 60)
    print()

    manager = GeneratorManager(
        output_directory=output_directory,
        template_directory=template_directory,
        core_directory=core_directory,
        blueprint_directory=blueprint_directory,
    )

    print("Registered Generators\n")

    for name in manager.available_generators():
        print(f" - {name}")

    print()
    print("=" * 60)
    print("Generating All Artifacts")
    print("=" * 60)
    print()

    outputs = manager.generate_all()

    passed = 0

    for name, output in outputs.items():

        exists = output.exists()

        status = "PASS" if exists else "FAIL"

        print(
            f"[{status}] "
            f"{name:<20}"
            f"{output.name}"
        )

        if exists:
            passed += 1

    print()
    print("=" * 60)

    print(
        f"Artifacts Generated : "
        f"{passed}/{len(outputs)}"
    )

    if passed == len(outputs):

        print(
            "Generator Engine Validation Successful."
        )

    else:

        print(
            "Generator Engine Validation Failed."
        )

    print("=" * 60)


if __name__ == "__main__":
    main()