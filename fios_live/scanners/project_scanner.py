"""
============================================================
Financial Intelligence OS (FIOS)
Project Scanner
============================================================

Module:
    fios_live.scanners.project_scanner

Purpose:
    Coordinates all FIOS Live scanners and builds the
    ProjectState (Digital Twin) of the repository.

Responsibilities:
    - Coordinate scanner execution
    - Populate ProjectState
    - Collect repository statistics

This scanner does NOT:
    - Generate reports
    - Display dashboards
    - Calculate project health

Author:
    Priyansh Soni

Project:
    Financial Intelligence OS (FIOS)
"""

from __future__ import annotations

from pathlib import Path

from fios_live.models.project_state import ProjectState
from fios_live.scanners.documentation_scanner import DocumentationScanner
from fios_live.scanners.file_scanner import FileScanner
from fios_live.scanners.folder_scanner import FolderScanner
from fios_live.scanners.git_scanner import GitScanner
from fios_live.scanners.python_scanner import PythonScanner


class ProjectScanner:
    """
    Coordinates all scanner services to construct the
    ProjectState.
    """

    def __init__(self) -> None:
        """Initialize all scanner dependencies."""

        self._folder_scanner = FolderScanner()
        self._file_scanner = FileScanner()
        self._python_scanner = PythonScanner()
        self._documentation_scanner = DocumentationScanner()
        self._git_scanner = GitScanner()

    def scan(self, root: Path) -> ProjectState:
        """
        Scan the complete repository.

        Args:
            root:
                Repository root.

        Returns:
            Fully populated ProjectState.
        """

        state = ProjectState()

        # Repository
        state.repository.root_path = str(root)
        state.repository.folders = self._folder_scanner.scan(root)
        state.repository.files = self._file_scanner.scan(root)

        # Source
        state.source = self._python_scanner.scan(root)

        # Documentation
        state.documentation = self._documentation_scanner.scan(root)

        # Git
        state.git = self._git_scanner.scan()

        # Statistics
        state.statistics.total_folders = len(state.repository.folders)
        state.statistics.total_files = len(state.repository.files)

        return state