from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "01_src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from fios_live.kernel.state.kernel_state import KernelState

app = FastAPI(title="FIOS")

_state: KernelState | None = None
@app.middleware("http")
async def no_cache_static(request, call_next):
    """
    Prevent browsers from serving stale FIOS static assets.
    """
    response = await call_next(request)

    if True:
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"

    return response



def set_state(state: KernelState) -> None:
    """
    Connect the web layer to the existing FIOS Kernel state.
    """
    global _state
    _state = state


def get_state() -> KernelState:
    """
    Return the connected Kernel state.
    """
    if _state is None:
        raise RuntimeError("FIOS web state has not been connected.")
    return _state


@app.get("/api/status")
def status():
    state = get_state()
    uptime_seconds = state.uptime_seconds

    modules = [
        ["Kernel Core", "ONLINE" if state.running else "OFFLINE"],
        ["AI Engine", "ONLINE" if state.brain_online else "OFFLINE"],
        ["Builder Engine", "ONLINE" if state.builder_online else "OFFLINE"],
        ["Automation", "ONLINE" if state.automation_online else "OFFLINE"],
    ]

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "uptime": (
            f"{uptime_seconds // 3600:02d}:"
            f"{uptime_seconds % 3600 // 60:02d}:"
            f"{uptime_seconds % 60:02d}"
        ),
        "health": state.health_score,
        "architecture": state.architecture_score,
        "modules": modules,
        "builder": state.builder_online,
        "automation": state.automation_online,
        "last_event": state.last_event,
    }


app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent / "static"),
    name="static",
)


@app.get("/")
def home():
    return FileResponse(Path(__file__).parent / "static" / "index.html")
