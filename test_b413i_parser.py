import requests

from platform_core.data.gold_benchmark_providers import IBJAGoldProvider

url = "https://www.ibjarates.com/index.aspx"

response = requests.get(
    url,
    timeout=30,
    headers={"User-Agent": "FIOS-Gold/1.0"},
)

response.raise_for_status()

values = IBJAGoldProvider._extract_current_gold_rates(
    response.text
)

print("========== B4.13I PARSER TEST ==========")
print("HTTP:", response.status_code)
print("VALUES:", values)

assert values is not None
assert "999" in values
assert "916" in values
assert values["999"] > 0
assert values["916"] > 0

print("999:", values["999"])
print("916:", values["916"])
print("B4.13I PARSER: PASS")
