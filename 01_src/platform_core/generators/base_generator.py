"""
Financial Intelligence OS
Base Generator

Purpose
-------
Provides the abstract foundation for all generators
within Financial Intelligence OS.

Every generator should inherit from BaseGenerator.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from datetime import datetime


class BaseGenerator(ABC):
    """
    Abstract base class for all FIOS generators.
    """

    def __init__(
        self,
        name: str,
        output_directory: Path,
    ) -> None:

        self.name = name
        self.output_directory = output_directory
        self.created_at = datetime.now()

    @property
    def generator_name(self) -> str:
        """
        Return the generator name.
        """

        return self.name

    @property
    def output_path(self) -> Path:
        """
        Return the output directory.
        """

        return self.output_directory

    def ensure_output_directory(self) -> None:
        """
        Create the output directory if it does not exist.
        """

        self.output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    @abstractmethod
    def generate(self, *args, **kwargs) -> None:
        """
        Generate an artifact.

        Must be implemented by every generator.
        """
        raise NotImplementedError

    def info(self) -> dict:
        """
        Return generator metadata.
        """

        return {
            "generator": self.name,
            "output_directory": str(self.output_directory),
            "created_at": self.created_at.isoformat(),
        }