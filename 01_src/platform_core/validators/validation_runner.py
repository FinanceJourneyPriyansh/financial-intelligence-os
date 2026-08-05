"""
Financial Intelligence OS (FIOS)
Validation Runner

Milestone 3 - Validation Platform

Coordinates execution of all validators, evaluates Builder health,
and generates validation reports.
"""

from __future__ import annotations

from pathlib import Path

from .blueprint_validator import BlueprintValidator
from .builder_health_check import BuilderHealthCheck
from .code_validator import CodeValidator
from .documentation_validator import DocumentationValidator
from .folder_validator import FolderValidator
from .generator_validator import GeneratorValidator
from .repository_validator import RepositoryValidator
from .validation_manager import ValidationManager
from .validation_report_generator import ValidationReportGenerator
from .yaml_validator import YAMLValidator


def run_validation(repository_root: Path):
    """
    Execute all Builder validators and generate reports.
    """

    manager = ValidationManager()

    # Folder validation
    manager.register(
        lambda: FolderValidator(repository_root).validate()
    )

    # Repository validation
    manager.register(
        lambda: RepositoryValidator(repository_root).validate()
    )

    # Documentation validation
    manager.register(
        lambda: DocumentationValidator(repository_root).validate()
    )

    # YAML validation
    manager.register(
        lambda: YAMLValidator(
            list(repository_root.rglob("*.yaml"))
            + list(repository_root.rglob("*.yml"))
        ).validate()
    )

    # Blueprint validation
    manager.register(
        lambda: BlueprintValidator(
            list(repository_root.rglob("*Blueprint*.md"))
        ).validate()
    )

    # Generator validation
    manager.register(
        lambda: GeneratorValidator(
            repository_root
            / "01_src"
            / "platform_core"
            / "generators"
        ).validate()
    )

    # Python code validation
    manager.register(
        lambda: CodeValidator(
            repository_root / "01_src"
        ).validate()
    )

    # Execute validators
    results = manager.run()

    # Calculate Builder health
    health = BuilderHealthCheck.evaluate(results)

    # Generate validation reports
    report_generator = ValidationReportGenerator(
        repository_root / "08_reports"
    )

    report_generator.generate(
        results=results,
        health=health,
    )

    return results, health


if __name__ == "__main__":

    repository_root = Path.cwd()

    validation_results, builder_health = run_validation(
        repository_root
    )

    print("=" * 60)
    print("FIOS Validation Report")
    print("=" * 60)

    for result in validation_results:

        status = "PASS" if result.passed else "FAIL"

        print(f"[{status}] {result.name}")
        print(f"    {result.message}")

    print("-" * 60)
    print(f"Overall Health : {builder_health.health_score:.2f}%")
    print(f"Checks Passed  : {builder_health.passed_checks}")
    print(f"Checks Failed  : {builder_health.failed_checks}")
    print("=" * 60)