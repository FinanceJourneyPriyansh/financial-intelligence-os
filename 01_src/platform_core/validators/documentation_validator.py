"""
Financial Intelligence OS (FIOS)
Documentation Validator

Milestone 3 - Validation Platform

Validates required project documentation.
"""

from __future__ import annotations

from pathlib import Path

from .validation_manager import ValidationResult


class DocumentationValidator:
    """
    Validates project documentation files.
    """

    REQUIRED_DOCUMENTS = [
        "README.md",
        "03_docs",
    ]

    def __init__(self, repository_root: Path) -> None:
        self.repository_root = repository_root

    def validate(self) -> ValidationResult:
        """
        Validate documentation resources.
        """
        issues: list[str] = []

        for item in self.REQUIRED_DOCUMENTS:
            path = self.repository_root / item

            if not path.exists():
                issues.append(f"Missing: {item}")
                continue

            if path.is_file() and path.stat().st_size == 0:
                issues.append(f"Empty document: {item}")

        if issues:
            return ValidationResult(
                name="Documentation Validator",
                passed=False,
                message="\n".join(issues),
            )

        return ValidationResult(
            name="Documentation Validator",
            passed=True,
            message="Documentation is valid.",
        )