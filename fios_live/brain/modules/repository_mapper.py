"""
============================================================
Financial Intelligence OS (FIOS)
Repository Mapper
============================================================
"""

from __future__ import annotations

from pathlib import Path

from fios_live.brain.models.repository_state import RepositoryState
from fios_live.config.scan_config import CONFIG


class RepositoryMapper:
    """
    Builds a high-level repository map.
    """

    def map(self, repository_root: Path) -> RepositoryState:

        state = RepositoryState()

        repository_root = repository_root.resolve()

        state.repository_name = repository_root.name
        state.root_path = str(repository_root)

        for root in CONFIG.resolved_roots(repository_root):

            for path in root.rglob("*"):

                if path.is_dir():

                    state.total_folders += 1

                    try:
                        if not any(path.iterdir()):
                            state.empty_directories.append(
                                str(path.relative_to(repository_root))
                            )
                    except Exception:
                        pass

                    continue

                state.total_files += 1

                suffix = path.suffix.lower()

                if suffix == ".py":
                    state.python_files += 1

                    if path.name == "__init__.py":
                        state.packages += 1
                    else:
                        state.modules += 1

                elif suffix == ".md":
                    state.markdown_files += 1

                elif suffix == ".json":
                    state.json_files += 1

                elif suffix in (".yaml", ".yml"):
                    state.yaml_files += 1

                if "tests" in path.parts:
                    state.tests += 1

        return state