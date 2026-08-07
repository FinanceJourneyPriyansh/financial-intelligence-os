"""
============================================================
Financial Intelligence OS (FIOS)
Documentation Scanner
============================================================

Module:
    fios_live.scanners.documentation_scanner

Purpose:
    Discovers documentation files within the Financial
    Intelligence OS repository.

Responsibilities:
    - Discover Markdown files
    - Count README files
    - Populate DocumentationState

This scanner does NOT:
    - Read document contents
    - Generate reports
    - Update ProjectState directly

Author:
    Priyansh Soni

Project:
    Financial Intelligence OS (FIOS)
"""

from __future__ import annotations

from pathlib import Path

from fios_live.models.project_state import DocumentationState
from fios_live.scanners.base_scanner import BaseScanner


class DocumentationScanner(BaseScanner):
    """
    Scanner responsible for discovering documentation files.
    """

    def scan(self, root: Path) -> DocumentationState:
        """
        Scan the repository for Markdown documentation.

        Args:
            root:
                Repository root directory.

        Returns:
            Populated DocumentationState.
        """
        state = DocumentationState()

        for path in self.walk(root):

            if not path.is_file():
                continue

            if path.suffix.lower() != ".md":
                continue

            state.markdown_files += 1

            if path.name.upper().startswith("README"):
                state.readme_files += 1

        return state