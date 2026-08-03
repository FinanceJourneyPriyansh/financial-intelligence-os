"""
Financial Intelligence OS
Forecasting Schemas

Purpose
-------
Define schema validation models for the
Forecasting Engine.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ForecastingTaskSchema:
    """
    Schema representing an automation task.
    """

    name: str
    description: str = ""
    enabled: bool = True


@dataclass
class ForecastingWorkflowSchema:
    """
    Schema representing an automation workflow.
    """

    name: str
    description: str = ""
    task_count: int = 0
