import logging, aiohttp, async_timeout, asyncio
import base64
from dataclasses import dataclass
from typing import List, Any
from homeassistant.helpers.entity import EntityDescription
from homeassistant.const import (
    PERCENTAGE, REVOLUTIONS_PER_MINUTE, UnitOfDataRate, UnitOfTemperature,
    UnitOfInformation, UnitOfTime, UnitOfFrequency
)

_LOGGER = logging.getLogger(__name__)


@dataclass
class UgreenEntity:
    description: EntityDescription
    endpoint: str
    path: str
    request_method: str = "GET"
    decimal_places: int = 2
    nas_part_category: str = ""


STATIC_CONFIG_ENTITIES: List[UgreenEntity] = [ ################ STATIC_CONFIG ##

    ### Device Info
    UgreenEntity(
        description=EntityDescription(
            key="model",
            name="NAS Model",
            icon="mdi:account",
            unit_of_measurement=None,
        ),
        endpoint="/ugreen/v1/sysinfo/machine/common",
        path="data.common.model",
        nas_part_category="Device",
    ),
    UgreenEntity(
        description=EntityDescription(
            key="type",
            name="NAS Type",
            icon="mdi:nas",
            unit_of_measurement=None,
        ),
        endpoint="/ugreen/v1/desktop/components/data?id=desktop.component.SystemStatus",
        path="data.type",
        nas_part_category="Device",
    ),
    UgreenEntity(
        description=EntityDescription(
            key="serial",
            name="NAS Serial",
            icon="mdi:focus-field",
            unit_of_measurement=None,
        ),
        endpoint="/ugreen/v1/sysinfo/machine/common",
        path="data.common.serial",
        nas_part_category="Device",
    ),
    UgreenEntity(
        description=EntityDescription(
            key="owner",
            name="NAS Owner",
            icon="mdi:account",
            unit_of_measurement=None,
        ),
        endpoint="/ugreen/v1/sysinfo/machine/common",
        path="data.common.nas_owner",
        nas_part_category="Device",
    ),
    UgreenEntity(
        description=EntityDescription(
            key="device_name",
            name="NAS Name",
            icon="mdi:nas",
            unit_of_measurement=None,
        ),
        endpoint="/ugreen/v1/desktop/components/data?id=desktop.component.SystemStatus",
        path="data.dev_name",
        nas_part_category="Device",
    ),
    UgreenEntity(
        description=EntityDescription(
            key="version",
            name="NAS UGOS Version",
            icon="mdi:numeric",
            unit_of_measurement=None,
        ),
        endpoint="/ugreen/v1/sysinfo/machine/common",
        path="data.common.system_version",
        nas_part_category="Device",
    ),

    ### Hardware Info
    UgreenEntity(
        description=EntityDescription(
            key="cpu_model",
            name="CPU Model",
            icon="mdi:chip",
            unit_of_measurement=None,
        ),
        endpoint="/ugreen/v1/sysinfo/machine/common",
        path="data.hardware.cpu[0].model",
        nas_part_category="Hardware",
    ),
    UgreenEntity(
        description=EntityDescription(
            key="cpu_ghz",
            name="CPU Speed",
            icon="mdi:speedometer",
            unit_of_measurement=UnitOfFrequency.MEGAHERTZ,
        ),
        endpoint="/ugreen/v1/sysinfo/machine/common",
        path="data.hardware.cpu[0].ghz",
        decimal_places=0,
        nas_part_category="Hardware",
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
        nas_part_category="Hardware",
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
        nas_part_category="Hardware",
    ),

    ### Runtime info
        UgreenEntity(
        description=EntityDescription(
            key="last_boot_date",
            name="Last Boot",
            icon="mdi:calendar",
            unit_of_measurement=None,
        ),
        endpoint="/ugreen/v1/desktop/components/data?id=desktop.component.SystemStatus",
        path="data.last_boot_date",
        nas_part_category="Status",
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
        nas_part_category="Status",
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
        nas_part_category="Status",
    ),

    ### System Status
    UgreenEntity(
        description=EntityDescription(
            key="server_status",
            name="Server Status",
            icon="mdi:server",
            unit_of_measurement=None,
        ),
        endpoint="/ugreen/v1/desktop/components/data?id=desktop.component.SystemStatus",
        path="data.server_status",
        nas_part_category="Status",
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
        nas_part_category="Status",
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
        nas_part_category="Status",
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
        nas_part_category="Status",
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
        nas_part_category="Status",
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
        nas_part_category="Status",
    ),
]


