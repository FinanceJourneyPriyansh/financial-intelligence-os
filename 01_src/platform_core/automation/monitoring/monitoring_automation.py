"""
Financial Intelligence OS (FIOS)
Builder Automation Platform

Module:
    Monitoring Automation

Description:
    Automation layer responsible for orchestrating Builder
    Monitoring Platform execution.

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
class MonitoringExecution:
    """
    Stores monitoring execution results.
    """

    completed: list[str] = field(default_factory=list)
    failed: list[str] = field(default_factory=list)


class MonitoringAutomation:
    """
    Coordinates execution of Builder monitoring tasks.
    """

    def __init__(self) -> None:

        self._monitors: dict[str, Callable[[], None]] = {}

    # -----------------------------------------------------

    def register(
        self,
        name: str,
        monitor: Callable[[], None],
    ) -> None:
        """
        Register a monitoring task.
        """

        self._monitors[name] = monitor

        logger.info(
            "Registered monitor: %s",
            name,
        )

    # -----------------------------------------------------

    def execute(self) -> MonitoringExecution:
        """
        Execute all registered monitoring tasks.
        """

        result = MonitoringExecution()

        logger.info("Monitoring execution started.")

        for name, monitor in self._monitors.items():

            try:

                monitor()

                result.completed.append(name)

                logger.info(
                    "Monitoring completed: %s",
                    name,
                )

            except Exception:

                result.failed.append(name)

                logger.exception(
                    "Monitoring failed: %s",
                    name,
                )

        logger.info("Monitoring execution completed.")

        return result

    # -----------------------------------------------------

    def count(self) -> int:
        """
        Return the number of registered monitoring tasks.
        """

        return len(self._monitors)

    def clear(self) -> None:
        """
        Remove all registered monitoring tasks.
        """

        self._monitors.clear()

        logger.info("Monitoring registry cleared.")