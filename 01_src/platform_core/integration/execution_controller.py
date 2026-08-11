"""
============================================================
Financial Intelligence OS (FIOS)
Execution Controller
============================================================

Milestone:
    Milestone 6 – Builder Integration Platform

Purpose:
    Controls the complete Builder execution lifecycle.

Responsibilities:
    - Start execution
    - Stop execution
    - Pause execution
    - Resume execution
    - Recovery
    - Failure handling
    - Runtime state management

Notes:
    This class controls execution only.

    It does NOT execute platform business logic.
    Workflow execution is delegated to the WorkflowEngine.

Version:
    v0.6.0-builder-m6
"""

from __future__ import annotations

import logging
from enum import Enum, auto

from .integration_context import IntegrationContext
from .workflow_engine import WorkflowEngine


LOGGER = logging.getLogger(__name__)


class ExecutionState(Enum):
    """
    Builder Runtime states.
    """

    IDLE = auto()

    INITIALIZING = auto()

    RUNNING = auto()

    PAUSED = auto()

    COMPLETED = auto()

    FAILED = auto()

    STOPPED = auto()


class ExecutionController:
    """
    Controls the Builder Runtime lifecycle.
    """

    def __init__(
        self,
        context: IntegrationContext,
        workflow: WorkflowEngine,
    ) -> None:

        self.context = context

        self.workflow = workflow

        self.state = ExecutionState.IDLE

    # ==========================================================
    # Lifecycle
    # ==========================================================

    def start(self) -> None:
        """
        Start Builder execution.
        """

        LOGGER.info("Starting Builder Runtime...")

        self.state = ExecutionState.INITIALIZING

        try:

            self.state = ExecutionState.RUNNING

            self.workflow.execute()

            self.context.complete()

            self.state = ExecutionState.COMPLETED

            LOGGER.info(
                "Builder Runtime completed successfully."
            )

        except Exception as error:

            self.context.errors.append(
                str(error)
            )

            self.state = ExecutionState.FAILED

            LOGGER.exception(
                "Builder Runtime execution failed."
            )

            raise
    def stop(self) -> None:
        """
        Stop Builder execution.
        """

        LOGGER.info("Stopping Builder Runtime.")

        self.state = ExecutionState.STOPPED

    def pause(self) -> None:
        """
        Pause Builder execution.
        """

        LOGGER.info("Pausing Builder Runtime.")

        self.state = ExecutionState.PAUSED

    def resume(self) -> None:
        """
        Resume Builder execution.
        """

        LOGGER.info("Resuming Builder Runtime.")

        self.state = ExecutionState.RUNNING

    # ==========================================================
    # Recovery
    # ==========================================================

    def restart(self) -> None:
        """
        Restart Builder execution.
        """

        LOGGER.info("Restarting Builder Runtime.")

        self.start()

    def reset(self) -> None:
        """
        Reset runtime to initial state.
        """

        LOGGER.info("Resetting Builder Runtime.")

        self.state = ExecutionState.IDLE

    # ==========================================================
    # Status
    # ==========================================================

    @property
    def is_running(self) -> bool:

        return self.state == ExecutionState.RUNNING

    @property
    def is_completed(self) -> bool:

        return self.state == ExecutionState.COMPLETED

    @property
    def is_failed(self) -> bool:

        return self.state == ExecutionState.FAILED

    @property
    def is_paused(self) -> bool:

        return self.state == ExecutionState.PAUSED

    @property
    def is_idle(self) -> bool:

        return self.state == ExecutionState.IDLE

    def status(self) -> dict:
        """
        Return runtime status.
        """

        return {
            "state": self.state.name,
            "success": self.context.success,
            "current_stage": self.context.current_stage,
            "executed_stages": len(
                self.context.executed_stages
            ),
            "duration": self.context.duration_seconds,
        }

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}"
            f"(state={self.state.name})"
        )
