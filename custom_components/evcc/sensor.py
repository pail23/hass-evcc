"""Sensor platform for hass_evcc."""

from __future__ import annotations

from typing import TYPE_CHECKING
from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.const import (
    UnitOfEnergy,
    UnitOfPower,
    UnitOfTime,
    UnitOfLength,
    UnitOfElectricCurrent,
)
from homeassistant.helpers.device_registry import DeviceInfo

from custom_components.evcc.api import EvccApiClient, LoadPoint
from custom_components.evcc.const import DOMAIN

from .entity import EvccEntity, EvccLoadPointEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import EvccDataUpdateCoordinator
    from .data import EvccConfigEntry


@dataclass(kw_only=True, frozen=True)
class EvccLoadpointSensorEntityDescription(SensorEntityDescription):
    """Describes Evcc sensor entity."""

    value_fn: Callable[[LoadPoint], float | int | None]


CHARGED_ENERGY = "hass_evcc_charged_energy"
TOTAL_CHARGED_ENERGY = "hass_evcc_total_charged_energy"
CHARGE_POWER = "hass_evcc_charge_power"
CHARGE_DURATION = "hass_evcc_charge_duration"
CHARGE_REMAINING_DURATION = "hass_evcc_charge_remaining_duration"
CHARGE_REMAINING_ENERGY = "hass_evcc_charge_remaining_energy"
VEHICLE_SOC = "hass_evcc_vehicle_soc"
VEHICLE_LIMIT_SOC = "hass_evcc_vehicle_limit_soc"
VEHICLE_RANGE = "hass_evcc_vehicle_range"
PHASES_ACTIVE = "hass_evcc_active_phases"
CHARGE_CURRENT_L1 = "hass_evcc_charge_current_l1"
CHARGE_CURRENT_L2 = "hass_evcc_charge_current_l2"
CHARGE_CURRENT_L3 = "hass_evcc_charge_current_l3"


ENTITY_DESCRIPTIONS = (
    EvccLoadpointSensorEntityDescription(
        key=CHARGED_ENERGY,
        name="Charged Energy",
        icon="mdi:battery-charging-high",
        translation_key=CHARGED_ENERGY,
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        suggested_display_precision=1,
        value_fn=lambda loadpoint: loadpoint.chargedEnergy,
        state_class=SensorStateClass.TOTAL,
    ),
    EvccLoadpointSensorEntityDescription(
        key=TOTAL_CHARGED_ENERGY,
        name="Total Charged Energy",
        icon="mdi:battery-charging-high",
        translation_key=TOTAL_CHARGED_ENERGY,
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        suggested_display_precision=1,
        value_fn=lambda loadpoint: loadpoint.totalChargedEnergy,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    EvccLoadpointSensorEntityDescription(
        key=CHARGE_POWER,
        name="Charge Power",
        icon="mdi:car-electric",
        translation_key=CHARGE_POWER,
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        suggested_display_precision=1,
        value_fn=lambda loadpoint: loadpoint.chargePower,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    EvccLoadpointSensorEntityDescription(
        key=CHARGE_DURATION,
        name="Charge Duration",
        icon="mdi:timer-settings-outline",
        translation_key=CHARGE_DURATION,
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.SECONDS,
        suggested_display_precision=0,
        value_fn=lambda loadpoint: loadpoint.chargeDuration,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    EvccLoadpointSensorEntityDescription(
        key=CHARGE_REMAINING_DURATION,
        name="Charge Remaining Duration",
        icon="mdi:timer-settings-outline",
        translation_key=CHARGE_REMAINING_DURATION,
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.SECONDS,
        suggested_display_precision=0,
        value_fn=lambda loadpoint: loadpoint.chargeRemainingDuration,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    EvccLoadpointSensorEntityDescription(
        key=CHARGE_REMAINING_ENERGY,
        name="Charge Remaining Energy",
        icon="mdi:battery-charging-high",
        translation_key=CHARGE_REMAINING_ENERGY,
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        suggested_display_precision=1,
        value_fn=lambda loadpoint: loadpoint.chargeRemainingEnergy,
        state_class=SensorStateClass.TOTAL,
    ),
    EvccLoadpointSensorEntityDescription(
        key=VEHICLE_SOC,
        name="Vehicle SoC",
        icon="mdi:battery",
        translation_key=VEHICLE_SOC,
        native_unit_of_measurement="%",
        suggested_display_precision=0,
        value_fn=lambda loadpoint: loadpoint.vehicleSoc,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    EvccLoadpointSensorEntityDescription(
        key=VEHICLE_LIMIT_SOC,
        name="Vehicle Limit SoC",
        icon="mdi:battery",
        translation_key=VEHICLE_LIMIT_SOC,
        native_unit_of_measurement="%",
        suggested_display_precision=0,
        value_fn=lambda loadpoint: loadpoint.vehicleLimitSoc,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    EvccLoadpointSensorEntityDescription(
        key=VEHICLE_RANGE,
        name="Vehicle Range",
        icon="mdi:map-marker-distance",
        translation_key=VEHICLE_RANGE,
        device_class=SensorDeviceClass.DISTANCE,
        native_unit_of_measurement=UnitOfLength.KILOMETERS,
        suggested_display_precision=1,
        value_fn=lambda loadpoint: loadpoint.vehicleRange,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    EvccLoadpointSensorEntityDescription(
        key=CHARGE_CURRENT_L1,
        name="Charge Current L1",
        icon="mdi:current-ac",
        translation_key=CHARGE_CURRENT_L1,
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        suggested_display_precision=1,
        value_fn=lambda loadpoint: loadpoint.currentPhase1,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    EvccLoadpointSensorEntityDescription(
        key=CHARGE_CURRENT_L2,
        name="Charge Current L2",
        icon="mdi:current-ac",
        translation_key=CHARGE_CURRENT_L2,
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        suggested_display_precision=1,
        value_fn=lambda loadpoint: loadpoint.currentPhase2,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    EvccLoadpointSensorEntityDescription(
        key=CHARGE_CURRENT_L3,
        name="Charge Current L3",
        icon="mdi:current-ac",
        translation_key=CHARGE_CURRENT_L3,
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        suggested_display_precision=1,
        value_fn=lambda loadpoint: loadpoint.currentPhase3,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    EvccLoadpointSensorEntityDescription(
        key=PHASES_ACTIVE,
        name="Active Phases",
        icon="mdi:backburger",
        translation_key=PHASES_ACTIVE,
        value_fn=lambda loadpoint: loadpoint.phasesActive,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: EvccConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    async_add_entities(
        LoadpointEvccSensor(
            coordinator=entry.runtime_data.coordinator,
            client=entry.runtime_data.client,
            entity_description=entity_description,
            loadpoint_id=i + 1,
        )
        for entity_description in ENTITY_DESCRIPTIONS
        for i in range(3)
    )


class LoadpointEvccSensor(EvccLoadPointEntity, SensorEntity):
    """hass_evcc Sensor class."""

    def __init__(
        self,
        coordinator: EvccDataUpdateCoordinator,
        client: EvccApiClient,
        entity_description: EvccLoadpointSensorEntityDescription,
        loadpoint_id: int,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(
            coordinator,
            client,
            entity_description.key,
            loadpoint_id,
        )
        self.entity_description = entity_description

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        return (
            self.entity_description.value_fn(self.loadpoint)
            if self.loadpoint is not None
            else None
        )
