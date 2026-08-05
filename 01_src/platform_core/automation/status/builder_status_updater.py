"""
Financial Intelligence OS (FIOS)
Builder Automation Platform

Module:
    Builder Status Updater

Description:
    Maintains the Builder_Status.md document by storing and
    updating Builder operational metadata.

Author:
    FinanceJourneyPriyansh

Version:
    v0.5.0-builder-m5
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class BuilderStatus:

    builder_version: str
    completed_milestones: int
    total_milestones: int
    current_milestone: int
    builder_health: int
    repository_status: str
    working_tree: str
    latest_tag: str
    current_branch: str

    @property
    def progress(self) -> int:
        """
        Overall Builder completion percentage.
        """

        return int(
            (self.completed_milestones / self.total_milestones) * 100
        )


class BuilderStatusUpdater:
    """
    Stores and manages Builder status.

    Future Builder milestones will connect this class
    directly to Builder_Status.md.
    """

    def __init__(self) -> None:

        self._status: BuilderStatus | None = None

    # -----------------------------------------------------

    def update(
        self,
        status: BuilderStatus,
    ) -> None:
        """
        Update Builder status.
        """

        self._status = status

        logger.info(
            "Builder status updated to version %s",
            status.builder_version,
        )

    # -----------------------------------------------------

    def status(self) -> BuilderStatus | None:
        """
        Return current Builder status.
        """

        return self._status

    # -----------------------------------------------------

    def summary(self) -> dict:

        if self._status is None:

            return {}

        return {
            "builder_version": self._status.builder_version,
            "completed_milestones": self._status.completed_milestones,
            "total_milestones": self._status.total_milestones,
            "progress": self._status.progress,
            "builder_health": self._status.builder_health,
            "repository_status": self._status.repository_status,
            "working_tree": self._status.working_tree,
            "latest_tag": self._status.latest_tag,
            "current_branch": self._status.current_branch,
        }   