"""
Financial Intelligence OS (FIOS)

Service Manager

Starts and manages the existing FIOS core services.
"""

from __future__ import annotations

from pathlib import Path

from platform_core.integration.builder_integration_manager import (
    BuilderIntegrationManager,
)

from fios_live.brain.models.repository_state import RepositoryState
from fios_live.brain.repository_brain import RepositoryBrain
from fios_live.kernel.state.kernel_state import KernelState


class ServiceManager:
    """
    Starts and manages the existing FIOS services.
    """

    def __init__(self) -> None:
        self.state = KernelState()
        self.builder: BuilderIntegrationManager | None = None
        self.brain: RepositoryBrain | None = None
        self.repository_root: Path | None = None

    def boot(self) -> KernelState:
        """
        Boot the existing FIOS services and report real status.
        """

        self.state.running = True

        self.repository_root = Path.cwd()

        # Existing Repository Brain
        self.brain = RepositoryBrain()

        brain_state = self.brain.analyze(
            self.repository_root
        )

        self.state.repository_loaded = True
        self.state.brain_online = True

        self.state.architecture_score = (
            brain_state.architecture_score
        )

        self.state.health_score = (
            brain_state.health_score
        )

        # Existing Builder Integration Platform
        builder_state_path = (
            self.repository_root
            / "00_control_center"
            / "02_configs"
            / "10_builder_state.yaml"
        )

        self.builder = BuilderIntegrationManager(
            builder_state_path
        )

        self.builder.initialize()

        result = self.builder.execute()

        self.state.builder_online = result.success

        self.state.automation_online = (
            self.builder.automation_manager is not None
        )

        self.state.last_event = "SYSTEM_BOOT"

        return self.state

    def run_brain_cycle(self) -> RepositoryState:
        """
        Run one controlled Repository Brain cycle.

        Reuses the existing RepositoryBrain instance.

        This method does not execute the Builder.
        """

        if self.brain is None:
            raise RuntimeError(
                "Repository Brain is not initialized."
            )

        if self.repository_root is None:
            raise RuntimeError(
                "Repository root is not initialized."
            )

        brain_state = self.brain.analyze(
            self.repository_root
        )

        self.state.repository_loaded = True
        self.state.brain_online = True

        self.state.architecture_score = (
            brain_state.architecture_score
        )

        self.state.health_score = (
            brain_state.health_score
        )

        self.state.last_event = (
            "BRAIN_CYCLE_COMPLETE"
        )

        return brain_state

    def run_autonomous_cycle(self) -> RepositoryState | None:
        """
        Run one lightweight autonomous FIOS cycle.

        Reuses the existing RepositoryMonitor instance owned by
        the existing Builder MonitoringManager.

        The Repository Brain is executed only when the monitor
        detects a repository change.
        """

        if self.builder is None:
            raise RuntimeError(
                "Builder Integration Platform is not initialized."
            )

        if self.builder.monitoring_manager is None:
            raise RuntimeError(
                "Monitoring Manager is not initialized."
            )

        repository_monitor = (
            self.builder.monitoring_manager.repository_monitor
        )

        monitoring_result = repository_monitor.run()

        metrics = monitoring_result.get("metrics", {})

        changed = bool(metrics.get("changed", False))

        if not changed:
            self.state.last_event = (
                "REPOSITORY_UNCHANGED"
            )
            return None

        self.state.last_event = (
            "REPOSITORY_CHANGED"
        )

        return self.run_brain_cycle()