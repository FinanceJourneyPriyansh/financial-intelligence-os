from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timezone

from gold_intelligence.services.gold_market_snapshot import (
    GoldMarketSnapshot,
)
from gold_intelligence.services.gold_market_snapshot_service import (
    GoldMarketSnapshotService,
)


logger = logging.getLogger(__name__)


class GoldContinuousEngine:
    """
    Long-running Gold snapshot acquisition loop.

    The engine owns continuous execution only. Provider selection,
    market-state detection, and snapshot construction remain delegated
    to their respective services.
    """

    def __init__(
        self,
        snapshot_service: GoldMarketSnapshotService | None = None,
        interval_seconds: float = 1.0,
    ) -> None:
        if interval_seconds <= 0:
            raise ValueError("interval_seconds must be positive.")

        self.snapshot_service = (
            snapshot_service or GoldMarketSnapshotService()
        )
        self.interval_seconds = interval_seconds

        self._latest_snapshot: GoldMarketSnapshot | None = None
        self._task: asyncio.Task | None = None
        self._stop_event = asyncio.Event()

    @property
    def latest_snapshot(self) -> GoldMarketSnapshot | None:
        """Return the latest successfully acquired snapshot."""
        return self._latest_snapshot

    @property
    def running(self) -> bool:
        """Return whether the background engine task is active."""
        return self._task is not None and not self._task.done()

    async def poll_once(self) -> GoldMarketSnapshot:
        """
        Execute one acquisition cycle.

        Snapshot construction is synchronous today, so it is moved to a
        worker thread to avoid blocking the asyncio event loop.
        """

        snapshot = await asyncio.to_thread(
            self.snapshot_service.create_snapshot
        )

        self._latest_snapshot = snapshot

        return snapshot

    async def run(self) -> None:
        """Run continuously until stopped."""

        self._stop_event.clear()

        while not self._stop_event.is_set():
            started = datetime.now(timezone.utc)

            try:
                await self.poll_once()

            except asyncio.CancelledError:
                raise

            except Exception:
                logger.exception(
                    "Gold continuous acquisition cycle failed."
                )

            elapsed = (
                datetime.now(timezone.utc) - started
            ).total_seconds()

            delay = max(
                0.0,
                self.interval_seconds - elapsed,
            )

            try:
                await asyncio.wait_for(
                    self._stop_event.wait(),
                    timeout=delay,
                )

            except asyncio.TimeoutError:
                pass

    async def start(self) -> None:
        """Start the background engine once."""

        if self.running:
            return

        self._stop_event.clear()

        self._task = asyncio.create_task(
            self.run(),
            name="fios-gold-continuous-engine",
        )

    async def stop(self) -> None:
        """Stop the background engine gracefully."""

        self._stop_event.set()

        task = self._task

        if task is None:
            return

        self._task = None

        if not task.done():
            task.cancel()

        try:
            await task
        except asyncio.CancelledError:
            pass

