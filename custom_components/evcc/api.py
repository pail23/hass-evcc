"""Sample API Client."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.components.mqtt import ReceiveMessage

_LOGGER = logging.getLogger(__name__)


class EvccApiClientError(Exception):
    """Exception to indicate a general API error."""


class LoadPoint:
    """Load point data."""

    def __init__(self) -> None:
        """Create a new LoadPoint instance."""
        self.chargedEnergy: float = 0
        self.chargePower: float = 0


class Vehicle:
    """Vehicle data."""

    def __init__(self) -> None:
        """Create a new Vehicle instance."""
        self.title: str = ""
        self.capacity: float = 0


class EvccApiClient:
    """Evcc API Client."""

    def __init__(
        self,
        topic: str,
    ) -> None:
        """Evcc API Client."""
        self._topic = topic
        self.loadpoints: dict[int, LoadPoint] = {}
        self.vehicles: dict[int, Vehicle] = {}

    async def message_received(self, msg: ReceiveMessage) -> None:
        """Handle evcc mqtt messages."""
        _LOGGER.debug("New message: %s=%s", msg.topic, msg.payload)
        parts = msg.topic.split("/")
        if len(parts) > 3:
            if parts[1] == "loadpoints":
                identifier = int(parts[2])
                loadpoint = self.loadpoints.get(identifier)
                if loadpoint is None:
                    loadpoint = LoadPoint()
                    self.loadpoints[identifier] = loadpoint
                if parts[3] == "chargedEnergy":
                    loadpoint.chargedEnergy = float(msg.payload)
                elif parts[3] == "chargePower":
                    loadpoint.chargePower = float(msg.payload)
            elif parts[1] == "vehicle":
                identifier = int(parts[2])
                vehicle = self.vehicles.get(identifier)
                if vehicle is None:
                    vehicle = Vehicle()
                    self.vehicles[identifier] = vehicle
