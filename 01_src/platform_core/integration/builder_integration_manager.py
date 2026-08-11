"""
Financial Intelligence OS (FIOS)

Milestone:
Milestone 6 - Builder Integration Platform

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

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ..state.builder_state_manager import BuilderStateManager
from ..generators.generator_manager import GeneratorManager
from ..validators.validation_manager import ValidationManager
from ..monitoring.monitoring_manager import MonitoringManager
from ..automation.manager.automation_manager import AutomationManager
from .execution_controller import ExecutionController
from .integration_context import IntegrationContext
from .platform_connector import PlatformConnector
from .workflow_engine import WorkflowEngine

LOGGER = logging.getLogger(__name__)


@dataclass(slots=True)
class BuilderExecutionResult:
    """
    Result returned by the Builder Runtime.
    """

    success: bool = False

    reports: dict[str, Any] = field(default_factory=dict)

    metrics: dict[str, Any] = field(default_factory=dict)

    artifacts: dict[str, Any] = field(default_factory=dict)

    warnings: list[str] = field(default_factory=list)

    errors: list[str] = field(default_factory=list)

    executed_stages: list[str] = field(default_factory=list)

    duration_seconds: float | None = None

    def summary(self) -> dict[str, Any]:
        """
        Return a serializable Builder execution summary.
        """

        return {
            "success": self.success,
            "executed_stages": self.executed_stages,
            "stage_count": len(self.executed_stages),
            "reports": list(self.reports.keys()),
            "metrics": list(self.metrics.keys()),
            "artifacts": list(self.artifacts.keys()),
            "warnings": len(self.warnings),
            "errors": len(self.errors),
            "duration_seconds": self.duration_seconds,
        }


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

        self.generator_manager: GeneratorManager | None = None

        self.validation_manager: ValidationManager | None = None

        self.monitoring_manager: MonitoringManager | None = None

        self.automation_manager: AutomationManager | None = None

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

        root_directory = Path.cwd()

        self.generator_manager = GeneratorManager(
            output_directory=root_directory / "03_docs",
            template_directory=(
                root_directory
                / "00_control_center"
                / "05_templates"
                / "02_repository"
            ),
            core_directory=(
                root_directory
                / "00_control_center"
                / "00_core"
            ),
            blueprint_directory=(
                root_directory
                / "00_control_center"
                / "01_blueprint"
            ),
        )

        self.validation_manager = ValidationManager()

        self.monitoring_manager = MonitoringManager()

        self.automation_manager = AutomationManager()

        self.automation_manager.register_documentation_tasks(
            self.state_manager,
            root_directory,
        )

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

        self.register_generator_manager(
            self.generator_manager
        )

        self.register_validation_manager(
            self.validation_manager
        )

        self.register_monitoring_manager(
            self.monitoring_manager
        )

        self.register_automation_manager(
            self.automation_manager
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

        if self.controller is None:
            raise RuntimeError(
                "ExecutionController not initialized."
            )

        if self.context is None:
            raise RuntimeError(
                "IntegrationContext not initialized."
            )

        self.controller.start()

        return BuilderExecutionResult(
            success=self.controller.is_completed,
            reports=dict(self.context.reports),
            metrics=dict(self.context.metrics),
            artifacts=dict(self.context.artifacts),
            warnings=list(self.context.warnings),
            errors=list(self.context.errors),
            executed_stages=list(
                self.context.executed_stages
            ),
            duration_seconds=self.context.duration_seconds,
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
