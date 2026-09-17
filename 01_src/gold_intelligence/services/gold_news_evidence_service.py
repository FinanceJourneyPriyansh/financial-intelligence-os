"""
FIOS Gold News Evidence Service

Day 3 Phase 2:
Acquire and normalize recent gold-related news evidence.

This service is an evidence/discovery layer.
It does not claim that a news article caused a market move.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from urllib.parse import quote
import xml.etree.ElementTree as ET

import requests


@dataclass(frozen=True)
class GoldNewsEvidence:
    title: str
    source: str
    published_at: datetime
    url: str
    query: str
    retrieved_at: datetime


class GoldNewsEvidenceService:
    """Acquire recent gold-related news from Google News RSS."""

    BASE_URL = "https://news.google.com/rss/search"

    SOURCE = "google_news_rss"

    QUERIES = (
        "gold price",
        "gold market",
        "gold India",
    )

    def _request(self, query: str) -> bytes:
        url = (
            f"{self.BASE_URL}"
            f"?q={quote(query)}"
            "&hl=en-US"
            "&gl=US"
            "&ceid=US:en"
        )

        response = requests.get(
            url,
            timeout=20,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 "
                    "FIOS-Gold-Intelligence/0.1"
                ),
                "Accept": (
                    "application/rss+xml,"
                    "application/xml,text/xml,*/*"
                ),
            },
        )

        response.raise_for_status()

        return response.content

    @staticmethod
    def _parse_datetime(value: str) -> datetime:
        parsed = parsedate_to_datetime(value)

        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)

        return parsed

    def _parse(
        self,
        payload: bytes,
        query: str,
        retrieved_at: datetime,
    ) -> list[GoldNewsEvidence]:

        root = ET.fromstring(payload)

        evidence: list[GoldNewsEvidence] = []

        for item in root.findall(".//item"):

            title = item.findtext("title")
            link = item.findtext("link")
            pub_date = item.findtext("pubDate")
            source = item.findtext("source")

            if not title or not link or not pub_date:
                continue

            evidence.append(
                GoldNewsEvidence(
                    title=title.strip(),
                    source=(source or "unknown").strip(),
                    published_at=self._parse_datetime(
                        pub_date
                    ),
                    url=link.strip(),
                    query=query,
                    retrieved_at=retrieved_at,
                )
            )

        return evidence

    def fetch_recent(
        self,
        queries: tuple[str, ...] | None = None,
    ) -> list[GoldNewsEvidence]:

        selected_queries = (
            queries
            if queries is not None
            else self.QUERIES
        )

        retrieved_at = datetime.now(timezone.utc)

        results: list[GoldNewsEvidence] = []

        for query in selected_queries:

            payload = self._request(query)

            results.extend(
                self._parse(
                    payload,
                    query,
                    retrieved_at,
                )
            )

        # Deduplicate by URL while preserving order.
        unique: dict[str, GoldNewsEvidence] = {}

        for item in results:
            unique.setdefault(item.url, item)

        return list(unique.values())
