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
from .utils import extract_value_from_path, scale_bytes_per_second
from .api import (
    UgreenApiClient,
    UGREEN_STATIC_BUTTON_ENDPOINTS,
    UGREEN_STATIC_CONFIGURATION_ENDPOINTS,
    UGREEN_STATIC_STATUS_ENDPOINTS,
)

_LOGGER = logging.getLogger(__name__)
_ENTITY_COUNTS: dict[str, Any] = {}


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

    if not await api.authenticate(session):
        _LOGGER.error("[UGREEN NAS] Initial login failed. Aborting setup.")
        return False

    ### Build the list of configuration entities
    all_configuration_endpoints = list(UGREEN_STATIC_CONFIGURATION_ENDPOINTS)
    all_configuration_endpoints += (await api.get_configuration_storage_entities(session)) or []
    all_configuration_endpoints += (await api.get_configuration_fan_entities(session)) or []
    all_configuration_endpoints += (await api.get_configuration_lan_entities(session)) or []
    all_configuration_endpoints += (await api.get_configuration_usb_entities(session)) or []
    dynamic_mem_entities = (await api.get_configuration_mem_entities(session)) or []
    _ENTITY_COUNTS["ram_count"] = len(dynamic_mem_entities)
    all_configuration_endpoints += dynamic_mem_entities
    # Group endpoints to make sure only one request per request type per minute
    endpoint_to_configuration_entities = defaultdict(list)
    for entity in all_configuration_endpoints:
        endpoint_to_configuration_entities[entity.endpoint].append(entity)
    _LOGGER.debug("[UGREEN NAS] Configuration endpoints ready.")

    ### Build the list of status entities
    all_status_endpoints = list(UGREEN_STATIC_STATUS_ENDPOINTS)
    all_status_endpoints += (await api.get_disk_status_entities()) or []
    # Group endpoints to make sure only one request per request type every 5 seconds
    endpoint_to_status_entities = defaultdict(list)
    for entity in all_status_endpoints:
        endpoint_to_status_entities[entity.endpoint].append(entity)
    _LOGGER.debug("[UGREEN NAS] Status endpoints ready.")


    ### Helper function to fetch data from endpoints and extract values, used by update_xx_data
    async def collect_entity_values(api, session, endpoint_to_entities):
        data: dict[str, Any] = {}

        for endpoint_str, entities in endpoint_to_entities.items():
            try:
                response = await api.get(session, endpoint_str)
            except Exception as e:
                _LOGGER.warning("[UGREEN NAS] Failed to fetch '%s': %s", endpoint_str, e)
                for entity in entities:
                    data[entity.description.key] = None
                continue

            for entity in entities:
                try:
                    path = getattr(entity, "path", None)
                    if isinstance(path, str) and not path.startswith("calculated:"):
                        value = extract_value_from_path(response, path)
                    elif isinstance(path, str):
                        if path.startswith("calculated:ram_total_size"):
                            ram_count = _ENTITY_COUNTS.get("ram_count", 0)
                            value = sum(data.get(f"RAM{index}_size", 0) for index in range(ram_count))
                        elif path.startswith("calculated:scale_bytes_per_second:"):
                            key_to_scale = path.split(":", 2)[2]
                            raw = extract_value_from_path(response, key_to_scale)
                            value = scale_bytes_per_second(raw)
                        else:
                            value = None
                    data[entity.description.key] = value

                except Exception as e:
                    _LOGGER.warning("[UGREEN NAS] Failed to extract '%s': %s", entity.description.key, e)
                    data[entity.description.key] = None

        return data

    ### The actual update function for configuration entities (called every 60s by the coordinator).
    ### It utilizes collect_entity_values above to avoid redundant code.
    async def update_configuration_data() -> dict[str, Any]:
        try:
            _LOGGER.debug("[UGREEN NAS] Updating configuration data...")
            data: dict[str, Any] = {}
            configuration_endpoints = hass.data[DOMAIN][entry.entry_id]["configuration_endpoints"]
            endpoint_to_entities = hass.data[DOMAIN][entry.entry_id]["endpoint_to_configuration_entities"]
            data = await collect_entity_values(api, session, endpoint_to_entities)
            return data
        except Exception as err:
            raise UpdateFailed(f"[UGREEN NAS] Configuration entities update error: {err}") from err

    ### The actual update function for status entities (called every 5s by the coordinator).
    ### It utilizes collect_entity_values above to avoid redundant code.
    async def update_status_data() -> dict[str, Any]:
        try:
            _LOGGER.debug("[UGREEN NAS] Updating status data...")
            data: dict[str, Any] = {}
            all_status_endpoints = hass.data[DOMAIN][entry.entry_id]["status_endpoints"]
            endpoint_to_entities = hass.data[DOMAIN][entry.entry_id]["endpoint_to_status_entities"]
            data = await collect_entity_values(api, session, endpoint_to_entities)
            return data
        except Exception as err:
            raise UpdateFailed(f"[UGREEN NAS] Status entities update error: {err}") from err

    ### The coordinator for the configuration entities.
    configuration_coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="ugreen_configuration",
        update_method=update_configuration_data,
        update_interval=timedelta(seconds=60),
    )

    ### The coordinator for the status entities.
    status_coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="ugreen_status",
        update_method=update_status_data,
        update_interval=timedelta(seconds=entry.options.get("status_interval", 5)),
    )

    ### Hand over all runtime objects to HA's data container.
    hass.data[DOMAIN][entry.entry_id] = {
        "configuration_coordinator": configuration_coordinator,
        "configuration_endpoints": all_configuration_endpoints,
        "endpoint_to_configuration_entities": endpoint_to_configuration_entities,
        "status_coordinator": status_coordinator,
        "status_endpoints": all_status_endpoints,
        "endpoint_to_status_entities": endpoint_to_status_entities,
        "button_endpoints": UGREEN_STATIC_BUTTON_ENDPOINTS,
        "api": api
    }

    ### Initial refresh.
    await configuration_coordinator.async_config_entry_first_refresh()
    await status_coordinator.async_config_entry_first_refresh()

    ### Device registration.
    try:
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
        _LOGGER.warning("[UGREEN NAS] Device registration failed: %s", e)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    _LOGGER.debug("[UGREEN NAS] Forwarded entry setups to platforms - setup complete.")

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unload_ok
