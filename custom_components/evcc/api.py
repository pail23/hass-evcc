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
        self.totalChargedEnergy: float = 0
        self.chargePower: float = 0
        self.title = ""
        self.chargeDuration: float = 0  # in seconds
        self.chargeRemainingDuration: float = 0  # in seconds
        self.chargeRemainingEnergy: float = 0
        self.vehicleSoc: float = 0
        self.vehicleLimitSoc: float = 0
        self.vehicleRange: float = 0
        self.phasesActive: int = 0
        self.currentPhase1: float = 0
        self.currentPhase2: float = 0
        self.currentPhase3: float = 0


class Vehicle:
    """Vehicle data."""

    def __init__(self) -> None:
        """Create a new Vehicle instance."""
        self.title: str = ""
        self.capacity: float = 0
        self.title = ""


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
                elif parts[3] == "title":
                    loadpoint.title = str(msg.payload)
                elif parts[3] == "chargeTotalImport":
                    loadpoint.totalChargedEnergy = float(msg.payload)
                elif parts[3] == "chargeDuration":
                    loadpoint.chargeDuration = float(msg.payload)
                elif parts[3] == "chargeRemainingDuration":
                    loadpoint.chargeRemainingDuration = float(msg.payload)
                elif parts[3] == "chargeRemainingEnergy":
                    loadpoint.chargeRemainingEnergy = float(msg.payload)
                elif parts[3] == "vehicleSoc":
                    loadpoint.vehicleSoc = float(msg.payload)
                elif parts[3] == "vehicleLimitSoc":
                    loadpoint.vehicleLimitSoc = float(msg.payload)
                elif parts[3] == "vehicleRange":
                    loadpoint.vehicleRange = float(msg.payload)
                elif parts[3] == "phasesActive":
                    loadpoint.phasesActive = int(msg.payload)
                elif parts[3] == "chargeCurrents" and len(parts) > 4:
                    if parts[4] == "l1":
                        loadpoint.currentPhase1 = float(msg.payload)
                    elif parts[4] == "l2":
                        loadpoint.currentPhase2 = float(msg.payload)
                    elif parts[4] == "l3":
                        loadpoint.currentPhase3 = float(msg.payload)
            elif parts[1] == "vehicle":
                identifier = int(parts[2])
                vehicle = self.vehicles.get(identifier)
                if vehicle is None:
                    vehicle = Vehicle()
                    self.vehicles[identifier] = vehicle
                if parts[3] == "title":
                    vehicle.title = str(msg.payload)
                elif parts[3] == "capacity":
                    vehicle.capacity = float(msg.payload)
                elif parts[3] == "title":
                    vehicle.title = str(msg.payload)
