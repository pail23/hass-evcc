"""Sensor platform for hass_evcc."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription

from .entity import EvccEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import EvccDataUpdateCoordinator
    from .data import EvccConfigEntry

ENTITY_DESCRIPTIONS = (
    SensorEntityDescription(
        key="hass_evcc_charged_energy",
        name="Charged Energy",
        icon="mdi:format-quote-close",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: EvccConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    loadpoints = entry.runtime_data.client.loadpoints
    print(f"{len(loadpoints)} Loadpoints detected")
    async_add_entities(
        EvccSensor(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class EvccSensor(EvccEntity, SensorEntity):
    """hass_evcc Sensor class."""

    def __init__(
        self,
        coordinator: EvccDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        loadpoints = self.coordinator.data.get("loadpoints")
        loadpoint = loadpoints.get(1)

        return loadpoint.chargedEnergy if loadpoint is not None else None
