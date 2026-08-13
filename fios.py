"""
Financial Intelligence OS (FIOS)
Main launcher.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "01_src"
LOGS = ROOT / "09_logs"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


def _configure_output() -> None:
    """
    Keep FIOS alive when launched by pythonw.exe.

    pythonw.exe has no console stdout/stderr, so redirect output
    to the existing FIOS log directory.
    """
    if sys.stdout is None:
        LOGS.mkdir(parents=True, exist_ok=True)

        sys.stdout = open(
            LOGS / "fios_stdout.log",
            "a",
            encoding="utf-8",
            buffering=1,
        )

    if sys.stderr is None:
        LOGS.mkdir(parents=True, exist_ok=True)

        sys.stderr = open(
            LOGS / "fios_stderr.log",
            "a",
            encoding="utf-8",
            buffering=1,
        )


_configure_output()

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
