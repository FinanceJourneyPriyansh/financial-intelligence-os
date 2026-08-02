"""
Financial Intelligence OS
World Bank Service

High-level interface for accessing World Bank data.
"""

from src.data.clients.http_client import HTTPClient


class WorldBankService:
    """
    Service for interacting with the World Bank API.
    """

    def __init__(self):

        self.client = HTTPClient(
            base_url="https://api.worldbank.org/v2",
            timeout=30,
        )

    def get_countries(self):
        """
        Retrieve all countries.
        """

        return self.client.get(
            endpoint="/country",
            params={
                "format": "json",
                "per_page": 400,
            },
        )

    def get_country(self, country_code):
        """
        Retrieve a single country.
        """

        return self.client.get(
            endpoint=f"/country/{country_code}",
            params={
                "format": "json",
            },
        )

    def get_indicators(self):
        """
        Retrieve available indicators.
        """

        return self.client.get(
            endpoint="/indicator",
            params={
                "format": "json",
                "per_page": 500,
            },
        )

    def get_indicator(self, indicator_code):
        """
        Retrieve metadata for one indicator.
        """

        return self.client.get(
            endpoint=f"/indicator/{indicator_code}",
            params={
                "format": "json",
            },
        )

    def get_indicator_data(
        self,
        country,
        indicator,
        start_year=None,
        end_year=None,
    ):
        """
        Retrieve indicator values.
        """

        params = {
            "format": "json",
            "per_page": 1000,
        }

        if start_year:
            params["date"] = str(start_year)

        if start_year and end_year:
            params["date"] = f"{start_year}:{end_year}"

        return self.client.get(
            endpoint=f"/country/{country}/indicator/{indicator}",
            params=params,
        )