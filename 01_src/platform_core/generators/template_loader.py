"""
Financial Intelligence OS
Template Loader

Purpose
-------
Load and render Jinja2 templates from the Financial
Intelligence OS template library.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import TemplateNotFound


class TemplateLoader:
    """
    Load and render templates from the template library.
    """

    def __init__(
        self,
        template_directory: Path,
    ) -> None:

        self.template_directory = template_directory

        self.environment = Environment(
            loader=FileSystemLoader(template_directory),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def exists(
        self,
        template_name: str,
    ) -> bool:
        """
        Check whether a template exists.
        """

        return (self.template_directory / template_name).exists()

    def list_templates(self) -> list[str]:
        """
        Return all available templates.
        """

        return sorted(
            file.name
            for file in self.template_directory.glob("*")
            if file.is_file()
        )

    def render(
        self,
        template_name: str,
        context: dict[str, Any],
    ) -> str:
        """
        Render a template using the supplied context.
        """

        try:

            template = self.environment.get_template(
                template_name,
            )

        except TemplateNotFound as error:

            raise FileNotFoundError(
                f"Template '{template_name}' not found."
            ) from error

        return template.render(**context)