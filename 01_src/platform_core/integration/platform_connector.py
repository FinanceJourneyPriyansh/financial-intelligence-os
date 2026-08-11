"""
============================================================
Financial Intelligence OS (FIOS)
Platform Connector
============================================================

Milestone:
    Milestone 6 â€“ Builder Integration Platform

Purpose:
    Provides a unified interface between the Builder
    Integration Manager and all existing Builder platforms.

Responsibilities:
    - Register platform managers
    - Execute platform managers
    - Maintain execution order
    - Share Integration Context
    - Collect execution results

Version:
    v0.6.0-builder-m6
"""

from __future__ import annotations

from typing import Any, Dict

from .integration_context import IntegrationContext


class PlatformConnector:
    """
    Connects all Builder platforms together.

    This class does not implement any business logic.
    It delegates execution to the existing platform
    managers.
    """

    def __init__(self, context: IntegrationContext) -> None:

        self.context = context

        self.platforms: Dict[str, Any] = {}

    # ==========================================================
    # Registration
    # ==========================================================

    def register(
        self,
        name: str,
        manager: Any,
    ) -> None:
        """
        Register a platform manager.
        """

        self.platforms[name] = manager

    # ==========================================================
    # Lookup
    # ==========================================================

    def get(
        self,
        name: str,
    ) -> Any:
        """
        Return a registered platform.
        """

        return self.platforms.get(name)

    # ==========================================================
    # Execution
    # ==========================================================

    def execute(
        self,
        name: str,
    ) -> Any:
        """
        Execute a registered platform using its native API.
        """

        manager = self.get(name)

        if manager is None:
            raise ValueError(
                f"Platform '{name}' is not registered."
            )

        if name == "generator":

            return manager.generate_all()

        if name == "validation":

            results = manager.run()

            return {
                "results": results,
                "passed": manager.passed(results),
            }

        if name == "monitoring":

            return manager.run()

        if name == "automation":

            manager.execute()

            return {
                "status": "completed"
            }

        raise ValueError(
            f"Unsupported platform: {name}"
        )
    # ==========================================================
    # Bulk Execution
    # ==========================================================

    def execute_all(self) -> Dict[str, Any]:
        """
        Execute all registered platforms.
        """

        results: Dict[str, Any] = {}

        for name in self.platforms:

            results[name] = self.execute(name)

        return results

    # ==========================================================
    # Utilities
    # ==========================================================

    def registered_platforms(self) -> list[str]:
        """
        Return registered platform names.
        """

        return list(self.platforms.keys())

    def count(self) -> int:
        """
        Number of registered platforms.
        """

        return len(self.platforms)

    def clear(self) -> None:
        """
        Remove all registered platforms.
        """

        self.platforms.clear()


