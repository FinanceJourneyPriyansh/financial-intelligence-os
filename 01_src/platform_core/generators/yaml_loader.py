"""
Financial Intelligence OS
YAML Loader

Purpose
-------
Load YAML configuration files into Python dictionaries
for use by the Financial Intelligence OS Generator Engine.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class YAMLLoader:
    """
    Load YAML configuration files.
    """

    def load(
        self,
        yaml_file: Path,
    ) -> dict[str, Any]:
        """
        Load a YAML file into a Python dictionary.
        """

        if not yaml_file.exists():
            raise FileNotFoundError(
                f"YAML file not found: {yaml_file}"
            )

        with yaml_file.open(
            "r",
            encoding="utf-8",
        ) as file:

            data = yaml.safe_load(file)

        return data or {}

    def load_directory(
        self,
        directory: Path,
    ) -> dict[str, Any]:
        """
        Load every YAML file in a directory.

        Each YAML file contributes its top-level
        objects directly into the shared context.
        """

        if not directory.exists():
            raise FileNotFoundError(
                f"Directory not found: {directory}"
            )

        context: dict[str, Any] = {}

        for yaml_file in sorted(
            directory.glob("*.yaml")
        ):

            data = self.load(yaml_file)

            if not isinstance(
                data,
                dict,
            ):
                continue

            context.update(data)

        return context

    def load_blueprint(
        self,
        core_directory: Path,
        blueprint_directory: Path,
    ) -> dict[str, Any]:
        """
        Load the complete Financial Intelligence OS
        blueprint by combining Core and Blueprint
        directories into a single context.
        """

        context: dict[str, Any] = {}

        context.update(
            self.load_directory(
                core_directory
            )
        )

        context.update(
            self.load_directory(
                blueprint_directory
            )
        )

        return context