"""
Financial Intelligence OS
YAML Loader Validation

Purpose
-------
Validate the Financial Intelligence OS YAML Loader
by loading the complete blueprint context.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# Add Generator Platform to Python path
sys.path.insert(
    0,
    str(ROOT / "01_src" / "platform_core"),
)

from generators.yaml_loader import YAMLLoader


def main() -> None:
    """
    Execute YAML Loader validation.
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

    print("=" * 60)
    print("Financial Intelligence OS")
    print("YAML Loader Validation")
    print("=" * 60)
    print()

    loader = YAMLLoader()

    context = loader.load_blueprint(
        core_directory,
        blueprint_directory,
    )

    print(
        f"Loaded {len(context)} YAML objects."
    )

    print()
    print("Top Level Objects")
    print("-" * 60)

    for key in sorted(context.keys()):
        print(f"• {key}")

    print()
    print("-" * 60)
    print("Validation Successful")
    print("=" * 60)


if __name__ == "__main__":
    main()