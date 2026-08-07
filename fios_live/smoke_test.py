"""
============================================================
Financial Intelligence OS (FIOS)
FIOS Live Kernel Smoke Test
============================================================

Purpose:
    Performs an end-to-end validation of the FIOS Live
    kernel by exercising the ProjectScanner and
    HealthService.

This is a development utility and is not part of the
production runtime.
"""

from __future__ import annotations

from pathlib import Path

from fios_live.models.fios_state import FIOSState
from fios_live.scanners.project_scanner import ProjectScanner
from fios_live.services.health_service import HealthService


def main() -> None:
    """Run the FIOS Live smoke test."""

    print("=" * 60)
    print("      FINANCIAL INTELLIGENCE OS (FIOS)")
    print("            LIVE KERNEL SMOKE TEST")
    print("=" * 60)

    state = FIOSState()

    scanner = ProjectScanner()
    state.project = scanner.scan(Path("."))

    health_service = HealthService()
    state.health = health_service.evaluate(state.project)

    print()
    print("Repository")
    print(f"Root Path ............ {state.project.repository.root_path}")
    print(f"Folders .............. {state.project.statistics.total_folders}")
    print(f"Files ................ {state.project.statistics.total_files}")

    print()
    print("Python")
    print(f"Python Files ......... {state.project.source.python_files}")
    print(f"Packages ............. {state.project.source.packages}")
    print(f"Modules .............. {state.project.source.modules}")

    print()
    print("Documentation")
    print(f"Markdown Files ....... {state.project.documentation.markdown_files}")
    print(f"README Files ......... {state.project.documentation.readme_files}")

    print()
    print("Git")
    print(f"Branch ............... {state.project.git.branch}")
    print(f"Commit ............... {state.project.git.latest_commit}")
    print(f"Working Tree ......... {'Clean' if state.project.git.clean else 'Modified'}")

    print()
    print("Health")
    print(f"Score ................ {state.health.score:.0f}%")
    print(f"Status ............... {state.health.status}")

    print()
    print("=" * 60)
    print("FIOS LIVE KERNEL INITIALIZED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    main()