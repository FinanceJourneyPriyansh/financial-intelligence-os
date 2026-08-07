"""
============================================================
Financial Intelligence OS (FIOS)
Auditor Engine
============================================================

Module:
    fios_live.audit.auditor

Purpose:
    Coordinates audit generation for the Financial
    Intelligence OS (FIOS).

Responsibilities:
    - Generate Markdown audit report
    - Coordinate report generation
    - Provide a single reporting entry point

Author:
    Priyansh Soni

Project:
    Financial Intelligence OS (FIOS)
"""

from __future__ import annotations

from pathlib import Path

from fios_live.audit.markdown_report import MarkdownReport
from fios_live.models.fios_state import FIOSState


class Auditor:
    """
    Central reporting engine for FIOS Live.
    """

    def __init__(self, output_directory: Path) -> None:
        """
        Initialize the Auditor.

        Args:
            output_directory:
                Directory where reports will be generated.
        """

        self.output_directory = output_directory

        self._markdown = MarkdownReport()

    def generate(self, state: FIOSState) -> None:
        """
        Generate all audit reports.

        Args:
            state:
                Current FIOS runtime state.
        """

        print("=" * 60)
        print("FINANCIAL INTELLIGENCE OS (FIOS)")
        print("AUDITOR")
        print("=" * 60)
        print()

        report = self._markdown.generate(
            state=state,
            output_directory=self.output_directory,
        )

        print(f"[OK] Markdown Report : {report}")

        print()
        print("=" * 60)
        print("AUDIT COMPLETED SUCCESSFULLY")
        print("=" * 60)