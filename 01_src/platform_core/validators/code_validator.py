"""
Financial Intelligence OS (FIOS)
Code Validator

Milestone 3 - Validation Platform

Performs static validation of Python source files.
"""

from __future__ import annotations

import py_compile
from pathlib import Path

from .validation_manager import ValidationResult


class CodeValidator:
    """
    Validates Python source files by compiling them.
    """

    def __init__(self, source_directory: Path) -> None:
        self.source_directory = source_directory

    def validate(self) -> ValidationResult:
        """
        Validate all Python files within the source directory.
        """
        issues: list[str] = []

        for python_file in self.source_directory.rglob("*.py"):
            try:
                py_compile.compile(
                    str(python_file),
                    doraise=True,
                )
            except py_compile.PyCompileError:
                issues.append(str(python_file))

        if issues:
            return ValidationResult(
                name="Code Validator",
                passed=False,
                message="Compilation failed:\n" + "\n".join(issues),
            )

        return ValidationResult(
            name="Code Validator",
            passed=True,
            message="All Python files compiled successfully.",
        )