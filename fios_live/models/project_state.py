"""
============================================================
Financial Intelligence OS (FIOS)
Project State Model
============================================================

Module:
    fios_live.models.project_state

Purpose:
    Defines the master state object shared across the
    FIOS Live platform.

The ProjectState acts as the Digital Twin of the
Financial Intelligence OS.

Every service updates only its own section.

Author:
    Priyansh Soni

Project:
    Financial Intelligence OS (FIOS)
"""

from __future__ import annotations

from dataclasses import dataclass, field


# ============================================================
# Repository
# ============================================================

@dataclass(slots=True)
class RepositoryState:
    """Repository information."""

    root_path: str = ""
    folders: list[str] = field(default_factory=list)
    files: list[str] = field(default_factory=list)


# ============================================================
# Git
# ============================================================

@dataclass(slots=True)
class GitState:
    """Git repository information."""

    branch: str = ""
    latest_commit: str = ""
    latest_tag: str = ""
    clean: bool = False


# ============================================================
# Source Code
# ============================================================

@dataclass(slots=True)
class SourceState:
    """Python source information."""

    python_files: int = 0
    packages: int = 0
    modules: int = 0


# ============================================================
# Documentation
# ============================================================

@dataclass(slots=True)
class DocumentationState:
    """Documentation information."""

    markdown_files: int = 0
    readme_files: int = 0


# ============================================================
# Builder
# ============================================================

@dataclass(slots=True)
class BuilderState:
    """Builder platform status."""

    integrated: bool = False
    validation_ready: bool = False
    automation_ready: bool = False


# ============================================================
# Runtime
# ============================================================

@dataclass(slots=True)
class RuntimeState:
    """Runtime information."""

    running: bool = False
    active_workflow: str = ""


# ============================================================
# Tests
# ============================================================

@dataclass(slots=True)
class TestState:
    """Testing information."""

    total_tests: int = 0
    passed_tests: int = 0


# ============================================================
# Health
# ============================================================

@dataclass(slots=True)
class HealthState:
    """Overall project health."""

    score: float = 0.0
    status: str = "Unknown"


# ============================================================
# Statistics
# ============================================================

@dataclass(slots=True)
class StatisticsState:
    """General repository statistics."""

    total_folders: int = 0
    total_files: int = 0


# ============================================================
# Master State
# ============================================================

@dataclass(slots=True)
class ProjectState:
    """
    Master Digital Twin of the Financial Intelligence OS.

    Every FIOS Live service shares this object.
    """

    repository: RepositoryState = field(default_factory=RepositoryState)
    git: GitState = field(default_factory=GitState)
    source: SourceState = field(default_factory=SourceState)
    documentation: DocumentationState = field(default_factory=DocumentationState)
    builder: BuilderState = field(default_factory=BuilderState)
    runtime: RuntimeState = field(default_factory=RuntimeState)
    tests: TestState = field(default_factory=TestState)
    health: HealthState = field(default_factory=HealthState)
    statistics: StatisticsState = field(default_factory=StatisticsState)