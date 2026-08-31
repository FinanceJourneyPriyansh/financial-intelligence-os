"""
============================================================
Financial Intelligence OS (FIOS)
Code Analyzer
============================================================
"""

from __future__ import annotations

import ast
from pathlib import Path

from fios_live.brain.models.repository_state import RepositoryState
from fios_live.config.scan_config import CONFIG


class CodeAnalyzer:
    """
    Performs basic repository code quality analysis.
    """

    def analyze(
        self,
        repository_root: Path,
        state: RepositoryState,
    ) -> RepositoryState:

        class_count = 0
        function_count = 0

        for root in CONFIG.resolved_roots(repository_root):

            for file in root.rglob("*.py"):

                try:
                    tree = ast.parse(file.read_text(encoding="utf-8"))

                    for node in ast.walk(tree):

                        if isinstance(node, ast.ClassDef):
                            class_count += 1

                        elif isinstance(node, (
                            ast.FunctionDef,
                            ast.AsyncFunctionDef,
                        )):
                            function_count += 1

                except Exception:
                    continue

        state.recommendations.append(
            f"Detected {class_count} classes."
        )

        state.recommendations.append(
            f"Detected {function_count} functions."
        )

        return state