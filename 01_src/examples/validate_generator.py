"""
Financial Intelligence OS
Generator Platform Validation

Purpose
-------
Validate the complete Financial Intelligence OS
Generator Platform before executing project
generation workflows.
"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def check(path: Path) -> bool:
    """
    Check whether a file or directory exists.
    """

    exists = path.exists()

    status = "PASS" if exists else "FAIL"

    print(
        f"[{status}] {path.relative_to(ROOT)}"
    )

    return exists


def main() -> None:
    """
    Execute Generator Platform validation.
    """

    print("=" * 60)
    print("Financial Intelligence OS")
    print("Generator Platform Validation")
    print("=" * 60)
    print()

    paths = [

        # --------------------------------------------------
        # Control Center
        # --------------------------------------------------

        ROOT / "00_control_center",

        ROOT / "00_control_center"
        / "00_core",

        ROOT / "00_control_center"
        / "01_blueprint",

        ROOT / "00_control_center"
        / "05_templates",

        ROOT / "00_control_center"
        / "05_templates"
        / "00_python",

        ROOT / "00_control_center"
        / "05_templates"
        / "02_repository",

        ROOT / "00_control_center"
        / "05_templates"
        / "02_repository"
        / "00_readme.md.j2",

        # --------------------------------------------------
        # Generator Platform
        # --------------------------------------------------

        ROOT / "01_src"
        / "platform_core",

        ROOT / "01_src"
        / "platform_core"
        / "generators",

        ROOT / "01_src"
        / "platform_core"
        / "generators"
        / "base_generator.py",

        ROOT / "01_src"
        / "platform_core"
        / "generators"
        / "folder_generator.py",

        ROOT / "01_src"
        / "platform_core"
        / "generators"
        / "yaml_generator.py",

        ROOT / "01_src"
        / "platform_core"
        / "generators"
        / "yaml_loader.py",

        ROOT / "01_src"
        / "platform_core"
        / "generators"
        / "template_loader.py",

        ROOT / "01_src"
        / "platform_core"
        / "generators"
        / "readme_generator.py",

        ROOT / "01_src"
        / "platform_core"
        / "generators"
        / "generator_manager.py",

        ROOT / "01_src"
        / "platform_core"
        / "generators"
        / "__init__.py",
    ]

    passed = 0

    for path in paths:

        if check(path):
            passed += 1

    print()
    print("-" * 60)

    print(
        f"Validation Result : {passed}/{len(paths)}"
    )

    if passed == len(paths):

        print("Status            : SUCCESS")

    else:

        print("Status            : FAILED")

    print("=" * 60)


if __name__ == "__main__":
    main()