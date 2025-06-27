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

UGREEN_STATIC_SENSOR_ENDPOINTS: List[UgreenEntity] = [

    # Device Info
    UgreenEntity(
        description=EntityDescription(
            key="name",
            name="Name",
            icon="mdi:nas",
            unit_of_measurement=None,
        ),
        endpoint="/ugreen/v1/sysinfo/machine/common",
        path="data.common.nas_name",
    ),
    UgreenEntity(
        description=EntityDescription(
            key="owner",
            name="Owner",
            icon="mdi:account",
            unit_of_measurement=None,
        ),
        endpoint="/ugreen/v1/sysinfo/machine/common",
        path="data.common.nas_owner",
    ),
    UgreenEntity(
        description=EntityDescription(
            key="model",
            name="Model",
            icon="mdi:account",
            unit_of_measurement=None,
        ),
        endpoint="/ugreen/v1/sysinfo/machine/common",
        path="data.common.model",
    ),
    UgreenEntity(
        description=EntityDescription(
            key="serial",
            name="Serial",
            icon="mdi:focus-field",
            unit_of_measurement=None,
        ),
        endpoint="/ugreen/v1/sysinfo/machine/common",
        path="data.common.serial",
    ),
    UgreenEntity(
        description=EntityDescription(
            key="version",
            name="Version",
            icon="mdi:numeric",
            unit_of_measurement=None,
        ),
        endpoint="/ugreen/v1/sysinfo/machine/common",
        path="data.common.system_version",
    ),
    UgreenEntity(
        description=EntityDescription(
            key="type",
            name="Type",
            icon="mdi:nas",
            unit_of_measurement=None,
        ),
        endpoint="/ugreen/v1/desktop/components/data?id=desktop.component.SystemStatus",
        path="data.type",
    ),

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
        decimal_places=0
    ),
    UgreenEntity(
        description=EntityDescription(
            key="cpu_core",
            name="CPU Cores",
            icon="mdi:chip",
            unit_of_measurement=None,
        ),
        endpoint="/ugreen/v1/sysinfo/machine/common",
        path="data.hardware.cpu[0].core",
        decimal_places=0
    ),
    UgreenEntity(
        description=EntityDescription(
            key="cpu_thread",
            name="CPU Threads",
            icon="mdi:chip",
            unit_of_measurement=None,
        ),
        endpoint="/ugreen/v1/sysinfo/machine/common",
        path="data.hardware.cpu[0].thread",
        decimal_places=0
    ),
    UgreenEntity(
        description=EntityDescription(
            key="ram_manufacturer",
            name="RAM Manufacturer",
            icon="mdi:memory",
            unit_of_measurement=None,
        ),
        endpoint="/ugreen/v1/sysinfo/machine/common",
        path="data.hardware.mem[0].manufacturer",
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
    ),
    UgreenEntity(
        description=EntityDescription(
            key="ram_usage",
            name="RAM Usage",
            icon="mdi:memory",
            unit_of_measurement=PERCENTAGE,
        ),
        endpoint="/ugreen/v1/desktop/components/data?id=desktop.component.DeviceMonitoring",
        path="data.ram_usage_rate",
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
    ),

    # System Status
    # UgreenEntity( # duplicate and without year (useless); use last_boot_timestamp instead
    #     description=EntityDescription(
    #         key="last_boot_date",
    #         name="Last Boot",
    #         icon="mdi:calendar",
    #         unit_of_measurement=None,
    #     ),
    #     endpoint="/ugreen/v1/desktop/components/data?id=desktop.component.SystemStatus",
    #     path="data.last_boot_date",
    # ),
    UgreenEntity(
        description=EntityDescription(
            key="last_boot_timestamp",
            name="Last Boot Timestamp",
            icon="mdi:clock",
            unit_of_measurement=None,
        ),
        endpoint="/ugreen/v1/desktop/components/data?id=desktop.component.SystemStatus",
        path="data.last_boot_time",
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
    ),
    UgreenEntity(
        description=EntityDescription(
            key="last_turn_on_timestamp",
            name="Last turn on timestamp",
            icon="mdi:timer-outline",
            unit_of_measurement=None,
        ),
        endpoint="/ugreen/v1/sysinfo/machine/common",
        path="data.common.last_turn_on_time",
    ),
    UgreenEntity(
        description=EntityDescription(
            key="repair_start_time",
            name="Repair start time",
            icon="mdi:timer-outline",
            unit_of_measurement=None,
        ),
        endpoint="/ugreen/v1/sysinfo/machine/common",
        path="data.common.repair_start_time",
    ),
    UgreenEntity(
        description=EntityDescription(
            key="repair_end_time",
            name="Repair end time",
            icon="mdi:timer-outline",
            unit_of_measurement=None,
        ),
        endpoint="/ugreen/v1/sysinfo/machine/common",
        path="data.common.repair_end_time",
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
    ),
    # UgreenEntity( # duplicate, already as 'name' in 'common'
    #     description=EntityDescription(
    #         key="device_name",
    #         name="Device Name",
    #         icon="mdi:nas",
    #         unit_of_measurement=None,
    #     ),
    #     endpoint="/ugreen/v1/desktop/components/data?id=desktop.component.SystemStatus",
    #     path="data.dev_name",
    # ),

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
    ),
    UgreenEntity(
        description=EntityDescription(
            key="fan_speed",
            name="Main Fan Speed",
            icon="mdi:fan",
            unit_of_measurement=REVOLUTIONS_PER_MINUTE,
        ),
        endpoint="/ugreen/v1/desktop/components/data?id=desktop.component.TemperatureMonitoring",
        path="data.fan_speed",
    ),
    UgreenEntity(
        description=EntityDescription(
            key="fan_status",
            name="Fan Status",
            icon="mdi:fan-alert",
            unit_of_measurement=None,
        ),
        endpoint="/ugreen/v1/desktop/components/data?id=desktop.component.TemperatureMonitoring",
        path="data.fan_status",
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
    ),
    UgreenEntity(
        description=EntityDescription(
            key="fan1_speed",
            name="Fan 1 Speed",
            icon="mdi:fan",
            unit_of_measurement=REVOLUTIONS_PER_MINUTE,
        ),
        endpoint="/ugreen/v1/desktop/components/data?id=desktop.component.TemperatureMonitoring",
        path="data.fan_list[0].speed",
    ),
    UgreenEntity(
        description=EntityDescription(
            key="fan2_speed",
            name="Fan 2 Speed",
            icon="mdi:fan",
            unit_of_measurement=REVOLUTIONS_PER_MINUTE,
        ),
        endpoint="/ugreen/v1/desktop/components/data?id=desktop.component.TemperatureMonitoring",
        path="data.fan_list[1].speed",
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


    async def get_ram_entities(self, session: aiohttp.ClientSession) -> list[UgreenEntity]:
        endpoint = "/ugreen/v1/sysinfo/machine/common"
        response = await self.get(session, endpoint)

        mem_list = response.get("data", {}).get("hardware", {}).get("mem", [])
        if not isinstance(mem_list, list):
            _LOGGER.warning("[UGREEN NAS] RAM list is invalid or missing.")
            return []

        ram_count = len(mem_list)
        entities: list[UgreenEntity] = []
        size_paths = []

        if ram_count > 1:
            _LOGGER.debug("[UGREEN NAS] Detected %d RAM modules – using dynamic keys", ram_count)
        else:
            _LOGGER.debug("[UGREEN NAS] Single RAM module – using static keys")

        for index in range(ram_count):
            if ram_count > 1:
                # Multiple RAM modules
                prefix = f"ram{index+1}"
                name = f"RAM {index+1}"
            else:
                # Just 1 RAM module, using dobby's entity names
                prefix = "ram"
                name = "RAM"

            size_paths.append(f"data.hardware.mem[{index}].size")

            entities.extend([
                UgreenEntity(
                    description=EntityDescription(
                        key=f"{prefix}_model",
                        name=f"{name} Model",
                        icon="mdi:memory",
                        unit_of_measurement=None,
                    ),
                    endpoint=endpoint,
                    path=f"data.hardware.mem[{index}].model",
                ),
                UgreenEntity(
                    description=EntityDescription(
                        key=f"{prefix}_manufacturer",
                        name=f"{name} Manufacturer",
                        icon="mdi:factory",
                        unit_of_measurement=None,
                    ),
                    endpoint=endpoint,
                    path=f"data.hardware.mem[{index}].manufacturer",
                ),
                UgreenEntity(
                    description=EntityDescription(
                        key=f"{prefix}_size",
                        name=f"{name} Size",
                        icon="mdi:memory",
                        unit_of_measurement=UnitOfInformation.GIGABYTES,
                    ),
                    endpoint=endpoint,
                    path=f"data.hardware.mem[{index}].size",
                    decimal_places=0,
                ),
                UgreenEntity(
                    description=EntityDescription(
                        key=f"{prefix}_speed",
                        name=f"{name} Speed",
                        icon="mdi:speedometer",
                        unit_of_measurement="MHz",
                    ),
                    endpoint=endpoint,
                    path=f"data.hardware.mem[{index}].mhz",
                    decimal_places=0,
                ),
            ])

        # Add a sensor for the total RAM size (sum of all modules)
        if size_paths:
            entities.append(
                UgreenEntity(
                    description=EntityDescription(
                        key="ram_total_size",
                        name="RAM Total Size",
                        icon="mdi:memory",
                        unit_of_measurement=UnitOfInformation.GIGABYTES,
                    ),
                    endpoint=endpoint,
                    path=size_paths,  # This is a list of paths to sum
                    decimal_places=0,
                )
            )

        return entities



    async def get_storage_entities(self, session: aiohttp.ClientSession) -> List[UgreenEntity]:
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
                        ),
                ])

                if not hasattr(self, "_ugreen_disks_cache"):
                    disk_response = await self.get(session, "/ugreen/v2/storage/disk/list")
                    disks_global = disk_response.get("data", {}).get("result", [])
                    self._ugreen_disks_cache = {
                        disk["dev_name"]: (index, disk) for index, disk in enumerate(disks_global)
                    }

                for pool_disk_index, disk_ref in enumerate(pool.get("disks", [])):
                    dev_name = disk_ref.get("dev_name")
                    match = self._ugreen_disks_cache.get(dev_name)
                    disk_index, _ = match
                    prefix_disk_key = f"disk{pool_disk_index+1}_pool{pool_index+1}"
                    prefix_disk_name = f"(Pool {pool_index+1} | Disk {pool_disk_index+1})"
                    endpoint_disk = "/ugreen/v2/storage/disk/list"
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
                        ),
                    ])
        except Exception as e:
            _LOGGER.error("[UGREEN NAS] Error while building dynamic storage entities: %s", e)

        return entities
