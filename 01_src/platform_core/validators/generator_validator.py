"""
Financial Intelligence OS (FIOS)
Generator Validator

Validates the canonical Generator Platform.

The GeneratorManager is the single source of truth for
registered artifact generators.

Version:
v0.6.0-builder-m6
"""

from __future__ import annotations

from pathlib import Path

from ..generators.generator_manager import GeneratorManager
from .validation_manager import ValidationResult


class GeneratorValidator:
    """
    Validates the canonical Generator Platform.

    GeneratorManager owns the generator registry.
    This validator does not maintain a second generator registry.
    """

    def __init__(self, generators_path: Path) -> None:
        self.generators_path = generators_path

    def validate(self) -> ValidationResult:
        """
        Validate all generators registered by GeneratorManager.
        """

        try:
            manager = GeneratorManager(
                output_directory=self.generators_path,
                template_directory=self.generators_path,
                core_directory=self.generators_path,
                blueprint_directory=self.generators_path,
            )

            registered = manager.generators

        except Exception as exc:
            return ValidationResult(
                name="Generator Validator",
                passed=False,
                message=(
                    "Unable to initialize GeneratorManager: "
                    f"{exc}"
                ),
            )

        missing: list[str] = []

        for name, (generator, _template) in registered.items():

            module = generator.__class__.__module__

            if not module.startswith("platform_core.generators."):
                missing.append(
                    f"{name} (invalid generator module: {module})"
                )
                continue

            relative_module = module.removeprefix(
                "platform_core.generators."
            )

            generator_path = (
                self.generators_path
                / Path(
                    relative_module.replace(".", "/")
                    + ".py"
                )
            )

            if not generator_path.is_file():
                missing.append(
                    f"{name} ({generator_path.name} missing)"
                )

        if missing:
            return ValidationResult(
                name="Generator Validator",
                passed=False,
                message=(
                    "Missing registered generators: "
                    + ", ".join(missing)
                ),
            )

        return ValidationResult(
            name="Generator Validator",
            passed=True,
            message=(
                "All canonical GeneratorManager generators "
                "are present: "
                + ", ".join(sorted(registered))
            ),
        )