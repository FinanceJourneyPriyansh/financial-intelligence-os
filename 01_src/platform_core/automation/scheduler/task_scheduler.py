"""
Financial Intelligence OS (FIOS)
Builder Automation Platform

Module:
    Task Scheduler

Description:
    Maintains the execution order for Builder automation tasks.

Author:
    FinanceJourneyPriyansh

Version:
    v0.5.0-builder-m5
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class ScheduledTask:
    """
    Represents a scheduled Builder task.
    """

    name: str
    priority: int = 100


@dataclass
class TaskScheduler:
    """
    Maintains execution order for Builder automation tasks.
    """

    _tasks: list[ScheduledTask] = field(default_factory=list)

    def add_task(
        self,
        name: str,
        priority: int = 100,
    ) -> None:
        """
        Add a task to the scheduler.
        """

        self._tasks.append(
            ScheduledTask(
                name=name,
                priority=priority,
            )
        )

    def execution_order(self) -> list[str]:
        """
        Return tasks sorted by priority.
        Lower priority value executes first.
        """

        ordered = sorted(
            self._tasks,
            key=lambda task: task.priority,
        )

        return [task.name for task in ordered]

    def clear(self) -> None:
        """
        Remove all scheduled tasks.
        """

        self._tasks.clear()

    def task_count(self) -> int:
        """
        Return number of scheduled tasks.
        """

        return len(self._tasks)