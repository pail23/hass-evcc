"""
Custom integration to integrate evcc with Home Assistant.

For more details about this integration, please refer to
https://github.com/pail23/hass_evcc
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from homeassistant.components import mqtt
from homeassistant.const import Platform
from homeassistant.loader import async_get_loaded_integration

from .api import EvccApiClient
from .const import CONF_TOPIC
from .coordinator import EvccDataUpdateCoordinator
from .data import EvccData

_LOGGER = logging.getLogger(__name__)

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .data import EvccConfigEntry

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.SWITCH,
]


# https://developers.home-assistant.io/docs/config_entries_index/#setting-up-an-entry
async def async_setup_entry(
    hass: HomeAssistant,
    entry: EvccConfigEntry,
) -> bool:
    """Set up this integration using UI."""
    coordinator = EvccDataUpdateCoordinator(hass=hass, topic=entry.data[CONF_TOPIC])
    entry.runtime_data = EvccData(
        client=EvccApiClient(topic=entry.data[CONF_TOPIC]),
        integration=async_get_loaded_integration(hass, entry.domain),
        coordinator=coordinator,
    )

    await mqtt.async_wait_for_mqtt_client(hass)
    await mqtt.async_subscribe(
        hass, f"{entry.data[CONF_TOPIC]}/#", entry.runtime_data.client.message_received
    )

    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: EvccConfigEntry,
) -> bool:
    """Handle removal of an entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_reload_entry(
    hass: HomeAssistant,
    entry: EvccConfigEntry,
) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
