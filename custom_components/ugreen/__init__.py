import logging
from datetime import timedelta
from typing import Any
from collections import defaultdict

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

            # Build the list of entities (dynamic + static)
            all_sensor_endpoints = list(UGREEN_STATIC_SENSOR_ENDPOINTS)

            dynamic_storage_entities = await api.get_storage_entities(session)
            if dynamic_storage_entities:
                _LOGGER.debug("[UGREEN NAS] Retrieved %d dynamic storage entities", len(dynamic_storage_entities))
                all_sensor_endpoints.extend(dynamic_storage_entities)
            else:
                _LOGGER.debug("[UGREEN NAS] No dynamic storage entities found.")

            dynamic_fan_entities = await api.get_fan_entities(session)
            if dynamic_fan_entities:
                _LOGGER.debug("[UGREEN NAS] Retrieved %d dynamic fan entities", len(dynamic_fan_entities))
                all_sensor_endpoints.extend(dynamic_fan_entities)
            else:
                _LOGGER.debug("[UGREEN NAS] No dynamic fan entities found.")

            dynamic_mem_entities = await api.get_mem_entities(session)
            if dynamic_mem_entities:
                _LOGGER.debug("[UGREEN NAS] Retrieved %d dynamic mem entities", len(dynamic_mem_entities))
                all_sensor_endpoints.extend(dynamic_mem_entities)
            else:
                _LOGGER.debug("[UGREEN NAS] No dynamic mem entities found.")

            dynamic_lan_entities = await api.get_lan_entities(session)
            if dynamic_lan_entities:
                _LOGGER.debug("[UGREEN NAS] Retrieved %d dynamic lan entities", len(dynamic_lan_entities))
                all_sensor_endpoints.extend(dynamic_lan_entities)
            else:
                _LOGGER.debug("[UGREEN NAS] No dynamic lan entities found.")

            dynamic_usb_slot_entities = await api.get_usb_slot_entities(session)
            if dynamic_usb_slot_entities:
                _LOGGER.debug("[UGREEN NAS] Retrieved %d dynamic usb slot entities", len(dynamic_usb_slot_entities))
                all_sensor_endpoints.extend(dynamic_usb_slot_entities)
            else:
                _LOGGER.debug("[UGREEN NAS] No dynamic usb slot entities found.")

            hass.data[DOMAIN][entry.entry_id]["sensor_endpoints"] = all_sensor_endpoints
            _LOGGER.debug("[UGREEN NAS] Total endpoints to query: %d", len(all_sensor_endpoints))

            # Group entities by endpoint to optimize API calls
            endpoint_to_entities = defaultdict(list)

            for entity in all_sensor_endpoints:
                endpoint_to_entities[entity.endpoint].append(entity)

            for endpoint_str, entities in endpoint_to_entities.items():
                _LOGGER.debug("[UGREEN NAS] Querying endpoint: %s", endpoint_str)
                response = await api.get(session, endpoint_str)
                for entity in entities:
                    try:
                        if hasattr(entity, "path"):
                            parts = entity.path.split(".")
                        else:
                            _LOGGER.warning("[UGREEN NAS] Entity %s does not have a 'path' attribute, skipping.", getattr(entity, "key", str(entity)))
                            data[getattr(entity, "key", str(entity))] = None
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
                        data[entity.description.key] = value
                    except Exception as e:
                        _LOGGER.warning("[UGREEN NAS] Failed to extract '%s': %s", entity.description.key, e)
                        data[entity.description.key] = None

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
