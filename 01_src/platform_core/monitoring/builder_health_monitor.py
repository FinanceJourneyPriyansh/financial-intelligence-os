"""
Financial Intelligence OS (FIOS)
Monitoring Platform

Builder Health Monitor

Calculates the overall Builder Health Score.

Version:
    v0.4.0-builder-m4
"""

from __future__ import annotations

from typing import Any


class BuilderHealthMonitor:
    """Calculate the overall Builder health."""

    def calculate(
        self,
        metrics: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Calculate the Builder Health Score.

        Parameters
        ----------
        metrics : dict
            Consolidated monitoring metrics.

        Returns
        -------
        dict
            Builder health summary.
        """

        summary = metrics.get("summary", {})

        total = summary.get("modules_monitored", 0)
        successful = summary.get("successful_modules", 0)

        if total == 0:
            score = 0
        else:
            score = round((successful / total) * 100)

        return {
            "builder_health": score,
            "modules_monitored": total,
            "successful_modules": successful,
            "failed_modules": summary.get("failed_modules", 0),
            "status": "PASS" if score == 100 else "WARNING",
        }