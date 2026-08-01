"""
Financial Intelligence OS
Base Connector

Defines the standard interface for all data connectors.
"""

from abc import ABC, abstractmethod

from src.helper import setup_logger

logger = setup_logger()


class BaseConnector(ABC):
    """
    Abstract base class for all data connectors.
    """

    def __init__(self, name: str):
        self.name = name

    def connect(self) -> None:
        """
        Establish connection to the data source.
        """
        logger.info(f"{self.name}: Connecting...")
        print(f"Connecting to {self.name}...")

    @abstractmethod
    def fetch(self):
        """
        Fetch data from the data source.
        """
        pass

    def transform(self, data):
        """
        Transform raw data into a standard format.
        """
        logger.info(f"{self.name}: Transforming data...")
        return data

    def export(self, data):
        """
        Export processed data.

        This will be implemented in the Export Engine.
        """
        logger.info(f"{self.name}: Export step skipped.")
        return data

    def disconnect(self) -> None:
        """
        Close connection to the data source.
        """
        logger.info(f"{self.name}: Disconnecting...")
        print(f"Disconnected from {self.name}.")

    def run(self):
        """
        Execute complete connector lifecycle.
        """

        self.connect()

        raw_data = self.fetch()

        processed_data = self.transform(raw_data)

        self.disconnect()

        return processed_data