"""Custom types for hass_evcc."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .api import EvccApiClient
    from .coordinator import EvccDataUpdateCoordinator


type EvccConfigEntry = ConfigEntry[EvccData]


@dataclass
class EvccData:
    """Data for the Blueprint integration."""

    client: EvccApiClient
    coordinator: EvccDataUpdateCoordinator
    integration: Integration
