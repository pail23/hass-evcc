"""Binary sensor platform for hass_evcc."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)

from .entity import EvccEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import EvccDataUpdateCoordinator
    from .data import EvccConfigEntry

ENTITY_DESCRIPTIONS = (
    BinarySensorEntityDescription(
        key="hass_evcc",
        name="Integration Blueprint Binary Sensor",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: EvccConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the binary_sensor platform."""
    async_add_entities(
        IntegrationBlueprintBinarySensor(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class IntegrationBlueprintBinarySensor(EvccEntity, BinarySensorEntity):
    """hass_evcc binary_sensor class."""

    def __init__(
        self,
        coordinator: EvccDataUpdateCoordinator,
        entity_description: BinarySensorEntityDescription,
    ) -> None:
        """Initialize the binary_sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description

    @property
    def is_on(self) -> bool:
        """Return true if the binary_sensor is on."""
        return self.coordinator.data.get("title", "") == "foo"
