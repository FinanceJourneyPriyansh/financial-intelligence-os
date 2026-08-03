"""
Financial Intelligence OS
Automation Schemas

Purpose
-------
Define schema validation models for the
Automation Engine.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AutomationTaskSchema:
    """
    Schema representing an automation task.
    """

    name: str
    description: str = ""
    enabled: bool = True


@dataclass
class AutomationWorkflowSchema:
    """
    Schema representing an automation workflow.
    """

    name: str
    description: str = ""
    task_count: int = 0