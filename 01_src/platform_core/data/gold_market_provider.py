from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Protocol

from platform_core.data.market_observation import MarketObservation


class GoldMarketProvider(Protocol):
    """Contract for a Gold market data provider."""

    name: str

    def fetch_latest(self) -> MarketObservation:
        ...


@dataclass(frozen=True)
class ProviderResult:
    """Normalized provider execution result."""

    observation: MarketObservation
    provider: str
    fallback_used: bool


class YahooGoldProvider:
    """Yahoo Finance Gold provider using the existing acquisition logic."""

    name = "yahoo_finance"

    def __init__(self) -> None:
        from platform_core.data.gold_acquisition_service import (
            GoldAcquisitionService,
        )

        self._service = GoldAcquisitionService()

    def fetch_latest(self) -> MarketObservation:
        return self._service.fetch_latest()


class MockGoldProvider:
    """
    Deterministic fallback provider.

    This exists for development/test continuity when external market
    providers are unavailable. It is explicitly marked as mock data.
    """

    name = "mock_gold"

    def __init__(
        self,
        price: float = 0.0,
        previous_price: float | None = None,
    ) -> None:
        self.price = price
        self.previous_price = previous_price

    def fetch_latest(self) -> MarketObservation:
        if self.price <= 0:
            raise RuntimeError(
                "MockGoldProvider requires a positive price."
            )

        change_pct = None

        if self.previous_price not in (None, 0):
            change_pct = (
                (self.price - self.previous_price)
                / self.previous_price
                * 100.0
            )

        return MarketObservation(
            instrument="GC=F",
            source=self.name,
            timestamp=datetime.now(timezone.utc),
            price=self.price,
            previous_price=self.previous_price,
            change_pct=change_pct,
            volume=0,
        )


class GoldMarketProviderManager:
    """
    Execute the configured primary Gold provider with an optional fallback.

    Provider selection is centralized here so the rest of FIOS does not
    need to know which external source supplied the observation.
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
