from dataclasses import dataclass
import logging
import aiohttp
import async_timeout
from typing import List, Any
from homeassistant.helpers.entity import EntityDescription
from homeassistant.const import (
    PERCENTAGE,
    REVOLUTIONS_PER_MINUTE,
    UnitOfDataRate,
    UnitOfTemperature,
    UnitOfInformation,
    UnitOfTime,
    UnitOfFrequency
)

_LOGGER = logging.getLogger(__name__)

@dataclass
class UgreenEntity:
    description: EntityDescription
    endpoint: str
    path: str
    request_method: str = "GET"
    decimal_places: int = 2
    entity_category: str = ""

UGREEN_STATIC_SENSOR_ENDPOINTS: List[UgreenEntity] = [
    # Hardware Info
    UgreenEntity(
        description=EntityDescription(
            key="cpu_model",
            name="CPU Model",
            icon="mdi:chip",
            unit_of_measurement=None,
        ),
        endpoint="/ugreen/v1/sysinfo/machine/common",
        path="data.hardware.cpu[0].model",
        entity_category="Hardware",
    ),
    UgreenEntity(
        description=EntityDescription(
            key="cpu_ghz",
            name="CPU Frequency",
            icon="mdi:speedometer",
            unit_of_measurement=UnitOfFrequency.MEGAHERTZ,
        ),
        endpoint="/ugreen/v1/sysinfo/machine/common",
        path="data.hardware.cpu[0].ghz",
        decimal_places=0,
        entity_category="Hardware",
    ),
    UgreenEntity(
        description=EntityDescription(
            key="cpu_core",
            name="CPU Cores",
            icon="mdi:chip",
            unit_of_measurement="Cores",
        ),
        endpoint="/ugreen/v1/sysinfo/machine/common",
        path="data.hardware.cpu[0].core",
        decimal_places=0,
        entity_category="Hardware",
    ),
    UgreenEntity(
        description=EntityDescription(
            key="cpu_thread",
            name="CPU Threads",
            icon="mdi:chip",
            unit_of_measurement="Threads",
        ),
        endpoint="/ugreen/v1/sysinfo/machine/common",
        path="data.hardware.cpu[0].thread",
        decimal_places=0,
        entity_category="Hardware",
    ),
    
    # UPS
    UgreenEntity(
        description=EntityDescription(
            key="ups_model",
            name="UPS Model",
            icon="mdi:power-plug-battery",
            unit_of_measurement=None,
        ),
        endpoint="/ugreen/v1/sysinfo/machine/common",
        path="data.hardware.ups[0].model",
        entity_category="Hardware",
    ),
    UgreenEntity(
        description=EntityDescription(
            key="ups_vendor",
            name="UPS Vendor",
            icon="mdi:power-plug-battery",
            unit_of_measurement=None,
        ),
        endpoint="/ugreen/v1/sysinfo/machine/common",
        path="data.hardware.ups[0].vendor",
        entity_category="Hardware",
    ),
    UgreenEntity(
        description=EntityDescription(
            key="ups_power_free",
            name="UPS Power Remaining",
            icon="mdi:power-plug-battery",
            unit_of_measurement=PERCENTAGE,
        ),
        endpoint="/ugreen/v1/sysinfo/machine/common",
        path="data.hardware.ups[0].power_free",
        entity_category="Hardware",
    ),
    
    # Device Monitoring
     UgreenEntity(
        description=EntityDescription(
            key="cpu_usage",
            name="CPU Usage",
            icon="mdi:chip",
            unit_of_measurement=PERCENTAGE,
        ),
        endpoint="/ugreen/v1/desktop/components/data?id=desktop.component.DeviceMonitoring",
        path="data.cpu_usage_rate",
        entity_category="Status",
    ),
    UgreenEntity(
        description=EntityDescription(
            key="ram_size_total",
            name="RAM Size (Total)",
            icon="mdi:memory",
            unit_of_measurement=UnitOfInformation.GIGABYTES,
        ),
        endpoint="/ugreen/v1/taskmgr/stat/get_all",
        path="data.mem.structure.total",
        entity_category="Hardware",
    ),
    UgreenEntity(
        description=EntityDescription(
            key="ram_size_free",
            name="RAM Size (Free)",
            icon="mdi:memory",
            unit_of_measurement=UnitOfInformation.GIGABYTES,
        ),
        endpoint="/ugreen/v1/taskmgr/stat/get_all",
        path="data.mem.structure.free",
        entity_category="Status",
    ),
    UgreenEntity(
        description=EntityDescription(
            key="ram_size_cache",
            name="RAM Size (Cache)",
            icon="mdi:memory",
            unit_of_measurement=UnitOfInformation.GIGABYTES,
        ),
        endpoint="/ugreen/v1/taskmgr/stat/get_all",
        path="data.mem.structure.cache",
        entity_category="Status",
    ),
    UgreenEntity(
        description=EntityDescription(
            key="ram_size_used",
            name="RAM Size (Usage - Gigabytes)",
            icon="mdi:memory",
            unit_of_measurement=UnitOfInformation.GIGABYTES,
        ),
        endpoint="/ugreen/v1/taskmgr/stat/get_all",
        path="data.mem.structure.used",
        entity_category="Status",
    ),
    UgreenEntity(
        description=EntityDescription(
            key="ram_usage",
            name="RAM Size (Usage - Percentage)",
            icon="mdi:memory",
            unit_of_measurement=PERCENTAGE,
        ),
        endpoint="/ugreen/v1/desktop/components/data?id=desktop.component.DeviceMonitoring",
        path="data.ram_usage_rate",
        entity_category="Status",
    ),
    UgreenEntity(
        description=EntityDescription(
            key="upload_speed",
            name="Upload Speed",
            icon="mdi:upload",
            unit_of_measurement=UnitOfDataRate.MEGABITS_PER_SECOND,
        ),
        endpoint="/ugreen/v1/desktop/components/data?id=desktop.component.DeviceMonitoring",
        path="data.upload_speed.value",
        entity_category="Status",
    ),
    UgreenEntity(
        description=EntityDescription(
            key="download_speed",
            name="Download Speed",
            icon="mdi:download",
            unit_of_measurement=UnitOfDataRate.MEGABITS_PER_SECOND,
        ),
        endpoint="/ugreen/v1/desktop/components/data?id=desktop.component.DeviceMonitoring",
        path="data.download_speed.value",
        entity_category="Status",
    ),

    # System Status
        UgreenEntity(
        description=EntityDescription(
            key="last_boot_date",
            name="Last Boot",
            icon="mdi:calendar",
            unit_of_measurement=None,
        ),
        endpoint="/ugreen/v1/desktop/components/data?id=desktop.component.SystemStatus",
        path="data.last_boot_date",
        entity_category="Status",
    ),
    UgreenEntity(
        description=EntityDescription(
            key="last_boot_time",
            name="Last Boot Timestamp",
            icon="mdi:clock",
            unit_of_measurement=None,
        ),
        endpoint="/ugreen/v1/desktop/components/data?id=desktop.component.SystemStatus",
        path="data.last_boot_time",
        entity_category="Status",
    ),
    UgreenEntity(
        description=EntityDescription(
            key="message",
            name="System Message",
            icon="mdi:message",
            unit_of_measurement=None,
        ),
        endpoint="/ugreen/v1/desktop/components/data?id=desktop.component.SystemStatus",
        path="data.message",
        entity_category="Status",
    ),
    UgreenEntity(
        description=EntityDescription(
            key="server_status",
            name="Server Status",
            icon="mdi:server",
            unit_of_measurement=None,
        ),
        endpoint="/ugreen/v1/desktop/components/data?id=desktop.component.SystemStatus",
        path="data.server_status",
        entity_category="Status",
    ),
    UgreenEntity(
        description=EntityDescription(
            key="status",
            name="System Status Code",
            icon="mdi:information",
            unit_of_measurement=None,
        ),
        endpoint="/ugreen/v1/desktop/components/data?id=desktop.component.SystemStatus",
        path="data.status",
        entity_category="Status",
    ),
    UgreenEntity(
        description=EntityDescription(
            key="total_run_time",
            name="Total Runtime",
            icon="mdi:timer-outline",
            unit_of_measurement=UnitOfTime.SECONDS,
        ),
        endpoint="/ugreen/v1/desktop/components/data?id=desktop.component.SystemStatus",
        path="data.total_run_time",
        entity_category="Status",
    ),
    UgreenEntity(
        description=EntityDescription(
            key="device_name",
            name="Device Name",
            icon="mdi:nas",
            unit_of_measurement=None,
        ),
        endpoint="/ugreen/v1/desktop/components/data?id=desktop.component.SystemStatus",
        path="data.dev_name",
        entity_category="Device",
    ),

    # Temperature Monitoring
     UgreenEntity(
        description=EntityDescription(
            key="cpu_temperature",
            name="CPU Temperature",
            icon="mdi:thermometer",
            unit_of_measurement=UnitOfTemperature.CELSIUS,
        ),
        endpoint="/ugreen/v1/desktop/components/data?id=desktop.component.TemperatureMonitoring",
        path="data.cpu_temperature",
        entity_category="Status",
    ),
    UgreenEntity(
        description=EntityDescription(
            key="cpu_status",
            name="CPU Temperature Status",
            icon="mdi:alert",
            unit_of_measurement=None,
        ),
        endpoint="/ugreen/v1/desktop/components/data?id=desktop.component.TemperatureMonitoring",
        path="data.cpu_status",
        entity_category="Status",
    ),
    UgreenEntity(
        description=EntityDescription(
            key="fan_speed_overall",
            name="Fan Speed (Overall)",
            icon="mdi:fan",
            unit_of_measurement=REVOLUTIONS_PER_MINUTE,
        ),
        endpoint="/ugreen/v1/desktop/components/data?id=desktop.component.TemperatureMonitoring",
        path="data.fan_speed",
        entity_category="Status",
    ),
    UgreenEntity(
        description=EntityDescription(
            key="fan_status_overall",
            name="Fan Status (Overall)",
            icon="mdi:fan-alert",
            unit_of_measurement=None,
        ),
        endpoint="/ugreen/v1/desktop/components/data?id=desktop.component.TemperatureMonitoring",
        path="data.fan_status",
        entity_category="Status",
    ),
    UgreenEntity(
        description=EntityDescription(
            key="temperature_message",
            name="Temperature Message",
            icon="mdi:message-alert",
            unit_of_measurement=None,
        ),
        endpoint="/ugreen/v1/desktop/components/data?id=desktop.component.TemperatureMonitoring",
        path="data.message",
        entity_category="Status",
    ),
    UgreenEntity(
        description=EntityDescription(
            key="temperature_status",
            name="Temperature Status Code",
            icon="mdi:information",
            unit_of_measurement=None,
        ),
        endpoint="/ugreen/v1/desktop/components/data?id=desktop.component.TemperatureMonitoring",
        path="data.status",
        entity_category="Status",
    ),
]

