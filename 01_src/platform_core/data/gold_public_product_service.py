from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup

from platform_core.data.gold_acquisition_service import (
    GoldAcquisitionService,
)
from platform_core.data.gold_market_context_service import (
    GoldMarketContextService,
)
from platform_core.data.gold_news_evidence_service import (
    GoldNewsEvidenceService,
)
from platform_core.data.gold_move_analysis_service import (
    GoldMoveAnalysisService,
)
from platform_core.data.gold_india_outlook_service import (
    GoldIndiaOutlookService,
)
from platform_core.data.market_intelligence_pipeline_service import (
    MarketIntelligencePipeline,
)


@dataclass(frozen=True)
class GoldPublicIntelligence:
    """
    Public presentation contract for Gold Intelligence.

    This is an adapter over the existing reusable FIOS
    intelligence pipeline. It contains no market logic.
    """

    generated_at: datetime
    quote_timestamp: datetime
    retrieved_at: datetime
    price: float
    previous_price: float | None
    change_pct: float | None
    source: str
    instrument: str
    usd_inr: float | None

    india_rate_timestamp: datetime | None
    india_rate_source: str | None

    india_24k_10g: float | None
    india_22k_10g: float | None
    india_18k_10g: float | None
    india_transmission: str
    overall_confidence: str
    summary: str
    driver_assessments: tuple
    scenarios: tuple
    evidence: tuple


class GoldPublicProductService:
    """
    Thin public-product adapter.

    Reuses the existing FIOS intelligence capabilities.
    Does not modify the private FIOS dashboard/runtime.
    """

    def __init__(self) -> None:

        self.pipeline = MarketIntelligencePipeline(
            acquisition=GoldAcquisitionService(),
            context=GoldMarketContextService(),
            evidence=GoldNewsEvidenceService(),
            analysis=GoldMoveAnalysisService(),
            outlook=GoldIndiaOutlookService(),
        )

    def _fetch_india_gold_rates(self) -> dict:
        """
        Fetch published Indian gold rates from GoodReturns.

        This is a source-backed India-rate adapter for the
        public product. It does not replace the reusable
        FIOS market-intelligence pipeline.
        """

        url = "https://www.goodreturns.in/gold-rates/"

        response = requests.get(
            url,
            timeout=20,
            headers={
                "User-Agent":
                    "Mozilla/5.0 "
                    "FIOS-Gold-Intelligence/1.0"
            },
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser",
        )

        import re

        rates = {
            "24k_10g": None,
            "22k_10g": None,
            "18k_10g": None,
        }

        # GoodReturns publishes the India gold table in
        # PER-GRAM units.
        #
        # Example source row:
        #
        #   1 | 15,566 (+53) | 14,270 (+50) | 11,676 (+41)
        #
        # Source contract:
        #   24K / gram
        #   22K / gram
        #   18K / gram
        #
        # FIOS canonical contract:
        #   24K / 10g
        #   22K / 10g
        #   18K / 10g
        #
        # IMPORTANT:
        # Never parse the header row
        # "Gram | 24K | 22K | 18K" as prices.

        for row in soup.find_all("tr"):

            cells = row.find_all(
                ["th", "td"]
            )

            values = [
                cell.get_text(
                    " ",
                    strip=True,
                )
                for cell in cells
            ]

            if len(values) < 4:
                continue

            first = values[0].strip().lower()

            # The live India table uses weight "1"
            # for its per-gram row.
            if first != "1":
                continue

            parsed = []

            for value in values[1:4]:

                cleaned = value.replace(
                    ",",
                    "",
                )

                match = re.search(
                    r"(\d+(?:\.\d+)?)",
                    cleaned,
                    re.IGNORECASE,
                )

                if not match:
                    parsed.append(None)
                    continue

                parsed.append(
                    float(match.group(1))
                )

            if all(
                value is not None
                for value in parsed
            ):

                rates["24k_10g"] = (
                    parsed[0] * 10.0
                )

                rates["22k_10g"] = (
                    parsed[1] * 10.0
                )

                rates["18k_10g"] = (
                    parsed[2] * 10.0
                )

                break

        # Fallback: inspect visible text if the table layout
        # changes while keeping the same public-source contract.
        if any(
            value is None
            for value in rates.values()
        ):

            visible_text = soup.get_text(
                " ",
                strip=True,
            )

            for carat, key in (
                ("24K", "24k_10g"),
                ("22K", "22k_10g"),
                ("18K", "18k_10g"),
            ):

                if rates[key] is not None:
                    continue

                position = visible_text.lower().find(
                    carat.lower()
                )

                if position == -1:
                    continue

                window = visible_text[
                    position:
                    position + 500
                ]

                numbers = re.findall(
                    r"[0-9][0-9,]*",
                    window,
                )

                candidates = []

                for value in numbers:

                    numeric = float(
                        value.replace(",", "")
                    )

                    if numeric >= 1000:
                        candidates.append(
                            numeric
                        )

                if candidates:
                    rates[key] = candidates[0]

        missing = [
            key
            for key, value in rates.items()
            if value is None
        ]

        if missing:
            raise RuntimeError(
                "Unable to extract Indian gold rates: "
                + ", ".join(missing)
            )

        return {
            "source": "GoodReturns",
            "timestamp": datetime.now(timezone.utc),
            **rates,
        }

    def generate(self) -> GoldPublicIntelligence:

        result = self.pipeline.run()

        generated_at = datetime.now(timezone.utc)

        usd_inr = None

        for signal in result.context.signals:
            if signal.instrument == "INR=X":
                usd_inr = signal.value
                break

        india_rates = self._fetch_india_gold_rates()

        return GoldPublicIntelligence(
            generated_at=generated_at,
            quote_timestamp=result.observation.timestamp,
            retrieved_at=generated_at,
            price=result.observation.price,
            previous_price=result.observation.previous_price,
            change_pct=result.observation.change_pct,
            source=result.observation.source,
            instrument=result.observation.instrument,
            usd_inr=usd_inr,

            india_rate_timestamp=india_rates["timestamp"],
            india_rate_source=india_rates["source"],

            india_24k_10g=india_rates["24k_10g"],
            india_22k_10g=india_rates["22k_10g"],
            india_18k_10g=india_rates["18k_10g"],
            india_transmission=result.outlook.india_transmission,
            overall_confidence=result.analysis.overall_confidence,
            summary=result.analysis.summary,
            driver_assessments=result.analysis.assessments,
            scenarios=result.outlook.scenarios,
            evidence=tuple(result.evidence),
        )
