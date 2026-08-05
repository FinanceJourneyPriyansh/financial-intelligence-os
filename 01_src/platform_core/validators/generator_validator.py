"""
Financial Intelligence OS (FIOS)
Generator Validator

Milestone 3 - Validation Platform

Validates the availability of Builder generator modules.
"""

from __future__ import annotations

from pathlib import Path

from .validation_manager import ValidationResult


class GeneratorValidator:
    """
    Validates that required generator modules exist.
    """

    REQUIRED_GENERATORS = [
        "base_generator.py",
        "folder_generator.py",
        "yaml_generator.py",
        "readme_generator.py",
        "repository_structure_generator.py",
        "architecture_generator.py",
        "project_summary_generator.py",
        "blueprint_overview_generator.py",
        "technology_stack_generator.py",
        "roadmap_generator.py",
        "generator_manager.py",
        "template_loader.py",
        "yaml_loader.py",
    ]

    def __init__(self, generators_path: Path) -> None:
        self.generators_path = generators_path

    def validate(self) -> ValidationResult:
        """
        Validate required generator modules.
        """
        missing: list[str] = []

        for generator in self.REQUIRED_GENERATORS:
            if not (self.generators_path / generator).is_file():
                missing.append(generator)

        if missing:
            return ValidationResult(
                name="Generator Validator",
                passed=False,
                message="Missing generators: " + ", ".join(missing),
            )

        return ValidationResult(
            name="Generator Validator",
            passed=True,
            message="All required generators are present.",
        )