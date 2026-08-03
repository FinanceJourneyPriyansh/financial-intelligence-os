"""
Financial Intelligence OS
README Generator

Purpose
-------
Generate README.md files using the Financial
Intelligence OS template library.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .base_generator import BaseGenerator
from .template_loader import TemplateLoader


class ReadmeGenerator(BaseGenerator):
    """
    Generate README.md files from templates.
    """

    def __init__(
        self,
        output_directory: Path,
        template_directory: Path,
    ) -> None:

        super().__init__(
            name="README Generator",
            output_directory=output_directory,
        )

        self.loader = TemplateLoader(
            template_directory,
        )

    def generate(
        self,
        template_name: str,
        context: dict[str, Any],
        filename: str = "README.md",
    ) -> Path:
        """
        Generate a README file from a template.
        """

        self.ensure_output_directory()

        content = self.loader.render(
            template_name,
            context,
        )

        output_file = self.output_directory / filename

        output_file.write_text(
            content,
            encoding="utf-8",
        )

        return output_file