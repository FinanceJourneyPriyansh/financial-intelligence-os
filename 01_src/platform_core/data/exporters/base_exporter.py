"""
Financial Intelligence OS
Base Exporter

Defines the standard interface for all exporters.
"""

from abc import ABC, abstractmethod

from src.helper import setup_logger

logger = setup_logger()


class BaseExporter(ABC):
    """
    Abstract base exporter.
    """

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def export(self, data, output_path: str):
        """
        Export data.
        """
        pass

    def log_success(self, output_path: str):
        """
        Log successful export.
        """

        logger.info(f"{self.name}: Exported -> {output_path}")
        print(f"✓ Saved -> {output_path}")