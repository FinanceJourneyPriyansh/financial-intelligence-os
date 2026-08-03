"""
Financial Intelligence OS
Risk Schemas

Purpose
-------
Define schema validation models for the
Risk Engine.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RiskTaskSchema:
    """
    Schema representing an automation task.
    """

    name: str
    description: str = ""
    enabled: bool = True


@dataclass
class RiskWorkflowSchema:
    """
    Schema representing an automation workflow.
    """

    name: str
    description: str = ""
    task_count: int = 0
