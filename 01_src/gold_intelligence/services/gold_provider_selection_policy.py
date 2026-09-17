from __future__ import annotations

from gold_intelligence.services.gold_provider_capability import (
    GoldDataCapability,
    GoldProviderMetadata,
)


class GoldProviderSelectionPolicy:
    """
    Select the strongest available Gold provider capability.

    Priority:
        REALTIME > DELAYED > DAILY > REFERENCE > MOCK
    """

    _PRIORITY = {
        GoldDataCapability.REALTIME: 5,
        GoldDataCapability.DELAYED: 4,
        GoldDataCapability.DAILY: 3,
        GoldDataCapability.REFERENCE: 2,
        GoldDataCapability.MOCK: 1,
    }

    def rank(
        self,
        providers: list[GoldProviderMetadata],
    ) -> list[GoldProviderMetadata]:
        """Return providers from strongest to weakest capability."""

        if not providers:
            raise ValueError(
                "At least one Gold provider is required."
            )

        return sorted(
            providers,
            key=lambda provider: self._PRIORITY[
                provider.capability
            ],
            reverse=True,
        )

    def select(
        self,
        providers: list[GoldProviderMetadata],
    ) -> GoldProviderMetadata:
        if not providers:
            raise ValueError(
                "At least one Gold provider is required."
            )

        return self.rank(providers)[0]

