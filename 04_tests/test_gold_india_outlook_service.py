"""Tests for horizon-aware Gold India Outlook."""

from datetime import datetime, timezone

from gold_intelligence.services.gold_market_context_service import (
    GoldMarketContext,
    MarketSignal,
)
from gold_intelligence.services.gold_india_outlook_service import (
    GoldIndiaOutlook,
    GoldIndiaOutlookService,
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

    usdinr = MarketSignal(
        instrument="INR=X",
        source="yahoo_finance",
        timestamp=timestamp,
        value=95.59,
        previous_value=95.40,
        change_pct=0.20,
    )

    return GoldMarketContext(
        gold=gold,
        signals=(usdinr,),
        gold_change_pct=2.19,
        candidate_drivers=(
            "INR=X: India transmission signal",
        ),
    )


def test_outlook_returns_valid_result():

    outlook = GoldIndiaOutlookService().build_outlook(
        context=make_context()
    )

    assert isinstance(outlook, GoldIndiaOutlook)
    assert outlook.gold_price == 4476.5
    assert outlook.usdinr == 95.59
    assert outlook.current_gold_change_pct == 2.19


def test_all_horizons_exist():

    outlook = GoldIndiaOutlookService().build_outlook(
        context=make_context()
    )

    horizons = {
        item.horizon
        for item in outlook.scenarios
    }

    assert horizons == {
        "1D",
        "1W",
        "1M",
        "1Q",
        "1Y",
    }


def test_each_horizon_has_three_scenarios():

    outlook = GoldIndiaOutlookService().build_outlook(
        context=make_context()
    )

    for horizon in (
        "1D",
        "1W",
        "1M",
        "1Q",
        "1Y",
    ):

        scenarios = [
            item
            for item in outlook.scenarios
            if item.horizon == horizon
        ]

        assert {
            item.scenario
            for item in scenarios
        } == {
            "BASE",
            "UPSIDE",
            "DOWNSIDE",
        }


def test_india_transmission_is_detected():

    outlook = GoldIndiaOutlookService().build_outlook(
        context=make_context()
    )

    assert outlook.india_transmission == (
        "AMPLIFIED_UPSIDE"
    )


def test_short_term_confidence_is_not_reused_long_term():

    outlook = GoldIndiaOutlookService().build_outlook(
        context=make_context()
    )

    base = {
        item.horizon: item
        for item in outlook.scenarios
        if item.scenario == "BASE"
    }

    assert base["1D"].confidence == "HIGH"
    assert base["1W"].confidence == "MEDIUM"
    assert base["1M"].confidence == "MEDIUM"
    assert base["1Q"].confidence == "LOW"
    assert base["1Y"].confidence == "LOW"


def test_scenarios_have_assumptions_and_invalidation():

    outlook = GoldIndiaOutlookService().build_outlook(
        context=make_context()
    )

    for scenario in outlook.scenarios:

        assert scenario.drivers
        assert scenario.assumptions
        assert scenario.invalidation
        assert scenario.direction
        assert scenario.confidence


def test_missing_gold_change_reduces_confidence():

    context = make_context()

    context = GoldMarketContext(
        gold=context.gold,
        signals=context.signals,
        gold_change_pct=None,
        candidate_drivers=context.candidate_drivers,
    )

    outlook = GoldIndiaOutlookService().build_outlook(
        context=context
    )

    assert all(
        item.confidence == "LOW"
        for item in outlook.scenarios
        if item.scenario == "BASE"
    )

