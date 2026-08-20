"""
FIOS Silver Acquisition Service

B3.1:
Acquire external silver-market data and normalize it into
the generic FIOS MarketObservation contract.
"""

from __future__ import annotations

import yfinance as yf

from platform_core.data.market_observation import MarketObservation


class SilverAcquisitionService:
    """Acquire silver market observations from Yahoo Finance."""

    SYMBOL = "SI=F"
    SOURCE = "yahoo_finance"

    def fetch_latest(self) -> MarketObservation:
        """Fetch the latest valid silver observation."""

        history = yf.Ticker(self.SYMBOL).history(
            period="5d",
            interval="1d",
        )

        if history.empty:
            raise RuntimeError(
                f"No silver market data returned for {self.SYMBOL}."
            )

        valid = history.dropna(subset=["Close"])

        if valid.empty:
            raise RuntimeError(
                f"No valid silver closing price returned for {self.SYMBOL}."
            )

        row = valid.iloc[-1]

        timestamp = valid.index[-1]

        if hasattr(timestamp, "to_pydatetime"):
            timestamp = timestamp.to_pydatetime()

        previous_price = None

        if len(valid) >= 2:
            previous_price = float(
                valid.iloc[-2]["Close"]
            )

        price = float(row["Close"])

        change_pct = None

        if previous_price not in (None, 0):
            change_pct = (
                (price - previous_price)
                / previous_price
                * 100.0
            )

        return MarketObservation(
            instrument=self.SYMBOL,
            source=self.SOURCE,
            timestamp=timestamp,
            price=price,
            volume=int(row["Volume"]),
            previous_price=previous_price,
            change_pct=change_pct,
        )
