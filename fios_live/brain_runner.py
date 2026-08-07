"""
============================================================
Financial Intelligence OS (FIOS)
Repository Brain Runner
============================================================
"""

from __future__ import annotations

from pathlib import Path

from fios_live.brain.repository_brain import RepositoryBrain
from fios_live.brain.repository_report import RepositoryReport


def main() -> None:

    print("=" * 60)
    print("FINANCIAL INTELLIGENCE OS (FIOS)")
    print("REPOSITORY BRAIN")
    print("=" * 60)
    print()

    brain = RepositoryBrain()

    state = brain.analyze(Path("."))

    report = RepositoryReport().generate(
        state,
        Path("fios_live/reports"),
    )

    print(f"Repository : {state.repository_name}")
    print(f"Root       : {state.root_path}")
    print()

    print(f"Folders    : {state.total_folders}")
    print(f"Files      : {state.total_files}")
    print(f"Python     : {state.python_files}")
    print(f"Packages   : {state.packages}")
    print(f"Modules    : {state.modules}")
    print()

    print(f"Architecture : {state.architecture_score:.1f}%")
    print(f"Health       : {state.health_score:.1f}%")
    print()

    print(f"[OK] Report Generated : {report}")

    print()
    print("=" * 60)
    print("REPOSITORY BRAIN COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()