"""
Financial Intelligence OS (FIOS)
Builder AI
"""

from __future__ import annotations

from fios_live.brain.models.repository_state import RepositoryState


class BuilderAI:
    """
    Converts Repository Brain findings into actionable recommendations.

    BuilderAI is the single action-planning layer of the Repository Brain.
    It does not scan the repository and does not modify files.
    """

    def analyze(
        self,
        state: RepositoryState,
    ) -> RepositoryState:

        actions: list[str] = []

        if state.empty_directories:
            actions.append(
                f"Remove or reuse {len(state.empty_directories)} empty directories."
            )

        if state.duplicate_files:
            actions.append(
                f"Merge or review {len(state.duplicate_files)} duplicate files."
            )

        if state.dead_files:
            actions.append(
                f"Review or archive {len(state.dead_files)} unused files."
            )

        if state.architecture_score < 95:
            actions.append(
                "Improve repository architecture."
            )

        if state.health_score < 95:
            actions.append(
                "Improve repository health."
            )

        if not actions:
            actions.append(
                "Repository is operating optimally."
            )

        state.recommendations.extend(actions)

        return state