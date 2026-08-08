"""
Financial Intelligence OS (FIOS)
Repository Brain
"""

from __future__ import annotations

from pathlib import Path

from fios_live.brain.models.repository_state import RepositoryState
from fios_live.brain.modules.architecture_analyzer import ArchitectureAnalyzer
from fios_live.brain.modules.builder_ai import BuilderAI
from fios_live.brain.modules.cleanup_engine import CleanupEngine
from fios_live.brain.modules.code_analyzer import CodeAnalyzer
from fios_live.brain.modules.dependency_analyzer import DependencyAnalyzer
from fios_live.brain.modules.documentation_analyzer import DocumentationAnalyzer
from fios_live.brain.modules.repository_health import RepositoryHealth
from fios_live.brain.modules.repository_mapper import RepositoryMapper
from fios_live.brain.modules.self_healing_engine import SelfHealingEngine
from fios_live.brain.repository_report import RepositoryReport


class RepositoryBrain:
    """
    Central intelligence engine for the FIOS repository.
    """

    def analyze(
        self,
        repository_root: Path,
    ) -> RepositoryState:

        repository_root = repository_root.resolve()

        state = RepositoryMapper().map(repository_root)

        state = ArchitectureAnalyzer().analyze(state)

        state = DependencyAnalyzer().analyze(
            repository_root,
            state,
        )

        state = CodeAnalyzer().analyze(
            repository_root,
            state,
        )

        state = DocumentationAnalyzer().analyze(
            repository_root,
            state,
        )

        state = CleanupEngine().analyze(state)

        state = RepositoryHealth().evaluate(state)

        state = SelfHealingEngine().analyze(state)

        state = BuilderAI().analyze(state)

        RepositoryReport().generate(
            state,
            repository_root / "fios_live" / "reports",
        )

        return state