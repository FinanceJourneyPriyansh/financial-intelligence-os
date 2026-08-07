"""
============================================================
Financial Intelligence OS (FIOS)
Repository Health Engine
============================================================
"""

from __future__ import annotations

from fios_live.brain.models.repository_state import RepositoryState


class RepositoryHealth:
    """
    Computes the overall repository health score.
    """

    def evaluate(
        self,
        state: RepositoryState,
    ) -> RepositoryState:

        score = 100.0

        score -= min(len(state.architecture_issues) * 2, 20)

        score -= min(len(state.empty_directories), 10)

        score -= min(len(state.dead_files), 10)

        score -= min(len(state.duplicate_files), 10)

        state.health_score = max(score, 0.0)

        if state.health_score >= 95:
            state.recommendations.append(
                "Repository health is Excellent."
            )
        elif state.health_score >= 85:
            state.recommendations.append(
                "Repository health is Good."
            )
        elif state.health_score >= 70:
            state.recommendations.append(
                "Repository health is Fair."
            )
        else:
            state.recommendations.append(
                "Repository requires attention."
            )

        return state