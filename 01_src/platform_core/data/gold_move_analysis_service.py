"""
FIOS Gold Move Analysis Service

Day 4 Phase 2:
Combine market context and news evidence into a structured,
evidence-aware explanation of a gold movement.

Important:
This engine reports supported signals and evidence.
It does NOT claim confirmed causation from correlation alone.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import re

from platform_core.data.gold_market_context_service import (
    GoldMarketContext,
    GoldMarketContextService,
    MarketSignal,
)
from platform_core.data.gold_news_evidence_service import (
    GoldNewsEvidence,
    GoldNewsEvidenceService,
)


@dataclass(frozen=True)
class DriverAssessment:
    driver: str
    score: float
    confidence: str
    evidence_count: int
    supporting_signals: tuple[str, ...]
    explanation: str


@dataclass(frozen=True)
class GoldMoveAnalysis:
    generated_at: datetime
    gold_price: float
    gold_change_pct: float | None
    assessments: tuple[DriverAssessment, ...]
    overall_confidence: str
    summary: str


class GoldMoveAnalysisService:
    """
    Analyze Gold market movement using observed market signals
    and recent news evidence.
    """

    NEWS_SOURCE_WEIGHTS = {
        "Reuters": 1.00,
        "World Gold Council": 0.95,
        "CNBC": 0.90,
        "KITCO": 0.85,
        "FXStreet": 0.80,
        "The Times of India": 0.80,
    }

    DRIVER_KEYWORDS = {
        "USD weakness": (
            "weaker dollar",
            "weak dollar",
            "dollar weakness",
            "dollar fell",
            "dollar declines",
            "dollar dropped",
        ),
        "Fed expectations": (
            "fed",
            "rate hike",
            "rate cuts",
            "interest rate",
            "rate expectations",
            "fed-hike",
            "fed rate",
        ),
        "Inflation": (
            "inflation",
            "consumer prices",
            "cpi",
            "price pressure",
        ),
        "Geopolitical risk": (
            "war",
            "geopolitical",
            "conflict",
            "iran",
            "tension",
            "safe-haven",
        ),
        "Central-bank demand": (
            "central bank",
            "official sector buying",
            "sovereign buying",
            "central-bank",
        ),
        "India demand": (
            "india",
            "indian",
            "jeweller",
            "jewelry",
            "jewellery",
            "import",
            "physical demand",
        ),
    }

    def __init__(
        self,
        context_service: GoldMarketContextService | None = None,
        news_service: GoldNewsEvidenceService | None = None,
    ):
        self.context_service = (
            context_service or GoldMarketContextService()
        )
        self.news_service = (
            news_service or GoldNewsEvidenceService()
        )

    @staticmethod
    def _contains_any(
        text: str,
        keywords: tuple[str, ...],
    ) -> bool:
        normalized = text.lower()

        return any(
            keyword.lower() in normalized
            for keyword in keywords
        )

    @staticmethod
    def _confidence(score: float) -> str:
        if score >= 0.75:
            return "HIGH"

        if score >= 0.45:
            return "MEDIUM"

        return "LOW"

    def _news_evidence(
        self,
        driver: str,
        news: list[GoldNewsEvidence],
    ) -> tuple[float, int]:

        keywords = self.DRIVER_KEYWORDS[driver]

        score = 0.0
        count = 0

        for item in news:

            text = item.title

            if not self._contains_any(
                text,
                keywords,
            ):
                continue

            source_weight = self.NEWS_SOURCE_WEIGHTS.get(
                item.source,
                0.50,
            )

            # Each independent article contributes evidence,
            # with diminishing weight after the first few.
            contribution = source_weight

            if count >= 1:
                contribution *= 0.60

            if count >= 2:
                contribution *= 0.50

            score += contribution
            count += 1

        return score, count

    def _market_evidence(
        self,
        driver: str,
        context: GoldMarketContext,
    ) -> tuple[float, list[str]]:

        gold_change = context.gold_change_pct

        if gold_change is None:
            return 0.0, []

        gold_up = gold_change > 0
        gold_down = gold_change < 0

        score = 0.0
        signals: list[str] = []

        for signal in context.signals:

            if signal.change_pct is None:
                continue

            change = signal.change_pct

            if driver == "USD weakness":
                if signal.instrument == "DX-Y.NYB":
                    if (gold_up and change < 0) or (
                        gold_down and change > 0
                    ):
                        score += 0.45
                        signals.append(
                            "USD moved opposite to gold"
                        )

            elif driver == "Fed expectations":
                if signal.instrument == "^TNX":
                    if (gold_up and change < 0) or (
                        gold_down and change > 0
                    ):
                        score += 0.30
                        signals.append(
                            "US 10Y yield moved opposite to gold"
                        )

            elif driver == "India demand":
                if signal.instrument == "INR=X":
                    score += 0.20
                    signals.append(
                        "USD/INR provides India transmission context"
                    )

        return min(score, 1.0), signals

    def analyze(
        self,
        context: GoldMarketContext | None = None,
        news: list[GoldNewsEvidence] | None = None,
    ) -> GoldMoveAnalysis:

        context = (
            context
            if context is not None
            else self.context_service.fetch_context()
        )

        news = (
            news
            if news is not None
            else self.news_service.fetch_recent(
                queries=("gold market", "gold India")
            )
        )

        assessments: list[DriverAssessment] = []

        for driver in self.DRIVER_KEYWORDS:

            news_score, evidence_count = (
                self._news_evidence(
                    driver,
                    news,
                )
            )

            market_score, market_signals = (
                self._market_evidence(
                    driver,
                    context,
                )
            )

            # Normalize news contribution.
            normalized_news = min(
                news_score / 1.5,
                1.0,
            )

            combined_score = min(
                (normalized_news * 0.60)
                + (market_score * 0.40),
                1.0,
            )

            if combined_score <= 0:
                continue

            confidence = self._confidence(
                combined_score
            )

            evidence_text = []

            if evidence_count:
                evidence_text.append(
                    f"{evidence_count} relevant news item(s)"
                )

            evidence_text.extend(
                market_signals
            )

            explanation = (
                f"{driver} has {confidence.lower()} "
                f"evidence based on "
                f"market context and available news."
            )

            assessments.append(
                DriverAssessment(
                    driver=driver,
                    score=round(combined_score, 3),
                    confidence=confidence,
                    evidence_count=evidence_count,
                    supporting_signals=tuple(
                        evidence_text
                    ),
                    explanation=explanation,
                )
            )

        assessments.sort(
            key=lambda item: item.score,
            reverse=True,
        )

        if assessments:
            top = assessments[0]

            overall_confidence = top.confidence

            summary = (
                f"Gold is {context.gold_change_pct:+.2f}% "
                f"with the strongest observed evidence "
                f"pointing toward {top.driver}. "
                f"This is an evidence-based assessment, "
                f"not confirmed causation."
            )

        else:
            overall_confidence = "LOW"

            summary = (
                "Gold movement detected, but available "
                "market and news evidence is insufficient "
                "to identify a strong driver."
            )

        return GoldMoveAnalysis(
            generated_at=datetime.now(timezone.utc),
            gold_price=context.gold.value,
            gold_change_pct=context.gold_change_pct,
            assessments=tuple(assessments),
            overall_confidence=overall_confidence,
            summary=summary,
        )
