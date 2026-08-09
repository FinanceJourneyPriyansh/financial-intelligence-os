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


class RepositoryMonitor:
    """Monitor the repository structure."""

    EXCLUDED_DIRECTORIES = {
        ".git",
        ".venv",
        ".pytest_cache",
        "__pycache__",
        ".mypy_cache",
        ".idea",
        ".vscode",
        "node_modules",
    }

    def __init__(self) -> None:
        # Repository root
        self.repository_root = Path(__file__).resolve().parents[3]

    def _iter_project_items(self):
        """
        Yield project files and folders.

        Excluded directories are removed before traversal,
        preventing unnecessary scanning.
        """

        for root, dirs, files in os.walk(self.repository_root):

            # Stop traversal into excluded folders
            dirs[:] = [
                directory
                for directory in dirs
                if directory not in self.EXCLUDED_DIRECTORIES
            ]

            root_path = Path(root)

            for directory in dirs:
                yield root_path / directory

            for file in files:
                yield root_path / file

    def run(self) -> dict[str, Any]:
        """Collect repository metrics."""

        folders = []
        files = []

        for item in self._iter_project_items():

            if item.is_dir():
                folders.append(item)

            elif item.is_file():
                files.append(item)

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
            },
            "warnings": missing_directories,
            "errors": [],
            "timestamp": datetime.now().isoformat(),
        }