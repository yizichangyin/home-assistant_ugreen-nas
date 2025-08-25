import logging
from datetime import timedelta
from typing import Any
from collections import defaultdict

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.device_registry import async_get as async_get_device_registry, CONNECTION_NETWORK_MAC

from .const import DOMAIN, PLATFORMS
from .utils import extract_value_from_path, scale_bytes_per_second
from .api import UgreenApiClient, STATIC_BUTTON_ENTITIES, STATIC_CONFIG_ENTITIES, STATIC_STATUS_ENTITIES

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

    ### Initial authentication through API.
    if not await api.authenticate(session):
        _LOGGER.error("[UGREEN NAS] Initial login failed. Aborting setup.")
        return False

    # Create global counters for dynamic entities and RAM.
    dynamic_entity_counts = await api.count_dynamic_entities(session)
    _LOGGER.debug("[UGREEN NAS] Entity counts done: %s", dynamic_entity_counts)

    ### Build list of config entities; group it to ensure single 60s API requests.
    ### Keeping it the 'long' way (no loop) for better readability.
    config_entities  = list(STATIC_CONFIG_ENTITIES)
    config_entities += await api.get_dynamic_config_entities_storage(session) or []
    config_entities += await api.get_dynamic_config_entities_mem(session) or []
    config_entities += await api.get_dynamic_config_entities_lan(session) or []
    config_entities += await api.get_dynamic_config_entities_usb(session) or []
    config_entities += await api.get_dynamic_config_entities_ups(session) or []
    config_entities_grouped_by_endpoint = defaultdict(list)
    for entity in config_entities:
        config_entities_grouped_by_endpoint[entity.endpoint].append(entity)
    _LOGGER.debug("[UGREEN NAS] List of config entities prepared.")

    ### Build list of status entities; group it to ensure single 5s API requests.
    ### Keeping it the 'long' way (no loop) for better readability.
    status_entities  = list(STATIC_STATUS_ENTITIES)
    status_entities += await api.get_dynamic_status_entities_storage() or []
    status_entities += await api.get_dynamic_status_entities_lan() or []
    status_entities += await api.get_dynamic_status_entities_fan() or []
    status_entities_grouped_by_endpoint = defaultdict(list)
    for entity in status_entities:
        status_entities_grouped_by_endpoint[entity.endpoint].append(entity)
    _LOGGER.debug("[UGREEN NAS] List of status entities prepared.")

    ### Updater for config entities (called every 60s by the config coordinator).
    async def update_configuration_data() -> dict[str, Any]:
        try:
            _LOGGER.debug("[UGREEN NAS] Updating configuration data...")
            endpoint_to_entities = hass.data[DOMAIN][entry.entry_id]["config_entities_grouped_by_endpoint"]
            return await get_entity_data_from_api(api, session, endpoint_to_entities)
        except Exception as err:
            raise UpdateFailed(f"[UGREEN NAS] Configuration entities update error: {err}") from err

    ### Updater for status entities (called every 5s by the status coordinator).
    async def update_status_data() -> dict[str, Any]:
        try:
            _LOGGER.debug("[UGREEN NAS] Updating status data...")
            endpoint_to_entities = hass.data[DOMAIN][entry.entry_id]["status_entities_grouped_by_endpoint"]
            return await get_entity_data_from_api(api, session, endpoint_to_entities)
        except Exception as err:
            raise UpdateFailed(f"[UGREEN NAS] Status entities update error: {err}") from err

    # Helper function to fetch data and extract values, used by both 'update_xx' functions above.
    # Put below for easier code readability (grrr, looks unusual to have it called before defined).
    async def get_entity_data_from_api(api, session, endpoint_to_entities):
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
                    elif isinstance(path, str): # 'virtual' endpoints handling
                        if path.startswith("calculated:ram_total_size"):
                            value = sum(v for k, v in data.items() if k.startswith("RAM") and k.endswith("_size"))
                        elif path.startswith("calculated:scale_bytes_per_second:"):
                            value = scale_bytes_per_second(extract_value_from_path(response, path.split(":", 2)[2]))
                        else:
                            value = None # fallback for unknown 'calculated' identifiers
                    data[entity.description.key] = value
                except Exception as e:
                    _LOGGER.warning("[UGREEN NAS] Failed to extract '%s': %s", entity.description.key, e)
                    data[entity.description.key] = None
        return data

    ### Create update coordinator for config entities.
    config_coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="ugreen_configuration",
        update_method=update_configuration_data,
        update_interval=timedelta(seconds=60),
    )

    ### Create update coordinator for status entities.
    status_coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="ugreen_status",
        update_method=update_status_data,
        update_interval=timedelta(seconds=entry.options.get("status_interval", 5)),
    )

    ### Hand over all runtime objects to HA's data container.
    hass.data[DOMAIN][entry.entry_id] = {
        "config_coordinator": config_coordinator,
        "config_entities": config_entities,
        "config_entities_grouped_by_endpoint": config_entities_grouped_by_endpoint,

        "status_coordinator": status_coordinator,
        "status_entities": status_entities,
        "status_entities_grouped_by_endpoint": status_entities_grouped_by_endpoint,

        "button_entities": STATIC_BUTTON_ENTITIES,

        "dynamic_entity_counts": dynamic_entity_counts,
        "api": api,
    }

    ### Initial refresh through coordinators.
    await config_coordinator.async_config_entry_first_refresh()
    await status_coordinator.async_config_entry_first_refresh()

    ### Device registration - identify through serial # and MAC addresses (fallback).
    ### These will be added on-the-fly, no re-registration of the NAS after update needed.
    try:
        dev_reg = async_get_device_registry(hass)
        sys_info = await api.get(session, "/ugreen/v1/sysinfo/machine/common")

        common  = (sys_info or {}).get("data", {}).get("common", {})
        model   = common.get("model", "Unknown")
        version = common.get("system_version", "Unknown")
        name    = common.get("nas_name", "UGREEN NAS")
        serial  = (common.get("serial") or "").strip()
        macs    = common.get("mac") or []

        # Unique device identifiers - serial# (main identifier, if available)
        identifiers = {(DOMAIN, "ugreen_nas"), (DOMAIN, "ugreen")}
        if serial:
            identifiers.add((DOMAIN, f"serial:{serial}"))

        # Unique device identifiers - MAC's (lowercase; fallback if no serial #)
        connections = {(CONNECTION_NETWORK_MAC, m.lower()) for m in macs if isinstance(m, str) and m}

        dev_reg.async_get_or_create(
            config_entry_id=entry.entry_id,
            identifiers=identifiers,
            connections=connections,
            manufacturer="UGREEN",
            name=name,
            model=model,
            sw_version=version,
            serial_number=serial or None,
        )
        _LOGGER.info("[UGREEN NAS] Device registered: Model=%s, Version=%s", model, version)

        # Make 'model' available for sensor.py and button.py for displaying on child devices.
        hass.data[DOMAIN][entry.entry_id]["nas_model"] = model

    except Exception as e:
        _LOGGER.warning("[UGREEN NAS] Device registration failed: %s", e)

    # A final step, and initialization / startup is done.
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    _LOGGER.debug("[UGREEN NAS] Forwarded entry setups to platforms - setup complete.")

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unload_ok
