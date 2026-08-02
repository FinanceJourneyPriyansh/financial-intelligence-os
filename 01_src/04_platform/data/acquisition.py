"""
Financial Intelligence OS
Data Acquisition Engine
"""

from src.helper import setup_logger
from src.data.exporter.csv_exporter import CSVExporter

logger = setup_logger()


class DataAcquisitionEngine:
    """
    Central engine responsible for coordinating
    all data acquisition connectors.
    """

    def __init__(self):
        self.connectors = []
        self.exporter = CSVExporter()

    def register_connector(self, connector):
        """
        Register a data connector.
        """
        self.connectors.append(connector)

    def run(self):
        """
        Execute all registered connectors.
        """

        print("=" * 70)
        print("DATA ACQUISITION ENGINE")
        print("=" * 70)

        for connector in self.connectors:

            data = connector.run()

            self.exporter.export(
                data,
                connector.name.lower().replace(" ", "_"),
            )

        print()
        print("=" * 70)
        print("Data Acquisition Completed")
        print("=" * 70)