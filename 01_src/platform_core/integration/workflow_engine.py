"""
Financial Intelligence OS (FIOS)

Milestone:
Milestone 6 - Builder Integration Platform

Purpose:
Defines and executes the Builder workflow.

Responsibilities:
- Define execution stages
- Execute stages in order
- Coordinate Platform Connector
- Update Integration Context
- Collect execution results

Version:
v0.6.0-builder-m6
"""

from __future__ import annotations

import logging
from typing import Any

from .integration_context import IntegrationContext
from .platform_connector import PlatformConnector

LOGGER = logging.getLogger(__name__)


class WorkflowEngine:
    """
    Executes the complete Builder workflow.
    """

    DEFAULT_WORKFLOW = (
        "generator",
        "validation",
        "monitoring",
        "automation",
    )

    def __init__(
        self,
        context: IntegrationContext,
        connector: PlatformConnector,
    ) -> None:

        self.context = context
        self.connector = connector

    # ==========================================================
    # Workflow
    # ==========================================================

    def execute(self) -> None:
        """
        Execute the complete workflow.
        """

        LOGGER.info("Starting Builder workflow...")

        for stage in self.DEFAULT_WORKFLOW:

            result = self.execute_stage(stage)

            self.context.reports[stage] = result

            self._collect_result(stage, result)

        LOGGER.info("Builder workflow completed.")

    def execute_stage(
        self,
        stage: str,
    ) -> Any:
        """
        Execute a single workflow stage.
        """

        LOGGER.info(
            "Executing stage: %s",
            stage,
        )

        self.context.start_stage(stage)

        result = self.connector.execute(stage)

        LOGGER.info(
            "Completed stage: %s",
            stage,
        )

        return result

    # ==========================================================
    # Result Collection
    # ==========================================================

    def _collect_result(
        self,
        stage: str,
        result: Any,
    ) -> None:
        """
        Collect canonical metrics and artifacts already produced
        by existing Builder platforms.

        This method only routes existing platform outputs into the
        shared IntegrationContext. It does not create new business
        logic or duplicate platform calculations.
        """

        if not isinstance(result, dict):
            return

        if stage == "generator":
            self.context.artifacts["generator"] = dict(result)
            return

        if stage == "validation":
            validation_results = result.get("results")

            if validation_results is not None:
                self.context.metrics["validation"] = {
                    "passed": result.get("passed", False),
                    "result_count": len(validation_results),
                }

            return

        if stage == "monitoring":
            metrics = result.get("metrics")

            if metrics is not None:
                self.context.metrics["monitoring"] = metrics

            artifacts: dict[str, Any] = {}

            if result.get("report") is not None:
                artifacts["report"] = result["report"]

            if result.get("dashboard") is not None:
                artifacts["dashboard"] = result["dashboard"]

            if artifacts:
                self.context.artifacts["monitoring"] = artifacts

            return

        if stage == "automation":
            if result.get("status") is not None:
                self.context.metrics["automation"] = {
                    "status": result["status"],
                }

    # ==========================================================
    # Workflow Utilities
    # ==========================================================

    def stages(self) -> tuple[str, ...]:
        """
        Return workflow stages.
        """

        return self.DEFAULT_WORKFLOW

    def stage_count(self) -> int:
        """
        Return number of workflow stages.
        """

        return len(self.DEFAULT_WORKFLOW)

    def contains(
        self,
        stage: str,
    ) -> bool:
        """
        Check whether a stage exists.
        """

        return stage in self.DEFAULT_WORKFLOW
