"""
Financial Intelligence OS (FIOS)
Command Line Interface
"""

from __future__ import annotations

import sys
from pathlib import Path

import typer


# Repository root:
# <root>/01_src/fios/cli.py -> parents[2] == <root>
ROOT = Path(__file__).resolve().parents[2]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fios_live.kernel.kernel import Kernel


app = typer.Typer(
    help="Financial Intelligence OS",
    no_args_is_help=True,
)


@app.callback()
def main() -> None:
    """
    Financial Intelligence OS CLI.
    """
    pass


@app.command()
def build() -> None:
    """
    Start the canonical FIOS Kernel runtime.
    """
    Kernel().start()


if __name__ == "__main__":
    app()