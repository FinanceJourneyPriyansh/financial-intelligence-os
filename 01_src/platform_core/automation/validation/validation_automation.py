"""
Financial Intelligence OS (FIOS)
Builder Automation Platform

Module:
    Validation Automation

Description:
    Automation layer responsible for orchestrating Builder
    Validation Platform execution.

Author:
    FinanceJourneyPriyansh

Version:
    v0.5.0-builder-m5
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Callable

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class ValidationExecution:
    """
    Stores validation execution results.
    """

    passed: list[str] = field(default_factory=list)
    failed: list[str] = field(default_factory=list)


class ValidationAutomation:
    """
    Coordinates execution of Builder validation tasks.
    """

    def __init__(self) -> None:

        self._validators: dict[str, Callable[[], None]] = {}

    # -----------------------------------------------------

    def register(
        self,
        name: str,
        validator: Callable[[], None],
    ) -> None:
        """
        Register a validation task.
        """

        self._validators[name] = validator

        logger.info(
            "Registered validator: %s",
            name,
        )

    # -----------------------------------------------------

    def execute(self) -> ValidationExecution:
        """
        Execute all registered validation tasks.
        """

        result = ValidationExecution()

        logger.info("Validation execution started.")

        for name, validator in self._validators.items():

            try:

                validator()

                result.passed.append(name)

                logger.info(
                    "Validation passed: %s",
                    name,
                )

            except Exception:

                result.failed.append(name)

                logger.exception(
                    "Validation failed: %s",
                    name,
                )

        logger.info("Validation execution completed.")

        return result

    # -----------------------------------------------------

    def count(self) -> int:
        """
        Return the number of registered validators.
        """

        return len(self._validators)

    def clear(self) -> None:
        """
        Remove all registered validators.
        """

        self._validators.clear()

        logger.info("Validation registry cleared.")