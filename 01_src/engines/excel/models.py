"""
Financial Intelligence OS
Excel Models

Purpose
-------
Define the core data models used by the
Excel Engine.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ExcelTask:
    """
    Represents a single automation task.
    """

    name: str
    description: str = ""
    enabled: bool = True
    status: str = "Pending"
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class ExcelWorkflow:
    """
    Represents an automation workflow.
    """

    name: str
    tasks: list[ExcelTask] = field(default_factory=list)

    def add_task(self, task: ExcelTask) -> None:
        """
        Add a task to the workflow.
        """

        self.tasks.append(task)

    def task_count(self) -> int:
        """
        Return the total number of tasks.
        """

        return len(self.tasks)
