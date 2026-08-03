"""
Financial Intelligence OS
Analytics Models

Purpose
-------
Define the core data models used by the
Analytics Engine.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class AnalysisTask:
    """
    Represents a single analytics task.
    """

    name: str
    description: str = ""
    enabled: bool = True
    status: str = "Pending"
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class AnalysisWorkflow:
    """
    Represents an analytics workflow.
    """

    name: str
    tasks: list[AnalysisTask] = field(default_factory=list)

    def add_task(self, task: AnalysisTask) -> None:
        """
        Add a task to the workflow.
        """

        self.tasks.append(task)

    def task_count(self) -> int:
        """
        Return the total number of tasks.
        """

        return len(self.tasks)