import logging
import aiohttp
import async_timeout
from dataclasses import dataclass
from typing import Literal, Optional, List, Any
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
class UgreenSensorAPIEndpoint:
    key: str
    name: str
    endpoint: str
    path: str
    unit: Optional[str] = None
    icon: Optional[str] = None
    
@dataclass
class UgreenButtonAPIEndpoint:
    key: str
    name: str
    request_method: Literal["GET", "POST"]
    path: str
    icon: Optional[str] = None

UGREEN_STATIC_SENSOR_ENDPOINTS: List[UgreenSensorAPIEndpoint] = [
    # Hardware Info
    UgreenSensorAPIEndpoint("cpu_model", "CPU Model", "/ugreen/v1/sysinfo/machine/common", "data.hardware.cpu[0].model", None, "mdi:chip"),
    UgreenSensorAPIEndpoint("cpu_ghz", "CPU Frequency", "/ugreen/v1/sysinfo/machine/common", "data.hardware.cpu[0].ghz", UnitOfFrequency.MEGAHERTZ, "mdi:speedometer"),
    UgreenSensorAPIEndpoint("cpu_core", "CPU Cores", "/ugreen/v1/sysinfo/machine/common", "data.hardware.cpu[0].core", None, "mdi:chip"),
    UgreenSensorAPIEndpoint("cpu_thread", "CPU Threads", "/ugreen/v1/sysinfo/machine/common", "data.hardware.cpu[0].thread", None, "mdi:chip"),
    UgreenSensorAPIEndpoint("ram_manufacturer", "RAM Manufacturer", "/ugreen/v1/sysinfo/machine/common", "data.hardware.mem[0].manufacturer", None, "mdi:memory"),
    UgreenSensorAPIEndpoint("ram_model", "RAM Model", "/ugreen/v1/sysinfo/machine/common", "data.hardware.mem[0].model", None, "mdi:memory"),
    UgreenSensorAPIEndpoint("ram_size", "RAM Size", "/ugreen/v1/sysinfo/machine/common", "data.hardware.mem[0].size", UnitOfInformation.GIGABYTES, "mdi:memory"),
    UgreenSensorAPIEndpoint("ram_mhz", "RAM Speed", "/ugreen/v1/sysinfo/machine/common", "data.hardware.mem[0].mhz", None, "mdi:speedometer"),

    # Device Monitoring
    UgreenSensorAPIEndpoint("cpu_usage", "CPU Usage", "/ugreen/v1/desktop/components/data?id=desktop.component.DeviceMonitoring", "data.cpu_usage_rate", PERCENTAGE, "mdi:chip"),
    UgreenSensorAPIEndpoint("ram_usage", "RAM Usage", "/ugreen/v1/desktop/components/data?id=desktop.component.DeviceMonitoring", "data.ram_usage_rate", PERCENTAGE, "mdi:memory"),
    UgreenSensorAPIEndpoint("upload_speed", "Upload Speed", "/ugreen/v1/desktop/components/data?id=desktop.component.DeviceMonitoring", "data.upload_speed.value", UnitOfDataRate.MEGABITS_PER_SECOND, "mdi:upload"),
    UgreenSensorAPIEndpoint("download_speed", "Download Speed", "/ugreen/v1/desktop/components/data?id=desktop.component.DeviceMonitoring", "data.download_speed.value", UnitOfDataRate.MEGABITS_PER_SECOND, "mdi:download"),

    # System Status
    UgreenSensorAPIEndpoint("last_boot_date", "Last Boot", "/ugreen/v1/desktop/components/data?id=desktop.component.SystemStatus", "data.last_boot_date", None, "mdi:calendar"),
    UgreenSensorAPIEndpoint("last_boot_time", "Last Boot Timestamp", "/ugreen/v1/desktop/components/data?id=desktop.component.SystemStatus", "data.last_boot_time", None, "mdi:clock"),
    UgreenSensorAPIEndpoint("message", "System Message", "/ugreen/v1/desktop/components/data?id=desktop.component.SystemStatus", "data.message", None, "mdi:message"),
    UgreenSensorAPIEndpoint("server_status", "Server Status", "/ugreen/v1/desktop/components/data?id=desktop.component.SystemStatus", "data.server_status", None, "mdi:server"),
    UgreenSensorAPIEndpoint("status", "System Status Code", "/ugreen/v1/desktop/components/data?id=desktop.component.SystemStatus", "data.status", None, "mdi:information"),
    UgreenSensorAPIEndpoint("total_run_time", "Total Runtime", "/ugreen/v1/desktop/components/data?id=desktop.component.SystemStatus", "data.total_run_time", UnitOfTime.SECONDS, "mdi:timer-outline"),
    UgreenSensorAPIEndpoint("device_name", "Device Name", "/ugreen/v1/desktop/components/data?id=desktop.component.SystemStatus", "data.dev_name", None, "mdi:nas"),

    # Temperature Monitoring
    UgreenSensorAPIEndpoint("cpu_temperature", "CPU Temperature", "/ugreen/v1/desktop/components/data?id=desktop.component.TemperatureMonitoring", "data.cpu_temperature", UnitOfTemperature.CELSIUS, "mdi:thermometer"),
    UgreenSensorAPIEndpoint("cpu_status", "CPU Temperature Status", "/ugreen/v1/desktop/components/data?id=desktop.component.TemperatureMonitoring", "data.cpu_status", None, "mdi:alert"),
    UgreenSensorAPIEndpoint("fan_speed", "Main Fan Speed", "/ugreen/v1/desktop/components/data?id=desktop.component.TemperatureMonitoring", "data.fan_speed", REVOLUTIONS_PER_MINUTE, "mdi:fan"),
    UgreenSensorAPIEndpoint("fan_status", "Fan Status", "/ugreen/v1/desktop/components/data?id=desktop.component.TemperatureMonitoring", "data.fan_status", None, "mdi:fan-alert"),
    UgreenSensorAPIEndpoint("temperature_message", "Temperature Message", "/ugreen/v1/desktop/components/data?id=desktop.component.TemperatureMonitoring", "data.message", None, "mdi:message-alert"),
    UgreenSensorAPIEndpoint("temperature_status", "Temperature Status Code", "/ugreen/v1/desktop/components/data?id=desktop.component.TemperatureMonitoring", "data.status", None, "mdi:information"),
    UgreenSensorAPIEndpoint("fan1_speed", "Fan 1 Speed", "/ugreen/v1/desktop/components/data?id=desktop.component.TemperatureMonitoring", "data.fan_list[0].speed", REVOLUTIONS_PER_MINUTE, "mdi:fan"),
    UgreenSensorAPIEndpoint("fan2_speed", "Fan 2 Speed", "/ugreen/v1/desktop/components/data?id=desktop.component.TemperatureMonitoring", "data.fan_list[1].speed", REVOLUTIONS_PER_MINUTE, "mdi:fan"),
]

