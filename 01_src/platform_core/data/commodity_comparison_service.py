from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from platform_core.data.diamond_reference_observation import (
    DiamondReferenceObservation,
)
from platform_core.data.market_observation import MarketObservation


@dataclass(frozen=True)
class CommodityComparison:
    """Normalized comparison view for Gold, Silver and Diamonds."""

    asset: str
    value: float
    value_type: str
    change_pct: float | None
    timestamp: datetime
    source: str
    direction: str


class CommodityComparisonService:
    """
    Compare the three FIOS B3 assets.

    Gold and Silver are market observations.
    Diamonds are represented by the IDEX Diamond Index reference.
    """

    ASSETS = ("gold", "silver", "diamond")

    @staticmethod
    def _direction(change_pct: float | None) -> str:
        if change_pct is None:
            return "UNKNOWN"

        if change_pct > 0:
            return "UP"

        if change_pct < 0:
            return "DOWN"

        return "FLAT"

    def compare(
        self,
        gold: MarketObservation,
        silver: MarketObservation,
        diamond: DiamondReferenceObservation,
    ) -> tuple[CommodityComparison, ...]:

        return (
            CommodityComparison(
                asset="gold",
                value=gold.price,
                value_type="market_price",
                change_pct=gold.change_pct,
                timestamp=gold.timestamp,
                source=gold.source,
                direction=self._direction(
                    gold.change_pct
                ),
            ),
            CommodityComparison(
                asset="silver",
                value=silver.price,
                value_type="market_price",
                change_pct=silver.change_pct,
                timestamp=silver.timestamp,
                source=silver.source,
                direction=self._direction(
                    silver.change_pct
                ),
            ),
            CommodityComparison(
                asset="diamond",
                value=diamond.index_value,
                value_type="reference_index",
                change_pct=diamond.change_pct,
                timestamp=diamond.timestamp,
                source=diamond.source,
                direction=self._direction(
                    diamond.change_pct
                ),
            ),
        )
