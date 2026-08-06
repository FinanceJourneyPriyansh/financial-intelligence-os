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
    Load and save YAML configuration files.
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
