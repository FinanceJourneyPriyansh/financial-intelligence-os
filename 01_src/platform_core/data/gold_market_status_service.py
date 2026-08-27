from __future__ import annotations

from datetime import date, datetime, time
from enum import Enum
from zoneinfo import ZoneInfo

from platform_core.data.gold_market_snapshot import MarketStatus


class GoldMarketStatusService:
    """Determine the current FIOS Gold market session state."""

    TIMEZONE = ZoneInfo("Asia/Kolkata")

    # MCX Gold regular weekday session.
    SESSION_OPEN = time(9, 0)
    SESSION_CLOSE = time(23, 30)

    # Explicitly maintained holidays. Keep this small and auditable;
    # future holiday-calendar integration can replace this set.
    HOLIDAYS: frozenset[date] = frozenset()

    def now_ist(self) -> datetime:
        """Return the current timezone-aware IST datetime."""
        return datetime.now(self.TIMEZONE)

    def status_at(self, moment: datetime | None = None) -> MarketStatus:
        """Return OPEN, CLOSED, or HOLIDAY for a supplied/current IST time."""

        if moment is None:
            current = self.now_ist()
        else:
            if moment.tzinfo is None:
                current = moment.replace(tzinfo=self.TIMEZONE)
            else:
                current = moment.astimezone(self.TIMEZONE)

        if current.date() in self.HOLIDAYS:
            return MarketStatus.HOLIDAY

        # Monday=0 ... Sunday=6.
        if current.weekday() >= 5:
            return MarketStatus.CLOSED

        current_time = current.time()

        if self.SESSION_OPEN <= current_time < self.SESSION_CLOSE:
            return MarketStatus.OPEN

        return MarketStatus.CLOSED
