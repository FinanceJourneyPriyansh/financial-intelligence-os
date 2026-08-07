"""
============================================================
Financial Intelligence OS (FIOS)
Cleanup Engine
============================================================
"""

from __future__ import annotations

from fios_live.brain.models.repository_state import RepositoryState


class CleanupEngine:
    """
    Generates safe cleanup recommendations.
    """

    def analyze(
        self,
        state: RepositoryState,
    ) -> RepositoryState:

        if state.empty_directories:
            state.recommendations.append(
                f"Remove or reuse {len(state.empty_directories)} empty directories."
            )

        if state.dead_files:
            state.recommendations.append(
                f"Review {len(state.dead_files)} unused files."
            )

        if state.duplicate_files:
            state.recommendations.append(
                f"Merge or remove {len(state.duplicate_files)} duplicate files."
            )

        if not (
            state.empty_directories
            or state.dead_files
            or state.duplicate_files
        ):
            state.recommendations.append(
                "Repository cleanup not required."
            )

        return state