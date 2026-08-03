"""
Financial Intelligence OS
Project Generator

Purpose
-------
Generate complete Financial Intelligence OS projects
using the Generator Platform and Template Library.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .base_generator import BaseGenerator
from .folder_generator import FolderGenerator
from .yaml_generator import YAMLGenerator
from .readme_generator import ReadmeGenerator
from .engine_generator import EngineGenerator
from .domain_generator import DomainGenerator
from .product_generator import ProductGenerator
from .interface_generator import InterfaceGenerator


class ProjectGenerator(BaseGenerator):
    """
    Generate complete Financial Intelligence OS projects.
    """

    def __init__(
        self,
        output_directory: Path,
        template_directory: Path,
    ) -> None:

        super().__init__(
            name="Project Generator",
            output_directory=output_directory,
        )

        self.folder_generator = FolderGenerator(output_directory)
        self.yaml_generator = YAMLGenerator(output_directory)
        self.readme_generator = ReadmeGenerator(
            output_directory,
            template_directory,
        )

        self.engine_generator = EngineGenerator(
            output_directory,
            template_directory,
        )

        self.domain_generator = DomainGenerator(
            output_directory,
            template_directory,
        )

        self.product_generator = ProductGenerator(
            output_directory,
            template_directory,
        )

        self.interface_generator = InterfaceGenerator(
            output_directory,
            template_directory,
        )

    def generate(
        self,
        project_name: str,
        context: dict[str, Any],
    ) -> Path:
        """
        Generate a complete project structure.
        """

        self.ensure_output_directory()

        project_path = self.folder_generator.create(
            project_name,
        )

        self.readme_generator.generate(
            template_name="00_readme.md.j2",
            context=context,
            filename=str(project_path / "README.md"),
        )

        return project_path