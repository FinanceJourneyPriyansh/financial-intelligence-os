"""
Financial Intelligence OS (FIOS)
Validation Report Generator

Milestone 3 - Validation Platform

Generates validation reports for the Builder.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import List

from .builder_health_check import BuilderHealthReport
from .validation_manager import ValidationResult


class ValidationReportGenerator:
    """
    Generates validation reports in Markdown and JSON formats.
    """

    def __init__(self, reports_directory: Path) -> None:
        self.reports_directory = reports_directory
        self.reports_directory.mkdir(parents=True, exist_ok=True)

    def generate(
        self,
        results: List[ValidationResult],
        health: BuilderHealthReport,
    ) -> None:
        """
        Generate all validation reports.
        """
        self._generate_validation_report(results)
        self._generate_health_report(health)
        self._generate_json_log(results, health)

    def _generate_validation_report(
        self,
        results: List[ValidationResult],
    ) -> None:

        report = self.reports_directory / "Validation_Report.md"

        with report.open("w", encoding="utf-8") as file:

            file.write("# Validation Report\n\n")

            for result in results:

                status = "PASS" if result.passed else "FAIL"

                file.write(f"## {result.name}\n")
                file.write(f"- Status : {status}\n")
                file.write(f"- Message: {result.message}\n\n")

    def _generate_health_report(
        self,
        health: BuilderHealthReport,
    ) -> None:

        report = self.reports_directory / "Health_Report.md"

        with report.open("w", encoding="utf-8") as file:

            file.write("# Builder Health Report\n\n")

            file.write(f"- Total Checks : {health.total_checks}\n")
            file.write(f"- Passed Checks: {health.passed_checks}\n")
            file.write(f"- Failed Checks: {health.failed_checks}\n")
            file.write(f"- Health Score : {health.health_score:.2f}%\n")
            file.write(f"- Healthy      : {health.healthy}\n")

    def _generate_json_log(
        self,
        results: List[ValidationResult],
        health: BuilderHealthReport,
    ) -> None:

        log = self.reports_directory / "Validation_Log.json"

        data = {
            "health": {
                "total_checks": health.total_checks,
                "passed_checks": health.passed_checks,
                "failed_checks": health.failed_checks,
                "health_score": health.health_score,
                "healthy": health.healthy,
            },
            "results": [
                {
                    "name": result.name,
                    "passed": result.passed,
                    "message": result.message,
                }
                for result in results
            ],
        }

        with log.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)