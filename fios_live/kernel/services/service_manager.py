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
from platform_core.monitoring.monitoring_manager import MonitoringManager

from fios_live.brain.repository_brain import RepositoryBrain
from fios_live.kernel.state.kernel_state import KernelState


class ServiceManager:
    """
    Starts and manages the existing FIOS services.
    """

    def __init__(self) -> None:
        self.state = KernelState()
        self.monitoring = MonitoringManager()
        self.builder: BuilderIntegrationManager | None = None
        self.brain: RepositoryBrain | None = None

    def boot(self) -> KernelState:
        """
        Boot the existing FIOS services and report real status.
        """

        self.state.running = True

        root = Path.cwd()

        # Existing Repository Brain
        self.brain = RepositoryBrain()
        brain_state = self.brain.analyze(root)

        self.state.repository_loaded = True
        self.state.brain_online = True
        self.state.architecture_score = brain_state.architecture_score
        self.state.health_score = brain_state.health_score

        # Existing Monitoring Platform
        self.monitoring.run()

        # Existing Builder Integration Platform
        builder_state_path = (
            root
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


