from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class GoldQuoteObservation:
    """Normalized Gold market quote independent of provider."""

    instrument: str
    source: str
    timestamp: datetime

    ltp: float

    open: float | None = None
    high: float | None = None
    low: float | None = None
    previous_close: float | None = None

    bid: float | None = None
    ask: float | None = None

    change_abs: float | None = None
    change_pct: float | None = None

    volume: float | None = None

    currency: str = "USD"
    unit: str = "troy_ounce"

    is_realtime: bool = False

    # India Gold purity rates.
    # Values use the same currency/unit as the observation.
    purity_rates: dict[str, float] | None = None
