"""
============================================================
Financial Intelligence OS (FIOS)
Base Scanner
============================================================

Module:
    fios_live.scanners.base_scanner

Purpose:
    Provides common scanning functionality shared by every
    FIOS Live scanner.

Responsibilities:
    - Repository traversal
    - Scan root resolution
    - Directory exclusion
    - File exclusion

Author:
    Priyansh Soni

Project:
    Financial Intelligence OS (FIOS)
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Iterator

from fios_live.config.scan_config import CONFIG


class BaseScanner:
    """
    Base class for all FIOS Live scanners.
    """

    def walk(self, repository_root: Path) -> Iterator[Path]:
        """
        Walk every configured FIOS scan root.

        Args:
            repository_root:
                Repository root directory.

        Yields:
            Paths belonging only to configured scan roots.
        """

        for scan_root in CONFIG.resolved_roots(repository_root):

            for current_root, dirs, files in os.walk(scan_root):

                #
                # Remove excluded directories BEFORE descending.
                #
                dirs[:] = [
                    directory
                    for directory in dirs
                    if directory not in CONFIG.excluded_directories
                ]

                current = Path(current_root)

                #
                # Yield directory.
                #
                yield current

                #
                # Yield files.
                #
                for filename in files:

                    file_path = current / filename

                    if (
                        file_path.suffix.lower()
                        in CONFIG.excluded_extensions
                    ):
                        continue

                    yield file_path

    @staticmethod
    def relative_to_repository(
        path: Path,
        repository_root: Path,
    ) -> str:
        """
        Convert an absolute path into a repository-relative path.
        """

        return str(path.relative_to(repository_root))