"""
Financial Intelligence OS
Excel Schemas

Purpose
-------
Define schema validation models for the
Excel Engine.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ExcelTaskSchema:
    """
    Schema representing an automation task.
    """

    name: str
    description: str = ""
    enabled: bool = True


@dataclass
class ExcelWorkflowSchema:
    """
    Schema representing an automation workflow.
    """

    name: str
    description: str = ""
    task_count: int = 0
