"""
Financial Intelligence OS (FIOS)
Folder Validator

Milestone 3 - Validation Platform

Validates that the required repository folders exist.
"""

from __future__ import annotations

from pathlib import Path

from .validation_manager import ValidationResult


class FolderValidator:
    """
    Validates the repository directory structure.
    """

    REQUIRED_FOLDERS = [
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
    ]

    def __init__(self, repository_root: Path) -> None:
        self.repository_root = repository_root

    def validate(self) -> ValidationResult:
        """
        Validate that all required folders exist.
        """
        missing = []

        for folder in self.REQUIRED_FOLDERS:
            path = self.repository_root / folder

            if not path.exists():
                missing.append(folder)

        if missing:
            return ValidationResult(
                name="Folder Validator",
                passed=False,
                message=f"Missing folders: {', '.join(missing)}",
            )

        return ValidationResult(
            name="Folder Validator",
            passed=True,
            message="All required folders are present.",
        )