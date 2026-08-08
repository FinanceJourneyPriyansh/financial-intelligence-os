"""
Financial Intelligence OS (FIOS)
Main launcher.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "01_src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from fios_live.kernel.kernel import Kernel


def main() -> None:
    print()
    print("=" * 70)
    print("        FINANCIAL INTELLIGENCE OS (FIOS)")
    print("               KERNEL BOOT")
    print("=" * 70)

    Kernel().start()


if __name__ == "__main__":
    main()