from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from platform_core.data.gold_quote_observation import (
    GoldQuoteObservation,
)


class GoldMarketProvider(Protocol):
    """Provider contract returning the canonical Gold quote contract."""

    name: str

    def fetch_latest(self) -> GoldQuoteObservation:
        ...


@dataclass(frozen=True)
class ProviderResult:
    """Normalized provider execution result."""

    observation: GoldQuoteObservation
    provider: str
    fallback_used: bool


class YahooGoldProvider:
    """Yahoo Finance adapter normalized to GoldQuoteObservation."""

    name = "yahoo_finance"

    def __init__(self) -> None:
        from platform_core.data.gold_acquisition_service import (
            GoldAcquisitionService,
        )

        self._service = GoldAcquisitionService()

    def fetch_latest(self) -> GoldQuoteObservation:
        observation = self._service.fetch_latest()

        return GoldQuoteObservation(
            instrument=observation.instrument,
            source=self.name,
            timestamp=observation.timestamp,
            ltp=observation.price,
            previous_close=observation.previous_price,
            change_pct=observation.change_pct,
            change_abs=(
                observation.price - observation.previous_price
                if observation.previous_price not in (None, 0)
                else None
            ),
            volume=float(observation.volume),
            currency="USD",
            unit="troy_ounce",
            is_realtime=False,
        )


class MockGoldProvider:
    """Deterministic Gold provider for development continuity."""

    name = "mock_gold"

    def __init__(
        self,
        price: float = 0.0,
        previous_price: float | None = None,
    ) -> None:
        self.price = price
        self.previous_price = previous_price

    def fetch_latest(self) -> GoldQuoteObservation:
        if self.price <= 0:
            raise RuntimeError(
                "MockGoldProvider requires a positive price."
            )

        change_abs = None
        change_pct = None

        if self.previous_price not in (None, 0):
            change_abs = self.price - self.previous_price
            change_pct = (
                change_abs
                / self.previous_price
                * 100.0
            )

        from datetime import datetime, timezone

        return GoldQuoteObservation(
            instrument="GC=F",
            source=self.name,
            timestamp=datetime.now(timezone.utc),
            ltp=self.price,
            previous_close=self.previous_price,
            change_abs=change_abs,
            change_pct=change_pct,
            volume=0.0,
            currency="USD",
            unit="troy_ounce",
            is_realtime=False,
        )


class GoldMarketProviderManager:
    """
    Central Gold provider failover.

    Primary provider is attempted first. If it fails, the configured
    fallback provider is used. All providers return the same contract.
    """

    def __init__(
        self,
        primary: GoldMarketProvider | None = None,
        fallback: GoldMarketProvider | None = None,
    ) -> None:
        self.primary = primary or YahooGoldProvider()
        self.fallback = fallback

    def fetch_latest(self) -> ProviderResult:
        try:
            observation = self.primary.fetch_latest()

            return ProviderResult(
                observation=observation,
                provider=self.primary.name,
                fallback_used=False,
            )

        except Exception as primary_error:
            if self.fallback is None:
                raise RuntimeError(
                    f"Primary Gold provider "
                    f"{self.primary.name!r} failed and no fallback "
                    "provider is configured."
                ) from primary_error

            observation = self.fallback.fetch_latest()

            return ProviderResult(
                observation=observation,
                provider=self.fallback.name,
                fallback_used=True,
            )
