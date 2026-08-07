"""
============================================================
Financial Intelligence OS (FIOS)
Python Scanner
============================================================

Module:
    fios_live.scanners.python_scanner

Purpose:
    Discovers Python source files within the Financial
    Intelligence OS repository.

Responsibilities:
    - Discover Python files
    - Count Python packages
    - Count Python modules

Author:
    Priyansh Soni

Project:
    Financial Intelligence OS (FIOS)
"""

from __future__ import annotations

from pathlib import Path

from fios_live.models.project_state import SourceState
from fios_live.scanners.base_scanner import BaseScanner


class PythonScanner(BaseScanner):
    """Scans the repository for Python source files."""

    def scan(self, root: Path) -> SourceState:
        """
        Scan the repository.

        Args:
            root: Repository root.

        Returns:
            Populated SourceState.
        """
        state = SourceState()

        for path in self.walk(root):
            if not path.is_file():
                continue

            if path.suffix != ".py":
                continue

            state.python_files += 1

            if path.name == "__init__.py":
                state.packages += 1
            else:
                state.modules += 1

        return state