UGREEN_STATIC_BUTTON_ENDPOINTS: List[UgreenEntity] = [
    # System Actions
    UgreenEntity(
        description=EntityDescription(
            key="shutdown",
            name="Shutdown",
            icon="mdi:power",
        ),
        endpoint="/ugreen/v1/desktop/shutdown",
        path="",
        request_method="POST",
        entity_category="",
    ),
    UgreenEntity(
        description=EntityDescription(
            key="reboot",
            name="Reboot",
            icon="mdi:restart",
        ),
        endpoint="/ugreen/v1/desktop/reboot",
        path="",
        request_method="POST",
        entity_category="",
    ),
]

class UgreenApiClient:
    def __init__(
        self,
        ugreen_nas_host: str,
        ugreen_nas_port: int,
        auth_port: int,
        username: str = "",
        password: str = "",
        token: str = "",
        use_https: bool = False,
        verify_ssl: bool = True,                               
    ):
        protocol = "https" if use_https else "http"
        self.base_url = f"{protocol}://{ugreen_nas_host}:{ugreen_nas_port}"
        self.token_url = f"http://{ugreen_nas_host}:{auth_port}"
        self.username = username
        self.password = password
        self.token = token
        self.verify_ssl = verify_ssl

    async def authenticate(self, session: aiohttp.ClientSession) -> bool:
        """Login and fetch new token."""
        url = f"{self.token_url}/token?username={self.username}&password={self.password}"
        
        _LOGGER.debug("[UGREEN NAS] Sending authentication GET to: %s", url)
        try:
            async with session.get(url, ssl=self.verify_ssl) as resp:
                resp.raise_for_status()
                data = await resp.json()
                _LOGGER.debug("[UGREEN NAS] Authentication response: %s", data)

                if data.get("code") != 200:
                    _LOGGER.warning("[UGREEN NAS] Authentication failed with code: %s", data.get("code"))
                    return False

                token = data.get("data", {}).get("token")
                if not token:
                    _LOGGER.error("[UGREEN NAS] Login succeeded but token not found in response")
                    return False

                self.token = token
                _LOGGER.info("[UGREEN NAS] Token received and stored")
                return True

        except Exception as e:
            _LOGGER.exception("[UGREEN NAS] Authentication request failed: %s", e)
            return False
        
    async def get(self, session: aiohttp.ClientSession, endpoint: str) -> dict[str, Any]:
        """Perform GET with retry on token expiration (code 1024)."""
        async def _do_get() -> dict[str, Any]:
            url = f"{self.base_url}{endpoint}"
            delimiter = "&" if "?" in url else "?"
            url += f"{delimiter}token={self.token}"
            _LOGGER.debug("[UGREEN NAS] Sending GET request to: %s", url)
            async with async_timeout.timeout(10):
                async with session.get(url, ssl=self.verify_ssl) as resp:
                    resp.raise_for_status()
                    data = await resp.json()
                    return data
        try:
            data = await _do_get()
            if data.get("code") == 1024:
                _LOGGER.warning("[UGREEN NAS] Token expired (code 1024), refreshing...")
                if await self.authenticate(session):
                    data = await _do_get()
                else:
                    _LOGGER.error("[UGREEN NAS] Token refresh failed")
                    return {}
            return data
        except Exception as e:
            _LOGGER.error("[UGREEN NAS] GET request to %s failed: %s", endpoint, e)
            return {}
        
    async def post(self, session: aiohttp.ClientSession, endpoint: str, payload: dict[str, Any] = {}) -> dict[str, Any]:
        """Perform POST request (formerly GET) with optional payload and retry on token expiration (code 1024)."""
        async def _do_post() -> dict[str, Any]:
            url = f"{self.base_url}{endpoint}"
            delimiter = "&" if "?" in url else "?"
            url += f"{delimiter}token={self.token}"
            _LOGGER.debug("[UGREEN NAS] Sending POST request to: %s with payload: %s", url, payload)
            async with async_timeout.timeout(10):
                async with session.post(url, json=payload, ssl=self.verify_ssl) as resp:
                    resp.raise_for_status()
                    data = await resp.json()
                    return data

        try:
            data = await _do_post()
            if data.get("code") == 1024:
                _LOGGER.warning("[UGREEN NAS] Token expired (code 1024), refreshing...")
                if await self.authenticate(session):
                    data = await _do_post()
                else:
                    _LOGGER.error("[UGREEN NAS] Token refresh failed during POST")
                    return {}
            return data

        except Exception as e:
            _LOGGER.error("[UGREEN NAS] POST request to %s failed: %s", endpoint, e)
            return {}

    async def get_fan_entities(self, session: aiohttp.ClientSession) -> List[UgreenEntity]:
        """Fetch and build dynamic fan entities."""
        endpoint = "/ugreen/v1/desktop/components/data?id=desktop.component.TemperatureMonitoring"
        _LOGGER.debug("[UGREEN NAS] Fetching dynamic fan entities from %s", endpoint)
        data = await self.get(session, endpoint)

        if not data:
            _LOGGER.warning("[UGREEN NAS] No data received from %s", endpoint)
            return []

        fan_list = data.get("data", {}).get("fan_list", [])
        if not fan_list:
            _LOGGER.warning("[UGREEN NAS] 'fan_list' field is missing or empty in response from %s", endpoint)
            return []

        entities: List[UgreenEntity] = []

        try:
            for fan_index, _ in enumerate(fan_list):
                prefix_fan_key = f"fan{"" if len(fan_list) <= 1 else fan_index + 1}"
                prefix_fan_name = f"Fan" if len(fan_list) <= 1 else f"Fan {fan_index + 1}"
                _LOGGER.debug("[UGREEN NAS] Processing fan entity: %s", prefix_fan_key)

                entities.extend([
                    UgreenEntity(
                        description=EntityDescription(
                            key=f"{prefix_fan_key}_speed",
                            name=f"{prefix_fan_name} Speed",
                            icon="mdi:fan",
                            unit_of_measurement=REVOLUTIONS_PER_MINUTE,
                        ),
                        endpoint=endpoint,
                        path=f"data.fan_list[{fan_index}].speed",
                        decimal_places=0,
                        entity_category="Status",
                    ),
                    UgreenEntity(
                        description=EntityDescription(
                            key=f"{prefix_fan_key}_status",
                            name=f"{prefix_fan_name} Status",
                            icon="mdi:fan-alert",
                            unit_of_measurement=None,
                        ),
                        endpoint=endpoint,
                        path=f"data.fan_list[{fan_index}].status",
                        entity_category="Status",
                    ),
                ])
                
        except Exception as e:
            _LOGGER.error("[UGREEN NAS] Error while building dynamic fan entities: %s", e)

        return entities
    
    async def get_mem_entities(self, session: aiohttp.ClientSession) -> List[UgreenEntity]:
        """Fetch and build dynamic mem entities."""
        endpoint = "/ugreen/v1/sysinfo/machine/common"
        _LOGGER.debug("[UGREEN NAS] Fetching dynamic mem entities from %s", endpoint)
        data = await self.get(session, endpoint)

        if not data:
            _LOGGER.warning("[UGREEN NAS] No data received from %s", endpoint)
            return []

        hardware = data.get("data", {}).get("hardware", {})
        if not hardware:
            _LOGGER.warning("[UGREEN NAS] 'hardware' field is missing or empty in response from %s", endpoint)
            return []
        
        mem_list = data.get("data", {}).get("hardware", {}).get("mem", [])
        if not mem_list:
            _LOGGER.warning("[UGREEN NAS] 'mem' field is missing or empty in response from %s", endpoint)
            return []

        entities: List[UgreenEntity] = []

        try:
            for mem_index, _ in enumerate(mem_list):
                prefix_mem_key = f"RAM{"" if len(mem_list) <= 1 else mem_index + 1}"
                prefix_mem_name = f"RAM" if len(mem_list) <= 1 else f"RAM {mem_index + 1}"
                _LOGGER.debug("[UGREEN NAS] Processing mem entity: %s", prefix_mem_key)

                entities.extend([
                    UgreenEntity(
                        description=EntityDescription(
                            key=f"{prefix_mem_key}_model",
                            name=f"{prefix_mem_name} Model",
                            icon="mdi:memory",
                            unit_of_measurement=None,
                        ),
                        endpoint=endpoint,
                        path=f"data.hardware.mem[{mem_index}].model",
                        entity_category="Hardware",
                    ),
                    UgreenEntity(
                        description=EntityDescription(
                            key=f"{prefix_mem_key}_manufacturer",
                            name=f"{prefix_mem_name} Manufacturer",
                            icon="mdi:factory",
                            unit_of_measurement=None,
                        ),
                        endpoint=endpoint,
                        path=f"data.hardware.mem[{mem_index}].manufacturer",
                        entity_category="Hardware",
                    ),
                    UgreenEntity(
                        description=EntityDescription(
                            key=f"{prefix_mem_key}_size",
                            name=f"{prefix_mem_name} Size",
                            icon="mdi:memory",
                            unit_of_measurement=UnitOfInformation.GIGABYTES,
                        ),
                        endpoint=endpoint,
                        path=f"data.hardware.mem[{mem_index}].size",
                        decimal_places=0,
                        entity_category="Hardware",
                    ),
                    UgreenEntity(
                        description=EntityDescription(
                            key=f"{prefix_mem_key}_speed",
                            name=f"{prefix_mem_name} Speed",
                            icon="mdi:speedometer",
                            unit_of_measurement="MHz",
                        ),
                        endpoint=endpoint,
                        path=f"data.hardware.mem[{mem_index}].mhz",
                        decimal_places=0,
                        entity_category="Hardware",
                    ),
                ])
                
        except Exception as e:
            _LOGGER.error("[UGREEN NAS] Error while building dynamic mem entities: %s", e)

        return entities
    
    async def get_lan_entities(self, session: aiohttp.ClientSession) -> List[UgreenEntity]:
        """Fetch and build dynamic lan entities."""
        endpoint = "/ugreen/v1/sysinfo/machine/common"
        _LOGGER.debug("[UGREEN NAS] Fetching dynamic lan entities from %s", endpoint)
        data = await self.get(session, endpoint)

        if not data:
            _LOGGER.warning("[UGREEN NAS] No data received from %s", endpoint)
            return []
        
        hardware = data.get("data", {}).get("hardware", {})
        if not hardware:
            _LOGGER.warning("[UGREEN NAS] 'hardware' field is missing or empty in response from %s", endpoint)
            return []

        lan_list = data.get("data", {}).get("hardware", {}).get("net", [])
        if not lan_list:
            _LOGGER.warning("[UGREEN NAS] 'lan_list' field is missing or empty in response from %s", endpoint)
            return []

        entities: List[UgreenEntity] = []

        try:
            for lan_index, _ in enumerate(lan_list):
                prefix_lan_key = f"lan{"" if len(lan_list) <= 1 else lan_index + 1}"
                prefix_lan_name = f"lan" if len(lan_list) <= 1 else f"lan {lan_index + 1}"
                _LOGGER.debug("[UGREEN NAS] Processing lan entity: %s", prefix_lan_key)

                entities.extend([
                    UgreenEntity(
                        description=EntityDescription(
                            key=f"{prefix_lan_key}_model",
                            name=f"{prefix_lan_name} Model",
                            icon="mdi:lan",
                            unit_of_measurement=None,
                        ),
                        endpoint=endpoint,
                        path=f"data.hardware.net[{lan_index}].model",
                        entity_category="Network",
                    ),
                    UgreenEntity(
                        description=EntityDescription(
                            key=f"{prefix_lan_key}_ip",
                            name=f"{prefix_lan_name} IP",
                            icon="mdi:lan",
                            unit_of_measurement=None,
                        ),
                        endpoint=endpoint,
                        path=f"data.hardware.net[{lan_index}].ip",
                        entity_category="Network",
                    ),
                    UgreenEntity(
                        description=EntityDescription(
                            key=f"{prefix_lan_key}_mac",
                            name=f"{prefix_lan_name} MAC",
                            icon="mdi:lan",
                            unit_of_measurement=None,
                        ),
                        endpoint=endpoint,
                        path=f"data.hardware.net[{lan_index}].mac",
                        entity_category="Network",
                    ),
                    UgreenEntity(
                        description=EntityDescription(
                            key=f"{prefix_lan_key}_speed",
                            name=f"{prefix_lan_name} Speed",
                            icon="mdi:speedometer",
                            unit_of_measurement=UnitOfDataRate.MEGABITS_PER_SECOND,
                        ),
                        endpoint=endpoint,
                        path=f"data.hardware.net[{lan_index}].speed",
                        decimal_places=0,
                        entity_category="Network",
                    ),
                    UgreenEntity(
                        description=EntityDescription(
                            key=f"{prefix_lan_key}_duplex",
                            name=f"{prefix_lan_name} Duplex",
                            icon="mdi:lan",
                            unit_of_measurement=None,
                        ),
                        endpoint=endpoint,
                        path=f"data.hardware.net[{lan_index}].duplex",
                        entity_category="Network",
                    ),
                    UgreenEntity(
                        description=EntityDescription(
                            key=f"{prefix_lan_key}_mtu",
                            name=f"{prefix_lan_name} MTU",
                            icon="mdi:lan",
                            unit_of_measurement=None,
                        ),
                        endpoint=endpoint,
                        path=f"data.hardware.net[{lan_index}].mtu",
                        entity_category="Network",
                    ),
                    UgreenEntity(
                        description=EntityDescription(
                            key=f"{prefix_lan_key}_netmask",
                            name=f"{prefix_lan_name} Netmask",
                            icon="mdi:lan",
                            unit_of_measurement=None,
                        ),
                        endpoint=endpoint,
                        path=f"data.hardware.net[{lan_index}].mask",
                        entity_category="Network",
                    ),
                ])
                
        except Exception as e:
            _LOGGER.error("[UGREEN NAS] Error while building dynamic lan entities: %s", e)

        return entities
    
    async def get_usb_slot_entities(self, session: aiohttp.ClientSession) -> List[UgreenEntity]:
        """Fetch and build dynamic usb_slot entities."""
        endpoint = "/ugreen/v1/sysinfo/machine/common"
        _LOGGER.debug("[UGREEN NAS] Fetching dynamic usb_slot entities from %s", endpoint)
        data = await self.get(session, endpoint)

        if not data:
            _LOGGER.warning("[UGREEN NAS] No data received from %s", endpoint)
            return []
        
        hardware = data.get("data", {}).get("hardware", {})
        if not hardware:
            _LOGGER.warning("[UGREEN NAS] 'hardware' field is missing or empty in response from %s", endpoint)
            return []

        usb_slot_list = data.get("data", {}).get("hardware", {}).get("usb", [])
        if not usb_slot_list:
            _LOGGER.warning("[UGREEN NAS] 'usb' field is missing or empty in response from %s", endpoint)
            return []

        entities: List[UgreenEntity] = []

        try:
            for usb_slot_index, _ in enumerate(usb_slot_list):
                prefix_usb_slot_key = f"usb_slot{"" if len(usb_slot_list) <= 1 else usb_slot_index + 1}"
                prefix_usb_slot_name = f"usb_slot" if len(usb_slot_list) <= 1 else f"usb_slot {usb_slot_index + 1}"
                _LOGGER.debug("[UGREEN NAS] Processing usb_slot entity: %s", prefix_usb_slot_key)
                
                entities.extend([
                    UgreenEntity(
                        description=EntityDescription(
                            key=f"{prefix_usb_slot_key}_model",
                            name=f"{prefix_usb_slot_name} Model",
                            icon="mdi:usb-port",
                            unit_of_measurement=None,
                        ),
                        endpoint=endpoint,
                        path=f"data.hardware.usb[{usb_slot_index}].model",
                        entity_category="USB",
                    ),
                    UgreenEntity(
                        description=EntityDescription(
                            key=f"{prefix_usb_slot_key}_vendor",
                            name=f"{prefix_usb_slot_name} Vendor",
                            icon="mdi:usb-port",
                            unit_of_measurement=None,
                        ),
                        endpoint=endpoint,
                        path=f"data.hardware.usb[{usb_slot_index}].vendor",
                        entity_category="USB",
                    ),
                    UgreenEntity(
                        description=EntityDescription(
                            key=f"{prefix_usb_slot_key}_device_type",
                            name=f"{prefix_usb_slot_name} Device Type",
                            icon="mdi:usb-port",
                            unit_of_measurement=None,
                        ),
                        endpoint=endpoint,
                        path=f"data.hardware.usb[{usb_slot_index}].device_type",
                        entity_category="USB",
                    ),
            ])
                
        except Exception as e:
            _LOGGER.error("[UGREEN NAS] Error while building dynamic usb_slot entities: %s", e)

        return entities
    
    async def get_storage_entities(self, session: aiohttp.ClientSession) -> List[UgreenEntity]:
        """Fetch and build dynamic storage entities."""
        endpoint = "/ugreen/v1/storage/pool/list"
        _LOGGER.debug("[UGREEN NAS] Fetching dynamic storage entities from %s", endpoint)
        data = await self.get(session, endpoint)

        if not data:
            _LOGGER.warning("[UGREEN NAS] No data received from %s", endpoint)
            return []

        results = data.get("data", {}).get("result")
        if not results:
            _LOGGER.warning("[UGREEN NAS] 'result' field is missing or empty in response from %s", endpoint)
            return []

        entities: List[UgreenEntity] = []

        try:
            for pool_index, pool in enumerate(results):
                prefix_pool_key = f"pool{pool_index+1}"
                prefix_pool_name = f"(Pool {pool_index+1})"
                _LOGGER.debug("[UGREEN NAS] Processing pool entity: %s", prefix_pool_key)

                entities.extend([
                    UgreenEntity(
                            description=EntityDescription(
                                key=f"{prefix_pool_key}_name",
                                name=f"{prefix_pool_name} Name",
                                icon="mdi:chip",
                                unit_of_measurement=None,
                            ),
                            endpoint=endpoint,
                            path=f"data.result[{pool_index}].name",
                            entity_category="Pools",
                        ),
                        UgreenEntity(
                            description=EntityDescription(
                                key=f"{prefix_pool_key}_label",
                                name=f"{prefix_pool_name} Label",
                                icon="mdi:label",
                                unit_of_measurement=None,
                            ),
                            endpoint=endpoint,
                            path=f"data.result[{pool_index}].label",
                            entity_category="Pools",
                        ),
                        UgreenEntity(
                            description=EntityDescription(
                                key=f"{prefix_pool_key}_level",
                                name=f"{prefix_pool_name} Level",
                                icon="mdi:format-list-bulleted-type",
                                unit_of_measurement=None,
                            ),
                            endpoint=endpoint,
                            path=f"data.result[{pool_index}].level",
                            entity_category="Pools",
                        ),
                        UgreenEntity(
                            description=EntityDescription(
                                key=f"{prefix_pool_key}_status",
                                name=f"{prefix_pool_name} Status",
                                icon="mdi:check-circle-outline",
                                unit_of_measurement=None,
                            ),
                            endpoint=endpoint,
                            path=f"data.result[{pool_index}].status",
                            entity_category="Pools",
                        ),
                        UgreenEntity(
                            description=EntityDescription(
                                key=f"{prefix_pool_key}_total",
                                name=f"{prefix_pool_name} Total Size",
                                icon="mdi:database",
                                unit_of_measurement=UnitOfInformation.GIGABYTES,
                            ),
                            endpoint=endpoint,
                            path=f"data.result[{pool_index}].total",
                            entity_category="Pools",
                        ),
                        UgreenEntity(
                            description=EntityDescription(
                                key=f"{prefix_pool_key}_used",
                                name=f"{prefix_pool_name} Used Size",
                                icon="mdi:database-check",
                                unit_of_measurement=UnitOfInformation.GIGABYTES,
                            ),
                            endpoint=endpoint,
                            path=f"data.result[{pool_index}].used",
                            entity_category="Pools",
                        ),
                        UgreenEntity(
                            description=EntityDescription(
                                key=f"{prefix_pool_key}_free",
                                name=f"{prefix_pool_name} Free Size",
                                icon="mdi:database-remove",
                                unit_of_measurement=UnitOfInformation.GIGABYTES,
                            ),
                            endpoint=endpoint,
                            path=f"data.result[{pool_index}].free",
                            entity_category="Pools",
                        ),
                        UgreenEntity(
                            description=EntityDescription(
                                key=f"{prefix_pool_key}_available",
                                name=f"{prefix_pool_name} Available Size",
                                icon="mdi:database-plus",
                                unit_of_measurement=UnitOfInformation.GIGABYTES,
                            ),
                            endpoint=endpoint,
                            path=f"data.result[{pool_index}].available",
                            entity_category="Pools",
                        ),
                        UgreenEntity(
                            description=EntityDescription(
                                key=f"{prefix_pool_key}_disk_count",
                                name=f"{prefix_pool_name} Disk Count",
                                icon="mdi:harddisk",
                                unit_of_measurement=None,
                            ),
                            endpoint=endpoint,
                            path=f"data.result[{pool_index}].total_disk_num",
                            entity_category="Pools",
                        ),
                ])

                for disk_index, _ in enumerate(pool.get("disks", [])):
                    prefix_disk_key = f"disk{disk_index+1}_pool{pool_index+1}"
                    prefix_disk_name = f"(Pool {pool_index+1} | Disk {disk_index+1})"
                    endpoint_disk = f"/ugreen/v2/storage/disk/list"                    
                    _LOGGER.debug("[UGREEN NAS] Processing disk entity: %s", prefix_disk_key)

                    entities.extend([
                        UgreenEntity(
                            description=EntityDescription(
                                key=f"{prefix_disk_key}_model",
                                name=f"{prefix_disk_name} Model",
                                icon="mdi:chip",
                                unit_of_measurement=None,
                            ),
                            endpoint=endpoint_disk,
                            path=f"data.result[{disk_index}].model",
                            entity_category="Disks",
                        ),
                        UgreenEntity(
                            description=EntityDescription(
                                key=f"{prefix_disk_key}_serial",
                                name=f"{prefix_disk_name} Serial Number",
                                icon="mdi:identifier",
                                unit_of_measurement=None,
                            ),
                            endpoint=endpoint_disk,
                            path=f"data.result[{disk_index}].serial",
                            entity_category="Disks",
                        ),
                        UgreenEntity(
                            description=EntityDescription(
                                key=f"{prefix_disk_key}_size",
                                name=f"{prefix_disk_name} Size",
                                icon="mdi:database",
                                unit_of_measurement=UnitOfInformation.GIGABYTES,
                            ),
                            endpoint=endpoint_disk,
                            path=f"data.result[{disk_index}].size",
                            entity_category="Disks",
                        ),
                        UgreenEntity(
                            description=EntityDescription(
                                key=f"{prefix_disk_key}_name",
                                name=f"{prefix_disk_name} Name",
                                icon="mdi:harddisk",
                                unit_of_measurement=None,
                            ),
                            endpoint=endpoint_disk,
                            path=f"data.result[{disk_index}].name",
                            entity_category="Disks",
                        ),
                        UgreenEntity(
                            description=EntityDescription(
                                key=f"{prefix_disk_key}_dev_name",
                                name=f"{prefix_disk_name} Device Name",
                                icon="mdi:console",
                                unit_of_measurement=None,
                            ),
                            endpoint=endpoint_disk,
                            path=f"data.result[{disk_index}].dev_name",
                            entity_category="Disks",
                        ),
                        UgreenEntity(
                            description=EntityDescription(
                                key=f"{prefix_disk_key}_slot",
                                name=f"{prefix_disk_name} Slot",
                                icon="mdi:server-network",
                                unit_of_measurement=None,
                            ),
                            endpoint=endpoint_disk,
                            path=f"data.result[{disk_index}].slot",
                            entity_category="Disks",
                        ),
                        UgreenEntity(
                            description=EntityDescription(
                                key=f"{prefix_disk_key}_type",
                                name=f"{prefix_disk_name} Type",
                                icon="mdi:harddisk",
                                unit_of_measurement=None,
                            ),
                            endpoint=endpoint_disk,
                            path=f"data.result[{disk_index}].type",
                            entity_category="Disks",
                        ),
                        UgreenEntity(
                            description=EntityDescription(
                                key=f"{prefix_disk_key}_interface_type",
                                name=f"{prefix_disk_name} Interface Type",
                                icon="mdi:harddisk",
                                unit_of_measurement=None,
                            ),
                            endpoint=endpoint_disk,
                            path=f"data.result[{disk_index}].interface_type",
                            entity_category="Disks",
                        ),
                        UgreenEntity(
                            description=EntityDescription(
                                key=f"{prefix_disk_key}_label",
                                name=f"{prefix_disk_name} Label",
                                icon="mdi:label",
                                unit_of_measurement=None,
                            ),
                            endpoint=endpoint_disk,
                            path=f"data.result[{disk_index}].label",
                            entity_category="Disks",
                        ),
                        UgreenEntity(
                            description=EntityDescription(
                                key=f"{prefix_disk_key}_used_for",
                                name=f"{prefix_disk_name} Used For",
                                icon="mdi:database-marker",
                                unit_of_measurement=None,
                            ),
                            endpoint=endpoint_disk,
                            path=f"data.result[{disk_index}].used_for",
                            entity_category="Disks",
                        ),
                        UgreenEntity(
                            description=EntityDescription(
                                key=f"{prefix_disk_key}_status",
                                name=f"{prefix_disk_name} Status",
                                icon="mdi:check-circle-outline",
                                unit_of_measurement=None,
                            ),
                            endpoint=endpoint_disk,
                            path=f"data.result[{disk_index}].status",
                            entity_category="Disks",
                        ),
                        UgreenEntity(
                            description=EntityDescription(
                                key=f"{prefix_disk_key}_temperature",
                                name=f"{prefix_disk_name} Temperature",
                                icon="mdi:thermometer",
                                unit_of_measurement=UnitOfTemperature.CELSIUS,
                            ),
                            endpoint=endpoint_disk,
                            path=f"data.result[{disk_index}].temperature",
                            entity_category="Disks",
                        ),
                        UgreenEntity(
                            description=EntityDescription(
                                key=f"{prefix_disk_key}_power_on_hours",
                                name=f"{prefix_disk_name} Power-On Hours",
                                icon="mdi:clock-outline",
                                unit_of_measurement=None,
                            ),
                            endpoint=endpoint_disk,
                            path=f"data.result[{disk_index}].power_on_hours",
                            entity_category="Disks",
                        ),
                        UgreenEntity(
                            description=EntityDescription(
                                key=f"{prefix_disk_key}_brand",
                                name=f"{prefix_disk_name} Brand",
                                icon="mdi:tag",
                                unit_of_measurement=None,
                            ),
                            endpoint=endpoint_disk,
                            path=f"data.result[{disk_index}].brand",
                            entity_category="Disks",
                        ),
                    ])

                for volume_index, _ in enumerate(pool.get("volumes", [])):
                    prefix_volume_key = f"volume{volume_index+1}_pool{pool_index+1}"
                    prefix_volume_name = f"(Pool {pool_index+1} | Volume {volume_index+1})"
                    _LOGGER.debug("[UGREEN NAS] Processing volume entity: %s", prefix_volume_key)

                    entities.extend([
                        UgreenEntity(
                            description=EntityDescription(
                                key=f"{prefix_volume_key}_name",
                                name=f"{prefix_volume_name} Name",
                                icon="mdi:label",
                                unit_of_measurement=None,
                            ),
                            endpoint=endpoint,
                            path=f"data.result[{pool_index}].volumes[{volume_index}].name",
                            entity_category="Volumes",
                        ),
                        UgreenEntity(
                            description=EntityDescription(
                                key=f"{prefix_volume_key}_label",
                                name=f"{prefix_volume_name} Label",
                                icon="mdi:label-outline",
                                unit_of_measurement=None,
                            ),
                            endpoint=endpoint,
                            path=f"data.result[{pool_index}].volumes[{volume_index}].label",
                            entity_category="Volumes",
                        ),
                        UgreenEntity(
                            description=EntityDescription(
                                key=f"{prefix_volume_key}_poolname",
                                name=f"{prefix_volume_name} Pool Name",
                                icon="mdi:database",
                                unit_of_measurement=None,
                            ),
                            endpoint=endpoint,
                            path=f"data.result[{pool_index}].volumes[{volume_index}].poolname",
                            entity_category="Volumes",
                        ),
                        UgreenEntity(
                            description=EntityDescription(
                                key=f"{prefix_volume_key}_total",
                                name=f"{prefix_volume_name} Total Size",
                                icon="mdi:database",
                                unit_of_measurement=UnitOfInformation.GIGABYTES,
                            ),
                            endpoint=endpoint,
                            path=f"data.result[{pool_index}].volumes[{volume_index}].total",
                            entity_category="Volumes",
                        ),
                        UgreenEntity(
                            description=EntityDescription(
                                key=f"{prefix_volume_key}_used",
                                name=f"{prefix_volume_name} Used Size",
                                icon="mdi:database-check",
                                unit_of_measurement=UnitOfInformation.GIGABYTES,
                            ),
                            endpoint=endpoint,
                            path=f"data.result[{pool_index}].volumes[{volume_index}].used",
                            entity_category="Volumes",
                        ),
                        UgreenEntity(
                            description=EntityDescription(
                                key=f"{prefix_volume_key}_available",
                                name=f"{prefix_volume_name} Available Size",
                                icon="mdi:database-plus",
                                unit_of_measurement=UnitOfInformation.GIGABYTES,
                            ),
                            endpoint=endpoint,
                            path=f"data.result[{pool_index}].volumes[{volume_index}].available",
                            entity_category="Volumes",
                        ),
                        UgreenEntity(
                            description=EntityDescription(
                                key=f"{prefix_volume_key}_hascache",
                                name=f"{prefix_volume_name} Has Cache",
                                icon="mdi:cached",
                                unit_of_measurement=None,
                            ),
                            endpoint=endpoint,
                            path=f"data.result[{pool_index}].volumes[{volume_index}].hascache",
                            entity_category="Volumes",
                        ),
                        UgreenEntity(
                            description=EntityDescription(
                                key=f"{prefix_volume_key}_filesystem",
                                name=f"{prefix_volume_name} Filesystem",
                                icon="mdi:file-cog",
                                unit_of_measurement=None,
                            ),
                            endpoint=endpoint,
                            path=f"data.result[{pool_index}].volumes[{volume_index}].filesystem",
                            entity_category="Volumes",
                        ),
                        UgreenEntity(
                            description=EntityDescription(
                                key=f"{prefix_volume_key}_health",
                                name=f"{prefix_volume_name} Health",
                                icon="mdi:heart-pulse",
                                unit_of_measurement=None,
                            ),
                            endpoint=endpoint,
                            path=f"data.result[{pool_index}].volumes[{volume_index}].health",
                            entity_category="Volumes",
                        ),
                        UgreenEntity(
                            description=EntityDescription(
                                key=f"{prefix_volume_key}_status",
                                name=f"{prefix_volume_name} Status",
                                icon="mdi:checkbox-marked-circle-outline",
                                unit_of_measurement=None,
                            ),
                            endpoint=endpoint,
                            path=f"data.result[{pool_index}].volumes[{volume_index}].status",
                            entity_category="Volumes",
                        ),
                    ])
        except Exception as e:
            _LOGGER.error("[UGREEN NAS] Error while building dynamic storage entities: %s", e)

        return entities
