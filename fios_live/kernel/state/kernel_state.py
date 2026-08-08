"""
============================================================
Financial Intelligence OS (FIOS)
Kernel State
============================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class KernelState:
    """
    Global state of the FIOS Kernel.
    """

    boot_time: datetime = field(default_factory=datetime.now)

    running: bool = False

    repository_loaded: bool = False

    brain_online: bool = False

    builder_online: bool = False

    auditor_online: bool = False

    dashboard_online: bool = False

    automation_online: bool = False

    health_score: float = 0.0

    architecture_score: float = 0.0

    last_event: str = "BOOT"

    uptime_seconds: int = 0