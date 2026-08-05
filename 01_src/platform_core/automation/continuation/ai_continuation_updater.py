"""
Financial Intelligence OS (FIOS)
Builder Automation Platform

Module:
    AI Continuation Updater

Description:
    Stores and manages Builder continuation information used
    to generate the AI_Continuation_Guide.md document.

Author:
    FinanceJourneyPriyansh

Version:
    v0.5.0-builder-m5
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class AIContinuation:

    builder_version: str
    current_milestone: str
    completed_milestones: int
    total_milestones: int
    builder_health: int
    repository_status: str
    next_action: str
    notes: str = ""


class AIContinuationUpdater:
    """
    Stores Builder continuation information.

    Future Builder milestones will connect this class
    directly to AI_Continuation_Guide.md.
    """

    def __init__(self) -> None:

        self._continuation: AIContinuation | None = None

    # -----------------------------------------------------

    def update(
        self,
        continuation: AIContinuation,
    ) -> None:
        """
        Update Builder continuation state.
        """

        self._continuation = continuation

        logger.info(
            "Continuation updated for %s",
            continuation.current_milestone,
        )

    # -----------------------------------------------------

    def continuation(self) -> AIContinuation | None:
        """
        Return current continuation information.
        """

        return self._continuation

    # -----------------------------------------------------

    def summary(self) -> dict:

        if self._continuation is None:
            return {}

        return {
            "builder_version": self._continuation.builder_version,
            "current_milestone": self._continuation.current_milestone,
            "completed_milestones": self._continuation.completed_milestones,
            "total_milestones": self._continuation.total_milestones,
            "builder_health": self._continuation.builder_health,
            "repository_status": self._continuation.repository_status,
            "next_action": self._continuation.next_action,
            "notes": self._continuation.notes,
        }