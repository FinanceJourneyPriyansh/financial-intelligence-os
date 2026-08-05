"""
Financial Intelligence OS (FIOS)
Repository Validator

Milestone 3 - Validation Platform

Validates the overall integrity of the Financial Intelligence OS
repository structure.
"""

from __future__ import annotations

from pathlib import Path

from .validation_manager import ValidationResult


class RepositoryValidator:
    """
    Validates the overall repository structure.
    """

    REQUIRED_FILES = [
        ".gitignore",
        "LICENSE",
        "fios.py",
    ]

    REQUIRED_DIRECTORIES = [
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
        Validate repository integrity.
        """
        issues: list[str] = []

        # Validate required directories
        for directory in self.REQUIRED_DIRECTORIES:
            path = self.repository_root / directory
            if not path.is_dir():
                issues.append(f"Missing directory: {directory}")

        # Validate required files
        for file_name in self.REQUIRED_FILES:
            path = self.repository_root / file_name
            if not path.is_file():
                issues.append(f"Missing file: {file_name}")

        # Validate Git repository
        if not (self.repository_root / ".git").exists():
            issues.append("Git repository not initialized.")

        if issues:
            return ValidationResult(
                name="Repository Validator",
                passed=False,
                message="\n".join(issues),
            )

        return ValidationResult(
            name="Repository Validator",
            passed=True,
            message="Repository structure is valid.",
        )