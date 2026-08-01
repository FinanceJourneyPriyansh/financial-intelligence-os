"""
Financial Intelligence OS
Generic HTTP Client
"""

from typing import Any, Dict, Optional

import requests

from src.helper import setup_logger

logger = setup_logger()


class HTTPClient:
    """
    Generic HTTP client for REST APIs.

    Handles:
    - GET requests
    - Timeouts
    - Query parameters
    - JSON responses
    """

    def __init__(self, base_url: str, timeout: int = 30):

        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Any:
        """
        Execute a GET request.
        """

        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        logger.info(f"GET {url}")

        response = self.session.get(
            url,
            params=params,
            headers=headers,
            timeout=self.timeout,
        )

        response.raise_for_status()

        return response.json()