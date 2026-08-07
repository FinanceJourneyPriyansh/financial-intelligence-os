"""
============================================================
Financial Intelligence OS (FIOS)
Repository Brain Runner
============================================================
"""

from __future__ import annotations

from pathlib import Path

from fios_live.brain.repository_brain import RepositoryBrain


def main() -> None:

    print("=" * 60)
    print("FINANCIAL INTELLIGENCE OS (FIOS)")
    print("REPOSITORY BRAIN")
    print("=" * 60)
    print()

    brain = RepositoryBrain()

    state = brain.analyze(Path("."))

    print(f"Repository : {state.repository_name}")
    print(f"Root       : {state.root_path}")
    print()

    print(f"Folders    : {state.total_folders}")
    print(f"Files      : {state.total_files}")
    print(f"Python     : {state.python_files}")
    print(f"Packages   : {state.packages}")
    print(f"Modules    : {state.modules}")
    print(f"Markdown   : {state.markdown_files}")
    print(f"JSON       : {state.json_files}")
    print(f"YAML       : {state.yaml_files}")
    print(f"Tests      : {state.tests}")
    print()

    print(f"Architecture Score : {state.architecture_score:.1f}%")
    print(f"Repository Health  : {state.health_score:.1f}%")
    print()

    print("Recommendations")
    print("-" * 60)

    for recommendation in state.recommendations:
        print(f"• {recommendation}")

    print()

    print("=" * 60)
    print("REPOSITORY BRAIN COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()