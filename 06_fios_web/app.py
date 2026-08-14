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
from fios_live.kernel.services.service_manager import ServiceManager

app = FastAPI(title="FIOS")

_state: KernelState | None = None
_services: ServiceManager | None = None
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


def set_services(services: ServiceManager) -> None:
    """
    Connect the web layer to the existing FIOS ServiceManager.
    """
    global _services
    _services = services

def get_state() -> KernelState:
    """
    Return the connected Kernel state.
    """
    if _state is None:
        raise RuntimeError("FIOS web state has not been connected.")
    return _state


def _truth_status():
    """
    Canonical TEST truth projection.

    IMPORTANT:
        runtime  = actual kernel/runtime state
        monitored = actual monitoring results

    KernelState fields are NOT presented as modules.
    No dashboard names, statuses, percentages, or load
    values are invented here.
    """

    state = get_state()

    # --------------------------------------------------------
    # REAL RUNTIME STATE
    # --------------------------------------------------------

    runtime = []

    runtime_fields = (
        ("running", "Running"),
        ("repository_loaded", "Repository Loaded"),
        ("brain_online", "Brain Online"),
        ("builder_online", "Builder Online"),
        ("dashboard_online", "Dashboard Online"),
        ("automation_online", "Automation Online"),
    )

    for key, name in runtime_fields:

        value = getattr(
            state,
            key,
            None,
        )

        runtime.append(
            {
                "key": key,
                "name": name,
                "status": (
                    "ONLINE"
                    if value is True
                    else "OFFLINE"
                    if value is False
                    else "N/A"
                ),
                "healthy": (
                    value
                    if isinstance(value, bool)
                    else None
                ),
            }
        )

    # --------------------------------------------------------
    # REAL MONITORED MODULES
    # --------------------------------------------------------

    monitored = []

    try:

        # The live FIOS process already owns the service graph.
        # Reuse it when available; do not boot a second system.

        candidates = [
            # PRIMARY: the actual ServiceManager connected
            # through set_services().
            globals().get("_services"),

            # Compatibility with any existing aliases.
            globals().get("service_manager"),
            globals().get("manager"),
            globals().get("services"),
            globals().get("sm"),
        ]

        service_manager = next(
            (
                item
                for item in candidates
                if item is not None
            ),
            None,
        )

        builder = None

        if service_manager is not None:
            builder = getattr(
                service_manager,
                "builder",
                None,
            )

        if builder is None:
            builder = globals().get("builder")

        monitoring_manager = None

        if builder is not None:
            monitoring_manager = getattr(
                builder,
                "monitoring_manager",
                None,
            )

        monitoring_result = None

        if monitoring_manager is not None:
            monitoring_result = monitoring_manager.run()

        # ----------------------------------------------------
        # If the live Builder context is available, reuse it.
        # ----------------------------------------------------

        if monitoring_result is None and builder is not None:

            context = getattr(
                builder,
                "context",
                None,
            )

            if context is not None:

                monitoring_result = (
                    getattr(
                        context,
                        "reports",
                        {}
                    ) or {}
                ).get(
                    "monitoring"
                )

        if isinstance(
            monitoring_result,
            dict,
        ):

            for key, item in monitoring_result.items():
                # ------------------------------------------------
                # REAL MODULE PROJECTION GUARD
                # ------------------------------------------------
                # Aggregate telemetry records are not modules.
                # Only monitoring results with a real health value
                # are projected into monitored[].
                # ------------------------------------------------

                if not isinstance(item, dict):
                    continue

                if item.get("health") is None:
                    continue


                if key == "summary":
                    continue

                if not isinstance(
                    item,
                    dict,
                ):
                    continue

                monitored.append(
                    {
                        "key": key,

                        "name": item.get(
                            "module",
                            key,
                        ),

                        "status": item.get(
                            "status",
                            "UNKNOWN",
                        ),

                        "health": item.get(
                            "health"
                        ),

                        "metrics": item.get(
                            "metrics",
                            {},
                        ),

                        "warnings": item.get(
                            "warnings",
                            [],
                        ),

                        "errors": item.get(
                            "errors",
                            [],
                        ),

                        "timestamp": item.get(
                            "timestamp"
                        ),
                    }
                )

    except Exception as exc:

        monitored.append(
            {
                "key": "monitoring",
                "name": "Monitoring",
                "status": "ERROR",
                "health": None,
                "metrics": {},
                "warnings": [],
                "errors": [str(exc)],
                "timestamp": None,
            }
        )

    # --------------------------------------------------------
    # REAL LOAD
    # --------------------------------------------------------

    load = None

    try:
        import psutil

        load = round(
            float(
                psutil.cpu_percent(
                    interval=None
                )
            ),
            1,
        )

    except Exception:
        load = None

    # --------------------------------------------------------
    # CANONICAL TRUTH RESPONSE
    # --------------------------------------------------------

    return {
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),

        "uptime": (
            f"{state.uptime_seconds // 3600:02d}:"
            f"{state.uptime_seconds % 3600 // 60:02d}:"
            f"{state.uptime_seconds % 60:02d}"
        ),

        "health": state.health_score,

        "architecture": state.architecture_score,

        "runtime": runtime,

        "monitored": monitored,

        "last_event": state.last_event,

        "load": load,
    }

app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent / "static"),
    name="static",
)


@app.get("/")
def home():
    return FileResponse(Path(__file__).parent / "static" / "index.html")


@app.get("/api/status")
def status():
    """
    Production FIOS truth endpoint.

    Uses the exact same canonical truth projection as TEST.
    """
    return _truth_status()


@app.get("/api/test/status")
def test_status():
    """
    Explicit TEST truth endpoint.

    Uses the exact same canonical truth projection as LIVE.
    """
    return _truth_status()
