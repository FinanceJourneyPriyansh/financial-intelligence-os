"""
Financial Intelligence OS
YAML Generator

Purpose
-------
Generate YAML configuration files from structured
Python data.
"""

from __future__ import annotations

from pathlib import Path

import yaml

from .base_generator import BaseGenerator


class YAMLGenerator(BaseGenerator):
    """
    Generate YAML files.
    """

    def __init__(
        self,
        output_directory: Path,
    ) -> None:

        super().__init__(
            name="YAML Generator",
            output_directory=output_directory,
        )

    def generate(
        self,
        filename: str,
        data: dict,
    ) -> Path:
        """
        Generate a YAML file.
        """

        self.ensure_output_directory()

        output_file = self.output_directory / filename

        with output_file.open(
            "w",
            encoding="utf-8",
        ) as file:

            yaml.safe_dump(
                data,
                file,
                sort_keys=False,
                allow_unicode=True,
            )

        return output_file