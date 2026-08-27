from __future__ import annotations

import html
import json
import re
from datetime import datetime, timezone

import requests

from platform_core.data.gold_quote_observation import GoldQuoteObservation
from platform_core.data.gold_provider_capability import (
    GoldDataCapability,
    GoldProviderMetadata,
)


class IBJAGoldProvider:
    """
    IBJA India Gold benchmark adapter.

    IBJA publishes Gold benchmark history through the HdnGold
    hidden input as HTML-escaped JSON.

    This provider is a reference/benchmark source, not a
    second-by-second realtime market feed.
    """

    name = "ibja"

    URL = "https://www.ibjarates.com/index.aspx"

    PURITIES = ("999", "995", "916", "750", "585")

    def __init__(self, timeout: float = 15.0) -> None:
        self.timeout = timeout

    def available(self) -> bool:
        try:
            response = requests.get(
                self.URL,
                timeout=self.timeout,
                headers={"User-Agent": "FIOS-Gold/1.0"},
            )
            return response.ok
        except requests.RequestException:
            return False

    def fetch_latest(self) -> GoldQuoteObservation:
        response = requests.get(
            self.URL,
            timeout=self.timeout,
            headers={"User-Agent": "FIOS-Gold/1.0"},
        )
        response.raise_for_status()

        values = self._extract_current_gold_rates(response.text)

        if values is None:
            raise RuntimeError(
                "IBJA Gold rates could not be parsed."
            )

        quote_timestamp = self._extract_latest_label_timestamp(
            response.text
        )

        if quote_timestamp is None:
            raise RuntimeError(
                "IBJA Gold benchmark date could not be parsed."
            )

        return GoldQuoteObservation(
            instrument="IBJA-GOLD-999",
            source=self.name,
            timestamp=quote_timestamp,
            ltp=values["999"],
            previous_close=None,
            change_abs=None,
            change_pct=None,
            volume=None,
            currency="INR",
            unit="10_grams",
            is_realtime=False,
            purity_rates=values,
        )

    @staticmethod
    def _extract_latest_label_timestamp(
        text: str,
    ) -> datetime | None:
        """Extract the latest published IBJA benchmark date."""

        element_match = re.search(
            r'<input[^>]*\bid=["\']HdnGold["\'][^>]*>',
            text,
            flags=re.IGNORECASE | re.DOTALL,
        )

        if element_match is None:
            return None

        element = element_match.group(0)

        value_match = re.search(
            r'\bvalue\s*=\s*(["\'])(.*?)\1',
            element,
            flags=re.IGNORECASE | re.DOTALL,
        )

        if value_match is None:
            return None

        raw = html.unescape(value_match.group(2))

        try:
            payload = json.loads(raw)
        except (TypeError, ValueError, json.JSONDecodeError):
            return None

        if not isinstance(payload, dict):
            return None

        labels = payload.get("labels")

        if not isinstance(labels, list) or not labels:
            return None

        latest_label = labels[-1]

        if not isinstance(latest_label, str):
            return None

        try:
            return datetime.strptime(
                latest_label,
                "%d/%m/%Y",
            ).replace(tzinfo=timezone.utc)
        except ValueError:
            return None

    @staticmethod
    def _extract_current_gold_rates(
        text: str,
    ) -> dict[str, float] | None:
        """
        Extract the latest published Gold values from IBJA.

        The live IBJA page contains an input similar to:

            <input type="hidden"
                   name="HdnGold"
                   id="HdnGold"
                   value="HTML-escaped JSON" />

        The JSON contains:
            labels
            purity999
            purity916

        Additional purity series are accepted when IBJA publishes
        them. Missing series are never fabricated.
        """

        # Find the HdnGold input element.
        element_match = re.search(
            r'<input[^>]*\bid=["\']HdnGold["\'][^>]*>',
            text,
            flags=re.IGNORECASE | re.DOTALL,
        )

        if element_match is None:
            return None

        element = element_match.group(0)

        # Extract value="..." or value='...' from the isolated element.
        value_match = re.search(
            r'\bvalue\s*=\s*(["\'])(.*?)\1',
            element,
            flags=re.IGNORECASE | re.DOTALL,
        )

        if value_match is None:
            return None

        raw = html.unescape(value_match.group(2))

        try:
            payload = json.loads(raw)
        except (TypeError, ValueError, json.JSONDecodeError):
            return None

        if not isinstance(payload, dict):
            return None

        labels = payload.get("labels")

        if not isinstance(labels, list) or not labels:
            return None

        result: dict[str, float] = {}

        for purity in IBJAGoldProvider.PURITIES:
            series = payload.get(f"purity{purity}")

            if not isinstance(series, list) or not series:
                continue

            try:
                value = float(series[-1])
            except (TypeError, ValueError):
                continue

            if value <= 0:
                continue

            result[purity] = value

        if "999" not in result:
            return None

        return result

    def metadata(
        self,
        observation: GoldQuoteObservation,
    ) -> GoldProviderMetadata:
        retrieved_at = datetime.now(timezone.utc)

        timestamp = observation.timestamp

        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=timezone.utc)
        else:
            timestamp = timestamp.astimezone(timezone.utc)

        return GoldProviderMetadata(
            provider=self.name,
            capability=GoldDataCapability.REFERENCE,
            quote_timestamp=timestamp,
            retrieved_at=retrieved_at,
            data_age_seconds=max(
                0.0,
                (retrieved_at - timestamp).total_seconds(),
            ),
            is_realtime=False,
            market_role="india_gold_benchmark",
            instrument=observation.instrument,
        )


class WGCGoldProvider:
    """
    World Gold Council reference adapter.

    WGC data is treated as historical/reference data.
    No realtime quote is fabricated from the public page.
    """

    name = "wgc"

    URL = "https://www.gold.org/goldhub/data/gold-prices"

    def __init__(self, timeout: float = 15.0) -> None:
        self.timeout = timeout

    def available(self) -> bool:
        try:
            response = requests.get(
                self.URL,
                timeout=self.timeout,
                headers={"User-Agent": "FIOS-Gold/1.0"},
            )
            return response.ok
        except requests.RequestException:
            return False

    def fetch_latest(self) -> GoldQuoteObservation:
        response = requests.get(
            self.URL,
            timeout=self.timeout,
            headers={"User-Agent": "FIOS-Gold/1.0"},
        )
        response.raise_for_status()

        raise RuntimeError(
            "WGC public page is available as a reference source, "
            "but does not expose a directly consumable realtime "
            "GoldQuoteObservation."
        )

    def metadata(
        self,
        observation: GoldQuoteObservation,
    ) -> GoldProviderMetadata:
        retrieved_at = datetime.now(timezone.utc)

        timestamp = observation.timestamp

        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=timezone.utc)
        else:
            timestamp = timestamp.astimezone(timezone.utc)

        return GoldProviderMetadata(
            provider=self.name,
            capability=GoldDataCapability.REFERENCE,
            quote_timestamp=timestamp,
            retrieved_at=retrieved_at,
            data_age_seconds=max(
                0.0,
                (retrieved_at - timestamp).total_seconds(),
            ),
            is_realtime=False,
            market_role="global_gold_reference",
            instrument=observation.instrument,
        )