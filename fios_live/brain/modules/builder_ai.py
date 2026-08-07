"""
============================================================
Financial Intelligence OS (FIOS)
Builder AI
============================================================
"""

from __future__ import annotations

from fios_live.brain.models.repository_state import RepositoryState


class BuilderAI:
    """
    Generates high-level improvement plans for the repository.
    """

    def analyze(
        self,
        state: RepositoryState,
    ) -> RepositoryState:

        actions: list[str] = []

        if state.empty_directories:
            actions.append(
                f"Remove {len(state.empty_directories)} empty directories."
            )

        if state.duplicate_files:
            actions.append(
                f"Review {len(state.duplicate_files)} duplicate files."
            )

        if state.dead_files:
            actions.append(
                f"Archive {len(state.dead_files)} unused files."
            )

        if state.architecture_score < 95:
            actions.append(
                "Improve repository architecture."
            )

        if state.health_score < 95:
            actions.append(
                "Increase repository health score."
            )

        if not actions:
            actions.append(
                "Repository is operating optimally."
            )

        state.recommendations.extend(actions)

        return state