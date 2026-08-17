"""
FIOS Gold Move Analysis Service

Evidence-aware gold movement analysis.

Important:
Mention != evidence.
Correlation != causation.
A driver receives evidence only when the article language
contains a driver-specific signal.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from platform_core.data.gold_market_context_service import (
    GoldMarketContext,
    GoldMarketContextService,
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
            "fed rate",
            "fed rates",
            "fed policy",
            "rate hike",
            "rate hikes",
            "rate cut",
            "rate cuts",
            "rate expectations",
            "interest-rate expectations",
            "interest rate expectations",
        ),

        "Inflation": (
            "inflation",
            "consumer prices",
            "cpi",
            "price pressure",
            "inflation expectations",
        ),

        "Geopolitical risk": (
            "geopolitical risk",
            "geopolitical tensions",
            "geopolitical uncertainty",
            "safe-haven demand",
            "safe haven demand",
            "war risk",
            "conflict risk",
        ),

        "Central-bank demand": (
            "central bank buying",
            "central banks buying",
            "official sector buying",
            "sovereign buying",
            "central-bank demand",
            "central bank demand",
        ),

        "India demand": (
            "indian gold demand",
            "india gold demand",
            "indian jewellery demand",
            "indian jewelry demand",
            "india jewellery demand",
            "india jewelry demand",
            "indian consumer demand",
            "india consumer demand",
            "indian physical demand",
            "india physical demand",
            "indian bullion demand",
            "india bullion demand",
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

            if not self._contains_any(
                item.title,
                keywords,
            ):
                continue

            source_weight = self.NEWS_SOURCE_WEIGHTS.get(
                item.source,
                0.50,
            )

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

            normalized_news = min(
                news_score / 1.5,
                1.0,
            )

            combined_score = min(
                (normalized_news * 0.60)
                + (market_score * 0.40),
                1.0,
            )

            # No evidence means no driver assessment.
            if combined_score <= 0:
                continue

            confidence = self._confidence(
                combined_score
            )

            supporting = []

            if evidence_count:
                supporting.append(
                    f"{evidence_count} driver-specific "
                    "news item(s)"
                )

            supporting.extend(
                market_signals
            )

            assessments.append(
                DriverAssessment(
                    driver=driver,
                    score=round(combined_score, 3),
                    confidence=confidence,
                    evidence_count=evidence_count,
                    supporting_signals=tuple(
                        supporting
                    ),
                    explanation=(
                        f"{driver} has "
                        f"{confidence.lower()} evidence "
                        "based on driver-specific news "
                        "and observed market context."
                    ),
                )
            )

        assessments.sort(
            key=lambda item: item.score,
            reverse=True,
        )

        if assessments:

            top = assessments[0]

            overall_confidence = top.confidence

            change_text = (
                f"{context.gold_change_pct:+.2f}%"
                if context.gold_change_pct is not None
                else "an unquantified move"
            )

            summary = (
                f"Gold is {change_text} with the "
                f"strongest observed evidence pointing "
                f"toward {top.driver}. "
                "This is an evidence-based assessment, "
                "not confirmed causation."
            )

        else:

            overall_confidence = "LOW"

            summary = (
                "Gold movement detected, but available "
                "driver-specific evidence is insufficient "
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
