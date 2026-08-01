import pandas as pd

from src.data.exporter.csv_exporter import CSVExporter


def main():

    df = pd.DataFrame(
        {
            "Country": ["India", "USA"],
            "GDP": [3.8, 27.0],
        }
    )

    exporter = CSVExporter()

    exporter.export(
        df,
        "data/raw/test/sample.csv",
    )


if __name__ == "__main__":
    main()