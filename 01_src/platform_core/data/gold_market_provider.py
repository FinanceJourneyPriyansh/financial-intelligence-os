from __future__ import annotations
from datetime import datetime, timezone

from dataclasses import dataclass
from typing import Protocol

from platform_core.data.gold_quote_observation import (
    GoldQuoteObservation,
)
from platform_core.data.gold_provider_capability import (
    GoldDataCapability,
    GoldProviderMetadata,
)
from platform_core.data.gold_provider_selection_policy import (
    GoldProviderSelectionPolicy,
)
from platform_core.data.goldapi_provider import (
    GoldAPIProvider,
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
            capability=GoldDataCapability.DAILY,
            quote_timestamp=timestamp,
            retrieved_at=retrieved_at,
            data_age_seconds=age,
            is_realtime=observation.is_realtime,
            market_role="global_gold_reference",
            instrument=observation.instrument,
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


    def metadata(
        self,
        observation: GoldQuoteObservation,
    ) -> GoldProviderMetadata:
        retrieved_at = datetime.now(timezone.utc)

        return GoldProviderMetadata(
            provider=self.name,
            capability=GoldDataCapability.MOCK,
            quote_timestamp=observation.timestamp,
            retrieved_at=retrieved_at,
            data_age_seconds=0.0,
            is_realtime=False,
            market_role="development_fallback",
            instrument=observation.instrument,
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
        self.selection_policy = GoldProviderSelectionPolicy()

        self.goldapi = GoldAPIProvider()

        self.primary = primary or YahooGoldProvider()
        self.fallback = fallback or MockGoldProvider(
            price=0.0,
            previous_price=None,
        )

    def _available_providers(self) -> list[GoldMarketProvider]:
        """Return configured providers that can currently be attempted."""

        providers: list[GoldMarketProvider] = []

        if self.goldapi.available():
            providers.append(self.goldapi)

        providers.append(self.primary)
        providers.append(self.fallback)

        return providers

    def fetch_latest(self) -> ProviderResult:
        """Fetch Gold data using capability-ranked available providers.

        Each provider is fetched at most once. The successful observation and
        its metadata are retained together, ranked, and the winning result is
        returned without a second network request.
        """

        candidates = self._available_providers()

        successful: list[
            tuple[GoldMarketProvider, GoldQuoteObservation, GoldProviderMetadata]
        ] = []

        for provider in candidates:
            try:
                observation = provider.fetch_latest()
                metadata = provider.metadata(observation)

                successful.append(
                    (
                        provider,
                        observation,
                        metadata,
                    )
                )
            except Exception:
                continue

        if not successful:
            raise RuntimeError(
                "All configured Gold providers failed."
            )

        ranked_metadata = self.selection_policy.rank(
            [metadata for _, _, metadata in successful]
        )

        successful_by_provider = {
            provider.name: (
                provider,
                observation,
            )
            for provider, observation, _ in successful
        }

        for metadata in ranked_metadata:
            provider, observation = successful_by_provider[
                metadata.provider
            ]

            return ProviderResult(
                observation=observation,
                provider=provider.name,
                fallback_used=(
                    provider.name != self.primary.name
                ),
            )

        raise RuntimeError(
            "No ranked Gold provider result was available."
        )


        candidates = self._available_providers()

        metadata_candidates: list[tuple[GoldMarketProvider, GoldProviderMetadata]] = []

        for provider in candidates:
            try:
                observation = provider.fetch_latest()
                metadata = provider.metadata(observation)
                metadata_candidates.append((provider, metadata))
            except Exception:
                continue

        if not metadata_candidates:
            raise RuntimeError(
                "All configured Gold providers failed."
            )

        ranked_metadata = self.selection_policy.rank(
            [metadata for _, metadata in metadata_candidates]
        )

        provider_by_name = {
            provider.name: provider
            for provider, _ in metadata_candidates
        }

        for metadata in ranked_metadata:
            provider = provider_by_name[metadata.provider]

            try:
                observation = provider.fetch_latest()

                return ProviderResult(
                    observation=observation,
                    provider=provider.name,
                    fallback_used=(
                        provider.name != self.primary.name
                    ),
                )

            except Exception:
                continue

        raise RuntimeError(
            "All ranked Gold providers failed during final fetch."
        )
