"""
Financial Intelligence OS
Generic API Connector
"""

from typing import Any

import pandas as pd

from src.data.clients.http_client import HTTPClient
from src.data.connectors.base_connector import BaseConnector
from src.data.connectors.api_registry import API_REGISTRY


class APIConnector(BaseConnector):
    """
    Generic connector for all REST APIs.

    The connector reads its configuration from
    API_REGISTRY and uses HTTPClient to communicate
    with external services.
    """

    def __init__(self, source_name: str):

        if source_name not in API_REGISTRY:
            raise ValueError(f"Unknown data source: {source_name}")

        self.config = API_REGISTRY[source_name]

        super().__init__(self.config["name"])

        self.client = HTTPClient(
            base_url=self.config["base_url"],
            timeout=self.config["timeout"],
        )

    def fetch(self) -> Any:
        """
        Fetch raw data from the configured API.
        """

        endpoint = self.config["endpoints"]["countries"]

        params = {
            "format": self.config["format"],
        }

        return self.client.get(
            endpoint=endpoint,
            params=params,
        )

    def transform(self, data: Any) -> pd.DataFrame:
        """
        Convert API response into a DataFrame.
        """

        print(f"Transforming {self.name} response...")

        # World Bank returns:
        # [metadata, records]

        if isinstance(data, list) and len(data) > 1:
            return pd.DataFrame(data[1])

        return pd.DataFrame(data)