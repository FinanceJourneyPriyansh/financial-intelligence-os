"""
============================================================
Financial Intelligence OS (FIOS)
Dependency Analyzer
============================================================
"""

from __future__ import annotations

import ast
from pathlib import Path

from fios_live.brain.models.repository_state import RepositoryState
from fios_live.config.scan_config import CONFIG


class DependencyAnalyzer:
    """
    Analyzes Python imports across the repository.
    """

    def analyze(
        self,
        repository_root: Path,
        state: RepositoryState,
    ) -> RepositoryState:

        imports: set[str] = set()

        for root in CONFIG.resolved_roots(repository_root):

            for file in root.rglob("*.py"):

                try:
                    tree = ast.parse(file.read_text(encoding="utf-8"))

                    for node in ast.walk(tree):

                        if isinstance(node, ast.Import):
                            for alias in node.names:
                                imports.add(alias.name)

                        elif isinstance(node, ast.ImportFrom):
                            if node.module:
                                imports.add(node.module)

                except Exception:
                    continue

        state.recommendations.append(
            f"Discovered {len(imports)} unique Python dependencies."
        )

        return state