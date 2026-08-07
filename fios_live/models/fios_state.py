"""
============================================================
Financial Intelligence OS (FIOS)
FIOS State Model
============================================================

Module:
    fios_live.models.fios_state

Purpose:
    Defines the master runtime state for the FIOS Live
    platform.

The FIOSState acts as the root object of the FIOS Live
Kernel. It aggregates all runtime state objects into a
single shared model.

Responsibilities:
    - Own ProjectState
    - Own HealthState
    - Provide a single runtime object shared across
      FIOS Live components

Future Extensions:
    - RuntimeState
    - BuilderState
    - WorkflowState
    - AutomationState
    - DashboardState

Author:
    Priyansh Soni

Project:
    Financial Intelligence OS (FIOS)
"""

from __future__ import annotations

from dataclasses import dataclass, field

from fios_live.models.project_state import HealthState
from fios_live.models.project_state import ProjectState


@dataclass(slots=True)
class FIOSState:
    """
    Master runtime state for the Financial Intelligence OS.

    This object represents the Digital Twin of the complete
    FIOS platform. Every major FIOS Live component should
    consume this object rather than managing multiple
    independent state objects.
    """

    project: ProjectState = field(default_factory=ProjectState)

    health: HealthState = field(default_factory=HealthState)