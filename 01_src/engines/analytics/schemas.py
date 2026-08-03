"""
Financial Intelligence OS
Analytics Schemas

Purpose
-------
Define schema models for the Analytics Engine.
These schemas describe the structure of analytical
tasks and workflows.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AnalysisTaskSchema:
    """
    Schema representing an analytics task.
    """

    name: str
    description: str = ""
    enabled: bool = True


@dataclass
class AnalysisWorkflowSchema:
    """
    Schema representing an analytics workflow.
    """

    name: str
    description: str = ""
    task_count: int = 0