"""Tests for FIOS Gold Market Context."""

from gold_intelligence.services.gold_market_context_service import (
    GoldMarketContext,
    GoldMarketContextService,
)


def test_gold_market_context_is_observed():
    context = GoldMarketContextService().fetch_context()

    assert isinstance(context, GoldMarketContext)

    assert context.gold.instrument == "GC=F"
    assert context.gold.source == "yahoo_finance"
    assert context.gold.value > 0

    # Day 2 requires at least one contextual market signal.
    assert len(context.signals) >= 1

    for signal in context.signals:
        assert signal.instrument
        assert signal.source == "yahoo_finance"
        assert signal.value > 0


def test_gold_context_has_valid_movement_measurement():
    context = GoldMarketContextService().fetch_context()

    if context.gold.previous_value is not None:
        assert context.gold.previous_value > 0
        assert context.gold.change_pct is not None


def test_candidate_drivers_are_explicitly_labeled():
    context = GoldMarketContextService().fetch_context()

    for driver in context.candidate_drivers:
        assert isinstance(driver, str)
        assert len(driver) > 0

