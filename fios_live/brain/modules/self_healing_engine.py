"""
============================================================
Financial Intelligence OS (FIOS)
Self-Healing Engine
============================================================
"""

from __future__ import annotations

from fios_live.brain.models.repository_state import RepositoryState


class SelfHealingEngine:
    """
    Detects repository problems and proposes safe fixes.
    """

    def analyze(
        self,
        state: RepositoryState,
    ) -> RepositoryState:

        if state.empty_directories:
            state.recommendations.append(
                "Safe Action: Remove empty directories."
            )

        if state.duplicate_files:
            state.recommendations.append(
                "Safe Action: Review duplicate files."
            )

        if state.dead_files:
            state.recommendations.append(
                "Safe Action: Archive unused files."
            )

        if state.architecture_score < 95:
            state.recommendations.append(
                "Safe Action: Improve repository architecture."
            )

        if state.health_score < 95:
            state.recommendations.append(
                "Safe Action: Improve repository health."
            )

        return state