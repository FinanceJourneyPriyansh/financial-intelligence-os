"""
Financial Intelligence OS (FIOS)

Command Line Interface
"""

from __future__ import annotations

import typer

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
    Build the Financial Intelligence OS project.
    """
    typer.echo("FIOS Builder Runtime started.")


if __name__ == "__main__":
    app()