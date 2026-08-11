"""
Financial Intelligence OS (FIOS)

Monitoring Platform

Repository Monitor

Monitors the repository structure and reports
basic repository health metrics.

Version:
v0.4.0-builder-m4
"""

from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path
from typing import Any
from fios_live.config.scan_config import CONFIG


class RepositoryMonitor:
    """Monitor the repository structure."""

    def __init__(self) -> None:
        # Repository root
        self.repository_root = Path(__file__).resolve().parents[3]

        # Previous lightweight repository fingerprint.
        #
        # This is intentionally kept in memory so the existing
        # persistent RepositoryMonitor instance can compare
        # consecutive monitoring cycles without introducing
        # another state subsystem.
        self._previous_fingerprint: tuple[tuple[str, int, int], ...] | None = None

    def _iter_project_items(self):
        """
        Yield project files and folders.

        Uses the shared FIOS ScanConfig so repository monitoring
        follows the same scanning boundaries as the Repository Brain.
        """

        for scan_root in CONFIG.resolved_roots(self.repository_root):

            for root, dirs, files in os.walk(scan_root):

                root_path = Path(root)

                dirs[:] = [
                    directory
                    for directory in dirs
                    if directory not in CONFIG.excluded_directories
                    and str(
                        (root_path / directory).relative_to(
                            self.repository_root
                        )
                    ).replace("\\", "/")
                    not in CONFIG.excluded_paths
                ]

                for directory in dirs:
                    yield root_path / directory

                for file in files:

                    path = root_path / file

                    if path.suffix.lower() in CONFIG.excluded_extensions:
                        continue

                    yield path

    def _build_fingerprint(
        self,
        files: list[Path],
    ) -> tuple[tuple[str, int, int], ...]:
        """
        Build a lightweight repository fingerprint.

        The fingerprint uses:
        - relative file path
        - file size
        - modification timestamp in nanoseconds

        File contents are intentionally not hashed. This keeps
        change detection lightweight while still detecting normal
        file creation, deletion, and modification events.
        """

        fingerprint: list[tuple[str, int, int]] = []

        for file in files:

            try:
                stat = file.stat()

                fingerprint.append(
                    (
                        str(file.relative_to(self.repository_root)),
                        stat.st_size,
                        stat.st_mtime_ns,
                    )
                )

            except (OSError, ValueError):
                # File may disappear during the scan.
                continue

        fingerprint.sort()

        return tuple(fingerprint)

    def run(self) -> dict[str, Any]:
        """Collect repository metrics and detect repository changes."""

        folders = []
        files = []

        for item in self._iter_project_items():

            if item.is_dir():
                folders.append(item)

            elif item.is_file():
                files.append(item)

        current_fingerprint = self._build_fingerprint(files)

        first_scan = self._previous_fingerprint is None

        changed = (
            first_scan
            or current_fingerprint != self._previous_fingerprint
        )

        self._previous_fingerprint = current_fingerprint

        required_directories = [
            "00_control_center",
            "01_src",
            "02_data",
            "03_docs",
            "04_tests",
            "05_dashboards",
            "08_reports",
            "09_logs",
            "99_project",
        ]

        missing_directories = [
            directory
            for directory in required_directories
            if not (self.repository_root / directory).exists()
        ]

        status = "PASS" if not missing_directories else "WARNING"

        return {
            "module": "Repository",
            "status": status,
            "health": 100 if status == "PASS" else 80,
            "metrics": {
                "repository_root": str(self.repository_root),
                "folder_count": len(folders),
                "file_count": len(files),
                "missing_directories": missing_directories,
                "changed": changed,
                "first_scan": first_scan,
            },
            "warnings": missing_directories,
            "errors": [],
            "timestamp": datetime.now().isoformat(),
        }