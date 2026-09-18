"""Tests for FIOS Gold News Evidence."""

from datetime import datetime

from gold_intelligence.services.gold_news_evidence_service import (
    GoldNewsEvidence,
    GoldNewsEvidenceService,
)


def test_gold_news_evidence_fetches_recent_articles():
    service = GoldNewsEvidenceService()

    results = service.fetch_recent(
        queries=("gold market",)
    )

    assert len(results) > 0

    first = results[0]

    assert isinstance(first, GoldNewsEvidence)
    assert first.title
    assert first.source
    assert first.url.startswith("http")
    assert isinstance(first.published_at, datetime)
    assert isinstance(first.retrieved_at, datetime)
    assert first.query == "gold market"


def test_gold_news_evidence_deduplicates_urls():
    service = GoldNewsEvidenceService()

    results = service.fetch_recent(
        queries=("gold market", "gold market")
    )

    urls = [item.url for item in results]

    assert len(urls) == len(set(urls))


def test_gold_news_evidence_preserves_source():
    service = GoldNewsEvidenceService()

    results = service.fetch_recent(
        queries=("gold India",)
    )

    assert len(results) > 0

    assert all(
        item.source
        for item in results
    )

