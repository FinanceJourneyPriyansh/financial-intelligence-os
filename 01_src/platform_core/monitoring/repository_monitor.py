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

from datetime import datetime
from pathlib import Path
from typing import Any


class RepositoryMonitor:
    """Monitor the repository structure."""

    def __init__(self) -> None:
        # Repository root (01_src/platform_core/monitoring -> project root)
        self.repository_root = Path(__file__).resolve().parents[3]

    def run(self) -> dict[str, Any]:
        """Collect repository metrics."""

        folders = [
            item for item in self.repository_root.rglob("*")
            if item.is_dir()
        ]

        files = [
            item for item in self.repository_root.rglob("*")
            if item.is_file()
        ]

        required_directories = [
            "00_control_center",
            "01_src",
            "02_data",
            "03_docs",
            "04_tests",
            "05_dashboards",
            "06_models",
            "07_notebooks",
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