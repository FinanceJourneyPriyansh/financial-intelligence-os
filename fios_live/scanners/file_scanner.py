"""
============================================================
Financial Intelligence OS (FIOS)
File Scanner
============================================================

Module:
    fios_live.scanners.file_scanner

Purpose:
    Discovers files within the Financial Intelligence
    OS repository.

Responsibilities:
    - Discover repository files
    - Return relative file paths
    - Ignore excluded directories

This scanner does NOT:
    - Scan folders
    - Generate reports
    - Update ProjectState

Author:
    Priyansh Soni

Project:
    Financial Intelligence OS (FIOS)
"""

from __future__ import annotations

from pathlib import Path

from fios_live.scanners.base_scanner import BaseScanner


class FileScanner(BaseScanner):
    """
    Scanner responsible for discovering repository files.
    """

    def scan(self, root: Path) -> list[str]:
        """
        Scan the repository for files.

        Args:
            root:
                Repository root directory.

        Returns:
            Alphabetically sorted list of file paths
            relative to the repository root.
        """
        files: list[str] = []

        for path in self.walk(root):

            if not path.is_file():
                continue

            files.append(str(path.relative_to(root)))

        files.sort()

        return files