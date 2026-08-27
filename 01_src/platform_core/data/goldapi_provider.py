from __future__ import annotations

import os
from datetime import datetime, timezone

import requests

from platform_core.data.gold_quote_observation import (
    GoldQuoteObservation,
)
from platform_core.data.gold_provider_capability import (
    GoldDataCapability,
    GoldProviderMetadata,
)


class GoldAPIProvider:
    """
    Optional real-time GoldAPI.io provider.

    The provider is activated only when GOLDAPI_API_KEY is configured.
    FIOS remains operational without the paid provider.
    """

    name = "goldapi"

    URL = "https://www.goldapi.io/api/price/XAU/USD"

    def __init__(
        self,
        api_key: str | None = None,
        timeout: float = 10.0,
    ) -> None:
        self.api_key = (
            api_key
            or os.getenv("GOLDAPI_API_KEY")
        )
        self.timeout = timeout

    def available(self) -> bool:
        return bool(self.api_key)

    def fetch_latest(self) -> GoldQuoteObservation:
        if not self.api_key:
            raise RuntimeError(
                "GOLDAPI_API_KEY is not configured."
            )

        response = requests.get(
            self.URL,
            headers={
                "x-access-token": self.api_key,
                "Accept": "application/json",
                "User-Agent": "FIOS-Gold/1.0",
            },
            timeout=self.timeout,
        )

        response.raise_for_status()

        payload = response.json()

        timestamp = datetime.fromtimestamp(
            float(payload["timestamp"]),
            tz=timezone.utc,
        )

        ltp = float(payload["price"])

        previous_close = payload.get(
            "prev_close_price"
        )

        open_price = payload.get(
            "open_price"
        )

        high = payload.get(
            "high_price"
        )

        low = payload.get(
            "low_price"
        )

        bid = payload.get("bid")
        ask = payload.get("ask")

        change_abs = payload.get("ch")
        change_pct = payload.get("change_percent")

        if previous_close is not None:
            previous_close = float(previous_close)

        if open_price is not None:
            open_price = float(open_price)

        if high is not None:
            high = float(high)

        if low is not None:
            low = float(low)

        if bid is not None:
            bid = float(bid)

        if ask is not None:
            ask = float(ask)

        if change_abs is not None:
            change_abs = float(change_abs)

        if change_pct is not None:
            change_pct = float(change_pct)

        return GoldQuoteObservation(
            instrument=str(
                payload.get(
                    "symbol",
                    "XAUUSD",
                )
            ),
            source=self.name,
            timestamp=timestamp,
            ltp=ltp,
            open=open_price,
            high=high,
            low=low,
            previous_close=previous_close,
            bid=bid,
            ask=ask,
            change_abs=change_abs,
            change_pct=change_pct,
            currency=str(
                payload.get(
                    "currency",
                    "USD",
                )
            ),
            unit=str(
                payload.get(
                    "unit",
                    "troy_ounce",
                )
            ),
            is_realtime=True,
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

        age = max(
            0.0,
            (retrieved_at - timestamp).total_seconds(),
        )

        return GoldProviderMetadata(
            provider=self.name,
            capability=GoldDataCapability.REALTIME,
            quote_timestamp=timestamp,
            retrieved_at=retrieved_at,
            data_age_seconds=age,
            is_realtime=observation.is_realtime,
            market_role="global_realtime_gold",
            instrument=observation.instrument,
        )
