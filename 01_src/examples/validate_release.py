"""
Financial Intelligence OS
Release Validation

Purpose
-------
Run the complete Financial Intelligence OS
Milestone Release Validation.

This validator executes every major validation
required before committing a milestone.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

VALIDATIONS = [
    "validate_generator.py",
    "validate_yaml_loader.py",
    "validate_template_loader.py",
    "validate_readme_generator.py",
    "validate_repository_structure_generator.py",
    "validate_architecture_generator.py",
    "validate_project_summary_generator.py",
    "validate_blueprint_overview_generator.py",
    "validate_technology_stack_generator.py",
    "validate_roadmap_generator.py",
    "validate_generator_manager.py",
]


def main() -> None:

    print("=" * 70)
    print("FINANCIAL INTELLIGENCE OS")
    print("MILESTONE 2 RELEASE VALIDATION")
    print("=" * 70)
    print()

    passed = 0

    for validation in VALIDATIONS:

        print("-" * 70)
        print(f"Running : {validation}")
        print("-" * 70)

        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "01_src" / "examples" / validation),
            ]
        )

        if result.returncode == 0:

            print(f"[PASS] {validation}\n")
            passed += 1

        else:

            print(f"[FAIL] {validation}\n")

    print("=" * 70)

    print(
        f"Validation Summary : "
        f"{passed}/{len(VALIDATIONS)} Passed"
    )

    if passed == len(VALIDATIONS):

        print()
        print("RELEASE STATUS")
        print("READY TO COMMIT")

    else:

        print()
        print("RELEASE STATUS")
        print("VALIDATION FAILED")

    print("=" * 70)


if __name__ == "__main__":
    main()