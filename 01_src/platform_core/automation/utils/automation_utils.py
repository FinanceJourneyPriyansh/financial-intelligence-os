"""
Financial Intelligence OS (FIOS)
Builder Automation Platform

Module:
    Automation Utilities

Description:
    Shared utility functions used across the Builder
    Automation Platform.

Author:
    FinanceJourneyPriyansh

Version:
    v0.5.0-builder-m5
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path


class AutomationUtils:
    """
    Shared helper utilities for the Automation Platform.
    """

    @staticmethod
    def timestamp() -> str:
        """
        Return the current UTC timestamp in ISO 8601 format.
        """

        return datetime.utcnow().isoformat(timespec="seconds")

    @staticmethod
    def file_exists(path: str | Path) -> bool:
        """
        Check whether a file exists.
        """

        return Path(path).exists()

    @staticmethod
    def ensure_directory(path: str | Path) -> Path:
        """
        Create a directory if it does not already exist.
        """

        directory = Path(path)
        directory.mkdir(parents=True, exist_ok=True)
        return directory

    @staticmethod
    def repository_root() -> Path:
        """
        Return the current working directory.
        """

        return Path.cwd()

    @staticmethod
    def progress(
        completed: int,
        total: int,
    ) -> int:
        """
        Calculate completion percentage.
        """

        if total <= 0:
            return 0

        return int((completed / total) * 100)