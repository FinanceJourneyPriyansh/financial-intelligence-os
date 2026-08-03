"""
Financial Intelligence OS
Portfolio Schemas

Purpose
-------
Define schema validation models for the
Portfolio Engine.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PortfolioTaskSchema:
    """
    Schema representing an automation task.
    """

    name: str
    description: str = ""
    enabled: bool = True


@dataclass
class PortfolioWorkflowSchema:
    """
    Schema representing an automation workflow.
    """

    name: str
    description: str = ""
    task_count: int = 0
