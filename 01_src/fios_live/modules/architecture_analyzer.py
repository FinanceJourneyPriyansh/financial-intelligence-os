"""
============================================================
Financial Intelligence OS (FIOS)
Architecture Analyzer
============================================================
"""

from __future__ import annotations

from fios_live.brain.models.repository_state import RepositoryState


class ArchitectureAnalyzer:
    """
    Evaluates repository architecture.
    """

    def analyze(self, state: RepositoryState) -> RepositoryState:

        score = 100.0

        if state.total_files == 0:
            score -= 100

        if state.empty_directories:
            score -= min(len(state.empty_directories), 10)

            state.architecture_issues.append(
                f"{len(state.empty_directories)} empty directories detected."
            )

        if state.packages == 0:
            score -= 10

            state.architecture_issues.append(
                "No Python packages detected."
            )

        if state.python_files == 0:
            score -= 50

            state.architecture_issues.append(
                "No Python source files detected."
            )

        state.architecture_score = max(score, 0.0)

        return state