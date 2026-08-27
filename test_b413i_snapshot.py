from platform_core.data.gold_market_snapshot_service import (
    GoldMarketSnapshotService,
)


def main() -> None:
    print("========== B4.13I SNAPSHOT ==========")

    snapshot = GoldMarketSnapshotService().create_snapshot()

    print("STATUS:", snapshot.market_status.value)
    print("SOURCE:", snapshot.source)
    print("INSTRUMENT:", snapshot.instrument)
    print("LTP:", snapshot.ltp)
    print("CAPABILITY:", snapshot.capability.value)
    print("REALTIME:", snapshot.is_realtime)
    print("MARKET ROLE:", snapshot.market_role)
    print("PURITY:", snapshot.purity_rates)

    assert snapshot.ltp is not None

    # Yahoo remains the selected market ticker provider.
    assert snapshot.source == "yahoo_finance"

    # IBJA benchmark enrichment must reach the canonical snapshot.
    assert snapshot.purity_rates is not None
    assert "999" in snapshot.purity_rates
    assert "916" in snapshot.purity_rates

    assert snapshot.purity_rates["999"] > 0
    assert snapshot.purity_rates["916"] > 0

    print("B4.13I SNAPSHOT: PASS")


if __name__ == "__main__":
    main()