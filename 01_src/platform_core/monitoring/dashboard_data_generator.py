"""
Financial Intelligence OS (FIOS)
Monitoring Platform

Dashboard Data Generator

Exports monitoring metrics for dashboards.

Version:
    v0.4.0-builder-m4
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class DashboardDataGenerator:
    """Generate dashboard JSON data."""

    def __init__(self) -> None:
        self.dashboard_directory = (
            Path(__file__).resolve().parents[3] /
            "05_dashboards"
        )

        self.dashboard_directory.mkdir(exist_ok=True)

    def generate(
        self,
        metrics: dict[str, Any],
        health: dict[str, Any],
    ) -> Path:
        """Generate dashboard data."""

        output_file = (
            self.dashboard_directory /
            "dashboard_metrics.json"
        )

        data = {
            "health": health,
            "metrics": metrics,
        }

        output_file.write_text(
            json.dumps(data, indent=4),
            encoding="utf-8",
        )

        return output_file