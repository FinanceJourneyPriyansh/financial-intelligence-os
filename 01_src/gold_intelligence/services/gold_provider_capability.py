from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class GoldDataCapability(str, Enum):
    """Capability classification for Gold data providers."""

    REALTIME = "REALTIME"
    DELAYED = "DELAYED"
    DAILY = "DAILY"
    REFERENCE = "REFERENCE"
    MOCK = "MOCK"


@dataclass(frozen=True)
class GoldProviderMetadata:
    """Metadata describing the quality and role of a Gold quote."""

    provider: str
    capability: GoldDataCapability

    quote_timestamp: datetime
    retrieved_at: datetime

    data_age_seconds: float

    is_realtime: bool

    market_role: str
    instrument: str
