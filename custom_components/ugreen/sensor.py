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

        base_device_info = build_device_info(self._key, nas_model)

        if "disk" in self._key and "brand" in self._key:
            base_device_info["manufacturer"] = str(self.coordinator.data.get(self._key))
            
        if "disk" in self._key and "model" in self._key:
            base_device_info["model"] = str(self.coordinator.data.get(self._key))
        
        self._attr_device_info = base_device_info

    @property
    def native_value(self) -> StateType | date | datetime | Decimal: # type: ignore
        """Return the formatted value of the sensor."""
        raw = self.coordinator.data.get(self._key)
        return format_sensor_value(raw, self._endpoint)

    # ----
    @property
    def extra_state_attributes(self):
        base_attrs = super().extra_state_attributes or {}
        base_attrs.update({
            # for filtering purpose / multiple NAS: marker for all UGreen NAS sensors
            "device_type": "UGreen NAS",
            # reserved for later extension: marker for a specific UGreen NAS
            "device_id": "",
            # for filtering purpose: marker for similar sensors of the same 'group'
            "entity_category": self._endpoint.entity_category,
        })
        return base_attrs

    # pls delete before approval --------------------------------------------------------------
    #
    # @dobby: Above to be used for dashboard filtering (and more). The idea is to replace the fixed
    # 'UGreen_NAS_' in each sensor name in the future with a unique id (which also can be found
    # in "device_id"), which could be e.g. the device name or a user-defined string to be entered
    # during config_flow. That way you can have as many NAS as you want in the integration,
    # with the same 'core' sensor names, but still can distinguish in between them.
    #
    # With above attributes you can (mainly meant for visualization / Lovelace / auto_entities):
    # - get all entities of ALL UGreen NAS in the network (filter for device_type attribute)
    # - get all 'hardware' related entities of ANY NAS in the network
    # - get all 'hardware' related entities of a specific NAS only
    #
    # Thanks for approving, I'm currently preparing a corresponding dashboard in parallel. :)
    #
    # p.s. We will also need to adjust workflow to use MAC or device_id instead of IP,
    # because the current config_flow will not work in DHCP environments with flexible IP's
    # (currently it's IP fixed - as soon as you get a new DHCP IP, you'll need add the NAS again).
    #
    # ------------------------------------------------------------------------------------------

    def _handle_coordinator_update(self) -> None:
        """Update the sensor value from the coordinator."""
        self._attr_native_value = self.native_value
        super()._handle_coordinator_update()
