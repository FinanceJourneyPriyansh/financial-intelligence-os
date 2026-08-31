"""
============================================================
Financial Intelligence OS (FIOS)
Repository State Model
============================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class RepositoryState:

    repository_name: str = ""

    root_path: str = ""

    total_folders: int = 0

    total_files: int = 0

    python_files: int = 0

    markdown_files: int = 0

    json_files: int = 0

    yaml_files: int = 0

    tests: int = 0

    packages: int = 0

    modules: int = 0

    architecture_score: float = 0.0

    health_score: float = 0.0

    duplicate_files: list[str] = field(default_factory=list)

    dead_files: list[str] = field(default_factory=list)

    empty_directories: list[str] = field(default_factory=list)

    architecture_issues: list[str] = field(default_factory=list)

    recommendations: list[str] = field(default_factory=list)