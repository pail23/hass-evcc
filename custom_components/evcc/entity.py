"""BlueprintEntity class."""

from __future__ import annotations
from typing import TYPE_CHECKING
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from custom_components.evcc.api import EvccApiClient, LoadPoint

from .const import ATTRIBUTION, DOMAIN
from .coordinator import EvccDataUpdateCoordinator


class EvccEntity(CoordinatorEntity[EvccDataUpdateCoordinator]):
    """EvccEntity class."""

    _attr_attribution = ATTRIBUTION

    def __init__(self, coordinator: EvccDataUpdateCoordinator) -> None:
        """Initialize."""
        super().__init__(coordinator)


class EvccLoadPointEntity(EvccEntity):
    """EvccLoadPointEntity class."""

    def __init__(
        self,
        coordinator: EvccDataUpdateCoordinator,
        client: EvccApiClient,
        entity_type: str,
        loadpoint_id: int,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self.loadpoint_id = loadpoint_id
        self.client = client
        unique_id = coordinator.config_entry.entry_id
        self._attr_unique_id = f"{unique_id}_lp_{loadpoint_id}_{entity_type}"

    @property
    def loadpoint(self) -> LoadPoint | None:
        """Get the assigned load point."""
        return self.client.loadpoints.get(self.loadpoint_id)

    @property
    def device_info(self) -> DeviceInfo:
        """Return device specific attributes."""
        unique_id = f"{self.coordinator.config_entry.entry_id}_lp_{self.loadpoint_id}"
        return DeviceInfo(
            name=f"Load point {self.loadpoint.title if self.loadpoint is not None else self.loadpoint_id}",
            identifiers={(unique_id, DOMAIN)},
            manufacturer="EVCC",
        )
