"""
Financial Intelligence OS
Folder Generator

Purpose
-------
Generate folders and directory structures required
by Financial Intelligence OS.
"""

from __future__ import annotations

from pathlib import Path

from .base_generator import BaseGenerator


class FolderGenerator(BaseGenerator):
    """
    Generate project folders.
    """

    def __init__(
        self,
        output_directory: Path,
    ) -> None:

        super().__init__(
            name="Folder Generator",
            output_directory=output_directory,
        )

    def generate(
        self,
        folders: list[str],
    ) -> None:
        """
        Generate the specified folder structure.
        """

        self.ensure_output_directory()

        for folder in folders:

            path = self.output_directory / folder

            path.mkdir(
                parents=True,
                exist_ok=True,
            )

    def create(
        self,
        folder_name: str,
    ) -> Path:
        """
        Create a single folder.
        """

        path = self.output_directory / folder_name

        path.mkdir(
            parents=True,
            exist_ok=True,
        )

        return path