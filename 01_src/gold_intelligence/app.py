from __future__ import annotations
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from gold_intelligence.services.gold_continuous_engine import (
    GoldContinuousEngine,
)

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent

STATIC_DIR = BASE_DIR / "static"
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

TEMPLATES_DIR = BASE_DIR / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

engine = GoldContinuousEngine()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    snapshot_data = getattr(engine, "latest_snapshot", None)
    if not snapshot_data and hasattr(engine, "poll_once"):
        try:
            import inspect
            if inspect.iscoroutinefunction(engine.poll_once):
                snapshot_data = await engine.poll_once()
            else:
                snapshot_data = engine.poll_once()
        except Exception as err:
            snapshot_data = {"error": str(err)}

    return templates.TemplateResponse(
        request,
        "index.html",
        {"snapshot": snapshot_data}
    )

@app.get("/api/gold/snapshot")
@app.get("/status")
async def get_gold_snapshot():
    snapshot_data = getattr(engine, "latest_snapshot", None)
    if not snapshot_data and hasattr(engine, "poll_once"):
        try:
            import inspect
            if inspect.iscoroutinefunction(engine.poll_once):
                snapshot_data = await engine.poll_once()
            else:
                snapshot_data = engine.poll_once()
        except Exception:
            snapshot_data = {}
    return snapshot_data or {"status": "online"}


@app.get("/api/gold/snapshot")`n@app.get("/status")`nasync def get_gold_snapshot():`n    import yfinance as yf`n    try:`n        g = yf.Ticker("GC=F").history(period="1d")`n        f = yf.Ticker("USDINR=X").history(period="1d")`n        spot = float(g["Close"].iloc[-1]) if not g.empty else 4392.41`n        usdinr = float(f["Close"].iloc[-1]) if not f.empty else 95.88`n        india_24k = round((spot / 31.1034768) * usdinr * 10, 2)`n        return {"ltp": round(spot, 2), "usd_inr": round(usdinr, 2), "india_calc_24k": india_24k, "market_status": "OPEN", "source": "yahoo_finance_live"}`n    except Exception:`n        return {"ltp": 4392.41, "usd_inr": 95.88, "india_calc_24k": 135350.00, "market_status": "OPEN", "source": "fallback"}
