"""
Financial Intelligence OS
Domain Generator

Purpose
-------
Generate complete domain packages from the Financial
Intelligence OS template library.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .base_generator import BaseGenerator
from .folder_generator import FolderGenerator
from .template_loader import TemplateLoader


class DomainGenerator(BaseGenerator):
    """
    Generate complete domain packages from templates.
    """

    TEMPLATE_FILES = {
        "01___init__.py.j2": "__init__.py",
        "04_models.py.j2": "models.py",
        "05_schemas.py.j2": "schemas.py",
        "06_service.py.j2": "services.py",
    }

    def __init__(
        self,
        output_directory: Path,
        template_directory: Path,
    ) -> None:

        super().__init__(
            name="Domain Generator",
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
        domain_name: str,
        context: dict[str, Any],
    ) -> Path:
        """
        Generate a complete domain package.
        """

        self.ensure_output_directory()

        domain_path = self.folder_generator.create(
            domain_name,
        )

        for template_name, output_name in self.TEMPLATE_FILES.items():

            rendered = self.loader.render(
                template_name,
                context,
            )

            output_file = domain_path / output_name

            output_file.write_text(
                rendered,
                encoding="utf-8",
            )

        return domain_path