from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class DiamondReferenceObservation:
    asset: str
    source: str
    timestamp: datetime
    index_value: float
    change_pct: float | None
    update_frequency: str
