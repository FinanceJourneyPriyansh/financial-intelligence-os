"""
Financial Intelligence OS
Generator Manager

Purpose
-------
Coordinate and manage all generators within the
Financial Intelligence OS Generator platform_core.

The Generator Manager acts as the central orchestration
layer between:

- YAML Loader
- Template Loader
- Registered Generators
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .domain_generator import DomainGenerator
from .engine_generator import EngineGenerator
from .interface_generator import InterfaceGenerator
from .product_generator import ProductGenerator
from .project_generator import ProjectGenerator
from .yaml_loader import YAMLLoader


class GeneratorManager:
    """
    Central manager for all Financial Intelligence OS generators.
    """

    def __init__(
        self,
        output_directory: Path,
        template_directory: Path,
    ) -> None:

        self.output_directory = output_directory
        self.template_directory = template_directory

        self.yaml_loader = YAMLLoader()

        self.generators = {
            "engine": EngineGenerator(
                output_directory,
                template_directory,
            ),
            "domain": DomainGenerator(
                output_directory,
                template_directory,
            ),
            "product": ProductGenerator(
                output_directory,
                template_directory,
            ),
            "interface": InterfaceGenerator(
                output_directory,
                template_directory,
            ),
            "project": ProjectGenerator(
                output_directory,
                template_directory,
            ),
        }

    def available_generators(self) -> list[str]:
        """
        Return all registered generators.
        """

        return sorted(self.generators.keys())

    def exists(
        self,
        name: str,
    ) -> bool:
        """
        Check whether a generator exists.
        """

        return name in self.generators

    def get(
        self,
        name: str,
    ):
        """
        Return a registered generator.
        """

        generator = self.generators.get(name)

        if generator is None:
            raise ValueError(
                f"Unknown generator: {name}"
            )

        return generator

    def generate(
        self,
        generator_name: str,
        component_name: str,
        context: dict[str, Any],
    ):
        """
        Generate using an existing Python context.
        """

        generator = self.get(generator_name)

        return generator.generate(
            component_name,
            context,
        )

    def generate_from_yaml(
        self,
        generator_name: str,
        component_name: str,
        yaml_file: Path,
    ):
        """
        Generate directly from a YAML blueprint.
        """

        context = self.yaml_loader.load(
            yaml_file,
        )

        return self.generate(
            generator_name,
            component_name,
            context,
        )
