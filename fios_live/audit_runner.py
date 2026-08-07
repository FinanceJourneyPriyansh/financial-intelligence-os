"""
============================================================
Financial Intelligence OS (FIOS)
Audit Runner
============================================================

Module:
    fios_live.audit_runner

Purpose:
    Production entry point for generating the FIOS
    System Audit.

Workflow:
    Repository
        ↓
    ProjectScanner
        ↓
    ProjectState
        ↓
    HealthService
        ↓
    FIOSState
        ↓
    Auditor
        ↓
    Markdown Report

Author:
    Priyansh Soni

Project:
    Financial Intelligence OS (FIOS)
"""

from __future__ import annotations

from pathlib import Path

from fios_live.audit.auditor import Auditor
from fios_live.models.fios_state import FIOSState
from fios_live.scanners.project_scanner import ProjectScanner
from fios_live.services.health_service import HealthService


def main() -> None:
    """
    Execute the complete FIOS audit workflow.
    """

    print("=" * 60)
    print("FINANCIAL INTELLIGENCE OS (FIOS)")
    print("LIVE AUDIT RUNNER")
    print("=" * 60)
    print()

    # --------------------------------------------------------
    # Build Runtime State
    # --------------------------------------------------------

    state = FIOSState()

    scanner = ProjectScanner()
    state.project = scanner.scan(Path("."))

    health_service = HealthService()
    state.health = health_service.evaluate(state.project)

    # --------------------------------------------------------
    # Generate Reports
    # --------------------------------------------------------

    auditor = Auditor(
        output_directory=Path("fios_live/reports"),
    )

    auditor.generate(state)

    print()
    print("=" * 60)
    print("FIOS AUDIT COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()