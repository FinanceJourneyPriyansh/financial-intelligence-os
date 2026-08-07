"""
============================================================
Financial Intelligence OS (FIOS)
Folder Scanner
============================================================

Module:
    fios_live.scanners.folder_scanner

Purpose:
    Discovers directories within the Financial Intelligence
    OS repository.

Responsibilities:
    - Discover repository folders
    - Return relative folder paths
    - Ignore excluded directories

This scanner does NOT:
    - Scan files
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


class FolderScanner(BaseScanner):
    """
    Scanner responsible for discovering repository folders.
    """

    def scan(self, root: Path) -> list[str]:
        """
        Scan the repository for folders.

        Args:
            root:
                Repository root directory.

        Returns:
            Alphabetically sorted list of folder paths
            relative to the repository root.
        """
        folders: list[str] = []

        for path in self.walk(root):

            if not path.is_dir():
                continue

            if path == root:
                continue

            folders.append(str(path.relative_to(root)))

        folders.sort()

        return folders