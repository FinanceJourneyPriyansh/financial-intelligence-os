"""
Financial Intelligence OS (FIOS)
Builder Automation Platform

Module:
    Automation Manager

Description:
    Central orchestration engine responsible for registering,
    executing and managing Builder automation tasks.

Author:
    FinanceJourneyPriyansh

Version:
    v0.6.0-builder-m6
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ...generators.template_loader import TemplateLoader
from ...state.builder_state_manager import BuilderStateManager

import logging
from dataclasses import dataclass, field
from typing import Callable

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class AutomationTask:
    """
    Represents a single automation task.
    """

    name: str
    action: Callable[[], None]
    enabled: bool = True


@dataclass(slots=True)
class AutomationExecution:
    """
    Stores the result of an automation execution cycle.
    """

    executed: list[str] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)
    failed: list[str] = field(default_factory=list)

    @property
    def success(self) -> bool:
        """
        Return True when no executed task failed.
        """

        return not self.failed

    @property
    def completed_count(self) -> int:
        """
        Return the number of successfully executed tasks.
        """

        return len(self.executed)

    @property
    def failed_count(self) -> int:
        """
        Return the number of failed tasks.
        """

        return len(self.failed)

    @property
    def skipped_count(self) -> int:
        """
        Return the number of disabled tasks.
        """

        return len(self.skipped)

    def summary(self) -> dict[str, object]:
        """
        Return a serializable execution summary.
        """

        return {
            "success": self.success,
            "executed": self.executed,
            "skipped": self.skipped,
            "failed": self.failed,
            "completed_count": self.completed_count,
            "failed_count": self.failed_count,
            "skipped_count": self.skipped_count,
        }


class AutomationManager:
    """
    Central Builder automation manager.

    Responsibilities
    ----------------
    - Register tasks
    - Execute tasks
    - Enable/Disable tasks
    - Report execution results
    """

    def __init__(self) -> None:
        self._tasks: dict[str, AutomationTask] = {}

    # --------------------------------------------------
    # Registration
    # --------------------------------------------------

    def register(
        self,
        task: AutomationTask,
    ) -> None:
        """
        Register an automation task.
        """

        if task.name in self._tasks:
            raise ValueError(
                f"Task '{task.name}' already exists."
            )

        self._tasks[task.name] = task

        logger.info(
            "Registered automation task: %s",
            task.name,
        )

    # --------------------------------------------------
    # Execute
    # --------------------------------------------------

    def execute(self) -> AutomationExecution:
        """
        Execute every enabled automation task.

        Each task is isolated so one failed task does not
        prevent the remaining registered tasks from running.
        """

        result = AutomationExecution()

        logger.info(
            "Automation execution started. tasks=%d",
            len(self._tasks),
        )

        for task in self._tasks.values():

            if not task.enabled:

                result.skipped.append(task.name)

                logger.info(
                    "Skipping disabled task: %s",
                    task.name,
                )

                continue

            logger.info(
                "Executing task: %s",
                task.name,
            )

            try:

                task.action()

                result.executed.append(task.name)

                logger.info(
                    "Automation task completed: %s",
                    task.name,
                )

            except Exception:

                result.failed.append(task.name)

                logger.exception(
                    "Automation task failed: %s",
                    task.name,
                )

        logger.info(
            "Automation execution completed. "
            "executed=%d skipped=%d failed=%d",
            result.completed_count,
            result.skipped_count,
            result.failed_count,
        )

        return result

    # --------------------------------------------------
    # Utilities
    # --------------------------------------------------

    def register_documentation_tasks(
        self,
        state_manager: BuilderStateManager,
        repository_root: Path,
    ) -> None:
        """
        Register Builder documentation automation tasks.

        Documentation generation reuses the existing Builder State,
        TemplateLoader, configured output paths, and canonical templates.
        """

        state = state_manager.state

        documentation = state.get(
            "documentation",
            {},
        )

        automation = state.get(
            "automation",
            {},
        )

        template_directory = (
            repository_root
            / "00_control_center"
            / "05_templates"
            / "01_documentation"
        )

        loader = TemplateLoader(
            template_directory,
        )

        def generate_document(
            template_name: str,
            state_key: str,
        ) -> None:
            """
            Render one configured Builder document.
            """

            configuration = documentation.get(
                state_key,
                {},
            )

            output_path = configuration.get(
                "path",
            )

            if not output_path:
                raise ValueError(
                    f"Documentation path is not configured: {state_key}"
                )

            content = loader.render(
                template_name,
                state,
            )

            output_file = (
                repository_root
                / output_path
            )

            output_file.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            output_file.write_text(
                content,
                encoding="utf-8",
            )

        tasks = [
            (
                "builder_status",
                "00_builder_status.md.j2",
                "auto_update_builder_status",
            ),
            (
                "ai_continuation",
                "01_ai_continuation.md.j2",
                "auto_update_ai_continuation",
            ),
            (
                "builder_readme",
                "02_builder_readme.md.j2",
                "auto_generate_builder_readme",
            ),
            (
                "release_notes",
                "03_release_notes.md.j2",
                "auto_generate_release_notes",
            ),
            (
                "audit_report",
                "04_audit_report.md.j2",
                "auto_generate_audit_report",
            ),
        ]

        for task_name, template_name, automation_key in tasks:
            self.register(
                AutomationTask(
                    name=f"documentation:{task_name}",
                    action=lambda
                    template_name=template_name,
                    task_name=task_name: generate_document(
                        template_name,
                        task_name,
                    ),
                    enabled=bool(
                        automation.get(
                            automation_key,
                            False,
                        )
                    ),
                )
            )

    def list_tasks(self) -> list[str]:
        """
        Return registered task names.
        """

        return list(self._tasks.keys())

    def task_count(self) -> int:
        """
        Return number of registered tasks.
        """

        return len(self._tasks)

    def clear(self) -> None:
        """
        Remove all registered tasks.
        """

        self._tasks.clear()

        logger.info(
            "Automation registry cleared."
        )
