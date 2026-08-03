"""
Financial Intelligence OS
Installation Verification

Purpose
-------
Verify that the Financial Intelligence OS environment
is correctly installed before execution.
"""

import importlib

REQUIRED_PACKAGES = [
    "pandas",
    "numpy",
    "yfinance",
    "requests",
    "dotenv",
]


def verify_package(package_name: str) -> bool:
    """
    Verify that a package is installed.
    """

    try:
        importlib.import_module(package_name)
        print(f"✓ {package_name}")
        return True

    except ImportError:
        print(f"✗ {package_name}")
        return False


def verify_installation() -> bool:
    """
    Verify all required project dependencies.
    """

    print("=" * 70)
    print("Financial Intelligence OS")
    print("Installation Verification")
    print("=" * 70)

    success = True

    for package in REQUIRED_PACKAGES:
        if not verify_package(package):
            success = False

    print()

    if success:
        print("✓ All required packages are installed.")
    else:
        print("✗ Installation verification failed.")

    print("=" * 70)

    return success


if __name__ == "__main__":
    verify_installation()