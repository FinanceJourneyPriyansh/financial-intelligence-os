"""
Financial Intelligence OS (FIOS)
Monitoring Platform

Metrics Collector

Aggregates metrics produced by all monitoring modules.

Version:
v0.4.0-builder-m4
"""

from __future__ import annotations

from typing import Any


class MetricsCollector:
    """Collect and aggregate monitoring metrics."""

    def collect(
        self,
        repository_metrics: dict[str, Any],
        generator_metrics: dict[str, Any],
        validation_metrics: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Aggregate all monitoring metrics.

        Returns
        -------
        dict
            Consolidated monitoring metrics.
        """

        modules = [
            repository_metrics,
            generator_metrics,
            validation_metrics,
        ]

        successful_modules = sum(
            1
            for module in modules
            if module.get("status") == "PASS"
        )

        failed_modules = len(modules) - successful_modules

        return {
            "repository": repository_metrics,
            "generator": generator_metrics,
            "validation": validation_metrics,
            "summary": {
                "modules_monitored": len(modules),
                "successful_modules": successful_modules,
                "failed_modules": failed_modules,
            },
        }