"""
Financial Intelligence OS
CSV Exporter
"""

from src.config import RAW_DATA_DIR
from src.data.exporter.base_exporter import BaseExporter


class CSVExporter(BaseExporter):
    """
    Export pandas DataFrame to CSV.
    """

    def __init__(self):
        super().__init__("CSV Exporter")

    def export(self, dataframe, dataset_name):
        """
        Save DataFrame to CSV.
        """

        folder = RAW_DATA_DIR / dataset_name

        folder.mkdir(
            parents=True,
            exist_ok=True,
        )

        output = folder / "data.csv"

        dataframe.to_csv(
            output,
            index=False,
        )

        self.log_success(output)

        return output