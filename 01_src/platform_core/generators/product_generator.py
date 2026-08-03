"""
Financial Intelligence OS
Product Generator

Purpose
-------
Generate complete product packages from the Financial
Intelligence OS template library.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .base_generator import BaseGenerator
from .folder_generator import FolderGenerator
from .template_loader import TemplateLoader


class ProductGenerator(BaseGenerator):
    """
    Generate complete product packages from templates.
    """

    TEMPLATE_FILES = {
        "01___init__.py.j2": "__init__.py",
        "03_config.py.j2": "config.py",
        "06_service.py.j2": "service.py",
    }

    def __init__(
        self,
        output_directory: Path,
        template_directory: Path,
    ) -> None:

        super().__init__(
            name="Product Generator",
            output_directory=output_directory,
        )

        self.folder_generator = FolderGenerator(
            output_directory,
        )

        self.loader = TemplateLoader(
            template_directory,
        )

    def generate(
        self,
        product_name: str,
        context: dict[str, Any],
    ) -> Path:
        """
        Generate a complete product package.
        """

        self.ensure_output_directory()

        product_path = self.folder_generator.create(
            product_name,
        )

        for template_name, output_name in self.TEMPLATE_FILES.items():

            rendered = self.loader.render(
                template_name,
                context,
            )

            output_file = product_path / output_name

            output_file.write_text(
                rendered,
                encoding="utf-8",
            )

        return product_path