"""
Financial Intelligence OS (FIOS)
Builder Automation Platform

Module:
    Report Automation

Description:
    Coordinates Builder report generation tasks.

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
class ReportExecution:
    """
    Stores report generation results.
    """

    generated: list[str] = field(default_factory=list)
    failed: list[str] = field(default_factory=list)


class ReportAutomation:
    """
    Coordinates Builder report generation.

    Reports may include:

    - Validation Reports
    - Monitoring Reports
    - Builder Reports
    - Release Reports
    """

    def __init__(self) -> None:

        self._reports: dict[str, Callable[[], None]] = {}

    # --------------------------------------------------

    def register(
        self,
        name: str,
        report: Callable[[], None],
    ) -> None:

        self._reports[name] = report

        logger.info(
            "Registered report: %s",
            name,
        )

    # --------------------------------------------------

    def execute(self) -> ReportExecution:

        result = ReportExecution()

        logger.info("Report generation started.")

        for name, report in self._reports.items():

            try:

                report()

                result.generated.append(name)

                logger.info(
                    "Report generated: %s",
                    name,
                )

            except Exception:

                result.failed.append(name)

                logger.exception(
                    "Report failed: %s",
                    name,
                )

        logger.info("Report generation completed.")

        return result

    # --------------------------------------------------

    def count(self) -> int:

        return len(self._reports)

    def clear(self) -> None:

        self._reports.clear()

        logger.info("Report registry cleared.")