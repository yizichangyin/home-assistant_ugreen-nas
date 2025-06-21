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
from .api import UgreenEntity
from .utils import format_sensor_value

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback
) -> None:
    """Set up UGREEN NAS sensors based on a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    endpoints = hass.data[DOMAIN][entry.entry_id]["sensor_endpoints"]

    nas_model = hass.data[DOMAIN][entry.entry_id].get("nas_model")
    entities = [
        UgreenNasSensor(entry.entry_id, coordinator, endpoint, nas_model)
        for endpoint in endpoints
    ]

    async_add_entities(entities)

class UgreenNasSensor(CoordinatorEntity, SensorEntity): # type: ignore
    """Representation of a UGREEN NAS sensor."""

    def __init__(self, entry_id: str, coordinator: DataUpdateCoordinator, endpoint: UgreenEntity, nas_model: 'str | None' = None) -> None:
        super().__init__(coordinator)
        self._entry_id = entry_id
        self._endpoint = endpoint
        self._key = endpoint.description.key

        self._attr_name = f"UGREEN NAS {endpoint.description.name}"
        self._attr_unique_id = f"{entry_id}_{endpoint.description.key}"
        self._attr_icon = endpoint.description.icon
        self._attr_native_unit_of_measurement = endpoint.description.unit_of_measurement

        base_device_info = build_device_info(self._key)

        if "disk" in self._key and "brand" in self._key:
            base_device_info["manufacturer"] = str(self.coordinator.data.get(self._key) or "UGREEN")
            
        if "disk" in self._key and "model" in self._key:
            base_device_info["model"] = str(self.coordinator.data.get(self._key))
        
        self._attr_device_info = build_device_info(self._key, nas_model)

    @property
    def native_value(self) -> StateType | date | datetime | Decimal: # type: ignore
        """Return the formatted value of the sensor."""
        raw = self.coordinator.data.get(self._key)
        return format_sensor_value(raw, self._endpoint)
    
    def _handle_coordinator_update(self) -> None:
        """Update the sensor value from the coordinator."""
        self._attr_native_value = self.native_value
        super()._handle_coordinator_update()
