"""Evidence-quality tests for Gold Move Analysis."""

from datetime import datetime, timezone

from platform_core.data.gold_market_context_service import (
    GoldMarketContext,
    MarketSignal,
)
from platform_core.data.gold_news_evidence_service import (
    GoldNewsEvidence,
)
from platform_core.data.gold_move_analysis_service import (
    GoldMoveAnalysisService,
)


def make_context():

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


def test_generic_india_mention_is_not_india_demand():

    timestamp = datetime(
        2026,
        8,
        17,
        tzinfo=timezone.utc,
    )

    news = [
        GoldNewsEvidence(
            title="Gold price in India today",
            source="FXStreet",
            published_at=timestamp,
            url="https://example.com/india",
            query="gold India",
            retrieved_at=timestamp,
        )
    ]

    analysis = GoldMoveAnalysisService().analyze(
        context=make_context(),
        news=news,
    )

    india = [
        item
        for item in analysis.assessments
        if item.driver == "India demand"
    ]

    assert india == []


def test_india_demand_requires_driver_specific_language():

    timestamp = datetime(
        2026,
        8,
        17,
        tzinfo=timezone.utc,
    )

    news = [
        GoldNewsEvidence(
            title=(
                "Indian jewellery demand rises "
                "as gold prices stabilize"
            ),
            source="World Gold Council",
            published_at=timestamp,
            url="https://example.com/demand",
            query="gold India",
            retrieved_at=timestamp,
        )
    ]

    analysis = GoldMoveAnalysisService().analyze(
        context=make_context(),
        news=news,
    )

    india = [
        item
        for item in analysis.assessments
        if item.driver == "India demand"
    ]

    assert len(india) == 1
    assert india[0].evidence_count == 1


def test_usd_weakness_requires_specific_language():

    timestamp = datetime(
        2026,
        8,
        17,
        tzinfo=timezone.utc,
    )

    news = [
        GoldNewsEvidence(
            title="Gold market update",
            source="Reuters",
            published_at=timestamp,
            url="https://example.com/gold",
            query="gold market",
            retrieved_at=timestamp,
        )
    ]

    analysis = GoldMoveAnalysisService().analyze(
        context=make_context(),
        news=news,
    )

    usd = [
        item
        for item in analysis.assessments
        if item.driver == "USD weakness"
    ]

    assert len(usd) == 1
    assert usd[0].evidence_count == 0
    assert usd[0].score > 0
