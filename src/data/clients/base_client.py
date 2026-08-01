"""
Financial Intelligence OS
Base API Client
"""

from abc import ABC
import requests

from src.helper import setup_logger

logger = setup_logger()


class BaseClient(ABC):
    """
    Base HTTP client for all APIs.
    """

    def __init__(self, base_url: str):

        self.base_url = base_url

        self.session = requests.Session()

        self.timeout = 30

    def get(self, endpoint: str, params=None):

        url = f"{self.base_url}{endpoint}"

        logger.info(f"GET {url}")

        response = self.session.get(
            url,
            params=params,
            timeout=self.timeout,
        )

        response.raise_for_status()

        return response.json()