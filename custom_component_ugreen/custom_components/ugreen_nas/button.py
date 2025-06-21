import logging
import aiohttp
from homeassistant.components.button import ButtonEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .api import UgreenButtonAPIEndpoint, UgreenApiClient
from .device_info import build_device_info

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback
) -> None:
    """Set up UGREEN NAS buttons based on a config entry."""
    coordinator: DataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    endpoints: list[UgreenButtonAPIEndpoint] = hass.data[DOMAIN][entry.entry_id]["button_endpoints"]
    api = hass.data[DOMAIN][entry.entry_id]["api"]
    entities = [
        UgreenNasButton(entry.entry_id, coordinator, api, endpoint)
        for endpoint in endpoints
    ]

    async_add_entities(entities)

class UgreenNasButton(CoordinatorEntity, ButtonEntity):
    """Representation of a UGREEN NAS button."""
    def __init__(self, entry_id: str, coordinator: DataUpdateCoordinator, api: UgreenApiClient, endpoint: UgreenButtonAPIEndpoint) -> None:
        super().__init__(coordinator)
        self._entry_id = entry_id
        self._endpoint = endpoint
        self._key = endpoint.key
        self._api = api

        self._attr_name = f"UGREEN NAS {endpoint.name}"
        self._attr_unique_id = f"{entry_id}_{self._key}"
        self._attr_icon = endpoint.icon or "mdi:server"
        self._attr_device_info = build_device_info(self._key)

    async def async_press(self) -> None:
        """Perform the button action."""
        try:
            async with aiohttp.ClientSession() as session:
                await self._api.authenticate(session)

                method = self._endpoint.request_method.upper()
                path = self._endpoint.path

                if method == "POST":
                    await self._api.post(session, path)
                elif method == "GET":
                    await self._api.get(session, path)
                else:
                    _LOGGER.warning("Unsupported method: %s", method)

        except Exception as e:
            _LOGGER.error("Error pressing button %s: %s", self._key, e)

    def _handle_coordinator_update(self) -> None:
        """Update the sensor value from the coordinator."""
        super()._handle_coordinator_update()
