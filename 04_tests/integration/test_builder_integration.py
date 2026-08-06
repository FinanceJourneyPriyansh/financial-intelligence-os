"""
Financial Intelligence OS (FIOS)

Milestone 6
Builder Integration Test

Purpose
-------
Verify that the Builder Runtime initializes
successfully.
"""

from __future__ import annotations

from pathlib import Path

from platform_core.integration.builder_integration_manager import (
    BuilderIntegrationManager,
)

def test_builder_runtime_initialization() -> None:
    """
    Verify Builder Runtime initialization.
    """

    builder = BuilderIntegrationManager(
        builder_state_path=Path(
            "00_control_center/02_configs/10_builder_state.yaml"
        )
    )

    builder.initialize()

    assert builder.context is not None

    assert builder.connector is not None

    assert builder.workflow is not None

    assert builder.controller is not None

    