"""
Financial Intelligence OS (FIOS)
Builder Automation Platform

Module:
    Generator Automation

Description:
    Automation layer responsible for orchestrating Builder
    Generator Platform execution.

Author:
    FinanceJourneyPriyansh

Version:
    v0.5.0-builder-m5
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class GeneratorExecution:

    executed: list[str] = field(default_factory=list)

    failed: list[str] = field(default_factory=list)


class GeneratorAutomation:
    """
    Executes Builder generator tasks.

    This class does not generate repository artifacts directly.
    It coordinates execution of the existing Generator Platform.
    """

    def __init__(self) -> None:

        self._generators: dict[str, callable] = {}

    # -----------------------------------------------------

    def register(
        self,
        name: str,
        generator: callable,
    ) -> None:

        self._generators[name] = generator

        logger.info(
            "Registered generator: %s",
            name,
        )

    # -----------------------------------------------------

    def execute(self) -> GeneratorExecution:

        result = GeneratorExecution()

        logger.info("Generator execution started.")

        for name, generator in self._generators.items():

            try:

                generator()

                result.executed.append(name)

                logger.info(
                    "Generator completed: %s",
                    name,
                )

            except Exception:

                result.failed.append(name)

                logger.exception(
                    "Generator failed: %s",
                    name,
                )

        logger.info("Generator execution finished.")

        return result

    # -----------------------------------------------------

    def count(self) -> int:

        return len(self._generators)

    def clear(self) -> None:

        self._generators.clear()

        logger.info("Generator registry cleared.")