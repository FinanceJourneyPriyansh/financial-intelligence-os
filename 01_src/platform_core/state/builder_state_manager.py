"""
============================================================
Financial Intelligence OS (FIOS)
Builder State Manager
============================================================
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..generators.yaml_loader import YAMLLoader


class BuilderStateManager:
    """
    Central manager for the Builder State.
    """

    def __init__(
        self,
        builder_state_path: Path,
    ) -> None:

        self._path = Path(builder_state_path)

        self._loader = YAMLLoader()

        self._state: dict[str, Any] = {}

    # ---------------------------------------------------------
    # State
    # ---------------------------------------------------------

    def load(self) -> dict[str, Any]:

        self._state = self._loader.load(
            self._path
        )

        return self._state

    def save(self) -> None:

        self._loader.save(
            self._path,
            self._state,
        )

    def reload(self) -> dict[str, Any]:

        return self.load()

    # ---------------------------------------------------------
    # Access
    # ---------------------------------------------------------

    @property
    def state(self) -> dict[str, Any]:

        return self._state

    def section(
        self,
        name: str,
    ) -> dict[str, Any]:

        return self._state.get(
            name,
            {},
        )

    def get(
        self,
        *keys: str,
        default: Any = None,
    ) -> Any:

        value: Any = self._state

        for key in keys:

            if not isinstance(value, dict):

                return default

            value = value.get(
                key,
                default,
            )

        return value

    # ---------------------------------------------------------
    # Update
    # ---------------------------------------------------------

    def update(
        self,
        section: str,
        key: str,
        value: Any,
    ) -> None:

        if section not in self._state:

            self._state[section] = {}

        self._state[section][key] = value

    # ---------------------------------------------------------
    # Workflow
    # ---------------------------------------------------------

    def workflow(self) -> list[str]:

        return self.get(
            "release",
            "workflow",
            default=[],
        )

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def exists(self) -> bool:

        return self._path.exists()