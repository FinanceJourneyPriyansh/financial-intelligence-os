"""
============================================================
Financial Intelligence OS (FIOS)
Repository Brain
============================================================
"""

from __future__ import annotations

from pathlib import Path

from fios_live.brain.models.repository_state import RepositoryState
from fios_live.brain.modules.architecture_analyzer import ArchitectureAnalyzer
from fios_live.brain.modules.cleanup_engine import CleanupEngine
from fios_live.brain.modules.code_analyzer import CodeAnalyzer
from fios_live.brain.modules.dependency_analyzer import DependencyAnalyzer
from fios_live.brain.modules.documentation_analyzer import DocumentationAnalyzer
from fios_live.brain.modules.repository_health import RepositoryHealth
from fios_live.brain.modules.repository_mapper import RepositoryMapper


class RepositoryBrain:
    """
    Central intelligence engine for the FIOS repository.
    """

    def analyze(
        self,
        repository_root: Path,
    ) -> RepositoryState:

        repository_root = repository_root.resolve()

        mapper = RepositoryMapper()
        architecture = ArchitectureAnalyzer()
        dependencies = DependencyAnalyzer()
        code = CodeAnalyzer()
        documentation = DocumentationAnalyzer()
        cleanup = CleanupEngine()
        health = RepositoryHealth()

        state = mapper.map(repository_root)

        state = architecture.analyze(state)

        state = dependencies.analyze(
            repository_root,
            state,
        )

        state = code.analyze(
            repository_root,
            state,
        )

        state = documentation.analyze(
            repository_root,
            state,
        )

        state = cleanup.analyze(state)

        state = health.evaluate(state)

        return state