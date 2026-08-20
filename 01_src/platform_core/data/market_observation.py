from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class MarketObservation:
    instrument: str
    source: str
    timestamp: datetime
    price: float
    volume: int
    previous_price: float | None = None
    change_pct: float | None = None
