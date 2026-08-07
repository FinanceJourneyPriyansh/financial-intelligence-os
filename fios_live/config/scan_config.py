"""
============================================================
Financial Intelligence OS (FIOS)
Scan Configuration
============================================================

Module:
    fios_live.config.scan_config

Purpose:
    Defines the directories and rules used by all FIOS
    Live scanners.

This module acts as the single source of truth for
repository scanning.

Author:
    Priyansh Soni

Project:
    Financial Intelligence OS (FIOS)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True, slots=True)
class ScanConfig:
    """
    Configuration shared by every scanner.
    """

    # ---------------------------------------------------------
    # Repository roots to scan
    # ---------------------------------------------------------

    scan_roots: tuple[str, ...] = (
        "01_src",
        "fios_live",
        "99_project",
        "tests",
    )

    # ---------------------------------------------------------
    # Directories to ignore
    # ---------------------------------------------------------

    excluded_directories: frozenset[str] = field(
        default_factory=lambda: frozenset(
            {
                ".git",
                ".venv",
                "__pycache__",
                ".pytest_cache",
                ".mypy_cache",
                ".ruff_cache",
                ".tox",
                ".idea",
                ".vscode",
                "node_modules",
                "dist",
                "build",
                ".coverage",
            }
        )
    )

    # ---------------------------------------------------------
    # File extensions ignored globally
    # ---------------------------------------------------------

    excluded_extensions: frozenset[str] = field(
        default_factory=lambda: frozenset(
            {
                ".pyc",
                ".pyo",
                ".log",
                ".tmp",
            }
        )
    )

    def resolved_roots(self, repository_root: Path) -> list[Path]:
        """
        Resolve configured scan roots.

        Only existing directories are returned.

        Args:
            repository_root:
                Root of the FIOS repository.

        Returns:
            Existing scan root directories.
        """

        roots: list[Path] = []

        for directory in self.scan_roots:

            path = repository_root / directory

            if path.exists() and path.is_dir():
                roots.append(path)

        return roots


CONFIG = ScanConfig()