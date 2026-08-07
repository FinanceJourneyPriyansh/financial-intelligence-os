"""
============================================================
Financial Intelligence OS (FIOS)
Base Scanner
============================================================

Module:
    fios_live.scanners.base_scanner

Purpose:
    Provides shared functionality for all scanner services.

Responsibilities:
    - Shared exclusion rules
    - Efficient repository traversal
    - Common helper methods

Author:
    Priyansh Soni

Project:
    Financial Intelligence OS (FIOS)
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Iterator


class BaseScanner:
    """
    Base class for all FIOS Live scanners.

    Provides common repository traversal and exclusion
    handling shared across every scanner.
    """

    EXCLUDED_DIRECTORIES = frozenset(
        {
            ".git",
            ".venv",
            "__pycache__",
            ".pytest_cache",
            ".mypy_cache",
            ".ruff_cache",
            ".idea",
            ".vscode",
            ".tox",
            ".coverage",
            "node_modules",
        }
    )

    def is_excluded(self, path: Path) -> bool:
        """
        Determine whether a path should be ignored.

        Args:
            path:
                Path to evaluate.

        Returns:
            True if the path is inside an excluded directory.
        """
        return any(part in self.EXCLUDED_DIRECTORIES for part in path.parts)

    def walk(self, root: Path) -> Iterator[Path]:
        """
        Walk the repository efficiently.

        Excluded directories are removed before descending
        into them, preventing unnecessary traversal.

        Args:
            root:
                Repository root.

        Yields:
            Every directory and file that should be scanned.
        """
        for current_root, dirs, files in os.walk(root):

            # Prevent descending into excluded directories.
            dirs[:] = [
                directory
                for directory in dirs
                if directory not in self.EXCLUDED_DIRECTORIES
            ]

            current_path = Path(current_root)

            # Yield the current directory.
            yield current_path

            # Yield files inside the current directory.
            for filename in files:
                yield current_path / filename