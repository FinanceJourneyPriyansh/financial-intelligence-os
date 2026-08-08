"""
Financial Intelligence OS (FIOS)
Central Kernel
"""

from __future__ import annotations

import importlib.util
import threading
import time
from pathlib import Path

import uvicorn

from fios_live.kernel.events.event_bus import EventBus
from fios_live.kernel.services.service_manager import ServiceManager
from fios_live.kernel.state.kernel_state import KernelState


class Kernel:
    """
    Central FIOS Kernel.
    """

    def __init__(self) -> None:
        self._services = ServiceManager()
        self._events = EventBus()
        self._web_server: uvicorn.Server | None = None

    @property
    def state(self) -> KernelState:
        """
        Return the current Kernel state.
        """
        return self._services.state

    def _start_web_server(self) -> None:
        """
        Start the existing FIOS FastAPI application.
        """

        app_path = (
            Path(__file__).resolve().parents[2]
            / "06_fios_web"
            / "app.py"
        )

        spec = importlib.util.spec_from_file_location(
            "fios_web_app",
            app_path,
        )

        if spec is None or spec.loader is None:
            raise RuntimeError(
                f"Unable to load FIOS web application: {app_path}"
            )

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        module.set_state(self.state)

        config = uvicorn.Config(
            module.app,
            host="127.0.0.1",
            port=8000,
            log_level="warning",
        )

        self._web_server = uvicorn.Server(config)
        self._web_server.run()

    def start(self) -> None:
        """
        Boot FIOS and keep the Kernel continuously running.
        """

        state = self._services.boot()

        self._events.publish("SYSTEM_BOOT")

        print()
        print("=" * 70)
        print("FIOS KERNEL ONLINE")
        print("=" * 70)
        print()

        print("Repository :", state.repository_loaded)
        print("Brain      :", state.brain_online)
        print("Builder    :", state.builder_online)

        web_thread = threading.Thread(
            target=self._start_web_server,
            name="FIOS-Web",
            daemon=True,
        )

        web_thread.start()

        self.state.dashboard_online = True

        print()
        print("Dashboard  :", self.state.dashboard_online)
        print("Web Server : http://127.0.0.1:8000")
        print()

        while True:

            self.state.uptime_seconds = int(
                (time.time() - self.state.boot_time.timestamp())
            )

            while self._events.has_events():

                event = self._events.next_event()

                if event is not None:
                    print(f"[EVENT] {event}")

            time.sleep(1)