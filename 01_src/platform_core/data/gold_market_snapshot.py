from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from platform_core.data.gold_provider_capability import (
    GoldDataCapability,
)


class MarketStatus(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    HOLIDAY = "HOLIDAY"


@dataclass(frozen=True)
class GoldMarketSnapshot:
    """Canonical FIOS Gold market snapshot."""

    market_status: MarketStatus

    open: float | None
    high: float | None
    low: float | None
    ltp: float | None
    previous_close: float | None

    change_abs: float | None
    change_pct: float | None

    quote_timestamp: datetime
    retrieved_at: datetime

    source: str
    instrument: str

    capability: GoldDataCapability
    is_realtime: bool
    market_role: str
    fallback_used: bool

    data_age_seconds: float
    official_close: bool

    # Gold purity rates: 999, 995, 916, 750, 585.
    purity_rates: dict[str, float] | None = None
