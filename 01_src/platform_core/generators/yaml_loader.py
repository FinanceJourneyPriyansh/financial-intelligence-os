"""
Financial Intelligence OS (FIOS)

YAML Loader

Purpose
-------
Load and save YAML configuration files used by the
Financial Intelligence OS Builder.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class YAMLLoader:
    """
    Load and aggregate YAML configuration files.
    """

    def load(
        self,
        yaml_file: Path,
    ) -> dict[str, Any]:
        """
        Load a single YAML file.
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

            if isinstance(data, dict):
                context.update(data)

        return context

    def load_blueprint(
        self,
        core_directory: Path,
        blueprint_directory: Path,
    ) -> dict[str, Any]:
        """
        Load the complete Builder blueprint context.

        This combines the Core and Blueprint
        configuration directories into a single
        context dictionary.
        """

        context: dict[str, Any] = {}

        context.update(
            self.load_directory(core_directory)
        )

        context.update(
            self.load_directory(blueprint_directory)
        )

        return context