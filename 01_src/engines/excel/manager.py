"""
Financial Intelligence OS
Excel Manager

Purpose
-------
Manage automation workflows registered with
the Excel Engine.
"""

from __future__ import annotations


class AutomationManager:
    """
    Manage automation workflows.
    """

    def __init__(self) -> None:

        self._workflows: list[str] = []

    def register(self, workflow: str) -> None:
        """
        Register a workflow.
        """

        if workflow not in self._workflows:
            self._workflows.append(workflow)

    def unregister(self, workflow: str) -> None:
        """
        Remove a workflow.
        """

        if workflow in self._workflows:
            self._workflows.remove(workflow)

    def list_workflows(self) -> list[str]:
        """
        Return all registered workflows.
        """

        return sorted(self._workflows)

    def count(self) -> int:
        """
        Return the number of registered workflows.
        """

        return len(self._workflows)

    def clear(self) -> None:
        """
        Remove all registered workflows.
        """

        self._workflows.clear()
