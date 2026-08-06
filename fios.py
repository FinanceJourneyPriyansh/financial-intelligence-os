"""
============================================================
Financial Intelligence OS (FIOS)
Main Command Line Interface
============================================================

Purpose:
    Primary command-line entry point for FIOS.

Supported Commands:
    - init
    - scaffold
    - doctor
    - build
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).parent

# Allow imports from 01_src
sys.path.insert(0, str(ROOT / "01_src"))

from platform_core.integration.builder_integration_manager import (  # noqa: E402
    BuilderIntegrationManager,
)


def init() -> None:
    """
    Initialize the Financial Intelligence OS.
    """

    print("=" * 60)
    print("Initializing Financial Intelligence OS")
    print("=" * 60)
    print(f"Project Root : {ROOT}")


def scaffold() -> None:
    """
    Create the FIOS project directory structure.
    """

    folders = [
        "00_control_center",
        "01_src",
        "02_data",
        "03_docs",
        "04_tests",
        "05_dashboards",
        "06_models",
        "07_notebooks",
        "08_reports",
        "09_logs",
    ]

    print("\nCreating Project Structure...\n")

    for folder in folders:
        path = ROOT / folder
        path.mkdir(exist_ok=True)
        print(f"[OK] {folder}")

    print("\nProject Structure Ready.\n")


def doctor() -> None:
    """
    Verify the FIOS project structure.
    """

    print("\nFIOS Doctor\n")

    folders = [
        "00_control_center",
        "01_src",
        "02_data",
        "03_docs",
        "04_tests",
        "05_dashboards",
        "06_models",
        "07_notebooks",
        "08_reports",
        "09_logs",
    ]

    for folder in folders:

        if (ROOT / folder).exists():
            print(f"[PASS] {folder}")
        else:
            print(f"[FAIL] {folder}")


def build() -> None:
    """
    Execute the Builder Runtime.
    """

    print("=" * 60)
    print("Financial Intelligence OS")
    print("Builder Runtime")
    print("=" * 60)

    state_path = (
    ROOT
    / "00_control_center"
    / "02_configs"
    / "10_builder_state.yaml"
    )

    manager = BuilderIntegrationManager(
        builder_state_path=state_path,
    )

    result = manager.execute()

    if result.success:
        print("\n[PASS] Builder Runtime completed successfully.")

    else:
        print("\n[FAIL] Builder Runtime failed.")


def main() -> None:
    """
    Entry point for the FIOS CLI.
    """

    parser = argparse.ArgumentParser(
        prog="FIOS",
        description="Financial Intelligence Operating System",
    )

    sub = parser.add_subparsers(dest="command")

    sub.add_parser("init")
    sub.add_parser("scaffold")
    sub.add_parser("doctor")
    sub.add_parser("build")

    args = parser.parse_args()

    if args.command == "init":
        init()

    elif args.command == "scaffold":
        scaffold()

    elif args.command == "doctor":
        doctor()

    elif args.command == "build":
        build()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()