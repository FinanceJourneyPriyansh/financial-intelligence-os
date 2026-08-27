from __future__ import annotations

from datetime import datetime, timezone

from platform_core.data.gold_market_provider import (
    GoldMarketProviderManager,
)
from platform_core.data.gold_market_snapshot import (
    GoldMarketSnapshot,
    MarketStatus,
)
from platform_core.data.gold_market_status_service import (
    GoldMarketStatusService,
)


class GoldMarketSnapshotService:
    """
    Build the canonical Gold market snapshot.

    This service combines provider data with the current market-session
    state. It does not own provider selection or trading-calendar logic.
    """

    def __init__(
        self,
        provider_manager: GoldMarketProviderManager | None = None,
        status_service: GoldMarketStatusService | None = None,
    ) -> None:
        self.provider_manager = (
            provider_manager or GoldMarketProviderManager()
        )
        self.status_service = (
            status_service or GoldMarketStatusService()
        )

    def create_snapshot(
        self,
        now: datetime | None = None,
    ) -> GoldMarketSnapshot:
        """
        Create one canonical Gold market snapshot.

        Provider timestamps are preserved. Data age is calculated from
        the retrieval clock so downstream consumers can judge freshness.
        """

        retrieved_at = (
            now.astimezone(timezone.utc)
            if now is not None and now.tzinfo is not None
            else (
                now.replace(tzinfo=timezone.utc)
                if now is not None
                else datetime.now(timezone.utc)
            )
        )

        status = self.status_service.status_at(retrieved_at)

        result = self.provider_manager.fetch_latest()
        observation = result.observation

        quote_timestamp = observation.timestamp

        if quote_timestamp.tzinfo is None:
            quote_timestamp = quote_timestamp.replace(
                tzinfo=timezone.utc
            )
        else:
            quote_timestamp = quote_timestamp.astimezone(
                timezone.utc
            )

        data_age_seconds = max(
            0.0,
            (retrieved_at - quote_timestamp).total_seconds(),
        )

        previous_close = observation.previous_close
        ltp = observation.ltp

        change_abs = None
        change_pct = observation.change_pct

        if ltp is not None and previous_close not in (None, 0):
            change_abs = ltp - previous_close

        # The current Yahoo acquisition contract is daily OHLC data.
        # Until an intraday institutional provider is connected, the
        # observed close is the safest canonical LTP representation.
        open_price = None
        high_price = None
        low_price = None

        if status in (
            MarketStatus.CLOSED,
            MarketStatus.HOLIDAY,
        ):
            official_close = True
        else:
            official_close = False

        return GoldMarketSnapshot(
            market_status=status,
            open=open_price,
            high=high_price,
            low=low_price,
            ltp=ltp,
            previous_close=previous_close,
            change_abs=change_abs,
            change_pct=change_pct,
            quote_timestamp=quote_timestamp,
            retrieved_at=retrieved_at,
            source=result.provider,
            instrument=observation.instrument,
            data_age_seconds=data_age_seconds,
            official_close=official_close,
        )
