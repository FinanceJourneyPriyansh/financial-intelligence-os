"""
============================================================
Financial Intelligence OS (FIOS)
Event Bus
============================================================
"""

from __future__ import annotations

from collections import deque


class EventBus:
    """
    Central event dispatcher for the FIOS Kernel.
    """

    def __init__(self) -> None:

        self._events: deque[str] = deque()

    def publish(
        self,
        event: str,
    ) -> None:

        self._events.append(event)

    def has_events(self) -> bool:

        return len(self._events) > 0

    def next_event(self) -> str | None:

        if self._events:
            return self._events.popleft()

        return None