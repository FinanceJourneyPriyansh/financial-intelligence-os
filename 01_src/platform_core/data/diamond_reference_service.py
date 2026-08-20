from __future__ import annotations

from datetime import datetime, timezone
import re

import requests

from platform_core.data.diamond_reference_observation import (
    DiamondReferenceObservation,
)


class DiamondReferenceService:
    """Acquire the IDEX Diamond Index reference."""

    URL = "https://idexonline.com/diamond_prices_index"
    SOURCE = "idex_diamond_index"

    def fetch_latest(self) -> DiamondReferenceObservation:
        response = requests.get(
            self.URL,
            timeout=20,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 "
                    "FIOS-Commodity-Comparison/1.0"
                ),
            },
        )

        response.raise_for_status()

        html = response.text

        marker = "IDEX DIAMOND INDEX - TODAY`S CHANGE"
        position = html.find(marker)

        if position == -1:
            raise RuntimeError(
                "Unable to locate IDEX Diamond Index."
            )

        fragment = html[
            position:
            position + 600
        ]

        index_match = re.search(
            r"<span[^>]*>\s*"
            r"(?P<index>\d+(?:\.\d+)?)\s*"
            r"<img",
            fragment,
            re.IGNORECASE | re.DOTALL,
        )

        change_match = re.search(
            r"&nbsp;\s*"
            r"(?P<change>[+-]?\d+(?:\.\d+)?)%",
            fragment,
            re.IGNORECASE | re.DOTALL,
        )

        if not index_match:
            raise RuntimeError(
                "Unable to extract IDEX Diamond Index value."
            )

        if not change_match:
            raise RuntimeError(
                "Unable to extract IDEX Diamond Index change."
            )

        return DiamondReferenceObservation(
            asset="diamond",
            source=self.SOURCE,
            timestamp=datetime.now(timezone.utc),
            index_value=float(
                index_match.group("index")
            ),
            change_pct=float(
                change_match.group("change")
            ),
            update_frequency="hourly",
        )
