"""
Financial Intelligence OS (FIOS)
Validation Manager

Milestone 3 - Validation Platform

The Validation Manager orchestrates all validation modules.
It does not perform validation directly; instead, it coordinates
registered validators and aggregates their results.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, List


@dataclass
class ValidationResult:
    """
    Represents the outcome of a validator.
    """

    name: str
    passed: bool
    message: str = ""


class ValidationManager:
    """
    Coordinates execution of all validators.
    """

    def __init__(self) -> None:
        self._validators: List[Callable[[], ValidationResult]] = []

    def register(self, validator: Callable[[], ValidationResult]) -> None:
        """
        Register a validator.

        Parameters
        ----------
        validator : Callable
            Function returning a ValidationResult.
        """
        self._validators.append(validator)

    def run(self) -> List[ValidationResult]:
        """
        Execute all registered validators.
        """
        results: List[ValidationResult] = []

        for validator in self._validators:
            results.append(validator())

        return results

    @staticmethod
    def passed(results: List[ValidationResult]) -> bool:
        """
        Returns True if every validator passed.
        """
        return all(result.passed for result in results)