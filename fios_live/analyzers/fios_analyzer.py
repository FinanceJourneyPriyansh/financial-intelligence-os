"""
============================================================
Financial Intelligence OS (FIOS)
FIOS Analyzer
============================================================

Module:
    fios_live.analyzers.fios_analyzer

Purpose:
    Analyzes the current Financial Intelligence OS runtime
    state and produces high-level platform insights.

Unlike scanners, the analyzer does not inspect the file
system. It interprets the runtime state and determines
whether each FIOS subsystem is operational.

Responsibilities:
    - Analyze platform readiness
    - Evaluate subsystem status
    - Produce platform summary

Author:
    Priyansh Soni

Project:
    Financial Intelligence OS (FIOS)
"""

from __future__ import annotations

from fios_live.models.fios_state import FIOSState
from fios_live.models.platform_status import PlatformStatus


class FIOSAnalyzer:
    """
    Interprets the FIOS runtime state.

    Converts raw project information into meaningful
    platform-level operational status.
    """

    def analyze(self, state: FIOSState) -> PlatformStatus:
        """
        Analyze the current FIOS platform.

        Args:
            state:
                Current FIOS runtime state.

        Returns:
            PlatformStatus describing the operational
            readiness of the Financial Intelligence OS.
        """

        status = PlatformStatus()

        # ----------------------------------------------------
        # Foundation
        # ----------------------------------------------------
        if state.project.statistics.total_files > 0:
            status.foundation = "READY"

        # ----------------------------------------------------
        # Platform Core
        # ----------------------------------------------------
        if state.project.source.python_files > 0:
            status.platform_core = "READY"

        # ----------------------------------------------------
        # Builder
        # ----------------------------------------------------
        if state.project.git.branch:
            status.builder = "ACTIVE"

        # ----------------------------------------------------
        # Runtime
        # ----------------------------------------------------
        if state.health.score >= 75:
            status.runtime = "READY"

        # ----------------------------------------------------
        # FIOS Live
        # ----------------------------------------------------
        status.fios_live = "ACTIVE"

        # ----------------------------------------------------
        # Documentation
        # ----------------------------------------------------
        if state.project.documentation.markdown_files > 0:
            status.documentation = "GOOD"

        # ----------------------------------------------------
        # Tests
        # ----------------------------------------------------
        status.tests = "AVAILABLE"

        # ----------------------------------------------------
        # Overall Platform
        # ----------------------------------------------------
        if state.health.score >= 90:
            status.overall = "OPERATIONAL"
        elif state.health.score >= 75:
            status.overall = "READY"
        else:
            status.overall = "DEGRADED"

        return status