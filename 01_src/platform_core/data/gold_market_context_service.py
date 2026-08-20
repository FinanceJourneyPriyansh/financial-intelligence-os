"""
FIOS Gold Market Context Service

Day 2 Phase 2:
Observe gold together with key market signals and identify
candidate drivers of gold movement.

Important:
This module identifies contemporaneous relationships.
It does NOT claim causal attribution.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

import yfinance as yf


@dataclass(frozen=True)
class MarketSignal:
    instrument: str
    source: str
    timestamp: datetime
    value: float
    previous_value: float | None
    change_pct: float | None


@dataclass(frozen=True)
class GoldMarketContext:
    gold: MarketSignal
    signals: tuple[MarketSignal, ...]
    gold_change_pct: float | None
    candidate_drivers: tuple[str, ...]


class GoldMarketContextService:
    """
    Acquire gold and contextual market signals.

    Signals:
        GC=F      Gold futures
        DX-Y.NYB  US Dollar Index
        ^TNX      US 10Y Treasury yield
        INR=X     USD/INR
    """

    SOURCE = "yahoo_finance"

    SYMBOLS = {
        "gold": "GC=F",
        "dollar": "DX-Y.NYB",
        "us10y": "^TNX",
        "usdinr": "INR=X",
    }

    def _fetch_signal(self, symbol: str) -> MarketSignal:
        history = yf.Ticker(symbol).history(
            period="5d",
            interval="1d",
        )

        if history.empty:
            raise RuntimeError(
                f"No market data returned for {symbol}."
            )

        valid = history.dropna(subset=["Close"])

        if valid.empty:
            raise RuntimeError(
                f"No valid closing value returned for {symbol}."
            )

        latest = valid.iloc[-1]
        previous = valid.iloc[-2] if len(valid) >= 2 else None

        timestamp = valid.index[-1]

        if hasattr(timestamp, "to_pydatetime"):
            timestamp = timestamp.to_pydatetime()

        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=timezone.utc)

        value = float(latest["Close"])

        previous_value = (
            float(previous["Close"])
            if previous is not None
            else None
        )

        change_pct = None

        if previous_value not in (None, 0):
            change_pct = (
                (value - previous_value)
                / previous_value
                * 100.0
            )

        return MarketSignal(
            instrument=symbol,
            source=self.SOURCE,
            timestamp=timestamp,
            value=value,
            previous_value=previous_value,
            change_pct=change_pct,
        )

    def fetch_context(self, primary_observation=None) -> GoldMarketContext:
        if primary_observation is None:
            gold = self._fetch_signal(
                self.SYMBOLS["gold"]
            )
        else:
            timestamp = primary_observation.timestamp

            if timestamp.tzinfo is None:
                timestamp = timestamp.replace(
                    tzinfo=timezone.utc
                )

            gold = MarketSignal(
                instrument=primary_observation.instrument,
                source=primary_observation.source,
                timestamp=timestamp,
                value=float(primary_observation.price),
                previous_value=primary_observation.previous_price,
                change_pct=primary_observation.change_pct,
            )

        signals: list[MarketSignal] = []

        for name in ("dollar", "us10y", "usdinr"):
            try:
                signals.append(
                    self._fetch_signal(self.SYMBOLS[name])
                )
            except Exception:
                # Context signals are additive. Gold remains
                # the required primary observation.
                continue

        candidate_drivers: list[str] = []

        if gold.change_pct is not None:

            gold_up = gold.change_pct > 0
            gold_down = gold.change_pct < 0

            for signal in signals:

                if signal.change_pct is None:
                    continue

                symbol = signal.instrument
                signal_up = signal.change_pct > 0
                signal_down = signal.change_pct < 0

                # Dollar and yields commonly have an inverse
                # relationship with gold. This is only a
                # contemporaneous candidate relationship.
                if symbol in {"DX-Y.NYB", "^TNX"}:
                    if (gold_up and signal_down) or (
                        gold_down and signal_up
                    ):
                        candidate_drivers.append(
                            f"{symbol}: inverse-direction signal"
                        )

                # USD/INR is primarily an India transmission
                # signal, not a global gold causal signal.
                if symbol == "INR=X":
                    candidate_drivers.append(
                        "INR=X: India transmission signal"
                    )

        return GoldMarketContext(
            gold=gold,
            signals=tuple(signals),
            gold_change_pct=gold.change_pct,
            candidate_drivers=tuple(candidate_drivers),
        )