UGREEN_STATIC_BUTTON_ENDPOINTS: List[UgreenButtonAPIEndpoint] = [
    # System Actions
    UgreenButtonAPIEndpoint("shutdown", "Shutdown", "POST", "/ugreen/v1/desktop/shutdown", "mdi:power"),
    UgreenButtonAPIEndpoint("reboot", "Reboot", "POST", "/ugreen/v1/desktop/reboot", "mdi:restart")
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

    async def get_storage_entities(self, session: aiohttp.ClientSession) -> List[UgreenSensorAPIEndpoint]:
        """Fetch and build dynamic storage entities (unchanged logic)."""
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

        entities: List[UgreenSensorAPIEndpoint] = []

        try:
            for pool_index, pool in enumerate(results):
                prefix_pool_key = f"pool{pool_index+1}"
                prefix_pool_name = f"(Pool {pool_index+1})"
                _LOGGER.debug("[UGREEN NAS] Processing pool entity: %s", prefix_pool_key)

                entities.extend([
                    UgreenSensorAPIEndpoint(f"{prefix_pool_key}_name", f"{prefix_pool_name} Name", endpoint, f"data.result[{pool_index}].name", None, "mdi:chip"),
                    UgreenSensorAPIEndpoint(f"{prefix_pool_key}_label", f"{prefix_pool_name} Label", endpoint, f"data.result[{pool_index}].label", None, "mdi:label"),
                    UgreenSensorAPIEndpoint(f"{prefix_pool_key}_level", f"{prefix_pool_name} Level", endpoint, f"data.result[{pool_index}].level", None, "mdi:format-list-bulleted-type"),
                    UgreenSensorAPIEndpoint(f"{prefix_pool_key}_status", f"{prefix_pool_name} Status", endpoint, f"data.result[{pool_index}].status", None, "mdi:check-circle-outline"),
                    UgreenSensorAPIEndpoint(f"{prefix_pool_key}_total", f"{prefix_pool_name} Total Size", endpoint, f"data.result[{pool_index}].total", UnitOfInformation.GIGABYTES, "mdi:database"),
                    UgreenSensorAPIEndpoint(f"{prefix_pool_key}_used", f"{prefix_pool_name} Used Size", endpoint, f"data.result[{pool_index}].used", UnitOfInformation.GIGABYTES, "mdi:database-check"),
                    UgreenSensorAPIEndpoint(f"{prefix_pool_key}_free", f"{prefix_pool_name} Free Size", endpoint, f"data.result[{pool_index}].free", UnitOfInformation.GIGABYTES, "mdi:database-remove"),
                    UgreenSensorAPIEndpoint(f"{prefix_pool_key}_available", f"{prefix_pool_name} Available Size", endpoint, f"data.result[{pool_index}].available", UnitOfInformation.GIGABYTES, "mdi:database-plus"),
                    UgreenSensorAPIEndpoint(f"{prefix_pool_key}_disk_count", f"{prefix_pool_name} Disk Count", endpoint, f"data.result[{pool_index}].total_disk_num", None, "mdi:harddisk"),
                ])

                for disk_index, _ in enumerate(pool.get("disks", [])):
                    prefix_disk_key = f"disk{disk_index+1}_pool{pool_index+1}"
                    prefix_disk_name = f"(Pool {pool_index+1} | Disk {disk_index+1})"                    
                    _LOGGER.debug("[UGREEN NAS] Processing disk entity: %s", prefix_disk_key)

                    entities.extend([
                        UgreenSensorAPIEndpoint(f"{prefix_disk_key}_name", f"{prefix_disk_name} Name", endpoint, f"data.result[{pool_index}].disks[{disk_index}].name", None, "mdi:identifier"),
                        UgreenSensorAPIEndpoint(f"{prefix_disk_key}_label", f"{prefix_disk_name} Label", endpoint, f"data.result[{pool_index}].disks[{disk_index}].label", None, "mdi:label"),
                        UgreenSensorAPIEndpoint(f"{prefix_disk_key}_size", f"{prefix_disk_name} Size", endpoint, f"data.result[{pool_index}].disks[{disk_index}].size", UnitOfInformation.GIGABYTES, "mdi:database"),
                        UgreenSensorAPIEndpoint(f"{prefix_disk_key}_status", f"{prefix_disk_name} Status", endpoint, f"data.result[{pool_index}].disks[{disk_index}].status", None, "mdi:check-circle-outline"),
                        UgreenSensorAPIEndpoint(f"{prefix_disk_key}_slot", f"{prefix_disk_name} Slot", endpoint, f"data.result[{pool_index}].disks[{disk_index}].slot", None, "mdi:server-network"),
                        UgreenSensorAPIEndpoint(f"{prefix_disk_key}_type", f"{prefix_disk_name} Type", endpoint, f"data.result[{pool_index}].disks[{disk_index}].disk_type", None, "mdi:harddisk"),
                        UgreenSensorAPIEndpoint(f"{prefix_disk_key}_temperature", f"{prefix_disk_name} Temperature", "/ugreen/v1/desktop/components/data?id=desktop.component.TemperatureMonitoring", f"data.disk_list[{disk_index}].temperature", UnitOfTemperature.CELSIUS, "mdi:thermometer"),
                    ])

                for volume_index, _ in enumerate(pool.get("volumes", [])):
                    prefix_volume_key = f"volume{volume_index+1}_pool{pool_index+1}"
                    prefix_volume_name = f"(Pool {pool_index+1} | Volume {volume_index+1})"
                    _LOGGER.debug("[UGREEN NAS] Processing volume entity: %s", prefix_volume_key)

                    entities.extend([
                        UgreenSensorAPIEndpoint(f"{prefix_volume_key}_name", f"{prefix_volume_name} Name", endpoint, f"data.result[{pool_index}].volumes[{volume_index}].name", None, "mdi:label"),
                        UgreenSensorAPIEndpoint(f"{prefix_volume_key}_label",f"{prefix_volume_name} Label", endpoint, f"data.result[{pool_index}].volumes[{volume_index}].label", None, "mdi:label-outline"),
                        UgreenSensorAPIEndpoint(f"{prefix_volume_key}_poolname", f"{prefix_volume_name} Pool Name", endpoint, f"data.result[{pool_index}].volumes[{volume_index}].poolname", None, "mdi:database"),
                        UgreenSensorAPIEndpoint(f"{prefix_volume_key}_total", f"{prefix_volume_name} Total Size", endpoint, f"data.result[{pool_index}].volumes[{volume_index}].total", UnitOfInformation.GIGABYTES, "mdi:database"),
                        UgreenSensorAPIEndpoint(f"{prefix_volume_key}_used", f"{prefix_volume_name} Used Size", endpoint, f"data.result[{pool_index}].volumes[{volume_index}].used", UnitOfInformation.GIGABYTES, "mdi:database-check"),
                        UgreenSensorAPIEndpoint(f"{prefix_volume_key}_available", f"{prefix_volume_name} Available Size", endpoint, f"data.result[{pool_index}].volumes[{volume_index}].available", UnitOfInformation.GIGABYTES, "mdi:database-plus"),
                        UgreenSensorAPIEndpoint(f"{prefix_volume_key}_hascache", f"{prefix_volume_name} Has Cache", endpoint, f"data.result[{pool_index}].volumes[{volume_index}].hascache", None, "mdi:cached"),
                        UgreenSensorAPIEndpoint(f"{prefix_volume_key}_filesystem", f"{prefix_volume_name} Filesystem", endpoint, f"data.result[{pool_index}].volumes[{volume_index}].filesystem", None, "mdi:file-cog"),
                        UgreenSensorAPIEndpoint(f"{prefix_volume_key}_health", f"{prefix_volume_name} Health", endpoint, f"data.result[{pool_index}].volumes[{volume_index}].health", None, "mdi:heart-pulse"),
                        UgreenSensorAPIEndpoint(f"{prefix_volume_key}_status", f"{prefix_volume_name} Status", endpoint, f"data.result[{pool_index}].volumes[{volume_index}].status", None, "mdi:checkbox-marked-circle-outline"),
                    ])
        except Exception as e:
            _LOGGER.error("[UGREEN NAS] Error while building dynamic storage entities: %s", e)

        return entities