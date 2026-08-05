"""
Financial Intelligence OS (FIOS)
YAML Validator

Milestone 3 - Validation Platform

Validates YAML configuration files used throughout the Builder.
"""

from __future__ import annotations

from pathlib import Path

import yaml

from .validation_manager import ValidationResult


class YAMLValidator:
    """
    Validates one or more YAML configuration files.
    """

    def __init__(self, yaml_files: list[Path]) -> None:
        self.yaml_files = yaml_files

    def validate(self) -> ValidationResult:
        """
        Validate all configured YAML files.
        """
        invalid_files: list[str] = []

        for yaml_file in self.yaml_files:
            if not yaml_file.exists():
                invalid_files.append(f"{yaml_file} (missing)")
                continue

            try:
                with yaml_file.open("r", encoding="utf-8") as file:
                    yaml.safe_load(file)
            except yaml.YAMLError:
                invalid_files.append(str(yaml_file))

        if invalid_files:
            return ValidationResult(
                name="YAML Validator",
                passed=False,
                message="Invalid YAML: " + ", ".join(invalid_files),
            )

        return ValidationResult(
            name="YAML Validator",
            passed=True,
            message="All YAML files are valid.",
        )