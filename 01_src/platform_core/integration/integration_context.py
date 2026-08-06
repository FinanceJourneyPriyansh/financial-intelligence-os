"""
============================================================
Financial Intelligence OS (FIOS)
Integration Context
============================================================

Milestone:
    Milestone 6 – Builder Integration Platform

Purpose:
    Shared runtime context used by every Builder platform
    during a single Builder execution.

The Integration Context acts as the communication layer
between Generator, Validation, Monitoring,
Automation and Release Pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass(slots=True)
class IntegrationContext:
    """
    Shared Builder execution context.
    """

    builder_version: str

    builder_state: Dict[str, Any]

    started_at: datetime = field(default_factory=datetime.now)

    completed_at: Optional[datetime] = None

    current_stage: str = ""

    executed_stages: List[str] = field(default_factory=list)

    reports: Dict[str, Any] = field(default_factory=dict)

    metrics: Dict[str, Any] = field(default_factory=dict)

    artifacts: Dict[str, Any] = field(default_factory=dict)

    warnings: List[str] = field(default_factory=list)

    errors: List[str] = field(default_factory=list)

    metadata: Dict[str, Any] = field(default_factory=dict)

    def start_stage(self, stage: str) -> None:
        """
        Mark the beginning of a Builder stage.
        """

        self.current_stage = stage

        self.executed_stages.append(stage)

    def complete(self) -> None:
        """
        Mark Builder execution complete.
        """

        self.completed_at = datetime.now()

    @property
    def duration_seconds(self) -> Optional[float]:
        """
        Return Builder execution duration.
        """

        if self.completed_at is None:
            return None

        return (
            self.completed_at - self.started_at
        ).total_seconds()

    @property
    def success(self) -> bool:
        """
        Builder execution succeeded.
        """

        return len(self.errors) == 0

    def summary(self) -> Dict[str, Any]:
        """
        Return execution summary.
        """

        return {
            "builder_version": self.builder_version,
            "success": self.success,
            "current_stage": self.current_stage,
            "executed_stages": len(self.executed_stages),
            "warnings": len(self.warnings),
            "errors": len(self.errors),
            "duration_seconds": self.duration_seconds,
        }   