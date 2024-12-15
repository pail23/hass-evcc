"""
Custom integration to integrate evcc with Home Assistant.

For more details about this integration, please refer to
https://github.com/pail23/hass_evcc
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import logging

from homeassistant.const import CONF_PASSWORD, CONF_USERNAME, Platform
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.loader import async_get_loaded_integration

from homeassistant.components import mqtt

from .api import EvccApiClient
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
    coordinator = EvccDataUpdateCoordinator(
        hass=hass,
    )
    entry.runtime_data = EvccData(
        client=EvccApiClient(
            username=entry.data[CONF_USERNAME],
            password=entry.data[CONF_PASSWORD],
            session=async_get_clientsession(hass),
        ),
        integration=async_get_loaded_integration(hass, entry.domain),
        coordinator=coordinator,
    )

    async def message_received(msg):
        _LOGGER.debug("New intent: %s", msg.payload)
        print(msg.topic)

    await mqtt.async_subscribe(hass, "evcc/#", message_received)

    # https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
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
