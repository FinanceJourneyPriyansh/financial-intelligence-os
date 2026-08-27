from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


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

    data_age_seconds: float
    official_close: bool
