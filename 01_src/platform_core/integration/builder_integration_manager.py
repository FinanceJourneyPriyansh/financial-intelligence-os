"""
============================================================
Financial Intelligence OS (FIOS)
Builder Integration Manager
============================================================

Milestone:
    Milestone 6 – Builder Integration Platform

Purpose:
    Central orchestration layer for the Builder Runtime.

Responsibilities:
    - Load Builder State
    - Initialize Runtime
    - Register platform managers
    - Start Builder execution
    - Return execution results

Version:
    v0.6.0-builder-m6
"""

from __future__ import annotations

import logging

from dataclasses import dataclass
from pathlib import Path

from ..state.builder_state_manager import BuilderStateManager
from .execution_controller import ExecutionController
from .integration_context import IntegrationContext
from .platform_connector import PlatformConnector
from .workflow_engine import WorkflowEngine


LOGGER = logging.getLogger(__name__)


@dataclass(slots=True)
class BuilderExecutionResult:

    success: bool = False


class BuilderIntegrationManager:
    """
    Entry point for the Builder Runtime.
    """

    def __init__(
        self,
        builder_state_path: Path,
    ) -> None:

        self.state_manager = BuilderStateManager(
            builder_state_path
        )

        self.context: IntegrationContext | None = None

        self.connector: PlatformConnector | None = None

        self.workflow: WorkflowEngine | None = None

        self.controller: ExecutionController | None = None

        LOGGER.info(
            "Builder Integration Manager initialized."
        )
    
    # ==========================================================
    # Initialization
    # ==========================================================

    def initialize(self) -> None:
        """
        Initialize the Builder Runtime.
        """

        LOGGER.info("Initializing Builder Runtime...")

        builder_state = self.state_manager.load()

        version = (
            builder_state
            .get("builder", {})
            .get("version", "unknown")
        )

        self.context = IntegrationContext(
            builder_version=version,
            builder_state=builder_state,
        )

        self.connector = PlatformConnector(
            self.context
        )

        self.workflow = WorkflowEngine(
            self.context,
            self.connector,
        )

        self.controller = ExecutionController(
            self.context,
            self.workflow,
        )

        LOGGER.info(
            "Builder Runtime initialized."
        )

    # ==========================================================
    # Execution
    # ==========================================================

    def execute(self) -> BuilderExecutionResult:
        """
        Execute the complete Builder Runtime.
        """

        self.initialize()

        if self.controller is None:
            raise RuntimeError(
                "ExecutionController not initialized."
            )

        self.controller.start()

        return BuilderExecutionResult(
            success=self.controller.is_completed
        )

    # ==========================================================
    # Platform Registration
    # ==========================================================

    def register_generator_manager(
        self,
        manager,
    ) -> None:
        """
        Register the Generator Manager.
        """

        if self.connector is None:
            raise RuntimeError(
                "Runtime has not been initialized."
            )

        self.connector.register(
            "generator",
            manager,
        )

    def register_validation_manager(
        self,
        manager,
    ) -> None:
        """
        Register the Validation Manager.
        """

        if self.connector is None:
            raise RuntimeError(
                "Runtime has not been initialized."
            )

        self.connector.register(
            "validation",
            manager,
        )

    def register_monitoring_manager(
        self,
        manager,
    ) -> None:
        """
        Register the Monitoring Manager.
        """

        if self.connector is None:
            raise RuntimeError(
                "Runtime has not been initialized."
            )

        self.connector.register(
            "monitoring",
            manager,
        )

    def register_automation_manager(
        self,
        manager,
    ) -> None:
        """
        Register the Automation Manager.
        """

        if self.connector is None:
            raise RuntimeError(
                "Runtime has not been initialized."
            )

        self.connector.register(
            "automation",
            manager,
        )
