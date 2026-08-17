from datetime import datetime, timezone

from platform_core.data.gold_acquisition_service import (
    GoldObservation,
)
from platform_core.data.gold_market_context_service import (
    GoldMarketContext,
)
from platform_core.data.market_intelligence_pipeline_service import (
    MarketIntelligencePipeline,
    MarketIntelligenceResult,
)


class FakeAcquisition:

    def __init__(self):
        self.calls = 0

    def fetch_latest(self):

        self.calls += 1

        return GoldObservation(
            instrument="GC=F",
            source="test",
            timestamp=datetime.now(timezone.utc),
            price=4474.0,
            volume=100,
        )


class FakeContext:

    def __init__(self):
        self.primary_gold = None

    def fetch_context(self, primary_gold=None):

        self.primary_gold = primary_gold

        return GoldMarketContext(
            gold=primary_gold,
            signals=(),
            gold_change_pct=None,
            candidate_drivers=(),
        )


class FakeEvidence:

    def __init__(self):
        self.calls = 0

    def fetch_recent(self, queries=None):

        self.calls += 1
        return []


class FakeAnalysis:

    def __init__(self):
        self.context = None
        self.news = None

    def analyze(self, context=None, news=None):

        self.context = context
        self.news = news

        return {"analysis": "ok"}


class FakeOutlook:

    def __init__(self):
        self.context = None

    def build_outlook(self, context=None):

        self.context = context

        return {"outlook": "ok"}


def make_pipeline():

    acquisition = FakeAcquisition()
    context = FakeContext()
    evidence = FakeEvidence()
    analysis = FakeAnalysis()
    outlook = FakeOutlook()

    pipeline = MarketIntelligencePipeline(
        acquisition=acquisition,
        context=context,
        evidence=evidence,
        analysis=analysis,
        outlook=outlook,
    )

    return (
        pipeline,
        acquisition,
        context,
        evidence,
        analysis,
        outlook,
    )


def test_pipeline_returns_unified_result():

    pipeline, *_ = make_pipeline()

    result = pipeline.run()

    assert isinstance(
        result,
        MarketIntelligenceResult,
    )

    assert result.observation.price == 4474.0
    assert result.analysis == {"analysis": "ok"}
    assert result.outlook == {"outlook": "ok"}


def test_primary_observation_is_reused():

    (
        pipeline,
        acquisition,
        context,
        *_,
    ) = make_pipeline()

    result = pipeline.run()

    assert acquisition.calls == 1
    assert context.primary_gold is result.observation


def test_evidence_runs_once():

    (
        pipeline,
        _,
        _,
        evidence,
        *_,
    ) = make_pipeline()

    pipeline.run()

    assert evidence.calls == 1


def test_pipeline_preserves_stage_order():

    events = []

    class Acquisition:

        def fetch_latest(self):

            events.append("acquisition")

            return GoldObservation(
                instrument="GC=F",
                source="test",
                timestamp=datetime.now(timezone.utc),
                price=4474.0,
                volume=100,
            )

    class Context:

        def fetch_context(self, primary_gold=None):

            events.append("context")

            return GoldMarketContext(
                gold=primary_gold,
                signals=(),
                gold_change_pct=None,
                candidate_drivers=(),
            )

    class Evidence:

        def fetch_recent(self, queries=None):

            events.append("evidence")
            return []

    class Analysis:

        def analyze(self, context=None, news=None):

            events.append("analysis")
            return "analysis"

    class Outlook:

        def build_outlook(self, context=None):

            events.append("outlook")
            return "outlook"

    pipeline = MarketIntelligencePipeline(
        Acquisition(),
        Context(),
        Evidence(),
        Analysis(),
        Outlook(),
    )

    pipeline.run()

    assert events == [
        "acquisition",
        "context",
        "evidence",
        "analysis",
        "outlook",
    ]
