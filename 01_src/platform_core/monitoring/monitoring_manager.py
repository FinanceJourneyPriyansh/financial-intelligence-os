"""
Financial Intelligence OS (FIOS)
Monitoring Platform

Monitoring Manager

Coordinates all monitoring modules and produces a unified
monitoring result for the Builder platform.

Version:
    v0.4.0-builder-m4
"""

from __future__ import annotations

import logging
from typing import Any

from .repository_monitor import RepositoryMonitor
from .generator_monitor import GeneratorMonitor
from .validation_monitor import ValidationMonitor
from .metrics_collector import MetricsCollector
from .builder_health_monitor import BuilderHealthMonitor
from .monitoring_report_generator import MonitoringReportGenerator
from .dashboard_data_generator import DashboardDataGenerator


logger = logging.getLogger(__name__)


class MonitoringManager:
    """
    Central coordinator for the Monitoring Platform.
    """

    def __init__(self) -> None:
        self.repository_monitor = RepositoryMonitor()
        self.generator_monitor = GeneratorMonitor()
        self.validation_monitor = ValidationMonitor()

        self.metrics_collector = MetricsCollector()
        self.health_monitor = BuilderHealthMonitor()

        self.report_generator = MonitoringReportGenerator()
        self.dashboard_generator = DashboardDataGenerator()

    def run(self) -> dict[str, Any]:
        """
        Execute the complete monitoring workflow.

        Returns
        -------
        dict
            Complete monitoring summary.
        """

        logger.info("Starting Monitoring Platform")

        repository_metrics = self.repository_monitor.run()

        generator_metrics = self.generator_monitor.run()

        validation_metrics = self.validation_monitor.run()

        metrics = self.metrics_collector.collect(
            repository_metrics=repository_metrics,
            generator_metrics=generator_metrics,
            validation_metrics=validation_metrics,
        )

        health = self.health_monitor.calculate(metrics)

        report = self.report_generator.generate(metrics, health)

        dashboard = self.dashboard_generator.generate(metrics, health)

        logger.info("Monitoring completed successfully.")

        return {
            "repository": repository_metrics,
            "generator": generator_metrics,
            "validation": validation_metrics,
            "metrics": metrics,
            "health": health,
            "report": report,
            "dashboard": dashboard,
        }