STATIC_STATUS_ENTITIES = [ #################################### STATIC_STATUS ##

    ### CPU
    UgreenEntity(
        description=EntityDescription(
            key="cpu_usage",
            name="CPU Usage",
            icon="mdi:chip",
            unit_of_measurement=PERCENTAGE,
        ),
        decimal_places=0,
        endpoint="/ugreen/v1/taskmgr/stat/get_all",
        path="data.overview.cpu[0].used_percent",
        nas_part_category="Status",
    ),
    UgreenEntity(
        description=EntityDescription(
            key="cpu_temperature",
            name="CPU Temperature",
            icon="mdi:thermometer",
            unit_of_measurement=UnitOfTemperature.CELSIUS,
        ),
        decimal_places=0,
        endpoint="/ugreen/v1/taskmgr/stat/get_all",
        path="data.overview.cpu[0].temp",
        nas_part_category="Status",
    ),

    ### RAM
    UgreenEntity(
        description=EntityDescription(
            key="mem_usage",
            name="RAM Usage",
            icon="mdi:memory",
            unit_of_measurement=PERCENTAGE,
        ),
        endpoint="/ugreen/v1/taskmgr/stat/get_all",
        path="data.overview.mem[0].used_percent",
        nas_part_category="Status",
    ),
    UgreenEntity(
        description=EntityDescription(
            key="ram_usage_total_usable",
            name="RAM Usage (Usable RAM)",
            icon="mdi:memory",
            unit_of_measurement=UnitOfInformation.BYTES,
        ),
        endpoint="/ugreen/v1/taskmgr/stat/get_all",
        path="data.mem.structure.total",
        nas_part_category="Status",
    ),
    UgreenEntity(
        description=EntityDescription(
            key="ram_usage_free",
            name="RAM Usage (Free RAM)",
            icon="mdi:memory",
            unit_of_measurement=UnitOfInformation.BYTES,
        ),
        endpoint="/ugreen/v1/taskmgr/stat/get_all",
        path="data.mem.structure.free",
        nas_part_category="Status",
    ),
    UgreenEntity(
        description=EntityDescription(
            key="ram_usage_cache",
            name="RAM Usage (Cache)",
            icon="mdi:memory",
            unit_of_measurement=UnitOfInformation.BYTES,
        ),
        endpoint="/ugreen/v1/taskmgr/stat/get_all",
        path="data.mem.structure.cache",
        nas_part_category="Status",
    ),
    UgreenEntity(
        description=EntityDescription(
            key="ram_usage_shared",
            name="RAM Usage (Shared Mem)",
            icon="mdi:memory",
            unit_of_measurement=UnitOfInformation.BYTES,
        ),
        endpoint="/ugreen/v1/taskmgr/stat/get_all",
        path="data.mem.structure.share",
        nas_part_category="Status",
    ),
    UgreenEntity(
        description=EntityDescription(
            key="ram_usage_used_gb",
            name="RAM Usage (Used GB)",
            icon="mdi:memory",
            unit_of_measurement=UnitOfInformation.BYTES,
        ),
        endpoint="/ugreen/v1/taskmgr/stat/get_all",
        path="data.mem.structure.used",
        nas_part_category="Status",
    ),

    ### LAN (net.overview = first element, overall)
    UgreenEntity(
        description=EntityDescription(
            key="overall_lan_upload_raw",
            name="Overall LAN Upload (raw)",
            icon="mdi:upload-network",
            unit_of_measurement=UnitOfDataRate.BYTES_PER_SECOND,
        ),
        endpoint="/ugreen/v1/taskmgr/stat/get_all",
        path="data.net.series[0].send_rate",
        nas_part_category="Status",
    ),
    UgreenEntity(
        description=EntityDescription(
            key="overall_lan_upload",
            name="Overall LAN Upload",
            icon="mdi:upload-network",
            unit_of_measurement=None,
        ),
        endpoint="/ugreen/v1/taskmgr/stat/get_all",
        path="calculated:scale_bytes_per_second:data.net.series[0].send_rate",
        nas_part_category="Status",
    ),
    UgreenEntity(
        description=EntityDescription(
            key="overall_lan_download_raw",
            name="Overall LAN Download (raw)",
            icon="mdi:download-network",
            unit_of_measurement=UnitOfDataRate.BYTES_PER_SECOND,
        ),
        endpoint="/ugreen/v1/taskmgr/stat/get_all",
        path="data.net.series[0].recv_rate",
        nas_part_category="Status",
    ),
    UgreenEntity(
        description=EntityDescription(
            key="overall_lan_download",
            name="Overall LAN Download",
            icon="mdi:download-network",
            unit_of_measurement=None,
        ),
        endpoint="/ugreen/v1/taskmgr/stat/get_all",
        path="calculated:scale_bytes_per_second:data.net.series[0].recv_rate",
        nas_part_category="Status",
    ),

    ### Disks (disk.series only = first element, overall)
    UgreenEntity(
        description=EntityDescription(
            key="overall_disk_read_rate_raw",
            name="Overall Disk Read Rate (raw)",
            icon="mdi:harddisk",
            unit_of_measurement=UnitOfDataRate.BYTES_PER_SECOND,
        ),
        endpoint="/ugreen/v1/taskmgr/stat/get_all",
        path="data.disk.series[0].read_rate",
        nas_part_category="Status",
    ),
    UgreenEntity(
        description=EntityDescription(
            key="overall_disk_read_rate",
            name="Overall Disk Read Rate",
            icon="mdi:harddisk",
            unit_of_measurement=None,
        ),
        endpoint="/ugreen/v1/taskmgr/stat/get_all",
        path="calculated:scale_bytes_per_second:data.disk.series[0].read_rate",
        nas_part_category="Status",
    ),
    UgreenEntity(
        description=EntityDescription(
            key="overall_disk_write_rate_raw",
            name="Overall Disk Write Rate (raw)",
            icon="mdi:harddisk",
            unit_of_measurement=UnitOfDataRate.BYTES_PER_SECOND,
        ),
        endpoint="/ugreen/v1/taskmgr/stat/get_all",
        path="data.disk.series[0].write_rate",
        nas_part_category="Status",
    ),
    UgreenEntity(
        description=EntityDescription(
            key="overall_disk_write_rate",
            name="Overall Disk Write Rate",
            icon="mdi:harddisk",
            unit_of_measurement=None,
        ),
        endpoint="/ugreen/v1/taskmgr/stat/get_all",
        path="calculated:scale_bytes_per_second:data.disk.series[0].write_rate",
        nas_part_category="Status",
    ),

    ### Volumes (volume.series only = first element, overall)
    UgreenEntity(
        description=EntityDescription(
            key="overall_volume_read_rate_raw",
            name="Overall Volume Read Rate (raw)",
            icon="mdi:harddisk",
            unit_of_measurement=UnitOfDataRate.BYTES_PER_SECOND,
        ),
        endpoint="/ugreen/v1/taskmgr/stat/get_all",
        path="data.volume.series[0].read_rate",
        nas_part_category="Status",
    ),
    UgreenEntity(
        description=EntityDescription(
            key="overall_volume_read_rate",
            name="Overall Volume Read Rate",
            icon="mdi:harddisk",
            unit_of_measurement=None,
        ),
        endpoint="/ugreen/v1/taskmgr/stat/get_all",
        path="calculated:scale_bytes_per_second:data.volume.series[0].read_rate",
        nas_part_category="Status",
    ),
    UgreenEntity(
        description=EntityDescription(
            key="overall_volume_write_rate_raw",
            name="Overall Volume Write Rate (raw)",
            icon="mdi:harddisk",
            unit_of_measurement=UnitOfDataRate.BYTES_PER_SECOND,
        ),
        endpoint="/ugreen/v1/taskmgr/stat/get_all",
        path="data.volume.series[0].write_rate",
        nas_part_category="Status",
    ),
    UgreenEntity(
        description=EntityDescription(
            key="overall_volume_write_rate",
            name="Overall Volume Write Rate",
            icon="mdi:harddisk",
            unit_of_measurement=None,
        ),
        endpoint="/ugreen/v1/taskmgr/stat/get_all",
        path="calculated:scale_bytes_per_second:data.volume.series[0].write_rate",
        nas_part_category="Status",
    ),
]

