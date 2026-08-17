"""
FIOS Gold Acquisition Service

Day 1 Phase 2 proof:
Acquire external gold-market data and normalize it into
a timestamped FIOS observation.

This service intentionally keeps the first acquisition
vertical small. It does not modify the FIOS dashboard,
kernel, or existing internal runtime.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

import yfinance as yf


@dataclass(frozen=True)
class GoldObservation:
    instrument: str
    source: str
    timestamp: datetime
    price: float
    volume: int


class GoldAcquisitionService:
    """Acquire gold market observations from Yahoo Finance."""

    SYMBOL = "GC=F"
    SOURCE = "yahoo_finance"

    def fetch_latest(self) -> GoldObservation:
        """Fetch the latest valid gold observation."""

        history = yf.Ticker(self.SYMBOL).history(
            period="5d",
            interval="1d",
        )

        if history.empty:
            raise RuntimeError(
                f"No gold market data returned for {self.SYMBOL}."
            )

        latest = history.dropna(subset=["Close"]).tail(1)

        if latest.empty:
            raise RuntimeError(
                f"No valid gold closing price returned for {self.SYMBOL}."
            )

        row = latest.iloc[0]

        timestamp = latest.index[-1]

        if hasattr(timestamp, "to_pydatetime"):
            timestamp = timestamp.to_pydatetime()

        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=timezone.utc)

        return GoldObservation(
            instrument=self.SYMBOL,
            source=self.SOURCE,
            timestamp=timestamp,
            price=float(row["Close"]),
            volume=int(row["Volume"]),
        )
