"""
Financial Intelligence OS
Main CLI
"""

import argparse
from pathlib import Path


ROOT = Path(__file__).parent


def init():
    print("=" * 60)
    print("Initializing Financial Intelligence OS")
    print("=" * 60)
    print(f"Project Root : {ROOT}")


def scaffold():

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


def doctor():

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


parser = argparse.ArgumentParser(
    prog="FIOS",
    description="Financial Intelligence Operating System",
)

sub = parser.add_subparsers(dest="command")

sub.add_parser("init")
sub.add_parser("scaffold")
sub.add_parser("doctor")

args = parser.parse_args()

if args.command == "init":
    init()

elif args.command == "scaffold":
    scaffold()

elif args.command == "doctor":
    doctor()

else:
    parser.print_help()