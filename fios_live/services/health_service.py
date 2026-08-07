"""
============================================================
Financial Intelligence OS (FIOS)
Health Service
============================================================

Module:
    fios_live.services.health_service

Purpose:
    Evaluates the current health of the Financial
    Intelligence OS based on the ProjectState.

Responsibilities:
    - Evaluate repository health
    - Calculate overall health score
    - Determine project status

This service does NOT:
    - Scan the repository
    - Generate reports
    - Display dashboards

Author:
    Priyansh Soni

Project:
    Financial Intelligence OS (FIOS)
"""

from __future__ import annotations

from fios_live.models.project_state import HealthState
from fios_live.models.project_state import ProjectState


class HealthService:
    """
    Calculates the overall health of the FIOS project.
    """

    def evaluate(self, state: ProjectState) -> HealthState:
        """
        Evaluate project health.

        Args:
            state:
                Current ProjectState.

        Returns:
            Populated HealthState.
        """

        health = HealthState()

        score = 0

        # Repository discovered
        if state.statistics.total_folders > 0:
            score += 25

        if state.statistics.total_files > 0:
            score += 25

        # Python project exists
        if state.source.python_files > 0:
            score += 25

        # Git repository available
        if state.git.branch:
            score += 25

        health.score = float(score)

        if score >= 90:
            health.status = "Excellent"
        elif score >= 75:
            health.status = "Good"
        elif score >= 50:
            health.status = "Fair"
        else:
            health.status = "Poor"

        return health