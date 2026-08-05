"""
Financial Intelligence OS (FIOS)
Builder Automation Platform

Module:
    Automation Manager

Description:
    Central orchestration engine responsible for registering,
    executing and managing Builder automation tasks.

Author:
    FinanceJourneyPriyansh

Version:
    v0.5.0-builder-m5
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Callable


logger = logging.getLogger(__name__)


@dataclass(slots=True)
class AutomationTask:
    """
    Represents a single automation task.
    """

    name: str
    action: Callable[[], None]
    enabled: bool = True


class AutomationManager:
    """
    Central Builder automation manager.

    Responsibilities
    ----------------
    - Register tasks
    - Execute tasks
    - Enable/Disable tasks
    - Execution reporting
    """

    def __init__(self) -> None:

        self._tasks: dict[str, AutomationTask] = {}

    # --------------------------------------------------
    # Registration
    # --------------------------------------------------

    def register(
        self,
        task: AutomationTask,
    ) -> None:
        """
        Register a task.
        """

        if task.name in self._tasks:
            raise ValueError(
                f"Task '{task.name}' already exists."
            )

        self._tasks[task.name] = task

        logger.info(
            "Registered automation task: %s",
            task.name,
        )

    # --------------------------------------------------
    # Execute
    # --------------------------------------------------

    def execute(self) -> None:
        """
        Execute every enabled task.
        """

        logger.info("Automation execution started.")

        for task in self._tasks.values():

            if not task.enabled:

                logger.info(
                    "Skipping disabled task: %s",
                    task.name,
                )
                continue

            logger.info(
                "Executing task: %s",
                task.name,
            )

            task.action()

        logger.info("Automation execution completed.")

    # --------------------------------------------------
    # Utilities
    # --------------------------------------------------

    def list_tasks(self) -> list[str]:
        """
        Return registered task names.
        """

        return list(self._tasks.keys())

    def task_count(self) -> int:
        """
        Number of registered tasks.
        """

        return len(self._tasks)

    def clear(self) -> None:
        """
        Remove all registered tasks.
        """

        self._tasks.clear()

        logger.info("Automation registry cleared.")