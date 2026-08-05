"""
Financial Intelligence OS (FIOS)
Builder Automation Platform

Module:
    Dashboard Automation

Description:
    Coordinates Builder dashboard update tasks.

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
class DashboardExecution:
    """
    Stores dashboard update results.
    """

    updated: list[str] = field(default_factory=list)
    failed: list[str] = field(default_factory=list)


class DashboardAutomation:
    """
    Coordinates Builder dashboard update tasks.

    Dashboard targets may include:

    - dashboard_metrics.json
    - Builder health dashboards
    - Repository dashboards
    - Monitoring dashboards
    """

    def __init__(self) -> None:

        self._dashboards: dict[str, Callable[[], None]] = {}

    def register(
        self,
        name: str,
        dashboard: Callable[[], None],
    ) -> None:
        """
        Register a dashboard update task.
        """

        self._dashboards[name] = dashboard

        logger.info(
            "Registered dashboard: %s",
            name,
        )

    def execute(self) -> DashboardExecution:
        """
        Execute all registered dashboard update tasks.
        """

        result = DashboardExecution()

        logger.info("Dashboard update started.")

        for name, dashboard in self._dashboards.items():

            try:

                dashboard()

                result.updated.append(name)

                logger.info(
                    "Dashboard updated: %s",
                    name,
                )

            except Exception:

                result.failed.append(name)

                logger.exception(
                    "Dashboard update failed: %s",
                    name,
                )

        logger.info("Dashboard update completed.")

        return result

    def count(self) -> int:
        """
        Return number of registered dashboard tasks.
        """

        return len(self._dashboards)

    def clear(self) -> None:
        """
        Clear dashboard registry.
        """

        self._dashboards.clear()

        logger.info("Dashboard registry cleared.")