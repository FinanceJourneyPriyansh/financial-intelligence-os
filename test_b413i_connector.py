from platform_core.data.gold_benchmark_providers import IBJAGoldProvider

print("========== B4.13I IBJA CONNECTOR ==========")

provider = IBJAGoldProvider()

print("AVAILABLE:", provider.available())

observation = provider.fetch_latest()

print("SOURCE:", observation.source)
print("INSTRUMENT:", observation.instrument)
print("LTP:", observation.ltp)
print("UNIT:", observation.unit)
print("CURRENCY:", observation.currency)
print("REALTIME:", observation.is_realtime)
print("PURITY RATES:", observation.purity_rates)

assert observation.source == "ibja"
assert observation.ltp == 158386.0
assert observation.purity_rates is not None
assert observation.purity_rates["999"] == 158386.0
assert observation.purity_rates["916"] == 145082.0

print("B4.13I CONNECTOR: PASS")
