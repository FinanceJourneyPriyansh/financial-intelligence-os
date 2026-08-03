"""
Financial Intelligence OS
Valuation Schemas

Purpose
-------
Define schema validation models for the
Valuation Engine.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ValuationTaskSchema:
    """
    Schema representing an automation task.
    """

    name: str
    description: str = ""
    enabled: bool = True


@dataclass
class ValuationWorkflowSchema:
    """
    Schema representing an automation workflow.
    """

    name: str
    description: str = ""
    task_count: int = 0
