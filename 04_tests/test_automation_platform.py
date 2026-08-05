"""
Financial Intelligence OS (FIOS)
Builder Automation Platform

Integration Test Suite

Purpose:
    Validate Automation Platform integration.

Author:
    FinanceJourneyPriyansh

Version:
    v0.5.0-builder-m5
"""

from __future__ import annotations

import sys
from pathlib import Path

# ==========================================================
# Repository Setup
# ==========================================================

ROOT = Path(__file__).resolve().parents[1]

SRC = ROOT / "01_src"

sys.path.insert(0, str(SRC))

# ==========================================================
# Imports
# ==========================================================

from platform_core.automation.manager import (
    AutomationManager,
    AutomationTask,
)

from platform_core.automation.scheduler import (
    TaskScheduler,
)

from platform_core.automation.release import (
    ReleasePipeline,
)

from platform_core.automation.status import (
    BuilderStatus,
    BuilderStatusUpdater,
)

from platform_core.automation.continuation import (
    AIContinuation,
    AIContinuationUpdater,
)

from platform_core.automation.utils import (
    AutomationUtils,
)

# ==========================================================
# Tests
# ==========================================================


def test_automation_manager():

    print("Testing Automation Manager...")

    manager = AutomationManager()

    manager.register(
        AutomationTask(
            name="demo",
            action=lambda: None,
        )
    )

    assert manager.task_count() == 1

    print("PASS")


# ----------------------------------------------------------


def test_scheduler():

    print("Testing Task Scheduler...")

    scheduler = TaskScheduler()

    scheduler.add_task(
        "validation",
        20,
    )

    scheduler.add_task(
        "generator",
        10,
    )

    order = scheduler.execution_order()

    assert order == [
        "generator",
        "validation",
    ]

    print("PASS")


# ----------------------------------------------------------


def test_release_pipeline():

    print("Testing Release Pipeline...")

    pipeline = ReleasePipeline()

    pipeline.add_stage(
        "Stage 1",
        lambda: None,
    )

    pipeline.add_stage(
        "Stage 2",
        lambda: None,
    )

    result = pipeline.execute()

    assert len(result.completed) == 2

    print("PASS")


# ----------------------------------------------------------


def test_builder_status():

    print("Testing Builder Status...")

    updater = BuilderStatusUpdater()

    status = BuilderStatus(

        builder_version="v0.5.0",

        completed_milestones=5,

        total_milestones=6,

        current_milestone=5,

        builder_health=100,

        repository_status="READY",

        working_tree="CLEAN",

        latest_tag="v0.5.0",

        current_branch="feature/fios-cli",

    )

    updater.update(status)

    summary = updater.summary()

    assert summary["progress"] == 83

    print("PASS")


# ----------------------------------------------------------


def test_ai_continuation():

    print("Testing AI Continuation...")

    updater = AIContinuationUpdater()

    continuation = AIContinuation(

        builder_version="v0.5.0",

        current_milestone="Automation",

        completed_milestones=5,

        total_milestones=6,

        builder_health=100,

        repository_status="READY",

        next_action="Audit",

    )

    updater.update(continuation)

    summary = updater.summary()

    assert summary["builder_health"] == 100

    print("PASS")


# ----------------------------------------------------------


def test_utils():

    print("Testing Automation Utilities...")

    assert AutomationUtils.progress(5, 6) == 83

    assert AutomationUtils.file_exists(ROOT)

    assert AutomationUtils.repository_root().exists()

    print("PASS")


# ==========================================================
# Main
# ==========================================================

def main():

    print()

    print("=" * 60)
    print("FIOS Builder Automation Platform Integration Test")
    print("=" * 60)

    test_automation_manager()

    test_scheduler()

    test_release_pipeline()

    test_builder_status()

    test_ai_continuation()

    test_utils()

    print()

    print("=" * 60)
    print("ALL INTEGRATION TESTS PASSED")
    print("=" * 60)


if __name__ == "__main__":

    main()