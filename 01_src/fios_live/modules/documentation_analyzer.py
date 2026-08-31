"""
============================================================
Financial Intelligence OS (FIOS)
Documentation Analyzer
============================================================
"""

from __future__ import annotations

from pathlib import Path

from fios_live.brain.models.repository_state import RepositoryState
from fios_live.config.scan_config import CONFIG


class DocumentationAnalyzer:
    """
    Analyzes repository documentation.
    """

    def analyze(
        self,
        repository_root: Path,
        state: RepositoryState,
    ) -> RepositoryState:

        readme_count = 0

        for root in CONFIG.resolved_roots(repository_root):

            for file in root.rglob("*.md"):

                if file.name.lower().startswith("readme"):
                    readme_count += 1

        if readme_count == 0:
            state.recommendations.append(
                "No README files detected."
            )
        else:
            state.recommendations.append(
                f"Detected {readme_count} README files."
            )

        return state