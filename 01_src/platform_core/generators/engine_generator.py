"""
Financial Intelligence OS
Engine Generator

Purpose
-------
Generate complete engine packages from the Financial
Intelligence OS template library.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .base_generator import BaseGenerator
from .folder_generator import FolderGenerator
from .template_loader import TemplateLoader


class EngineGenerator(BaseGenerator):
    """
    Generate complete engine packages from templates.
    """

    TEMPLATE_FILES = {
        "01___init__.py.j2": "__init__.py",
        "04_models.py.j2": "models.py",
        "05_schemas.py.j2": "schemas.py",
        "06_service.py.j2": "service.py",
        "07_manager.py.j2": "manager.py",
        "08_engine.py.j2": "engine.py",
    }

    def __init__(
        self,
        output_directory: Path,
        template_directory: Path,
    ) -> None:

        super().__init__(
            name="Engine Generator",
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
        engine_name: str,
        context: dict[str, Any],
    ) -> Path:
        """
        Generate a complete engine package.
        """

        self.ensure_output_directory()

        engine_path = self.folder_generator.create(
            engine_name,
        )

        for template_name, output_name in self.TEMPLATE_FILES.items():

            rendered = self.loader.render(
                template_name,
                context,
            )

            output_file = engine_path / output_name

            output_file.write_text(
                rendered,
                encoding="utf-8",
            )

        return engine_path