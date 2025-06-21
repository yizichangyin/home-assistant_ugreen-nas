import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from datetime import date, datetime
from decimal import Decimal

from .device_info import build_device_info
from .const import DOMAIN
from .api import UgreenSensorAPIEndpoint
from .utils import format_bytes, format_duration, format_sensor_value

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback
) -> None:
    """Set up UGREEN NAS sensors based on a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    endpoints = hass.data[DOMAIN][entry.entry_id]["sensor_endpoints"]

    entities = [
        UgreenNasSensor(entry.entry_id, coordinator, endpoint)
        for endpoint in endpoints
    ]

    async_add_entities(entities)


class UgreenNasSensor(CoordinatorEntity, SensorEntity):
    """Representation of a UGREEN NAS sensor."""

    def __init__(self, entry_id: str, coordinator: DataUpdateCoordinator, endpoint: UgreenSensorAPIEndpoint) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._entry_id = entry_id
        self._endpoint = endpoint
        self._key = endpoint.key

        self._attr_name = f"UGREEN NAS {endpoint.name}"
        self._attr_unique_id = f"{entry_id}_{endpoint.key}"
        self._attr_icon = endpoint.icon
        self._attr_native_unit_of_measurement = endpoint.unit

        self._attr_device_info = build_device_info(self._key)

    @property
    def native_value(self) -> StateType | date | datetime | Decimal:
        """Return the formatted value of the sensor."""
        raw = self.coordinator.data.get(self._key)
        return format_sensor_value(raw, self._endpoint)
    
    def _handle_coordinator_update(self) -> None:
        """Update the sensor value from the coordinator."""
        self._attr_native_value = self.native_value
        super()._handle_coordinator_update()
