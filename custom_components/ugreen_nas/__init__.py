import logging
from datetime import timedelta
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.device_registry import async_get as async_get_device_registry

from .const import DOMAIN, PLATFORMS
from .api import UGREEN_STATIC_BUTTON_ENDPOINTS, UgreenApiClient, UGREEN_STATIC_SENSOR_ENDPOINTS

_LOGGER = logging.getLogger(__name__)        

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    _LOGGER.info("[UGREEN NAS] Setting up config entry: %s", entry.entry_id)
    hass.data.setdefault(DOMAIN, {})

    session = async_get_clientsession(hass)

    api = UgreenApiClient(
        ugreen_nas_host=entry.data["ugreen_host"],
        ugreen_nas_port=int(entry.data["ugreen_port"]),
        auth_port=int(entry.data["auth_port"]),
        username=entry.data["username"],
        password=entry.data["password"],
        use_https=entry.data.get("use_https", False),
        verify_ssl=entry.data.get("verify_ssl", False),
    )

    _LOGGER.debug("[UGREEN NAS] Attempting initial authentication...")
    if not await api.authenticate(session):
        _LOGGER.error("[UGREEN NAS] Initial login failed. Aborting setup.")
        return False

    all_sensor_endpoints = list(UGREEN_STATIC_SENSOR_ENDPOINTS)

    async def async_update_data() -> dict[str, Any]:
        try:
            _LOGGER.debug("[UGREEN NAS] Updating data from all endpoints...")
            data: dict[str, Any] = {}

            dynamic_entities = await api.get_storage_entities(session)
            if dynamic_entities:
                _LOGGER.debug("[UGREEN NAS] Retrieved %d dynamic storage entities", len(dynamic_entities))
                all_sensor_endpoints.extend(dynamic_entities)
            else:
                _LOGGER.debug("[UGREEN NAS] No dynamic storage entities found.")

            ram_entities = await api.get_ram_entities(session)
            all_sensor_endpoints.extend(ram_entities)

            hass.data[DOMAIN][entry.entry_id]["sensor_endpoints"] = all_sensor_endpoints
            _LOGGER.debug("[UGREEN NAS] Total endpoints to query: %d", len(all_sensor_endpoints))

            for endpoint in all_sensor_endpoints:
                endpoint_str = getattr(endpoint, "endpoint", str(endpoint))
                _LOGGER.debug("[UGREEN NAS] Querying endpoint: %s", endpoint_str)
                response = await api.get(session, endpoint_str)
                try:
                    if hasattr(endpoint, "path"):
                        parts = endpoint.path.split(".")
                    else:
                        _LOGGER.warning("[UGREEN NAS] Endpoint %s does not have a 'path' attribute, skipping.", getattr(endpoint, "key", str(endpoint)))
                        data[getattr(endpoint, "key", str(endpoint))] = None
                        continue

                    value: Any = response
                    for part in parts:
                        if "[" in part and "]" in part:
                            part_name, index = part[:-1].split("[")
                            if value is not None and isinstance(value, dict):
                                value_dict: dict[str, Any] = value  # type: ignore
                                value = value_dict.get(part_name, [])
                            else:
                                value = []
                            try:
                                if isinstance(value, list):
                                    value = value[int(index)]  # type: ignore
                                else:
                                    value = None
                            except (IndexError, ValueError, TypeError):
                                value = None
                        else:
                            if value is not None and isinstance(value, dict):
                                value_dict: dict[str, Any] = value  # type: ignore
                                value = value_dict.get(part)
                            else:
                                value = None
                    data[endpoint.description.key] = value
                except Exception as e:
                    _LOGGER.warning("[UGREEN NAS] Failed to extract '%s': %s", endpoint.description.key, e)
                    data[endpoint.description.key] = None

            return data

        except Exception as err:
            _LOGGER.exception("[UGREEN NAS] Exception during data update: %s", err)
            raise UpdateFailed(f"Error communicating with UGREEN NAS: {err}") from err

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="ugreen_nas",
        update_method=async_update_data,
        update_interval=timedelta(seconds=60),
    )

    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": coordinator,
        "sensor_endpoints": all_sensor_endpoints, 
        "button_endpoints": UGREEN_STATIC_BUTTON_ENDPOINTS,
        "api": api
    }

    await coordinator.async_config_entry_first_refresh()

    try:
        _LOGGER.debug("[UGREEN NAS] Registering device in registry...")
        dev_reg = async_get_device_registry(hass)
        sys_info = await api.get(session, "/ugreen/v1/sysinfo/machine/common")

        model = sys_info.get("data", {}).get("common", {}).get("model", "Unknown Model")
        hass.data[DOMAIN][entry.entry_id]["nas_model"] = model
        version = sys_info.get("data", {}).get("common", {}).get("system_version", "Unknown Version")
        name = sys_info.get("data", {}).get("common", {}).get("nas_name", "UGREEN NAS")

        dev_reg.async_get_or_create(
            config_entry_id=entry.entry_id,
            identifiers={(DOMAIN, "ugreen_nas")},
            manufacturer="UGREEN",
            name=name,
            model=model,
            sw_version=version,
        )
        _LOGGER.info("[UGREEN NAS] Device registered: Model=%s, Version=%s", model, version)

    except Exception as e:
        _LOGGER.warning("[UGREEN NAS] Could not register device info: %s", e)

    _LOGGER.debug("[UGREEN NAS] Forwarding entry setups to platforms...")
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    _LOGGER.info("[UGREEN NAS] Setup complete.")
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    _LOGGER.info("[UGREEN NAS] Unloading config entry: %s", entry.entry_id)
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
        _LOGGER.debug("[UGREEN NAS] Entry data removed from hass.data")
    return unload_ok
