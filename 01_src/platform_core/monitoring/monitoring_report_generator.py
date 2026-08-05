"""
Financial Intelligence OS (FIOS)
Monitoring Platform

Monitoring Report Generator

Generates a markdown monitoring report.

Version:
    v0.4.0-builder-m4
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any


class MonitoringReportGenerator:
    """Generate monitoring reports."""

    def __init__(self) -> None:
        self.report_directory = (
            Path(__file__).resolve().parents[3] / "08_reports"
        )

        self.report_directory.mkdir(exist_ok=True)

    def generate(
        self,
        metrics: dict[str, Any],
        health: dict[str, Any],
    ) -> Path:
        """Generate a monitoring report."""

        report_file = (
            self.report_directory /
            "Builder_Monitoring_Report.md"
        )

        report = f"""# Builder Monitoring Report

Generated:
{datetime.now().isoformat()}

---

## Builder Health

{health}

---

## Metrics

{metrics}
"""

        report_file.write_text(report, encoding="utf-8")

        return report_file