STATIC_BUTTON_ENTITIES: List[UgreenEntity] = [
    ### System Actions
    UgreenEntity(
        description=EntityDescription(
            key="shutdown",
            name="Shutdown",
            icon="mdi:power",
        ),
        endpoint="/ugreen/v1/desktop/shutdown",
        path="",
        request_method="POST",
        nas_part_category="",
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
        nas_part_category="",
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
        self._dynamic_entity_counts = None
        self._dynamic_entity_counts_lock = asyncio.Lock()


    ################################################ CORE API FUNCTIONS ########
    def encrypt_password(self, password, public_key):
        from Crypto.Cipher import PKCS1_v1_5
        from Crypto.PublicKey import RSA
        public_key = RSA.import_key(public_key)
        encrypted_password = PKCS1_v1_5.new(public_key).encrypt(password.encode())
        encrypted_base64 = base64.b64encode(encrypted_password).decode('utf-8')
        return encrypted_base64

    async def _get_public_key(self, session: aiohttp.ClientSession) -> str:
        url = f'{self.base_url}/ugreen/v1/verify/check?token='
        # print("get_public_key",url)
        payload = {
            "username": self.username
        }
        _LOGGER.debug("[UGREEN NAS] Sending _get_public_key POST to: %s", url)
        try:
            async with session.post(url, json=payload, ssl=self.verify_ssl) as resp:
                resp.raise_for_status()
                # data = await resp.json()
                # _LOGGER.debug("[UGREENPRO NAS] _get_public_key response: %s", data)

                x_rsa_token = resp.headers.get("x-rsa-token", "")
                x_rsa_token_bytes = x_rsa_token.encode('utf-8')
                dd = base64.b64decode(x_rsa_token_bytes)
                return dd
        except Exception as e:
            _LOGGER.exception("[UGREENPRO NAS] _get_public_key request failed: %s", e)
            return False

        pass


    async def login(self, session: aiohttp.ClientSession) -> str:
        url = f"{self.base_url}/ugreen/v1/verify/login"
        key = await self._get_public_key(session)
        password = self.encrypt_password(self.password, key)
        payload_json = {
            "is_simple": True,
            'keepalive': True,
            'otp': True,
            "username": self.username,
            "password": password
        }
        _LOGGER.debug("[UGREENPRO NAS] Sending login POST to: %s", url)
        try:
            async with session.post(url, json=payload_json, ssl=self.verify_ssl) as resp:
                resp.raise_for_status()
                data = await resp.json()
                _LOGGER.debug("[UGREENPRO NAS] Login response: %s", data)

                if data.get("code") != 200:
                    _LOGGER.warning("[UGREENPRO NAS] Login failed with code: %s", data.get("code"))
                    return False

                token = data.get("data", {}).get("token")
                if not token:
                    _LOGGER.error("[UGREENPRO NAS] Login succeeded but token not found in response")
                    return False

                self.token = token
                _LOGGER.info("[UGREENPRO NAS] Token received and stored token: %s", token)
                return True
        except Exception as e:
            _LOGGER.exception("[UGREENPRO NAS] Login request failed: %s", e)
            return False



    async def authenticate(self, session: aiohttp.ClientSession) -> bool:
        return self.login(session)
        """Login and fetch new token."""
        """url = f"{self.token_url}/token?username={self.username}&password={self.password}"
        
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
            return False"""


    async def get(self, session: aiohttp.ClientSession, endpoint: str) -> dict[str, Any]:
        """Perform GET with retry on token expiration (code 1024)."""
        async def _do_get() -> dict[str, Any]:
            url = f"{self.base_url}{endpoint}"
            delimiter = "&" if "?" in url else "?"
            url += f"{delimiter}token={self.token}"
            _LOGGER.debug("[UGREEN NAS] Sending GET request to: %s", url)

            # uncomment this to see each 5s/60s API call in the log:
            # _LOGGER.error("[UGREEN API] Calling endpoint: %s", endpoint)

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


    #################################################### COUNT DYNAMIC  ########


    async def count_dynamic_entities(self, session: aiohttp.ClientSession) -> dict:
        if self._dynamic_entity_counts is not None:
            return self._dynamic_entity_counts
        async with self._dynamic_entity_counts_lock:
            if self._dynamic_entity_counts is not None:
                return self._dynamic_entity_counts
            try:
                counts: dict[str, Any] = {}

                # 1) RAM / USB / UPS (sysinfo)
                sysinfo = await self.get(session, "/ugreen/v1/sysinfo/machine/common")
                if isinstance(sysinfo, dict):
                    hw = (sysinfo.get("data", {}) or {}).get("hardware", {}) or {}
                    counts["num_rams"] = len(hw.get("mem", []) or [])
                    counts["num_usbs"] = len(hw.get("usb", []) or [])
                    counts["has_ups"] = bool(hw.get("ups", []) or [])

                # 2) Storage: Disks / Pools / Volumes
                disks_resp = await self.get(session, "/ugreen/v2/storage/disk/list")
                if isinstance(disks_resp, dict):
                    counts["num_disks"] = len((disks_resp.get("data", {}) or {}).get("result", []) or [])

                pools_resp = await self.get(session, "/ugreen/v1/storage/pool/list")
                if isinstance(pools_resp, dict):
                    pools = (pools_resp.get("data", {}) or {}).get("result", []) or []
                    counts["num_pools"] = len(pools)
                    counts["num_volumes"] = sum(len(p.get("volumes", []) or []) for p in pools)

                # 3) NICs / Fans / GPU (stat/get_all)
                stat = await self.get(session, "/ugreen/v1/taskmgr/stat/get_all")
                if isinstance(stat, dict) and stat.get("code") == 200:
                    sdata = (stat.get("data", {}) or {})

                    # NICs (Serie ohne "overview")
                    net_series = ((sdata.get("net", {}) or {}).get("series", []) or [])
                    non_overview = [x for x in net_series if x.get("name") not in ("overview", "Overview", "Übersicht")]
                    counts["num_nics"] = len(non_overview)

                    # Fans (overview kann dict oder list sein)
                    overview = (sdata.get("overview", {}) or {})
                    cpu_fans = overview.get("cpu_fan") or []
                    dev_fans = overview.get("device_fan") or []
                    if isinstance(cpu_fans, dict):
                        cpu_fans = [cpu_fans]
                    if isinstance(dev_fans, dict):
                        dev_fans = [dev_fans]

                    counts["has_cpu_fan"] = len(cpu_fans) > 0
                    counts["num_device_fans"] = len(dev_fans)
                    counts["has_device_fan"] = counts["num_device_fans"] > 0

                    # GPU
                    gpu_series = ((sdata.get("gpu", {}) or {}).get("series", []) or [])
                    counts["has_gpu"] = any((g.get("gpu_name") or "").strip() for g in gpu_series)

                self._dynamic_entity_counts = counts
            except Exception as e:
                _LOGGER.warning("[UGREEN NAS] count_dynamic_entities failed: %s", e)
                self._dynamic_entity_counts = {}
            return self._dynamic_entity_counts


    def get_dynamic_entity_counts(self) -> dict:
        """Return counts of dynamic entities on request."""
        return self._dynamic_entity_counts or {}


    #################################################### DYNAMIC CONFIG ########


    async def get_dynamic_config_entities_mem(self, session: aiohttp.ClientSession) -> List[UgreenEntity]:
        """RAM entities and total from /sysinfo/machine/common (module count from num_rams)."""

        endpoint = "/ugreen/v1/sysinfo/machine/common"
        _LOGGER.debug("[UGREEN NAS] Fetching dynamic mem entities from %s", endpoint)
        data = await self.get(session, endpoint)

        mem_list = data.get("data", {}).get("hardware", {}).get("mem", []) if isinstance(data, dict) else []
        counts = self.get_dynamic_entity_counts() or {}

        n_modules = int(counts.get("num_rams", 0))
        single = (n_modules == 1)
        entities: List[UgreenEntity] = []

        for i in range(n_modules):
            # 1 module: Keys without index (RAM_size); otherwise: RAM1_size, RAM2_size
            prefix_key  = "RAM" if single else f"RAM{i+1}"
            prefix_name = "RAM Module" if single else f"RAM Module {i+1}"

            entities.extend([
                UgreenEntity(
                    description=EntityDescription(
                        key=f"{prefix_key}_model",
                        name=f"{prefix_name} Model",
                        icon="mdi:memory",
                        unit_of_measurement=None,
                    ),
                    endpoint=endpoint,
                    path=f"data.hardware.mem[{i}].model",
                    nas_part_category="Hardware",
                ),
                UgreenEntity(
                    description=EntityDescription(
                        key=f"{prefix_key}_manufacturer",
                        name=f"{prefix_name} Manufacturer",
                        icon="mdi:factory",
                        unit_of_measurement=None,
                    ),
                    endpoint=endpoint,
                    path=f"data.hardware.mem[{i}].manufacturer",
                    nas_part_category="Hardware",
                ),
                UgreenEntity(
                    description=EntityDescription(
                        key=f"{prefix_key}_size",
                        name=f"{prefix_name} Size",
                        icon="mdi:memory",
                        unit_of_measurement=UnitOfInformation.BYTES,
                    ),
                    endpoint=endpoint,
                    path=f"data.hardware.mem[{i}].size",
                    decimal_places=0,
                    nas_part_category="Hardware",
                ),
                UgreenEntity(
                    description=EntityDescription(
                        key=f"{prefix_key}_speed",
                        name=f"{prefix_name} Speed",
                        icon="mdi:speedometer",
                        unit_of_measurement="MHz",
                    ),
                    endpoint=endpoint,
                    path=f"data.hardware.mem[{i}].mhz",
                    decimal_places=0,
                    nas_part_category="Hardware",
                ),
            ])

        # Total comes as virtual entity (calculated in init.py)
        entities.append(
            UgreenEntity(
                description=EntityDescription(
                    key="ram_total_size",
                    name="RAM Total Size",
                    icon="mdi:memory",
                    unit_of_measurement=UnitOfInformation.BYTES,
                ),
                endpoint=endpoint,
                path="calculated:ram_total_size",
                decimal_places=0,
                nas_part_category="Hardware",
            )
        )

        return entities


    async def get_dynamic_config_entities_lan(self, session: aiohttp.ClientSession) -> List[UgreenEntity]:
        """LAN entities from /sysinfo/machine/common (no local counters; derived from response length)."""

        endpoint = "/ugreen/v1/sysinfo/machine/common"
        _LOGGER.debug("[UGREEN NAS] Fetching dynamic LAN entities from %s", endpoint)
        data = await self.get(session, endpoint)

        lan_list = (data or {}).get("data", {}).get("hardware", {}).get("net", []) or []
        if not lan_list:
            _LOGGER.warning("[UGREEN NAS] No 'net' list in %s response", endpoint)
            return []

        # One port: keys without index (LAN_*); otherwise: LAN1_*, LAN2_*, …
        single = len(lan_list) == 1
        entities: List[UgreenEntity] = []

        for i, _ in enumerate(lan_list):
            prefix_key  = "LAN" if single else f"LAN{i+1}"
            prefix_name = "LAN Port" if single else f"LAN Port {i+1}"

            entities.extend([
                UgreenEntity(
                    description=EntityDescription(
                        key=f"{prefix_key}_model",
                        name=f"{prefix_name} Model",
                        icon="mdi:lan",
                        unit_of_measurement=None,
                    ),
                    endpoint=endpoint,
                    path=f"data.hardware.net[{i}].model",
                    nas_part_category="Network",
                ),
                UgreenEntity(
                    description=EntityDescription(
                        key=f"{prefix_key}_ip",
                        name=f"{prefix_name} IP",
                        icon="mdi:lan",
                        unit_of_measurement=None,
                    ),
                    endpoint=endpoint,
                    path=f"data.hardware.net[{i}].ip",
                    nas_part_category="Network",
                ),
                UgreenEntity(
                    description=EntityDescription(
                        key=f"{prefix_key}_mac",
                        name=f"{prefix_name} MAC",
                        icon="mdi:lan",
                        unit_of_measurement=None,
                    ),
                    endpoint=endpoint,
                    path=f"data.hardware.net[{i}].mac",
                    nas_part_category="Network",
                ),
                UgreenEntity(
                    description=EntityDescription(
                        key=f"{prefix_key}_speed",
                        name=f"{prefix_name} Speed",
                        icon="mdi:speedometer",
                        unit_of_measurement=UnitOfDataRate.MEGABITS_PER_SECOND,
                    ),
                    endpoint=endpoint,
                    path=f"data.hardware.net[{i}].speed",
                    decimal_places=0,
                    nas_part_category="Network",
                ),
                UgreenEntity(
                    description=EntityDescription(
                        key=f"{prefix_key}_duplex",
                        name=f"{prefix_name} Duplex",
                        icon="mdi:lan",
                        unit_of_measurement=None,
                    ),
                    endpoint=endpoint,
                    path=f"data.hardware.net[{i}].duplex",
                    nas_part_category="Network",
                ),
                UgreenEntity(
                    description=EntityDescription(
                        key=f"{prefix_key}_mtu",
                        name=f"{prefix_name} MTU",
                        icon="mdi:lan",
                        unit_of_measurement=None,
                    ),
                    endpoint=endpoint,
                    path=f"data.hardware.net[{i}].mtu",
                    decimal_places=0,
                    nas_part_category="Network",
                ),
                UgreenEntity(
                    description=EntityDescription(
                        key=f"{prefix_key}_netmask",
                        name=f"{prefix_name} Netmask",
                        icon="mdi:lan",
                        unit_of_measurement=None,
                    ),
                    endpoint=endpoint,
                    path=f"data.hardware.net[{i}].mask",
                    nas_part_category="Network",
                ),
                
                # <todo>
                # To expose gateway/DNS per interface, add them here analogously:
                # UgreenEntity(... path=f"data.hardware.net[{i}].gateway", ...),
                # UgreenEntity(... path=f"data.hardware.net[{i}].dns", ...),
            ])

        return entities


    async def get_dynamic_config_entities_usb(self, session: aiohttp.ClientSession) -> List[UgreenEntity]:
        """USB devices from /sysinfo/machine/common (no local counters; derived from response list)."""

        endpoint = "/ugreen/v1/sysinfo/machine/common"
        _LOGGER.debug("[UGREEN NAS] Fetching dynamic USB entities from %s", endpoint)
        data = await self.get(session, endpoint)

        usb_list = (data or {}).get("data", {}).get("hardware", {}).get("usb", []) or []
        if not usb_list:
            _LOGGER.debug("[UGREEN NAS] No 'usb' list in %s response", endpoint)
            return []

        # One device: keys without index (USB_device_*); otherwise: USB_device1_*, USB_device2_*, …
        single = len(usb_list) == 1
        entities: List[UgreenEntity] = []

        for i, _ in enumerate(usb_list):
            prefix_key  = "USB_device" if single else f"USB_device{i+1}"
            prefix_name = "USB Device" if single else f"USB Device {i+1}"

            entities.extend([
                UgreenEntity(
                    description=EntityDescription(
                        key=f"{prefix_key}_model",
                        name=f"{prefix_name} Model",
                        icon="mdi:usb-port",
                        unit_of_measurement=None,
                    ),
                    endpoint=endpoint,
                    path=f"data.hardware.usb[{i}].model",
                    nas_part_category="USB",
                ),
                UgreenEntity(
                    description=EntityDescription(
                        key=f"{prefix_key}_vendor",
                        name=f"{prefix_name} Vendor",
                        icon="mdi:usb-port",
                        unit_of_measurement=None,
                    ),
                    endpoint=endpoint,
                    path=f"data.hardware.usb[{i}].vendor",
                    nas_part_category="USB",
                ),
                UgreenEntity(
                    description=EntityDescription(
                        key=f"{prefix_key}_type",
                        name=f"{prefix_name} Type",
                        icon="mdi:usb-port",
                        unit_of_measurement=None,
                    ),
                    endpoint=endpoint,
                    path=f"data.hardware.usb[{i}].device_type",
                    nas_part_category="USB",
                ),
            ])

        return entities


    async def get_dynamic_config_entities_ups(self, session: aiohttp.ClientSession) -> List[UgreenEntity]:
        """UPS config entities (optional) driven by has_ups count."""

        counts = self.get_dynamic_entity_counts() or {}
        if not counts.get("has_ups"):
            _LOGGER.debug("[UGREEN NAS] No UPS present (has_ups=False) – skipping UPS config entities")
            return []

        endpoint = "/ugreen/v1/sysinfo/machine/common"
        _LOGGER.debug("[UGREEN NAS] Fetching UPS info from %s", endpoint)
        data = await self.get(session, endpoint)

        # Exactly one UPS supported: take index 0
        entities: List[UgreenEntity] = []
        entities.extend([
            UgreenEntity(
                description=EntityDescription(
                    key="ups_model",
                    name="UPS Model",
                    icon="mdi:power-plug-battery",
                    unit_of_measurement=None,
                ),
                endpoint=endpoint,
                path="data.hardware.ups[0].model",
                nas_part_category="Hardware",
            ),
            UgreenEntity(
                description=EntityDescription(
                    key="ups_vendor",
                    name="UPS Vendor",
                    icon="mdi:factory",
                    unit_of_measurement=None,
                ),
                endpoint=endpoint,
                path="data.hardware.ups[0].vendor",
                nas_part_category="Hardware",
            ),
            UgreenEntity(
                description=EntityDescription(
                    key="ups_power_free",
                    name="UPS Power Remaining",
                    icon="mdi:power-plug-battery",
                    unit_of_measurement=None,  # comes as a string like '100%'
                ),
                endpoint=endpoint,
                path="data.hardware.ups[0].power_free",
                nas_part_category="Hardware",
            ),
        ])

        return entities


    async def get_dynamic_config_entities_storage(self, session: aiohttp.ClientSession) -> List[UgreenEntity]:
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
                        nas_part_category="Pools",
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
                        nas_part_category="Pools",
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
                        nas_part_category="Pools",
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
                        nas_part_category="Pools",
                    ),
                    UgreenEntity(
                        description=EntityDescription(
                            key=f"{prefix_pool_key}_total",
                            name=f"{prefix_pool_name} Total Size",
                            icon="mdi:database",
                            unit_of_measurement=UnitOfInformation.BYTES,
                        ),
                        endpoint=endpoint,
                        path=f"data.result[{pool_index}].total",
                        nas_part_category="Pools",
                    ),
                    UgreenEntity(
                        description=EntityDescription(
                            key=f"{prefix_pool_key}_used",
                            name=f"{prefix_pool_name} Used Size",
                            icon="mdi:database-check",
                            unit_of_measurement=UnitOfInformation.BYTES,
                        ),
                        endpoint=endpoint,
                        path=f"data.result[{pool_index}].used",
                        nas_part_category="Pools",
                    ),
                    UgreenEntity(
                        description=EntityDescription(
                            key=f"{prefix_pool_key}_free",
                            name=f"{prefix_pool_name} Free Size",
                            icon="mdi:database-remove",
                            unit_of_measurement=UnitOfInformation.BYTES,
                        ),
                        endpoint=endpoint,
                        path=f"data.result[{pool_index}].free",
                        nas_part_category="Pools",
                    ),
                    UgreenEntity(
                        description=EntityDescription(
                            key=f"{prefix_pool_key}_available",
                            name=f"{prefix_pool_name} Available Size",
                            icon="mdi:database-plus",
                            unit_of_measurement=UnitOfInformation.BYTES,
                        ),
                        endpoint=endpoint,
                        path=f"data.result[{pool_index}].available",
                        nas_part_category="Pools",
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
                        nas_part_category="Pools",
                    ),
                ])

                # Disk-Details über globale Diskliste (nur Cache pflegen, keine Zähler setzen)
                if not hasattr(self, "_ugreen_disks_cache"):
                    disk_response = await self.get(session, "/ugreen/v2/storage/disk/list")
                    disks_global = (disk_response or {}).get("data", {}).get("result", []) if isinstance(disk_response, dict) else []
                    self._ugreen_disks_cache = {
                        d.get("dev_name"): (idx, d) for idx, d in enumerate(disks_global)
                    }

                for pool_disk_index, disk_ref in enumerate(pool.get("disks", []) or []):
                    dev_name = disk_ref.get("dev_name")
                    match = self._ugreen_disks_cache.get(dev_name)
                    if match is None:
                        _LOGGER.warning("[UGREEN NAS] Disk with dev_name '%s' not found in global disk list, skipping.", dev_name)
                        continue
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
                            nas_part_category="Disks",
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
                            nas_part_category="Disks",
                        ),
                        UgreenEntity(
                            description=EntityDescription(
                                key=f"{prefix_disk_key}_size",
                                name=f"{prefix_disk_name} Size",
                                icon="mdi:database",
                                unit_of_measurement=UnitOfInformation.BYTES,
                            ),
                            endpoint=endpoint_disk,
                            path=f"data.result[{disk_index}].size",
                            nas_part_category="Disks",
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
                            nas_part_category="Disks",
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
                            nas_part_category="Disks",
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
                            nas_part_category="Disks",
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
                            nas_part_category="Disks",
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
                            nas_part_category="Disks",
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
                            nas_part_category="Disks",
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
                            nas_part_category="Disks",
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
                            nas_part_category="Disks",
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
                            nas_part_category="Disks",
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
                            nas_part_category="Disks",
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
                            nas_part_category="Disks",
                        ),
                    ])

                for volume_index, _ in enumerate(pool.get("volumes", []) or []):
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
                            nas_part_category="Volumes",
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
                            nas_part_category="Volumes",
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
                            nas_part_category="Volumes",
                        ),
                        UgreenEntity(
                            description=EntityDescription(
                                key=f"{prefix_volume_key}_total",
                                name=f"{prefix_volume_name} Total Size",
                                icon="mdi:database",
                                unit_of_measurement=UnitOfInformation.BYTES,
                            ),
                            endpoint=endpoint,
                            path=f"data.result[{pool_index}].volumes[{volume_index}].total",
                            nas_part_category="Volumes",
                        ),
                        UgreenEntity(
                            description=EntityDescription(
                                key=f"{prefix_volume_key}_used",
                                name=f"{prefix_volume_name} Used Size",
                                icon="mdi:database-check",
                                unit_of_measurement=UnitOfInformation.BYTES,
                            ),
                            endpoint=endpoint,
                            path=f"data.result[{pool_index}].volumes[{volume_index}].used",
                            nas_part_category="Volumes",
                        ),
                        UgreenEntity(
                            description=EntityDescription(
                                key=f"{prefix_volume_key}_available",
                                name=f"{prefix_volume_name} Available Size",
                                icon="mdi:database-plus",
                                unit_of_measurement=UnitOfInformation.BYTES,
                            ),
                            endpoint=endpoint,
                            path=f"data.result[{pool_index}].volumes[{volume_index}].available",
                            nas_part_category="Volumes",
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
                            nas_part_category="Volumes",
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
                            nas_part_category="Volumes",
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
                            nas_part_category="Volumes",
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
                            nas_part_category="Volumes",
                        ),
                    ])
        except Exception as e:
            _LOGGER.error("[UGREEN NAS] Error while building dynamic storage entities: %s", e)

        return entities

    #################################################### DYNAMIC STAUTS ########


    async def get_dynamic_status_entities_fan(self) -> List[UgreenEntity]:
        """Return list of fan-related dynamic status entities from taskmgr."""
        entities: List[UgreenEntity] = []
        counts = self.get_dynamic_entity_counts() or {}

        # CPU fan: gibt es nur 0 oder 1
        if counts.get("has_cpu_fan"):
            label = "CPU Fan"
            entities.append(UgreenEntity(
                description=EntityDescription(
                    key="cpu_fan_speed",
                    name=label,
                    icon="mdi:fan",
                    unit_of_measurement=REVOLUTIONS_PER_MINUTE,
                ),
                endpoint="/ugreen/v1/taskmgr/stat/get_all",
                path="data.overview.cpu_fan[0].speed",
                nas_part_category="Status",
            ))
            entities.append(UgreenEntity(
                description=EntityDescription(
                    key="cpu_fan_status",
                    name=f"{label} Status",
                    icon="mdi:fan-alert",
                    unit_of_measurement=None,
                ),
                endpoint="/ugreen/v1/taskmgr/stat/get_all",
                path="data.overview.cpu_fan[0].status",
                nas_part_category="Status",
            ))

        # Device fans
        n_dev = int(counts.get("num_device_fans", 0))
        for i in range(n_dev):
            single = (n_dev == 1)
            label  = "Device Fan" if single else f"Device Fan {i+1}"
            key    = "device_fan_speed" if single else f"device_fan{i+1}_speed"
            entities.append(UgreenEntity(
                description=EntityDescription(
                    key=key,
                    name=label,
                    icon="mdi:fan",
                    unit_of_measurement=REVOLUTIONS_PER_MINUTE,
                ),
                endpoint="/ugreen/v1/taskmgr/stat/get_all",
                path=f"data.overview.device_fan[{i}].speed",
                nas_part_category="Status",
            ))
            status_key = "device_fan_status" if single else f"device_fan{i+1}_status"
            entities.append(UgreenEntity(
                description=EntityDescription(
                    key=status_key,
                    name=f"{label} Status",
                    icon="mdi:fan-alert",
                    unit_of_measurement=None,
                ),
                endpoint="/ugreen/v1/taskmgr/stat/get_all",
                path=f"data.overview.device_fan[{i}].status",
                nas_part_category="Status",
            ))

        # Overall fan status
        entities.append(UgreenEntity(
            description=EntityDescription(
                key="fan_status_overall",
                name="Fan Status (overall)",
                icon="mdi:fan-alert",
                unit_of_measurement=None,
            ),
            endpoint="/ugreen/v1/desktop/components/data?id=desktop.component.TemperatureMonitoring",
            path="data.fan_status",
            nas_part_category="Status",
        ))

        return entities


    async def get_dynamic_status_entities_lan(self) -> List[UgreenEntity]:
        """Return upload/download status entities from taskmgr (per NIC)."""
        entities: List[UgreenEntity] = []
        n = int(self.get_dynamic_entity_counts().get("num_nics", 0))
        for i in range(n):
            idx = i + 1  # 0 = overview, daher +1
            label = f"LAN {idx}"
            prefix = f"lan{idx}"
            entities.extend([
                UgreenEntity(
                    description=EntityDescription(
                        key=f"{prefix}_upload_raw",
                        name=f"{label} Upload (raw)",
                        icon="mdi:upload-network",
                        unit_of_measurement=UnitOfDataRate.BYTES_PER_SECOND,
                    ),
                    endpoint="/ugreen/v1/taskmgr/stat/get_all",
                    path=f"data.net.series[{idx}].send_rate",
                    decimal_places=0,
                    nas_part_category="Status",
                ),
                UgreenEntity(
                    description=EntityDescription(
                        key=f"{prefix}_upload",
                        name=f"{label} Upload",
                        icon="mdi:upload-network",
                        unit_of_measurement=None,
                    ),
                    endpoint="/ugreen/v1/taskmgr/stat/get_all",
                    path=f"calculated:scale_bytes_per_second:data.net.series[{idx}].send_rate",
                    decimal_places=0,
                    nas_part_category="Status",
                ),
                UgreenEntity(
                    description=EntityDescription(
                        key=f"{prefix}_download_raw",
                        name=f"{label} Download (raw)",
                        icon="mdi:download-network",
                        unit_of_measurement=UnitOfDataRate.BYTES_PER_SECOND,
                    ),
                    endpoint="/ugreen/v1/taskmgr/stat/get_all",
                    path=f"data.net.series[{idx}].recv_rate",
                    decimal_places=0,
                    nas_part_category="Status",
                ),
                UgreenEntity(
                    description=EntityDescription(
                        key=f"{prefix}_download",
                        name=f"{label} Download",
                        icon="mdi:download-network",
                        unit_of_measurement=None,
                    ),
                    endpoint="/ugreen/v1/taskmgr/stat/get_all",
                    path=f"calculated:scale_bytes_per_second:data.net.series[{idx}].recv_rate",
                    decimal_places=0,
                    nas_part_category="Status",
                ),
            ])
        return entities


    async def get_dynamic_status_entities_storage(self) -> List[UgreenEntity]:
        """Return list of disk-related dynamic status entities (uses dynamic_entity_counts)."""
        entities: List[UgreenEntity] = []
        counts = self.get_dynamic_entity_counts() or {}
        n_disks = int(counts.get("num_disks", 0))

        for i in range(n_disks):
            idx = i + 1  # series[0] == overview; echte Disks starten bei 1
            prefix = f"disk{idx}"

            entities.extend([
                UgreenEntity(
                    description=EntityDescription(
                        key=f"{prefix}_read_rate_raw",
                        name=f"Disk {idx} Read Rate (raw)",
                        icon="mdi:download",
                        unit_of_measurement=UnitOfDataRate.BYTES_PER_SECOND,
                    ),
                    endpoint="/ugreen/v1/taskmgr/stat/get_all",
                    path=f"data.disk.series[{idx}].read_rate",
                    decimal_places=0,
                    nas_part_category="Status",
                ),
                UgreenEntity(
                    description=EntityDescription(
                        key=f"{prefix}_read_rate",
                        name=f"Disk {idx} Read Rate",
                        icon="mdi:download",
                        unit_of_measurement=None,  # skaliert (human readable)
                    ),
                    endpoint="/ugreen/v1/taskmgr/stat/get_all",
                    path=f"calculated:scale_bytes_per_second:data.disk.series[{idx}].read_rate",
                    decimal_places=0,
                    nas_part_category="Status",
                ),
                UgreenEntity(
                    description=EntityDescription(
                        key=f"{prefix}_write_rate_raw",
                        name=f"Disk {idx} Write Rate (raw)",
                        icon="mdi:upload",
                        unit_of_measurement=UnitOfDataRate.BYTES_PER_SECOND,
                    ),
                    endpoint="/ugreen/v1/taskmgr/stat/get_all",
                    path=f"data.disk.series[{idx}].write_rate",
                    decimal_places=0,
                    nas_part_category="Status",
                ),
                UgreenEntity(
                    description=EntityDescription(
                        key=f"{prefix}_write_rate",
                        name=f"Disk {idx} Write Rate",
                        icon="mdi:upload",
                        unit_of_measurement=None,  # skaliert (human readable)
                    ),
                    endpoint="/ugreen/v1/taskmgr/stat/get_all",
                    path=f"calculated:scale_bytes_per_second:data.disk.series[{idx}].write_rate",
                    decimal_places=0,
                    nas_part_category="Status",
                ),
                UgreenEntity(
                    description=EntityDescription(
                        key=f"{prefix}_temperature",
                        name=f"Disk {idx} Temperature",
                        icon="mdi:thermometer",
                        unit_of_measurement="°C",
                    ),
                    endpoint="/ugreen/v1/taskmgr/stat/get_all",
                    path=f"data.disk.series[{idx}].temperature",
                    decimal_places=1,
                    nas_part_category="Status",
                ),
            ])

        return entities
