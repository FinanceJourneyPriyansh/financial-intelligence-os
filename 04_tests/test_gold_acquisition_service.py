"""Tests for the FIOS Gold Acquisition Service."""

from datetime import datetime

from platform_core.data.gold_acquisition_service import (
    GoldAcquisitionService,
    GoldObservation,
)


def test_gold_acquisition_returns_valid_observation():
    observation = GoldAcquisitionService().fetch_latest()

    assert isinstance(observation, GoldObservation)
    assert observation.instrument == "GC=F"
    assert observation.source == "yahoo_finance"
    assert isinstance(observation.timestamp, datetime)
    assert observation.price > 0
    assert observation.volume >= 0
