"""Tests for FIOS Gold Move Analysis."""

from datetime import datetime, timezone

from platform_core.data.gold_market_context_service import (
    GoldMarketContext,
    MarketSignal,
)
from platform_core.data.gold_news_evidence_service import (
    GoldNewsEvidence,
)
from platform_core.data.gold_move_analysis_service import (
    GoldMoveAnalysis,
    GoldMoveAnalysisService,
)


def make_context() -> GoldMarketContext:

    timestamp = datetime(
        2026,
        8,
        17,
        tzinfo=timezone.utc,
    )

    gold = MarketSignal(
        instrument="GC=F",
        source="yahoo_finance",
        timestamp=timestamp,
        value=4476.5,
        previous_value=4380.0,
        change_pct=2.19,
    )

    dollar = MarketSignal(
        instrument="DX-Y.NYB",
        source="yahoo_finance",
        timestamp=timestamp,
        value=99.5,
        previous_value=99.7,
        change_pct=-0.20,
    )

    return GoldMarketContext(
        gold=gold,
        signals=(dollar,),
        gold_change_pct=2.19,
        candidate_drivers=(
            "DX-Y.NYB: inverse-direction signal",
        ),
    )


def make_news() -> list[GoldNewsEvidence]:

    timestamp = datetime(
        2026,
        8,
        17,
        tzinfo=timezone.utc,
    )

    return [
        GoldNewsEvidence(
            title=(
                "Gold climbs on weaker dollar, "
                "easing Fed rate hike concerns"
            ),
            source="Reuters",
            published_at=timestamp,
            url="https://example.com/reuters-gold",
            query="gold market",
            retrieved_at=timestamp,
        ),
        GoldNewsEvidence(
            title=(
                "Gold rises as weaker dollar supports prices"
            ),
            source="KITCO",
            published_at=timestamp,
            url="https://example.com/kitco-gold",
            query="gold market",
            retrieved_at=timestamp,
        ),
    ]


def test_gold_move_analysis_returns_structured_result():

    analysis = GoldMoveAnalysisService().analyze(
        context=make_context(),
        news=make_news(),
    )

    assert isinstance(
        analysis,
        GoldMoveAnalysis,
    )

    assert analysis.gold_price == 4476.5
    assert analysis.gold_change_pct == 2.19
    assert analysis.generated_at.tzinfo is not None


def test_gold_move_analysis_identifies_supported_driver():

    analysis = GoldMoveAnalysisService().analyze(
        context=make_context(),
        news=make_news(),
    )

    assert len(analysis.assessments) > 0

    top = analysis.assessments[0]

    assert top.driver == "USD weakness"
    assert top.score > 0
    assert top.confidence in {
        "HIGH",
        "MEDIUM",
        "LOW",
    }


def test_gold_move_analysis_does_not_claim_causation():

    analysis = GoldMoveAnalysisService().analyze(
        context=make_context(),
        news=make_news(),
    )

    assert "not confirmed causation" in analysis.summary


def test_gold_move_analysis_handles_missing_evidence():

    analysis = GoldMoveAnalysisService().analyze(
        context=make_context(),
        news=[],
    )

    assert isinstance(
        analysis,
        GoldMoveAnalysis,
    )

    assert analysis.overall_confidence in {
        "HIGH",
        "MEDIUM",
        "LOW",
    }
