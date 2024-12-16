"""Sample API Client."""

from __future__ import annotations

import logging

_LOGGER = logging.getLogger(__name__)


class EvccApiClientError(Exception):
    """Exception to indicate a general API error."""


class LoadPoint:
    """Load point data."""

    def __init__(self) -> None:
        self.chargedEnergy: float = 0
        self.chargePower: float = 0


class EvccApiClient:
    """Evcc API Client."""

    def __init__(
        self,
        topic: str,
    ) -> None:
        """Evcc API Client."""
        self._topic = topic
        self.loadpoints: dict[int, LoadPoint] = {}

    async def message_received(self, msg) -> None:
        """Handle evcc mqtt messages."""
        _LOGGER.debug("New message: %s=%s", msg.topic, msg.payload)
        # print(f"{msg.topic}={msg.payload}")
        parts = msg.topic.split("/")
        if len(parts) > 3:
            if parts[1] == "loadpoints":
                id = int(parts[2])
                loadpoint = self.loadpoints.get(id)
                if loadpoint is None:
                    loadpoint = LoadPoint()
                    self.loadpoints[id] = loadpoint
                if parts[3] == "chargedEnergy":
                    loadpoint.chargedEnergy = float(msg.payload)
                    print(f"{id}: Charged Energy={loadpoint.chargedEnergy}")
                elif parts[3] == "chargePower":
                    loadpoint.chargePower = float(msg.payload)
                    print(f"{id}: Charged Power={loadpoint.chargePower}")
