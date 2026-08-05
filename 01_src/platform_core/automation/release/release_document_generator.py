"""
Financial Intelligence OS (FIOS)
Builder Automation Platform

Module:
    Release Document Generator

Description:
    Generates Builder documentation from the Builder State
    configuration and Jinja2 templates.

Author:
    FinanceJourneyPriyansh

Version:
    v0.5.0-builder-m5
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import yaml
from jinja2 import Environment, FileSystemLoader

logger = logging.getLogger(__name__)


class ReleaseDocumentGenerator:
    """
    Generates Builder documentation from templates.
    """

    CONFIG_ROOT = Path("00_control_center") / "02_configs"

    TEMPLATE_ROOT = (
        Path("00_control_center")
        / "05_templates"
        / "01_documentation"
    )

    OUTPUTS = {

        "00_builder_status.md.j2":
            Path("03_docs/05_Phases/Builder_Status.md"),

        "01_ai_continuation.md.j2":
            Path("99_project/AI_Continuation_Guide.md"),

        "02_builder_readme.md.j2":
            Path("03_docs/06_Builder/README.md"),

        "03_release_notes.md.j2":
            Path("08_reports/Release_Notes.md"),

        "04_audit_report.md.j2":
            Path("08_reports/Automation_Platform_Audit_Report.md"),

    }

    def __init__(
        self,
        state_file: str = "10_builder_state.yaml",
    ) -> None:

        self._state_path = self.CONFIG_ROOT / state_file

        self._environment = Environment(

            loader=FileSystemLoader(
                self.TEMPLATE_ROOT
            ),

            autoescape=False,

            trim_blocks=True,

            lstrip_blocks=True,

        )

        self._state = self._load_state()

    # -----------------------------------------------------

    def _load_state(self) -> dict[str, Any]:

        logger.info(
            "Loading Builder State: %s",
            self._state_path,
        )

        with self._state_path.open(
            "r",
            encoding="utf-8",
        ) as stream:

            return yaml.safe_load(stream)

    # -----------------------------------------------------

    def render_template(
        self,
        template_name: str,
    ) -> str:

        logger.info(
            "Rendering template %s",
            template_name,
        )

        template = self._environment.get_template(
            template_name
        )

        return template.render(**self._state)

    # -----------------------------------------------------

    def write_document(
        self,
        template_name: str,
        output_path: Path,
    ) -> None:

        output = self.render_template(
            template_name
        )

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_path.write_text(

            output,

            encoding="utf-8",

        )

        logger.info(
            "Generated %s",
            output_path,
        )

    # -----------------------------------------------------

    def generate_all(self) -> None:

        logger.info(
            "Generating Builder documentation..."
        )

        for template_name, output_path in self.OUTPUTS.items():

            self.write_document(

                template_name,

                output_path,

            )

        logger.info(
            "Builder documentation generation completed."
        )