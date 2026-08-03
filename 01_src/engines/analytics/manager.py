"""
Financial Intelligence OS
Analytics Manager

Purpose
-------
Manage analytical workflows executed by the
Analytics Engine.
"""

from __future__ import annotations


class AnalyticsManager:
    """
    Manage analytics workflows.
    """

    def __init__(self) -> None:

        self._analyses: list[str] = []

    def register(self, analysis: str) -> None:
        """
        Register an analytics workflow.
        """

        if analysis not in self._analyses:
            self._analyses.append(analysis)

    def unregister(self, analysis: str) -> None:
        """
        Remove an analytics workflow.
        """

        if analysis in self._analyses:
            self._analyses.remove(analysis)

    def list_analyses(self) -> list[str]:
        """
        Return all registered analyses.
        """

        return sorted(self._analyses)

    def count(self) -> int:
        """
        Return the total number of registered analyses.
        """

        return len(self._analyses)

    def clear(self) -> None:
        """
        Remove all registered analyses.
        """

        self._analyses.clear()