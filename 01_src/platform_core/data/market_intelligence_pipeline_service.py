"""
FIOS reusable market intelligence pipeline.

This is an orchestration capability, not a Gold-specific architecture.

The pipeline receives capability implementations and connects them
into one execution flow:

acquisition -> context -> evidence -> analysis -> outlook

Future assets can reuse the same pipeline contract.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Generic, TypeVar


ObservationT = TypeVar("ObservationT")
ContextT = TypeVar("ContextT")
EvidenceT = TypeVar("EvidenceT")
AnalysisT = TypeVar("AnalysisT")
OutlookT = TypeVar("OutlookT")


@dataclass(frozen=True)
class MarketIntelligenceResult(
    Generic[
        ObservationT,
        ContextT,
        EvidenceT,
        AnalysisT,
        OutlookT,
    ]
):
    observation: ObservationT
    context: ContextT
    evidence: EvidenceT
    analysis: AnalysisT
    outlook: OutlookT


class MarketIntelligencePipeline(
    Generic[
        ObservationT,
        ContextT,
        EvidenceT,
        AnalysisT,
        OutlookT,
    ]
):
    """
    Reusable execution pipeline for market intelligence.

    Services are injected rather than hard-coded so the same pipeline
    can later support other assets without creating another architecture.
    """

    def __init__(
        self,
        acquisition: Any,
        context: Any,
        evidence: Any,
        analysis: Any,
        outlook: Any,
    ) -> None:

        self.acquisition = acquisition
        self.context = context
        self.evidence = evidence
        self.analysis = analysis
        self.outlook = outlook

    def run(self) -> MarketIntelligenceResult:

        observation = self.acquisition.fetch_latest()

        market_context = self.context.fetch_context(observation)

        news = self.evidence.fetch_recent()

        analysis = self.analysis.analyze(
            context=market_context,
            news=news,
        )

        outlook = self.outlook.build_outlook(
            context=market_context,
        )

        return MarketIntelligenceResult(
            observation=observation,
            context=market_context,
            evidence=news,
            analysis=analysis,
            outlook=outlook,
        )

