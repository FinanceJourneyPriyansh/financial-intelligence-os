"""
Financial Intelligence OS
Ai Schemas

Purpose
-------
Define schema validation models for the
Ai Engine.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AiTaskSchema:
    """
    Schema representing an automation task.
    """

    name: str
    description: str = ""
    enabled: bool = True


@dataclass
class AiWorkflowSchema:
    """
    Schema representing an automation workflow.
    """

    name: str
    description: str = ""
    task_count: int = 0
