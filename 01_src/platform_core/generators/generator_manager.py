"""
Financial Intelligence OS
Generator Manager

Purpose
-------
Central orchestration layer for all Financial
Intelligence OS artifact generators.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .architecture_generator import ArchitectureGenerator
from .blueprint_overview_generator import (
    BlueprintOverviewGenerator,
)
from .project_summary_generator import (
    ProjectSummaryGenerator,
)
from .readme_generator import ReadmeGenerator
from .repository_structure_generator import (
    RepositoryStructureGenerator,
)
from .roadmap_generator import RoadmapGenerator
from .technology_stack_generator import (
    TechnologyStackGenerator,
)
from .yaml_loader import YAMLLoader


class GeneratorManager:
    """
    Central manager for all repository
    artifact generators.
    """

    def __init__(
        self,
        output_directory: Path,
        template_directory: Path,
        core_directory: Path,
        blueprint_directory: Path,
    ) -> None:

        self.output_directory = output_directory

        self.template_directory = template_directory

        self.core_directory = core_directory

        self.blueprint_directory = blueprint_directory

        self.yaml_loader = YAMLLoader()

        self.generators = {

            "readme": (
                ReadmeGenerator(
                    output_directory,
                    template_directory,
                ),
                "00_readme.md.j2",
            ),

            "repository": (
                RepositoryStructureGenerator(
                    output_directory,
                    template_directory,
                ),
                "01_repository_structure.md.j2",
            ),

            "architecture": (
                ArchitectureGenerator(
                    output_directory,
                    template_directory,
                ),
                "02_architecture.md.j2",
            ),

            "project_summary": (
                ProjectSummaryGenerator(
                    output_directory,
                    template_directory,
                ),
                "03_project_summary.md.j2",
            ),

            "blueprint": (
                BlueprintOverviewGenerator(
                    output_directory,
                    template_directory,
                ),
                "04_blueprint_overview.md.j2",
            ),

            "technology": (
                TechnologyStackGenerator(
                    output_directory,
                    template_directory,
                ),
                "05_technology_stack.md.j2",
            ),

            "roadmap": (
                RoadmapGenerator(
                    output_directory,
                    template_directory,
                ),
                "06_roadmap.md.j2",
            ),
        }

    def available_generators(
        self,
    ) -> list[str]:
        """
        Return all registered generators.
        """

        return sorted(
            self.generators.keys()
        )

    def exists(
        self,
        name: str,
    ) -> bool:
        """
        Check whether a generator exists.
        """

        return name in self.generators

    def load_context(
        self,
    ) -> dict[str, Any]:
        """
        Load the complete Financial
        Intelligence OS blueprint.
        """

        return self.yaml_loader.load_blueprint(
            self.core_directory,
            self.blueprint_directory,
        )

    def generate(
        self,
        name: str,
    ) -> Path:
        """
        Generate a single artifact.
        """

        if name not in self.generators:

            raise ValueError(
                f"Unknown generator: {name}"
            )

        generator, template = (
            self.generators[name]
        )

        context = self.load_context()

        return generator.generate(
            template_name=template,
            context=context,
        )

    def generate_all(
        self,
    ) -> dict[str, Path]:
        """
        Generate every registered artifact.
        """

        outputs: dict[str, Path] = {}

        context = self.load_context()

        for name, (
            generator,
            template,
        ) in self.generators.items():

            outputs[name] = generator.generate(
                template_name=template,
                context=context,
            )

        return outputs