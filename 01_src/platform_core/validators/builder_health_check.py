"""
Financial Intelligence OS (FIOS)
Builder Health Check

Milestone 3 - Validation Platform

Aggregates validation results into an overall Builder health report.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .validation_manager import ValidationResult


@dataclass
class BuilderHealthReport:
    """
    Represents the overall health status of the Builder.
    """

    total_checks: int
    passed_checks: int
    failed_checks: int
    health_score: float
    healthy: bool


class BuilderHealthCheck:
    """
    Calculates overall Builder health based on validation results.
    """

    @staticmethod
    def evaluate(results: List[ValidationResult]) -> BuilderHealthReport:
        """
        Evaluate validation results and calculate health metrics.
        """
        total_checks = len(results)
        passed_checks = sum(result.passed for result in results)
        failed_checks = total_checks - passed_checks

        health_score = (
            (passed_checks / total_checks) * 100
            if total_checks > 0
            else 100.0
        )

        return BuilderHealthReport(
            total_checks=total_checks,
            passed_checks=passed_checks,
            failed_checks=failed_checks,
            health_score=round(health_score, 2),
            healthy=(failed_checks == 0),
        )