"""
Financial Intelligence OS (FIOS)
Builder Automation Platform

Module:
    Control Center Automation

Description:
    Coordinates automation tasks for the Builder Control Center.

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
class ControlCenterExecution:
    """
    Stores Control Center automation results.
    """

    completed: list[str] = field(default_factory=list)
    failed: list[str] = field(default_factory=list)


class ControlCenterAutomation:
    """
    Coordinates Builder Control Center automation tasks.
    """

    def __init__(self) -> None:

        self._tasks: dict[str, Callable[[], None]] = {}

    # --------------------------------------------------

    def register(
        self,
        name: str,
        task: Callable[[], None],
    ) -> None:
        """
        Register a Control Center task.
        """

        self._tasks[name] = task

        logger.info(
            "Registered Control Center task: %s",
            name,
        )

    # --------------------------------------------------

    def execute(self) -> ControlCenterExecution:
        """
        Execute all registered Control Center tasks.
        """

        result = ControlCenterExecution()

        logger.info("Control Center automation started.")

        for name, task in self._tasks.items():

            try:

                task()

                result.completed.append(name)

                logger.info(
                    "Completed Control Center task: %s",
                    name,
                )

            except Exception:

                result.failed.append(name)

                logger.exception(
                    "Control Center task failed: %s",
                    name,
                )

        logger.info("Control Center automation completed.")

        return result

    # --------------------------------------------------

    def count(self) -> int:
        """
        Return number of registered tasks.
        """

        return len(self._tasks)

    def clear(self) -> None:
        """
        Clear all registered tasks.
        """

        self._tasks.clear()

        logger.info("Control Center registry cleared.")