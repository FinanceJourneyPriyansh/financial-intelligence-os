"""
FIOS Gold India Outlook Service

Day 5 Phase 2:
Translate global gold and USD/INR conditions into an
India-focused scenario outlook across multiple horizons.

This is scenario analysis, not a guaranteed price forecast.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from platform_core.data.gold_market_context_service import (
    GoldMarketContext,
    GoldMarketContextService,
)


@dataclass(frozen=True)
class OutlookScenario:
    horizon: str
    scenario: str
    direction: str
    confidence: str
    drivers: tuple[str, ...]
    assumptions: tuple[str, ...]
    invalidation: tuple[str, ...]


@dataclass(frozen=True)
class GoldIndiaOutlook:
    generated_at: datetime
    gold_price: float
    usdinr: float | None
    current_gold_change_pct: float | None
    india_transmission: str
    scenarios: tuple[OutlookScenario, ...]
    summary: str


class GoldIndiaOutlookService:
    """
    Generate structured India-focused Gold scenarios.

    Horizons:
        1D, 1W, 1M, 1Q, 1Y
    """

    HORIZONS = (
        ("1D", "immediate"),
        ("1W", "short_term"),
        ("1M", "medium_term"),
        ("1Q", "quarter"),
        ("1Y", "structural"),
    )

    def __init__(
        self,
        context_service: GoldMarketContextService | None = None,
    ):
        self.context_service = (
            context_service
            or GoldMarketContextService()
        )

    @staticmethod
    def _confidence(
        gold_change: float | None,
        usdinr_change: float | None,
    ) -> str:

        if gold_change is None:
            return "LOW"

        magnitude = abs(gold_change)

        if magnitude >= 2.0:
            if usdinr_change is not None:
                return "HIGH"

            return "MEDIUM"

        if magnitude >= 1.0:
            return "MEDIUM"

        return "LOW"

    @staticmethod
    def _india_transmission(
        gold_change: float | None,
        usdinr_change: float | None,
    ) -> str:

        if gold_change is None:
            return "INSUFFICIENT_DATA"

        if usdinr_change is None:
            return "GOLD_SIGNAL_ONLY"

        if gold_change > 0 and usdinr_change > 0:
            return "AMPLIFIED_UPSIDE"

        if gold_change > 0 and usdinr_change < 0:
            return "GLOBAL_UPSIDE_PARTLY_OFFSET"

        if gold_change < 0 and usdinr_change > 0:
            return "INDIA_DECLINE_PARTLY_OFFSET"

        return "ALIGNED_DOWNSIDE"

    def _signal_map(
        self,
        context: GoldMarketContext,
    ) -> dict[str, float]:

        result: dict[str, float] = {}

        for signal in context.signals:

            if signal.change_pct is not None:
                result[signal.instrument] = (
                    signal.change_pct
                )

        return result

    def build_outlook(
        self,
        context: GoldMarketContext | None = None,
    ) -> GoldIndiaOutlook:

        context = (
            context
            if context is not None
            else self.context_service.fetch_context()
        )

        signal_map = self._signal_map(context)

        gold_change = context.gold_change_pct
        usdinr_change = signal_map.get("INR=X")

        transmission = self._india_transmission(
            gold_change,
            usdinr_change,
        )

        confidence = self._confidence(
            gold_change,
            usdinr_change,
        )

        scenarios: list[OutlookScenario] = []

        for horizon, horizon_type in self.HORIZONS:

            if horizon_type == "immediate":
                base_drivers = (
                    "Current global gold momentum",
                    "Current USD/INR transmission",
                )

                assumptions = (
                    "Current market regime persists",
                    "No major unexpected policy shock",
                )

                invalidation = (
                    "Gold reverses the current direction",
                    "USD/INR reverses materially",
                )

            elif horizon_type == "short_term":
                base_drivers = (
                    "Global gold momentum",
                    "US dollar direction",
                    "US rate expectations",
                    "USD/INR transmission",
                )

                assumptions = (
                    "Macro regime remains broadly stable",
                    "No extreme liquidity shock",
                )

                invalidation = (
                    "Major reversal in USD or yields",
                    "Unexpected central-bank policy shift",
                )

            elif horizon_type == "medium_term":
                base_drivers = (
                    "Interest-rate expectations",
                    "Dollar trend",
                    "Central-bank demand",
                    "Indian currency transmission",
                )

                assumptions = (
                    "Global monetary expectations remain the "
                    "dominant macro driver",
                    "Central-bank demand remains supportive",
                )

                invalidation = (
                    "Sustained dollar strengthening",
                    "Material change in central-bank demand",
                )

            elif horizon_type == "quarter":
                base_drivers = (
                    "Global monetary policy",
                    "Central-bank purchases",
                    "Investment demand",
                    "Indian physical demand",
                    "USD/INR",
                )

                assumptions = (
                    "No prolonged global liquidity shock",
                    "Indian physical market remains functional",
                    "Central-bank demand does not collapse",
                )

                invalidation = (
                    "Major monetary-policy regime change",
                    "Sharp sustained dollar appreciation",
                    "Material demand deterioration",
                )

            else:
                base_drivers = (
                    "Global monetary regime",
                    "Central-bank gold demand",
                    "Investment allocation",
                    "Indian structural demand",
                    "Currency regime",
                )

                assumptions = (
                    "Gold retains its strategic reserve/investment role",
                    "Central-bank demand remains structurally relevant",
                    "India remains a major physical gold market",
                )

                invalidation = (
                    "Structural change in gold reserve demand",
                    "Long-lasting collapse in investment demand",
                    "Major currency or policy regime shift",
                )

            if gold_change is None:
                base_direction = "NEUTRAL"
            elif gold_change > 0:
                base_direction = "BULLISH_BIAS"
            elif gold_change < 0:
                base_direction = "BEARISH_BIAS"
            else:
                base_direction = "NEUTRAL"

            scenarios.extend(
                [
                    OutlookScenario(
                        horizon=horizon,
                        scenario="BASE",
                        direction=base_direction,
                        confidence=confidence,
                        drivers=base_drivers,
                        assumptions=assumptions,
                        invalidation=invalidation,
                    ),
                    OutlookScenario(
                        horizon=horizon,
                        scenario="UPSIDE",
                        direction="BULLISH",
                        confidence="MEDIUM",
                        drivers=(
                            *base_drivers,
                            "Renewed safe-haven or investment demand",
                        ),
                        assumptions=(
                            *assumptions,
                            "Gold momentum strengthens",
                            "Dollar/rates become more supportive",
                        ),
                        invalidation=(
                            *invalidation,
                            "Gold loses momentum",
                        ),
                    ),
                    OutlookScenario(
                        horizon=horizon,
                        scenario="DOWNSIDE",
                        direction="BEARISH",
                        confidence="MEDIUM",
                        drivers=(
                            *base_drivers,
                            "Stronger dollar or higher real-rate pressure",
                        ),
                        assumptions=(
                            *assumptions,
                            "Dollar strengthens",
                            "Rate expectations become less supportive",
                        ),
                        invalidation=(
                            *invalidation,
                            "Gold momentum accelerates upward",
                        ),
                    ),
                ]
            )

        summary = (
            f"India transmission is {transmission}. "
            f"Current gold momentum is "
            f"{gold_change:+.2f}% "
            if gold_change is not None
            else "Current gold momentum is unavailable. "
        )

        summary += (
            "The outlook uses scenario conditions rather than "
            "claiming an exact future price."
        )

        return GoldIndiaOutlook(
            generated_at=datetime.now(timezone.utc),
            gold_price=context.gold.value,
            usdinr=(
                next(
                    (
                        signal.value
                        for signal in context.signals
                        if signal.instrument == "INR=X"
                    ),
                    None,
                )
            ),
            current_gold_change_pct=gold_change,
            india_transmission=transmission,
            scenarios=tuple(scenarios),
            summary=summary,
        )
