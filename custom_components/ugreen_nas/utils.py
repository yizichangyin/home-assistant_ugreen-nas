from typing import Optional, Tuple, Any, Union
from datetime import datetime
from decimal import Decimal
from .api import UgreenEntity


def format_bytes(size_bytes: Optional[float]) -> Optional[Tuple[float, str]]:
    """Format bytes into a human-readable format."""
    try:
        if size_bytes is None:
            return None
        size = float(size_bytes)
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return round(size, 2), unit
            size /= 1024
        return round(size, 2), 'PB'
    except Exception:
        return None


def format_duration(seconds: float) -> str:
    """Format seconds into a human-readable duration."""
    try:
        seconds = float(seconds)
        if seconds < 60:
            return f"{int(seconds)} s"
        elif seconds < 3600:
            return f"{seconds / 60:.1f} min"
        elif seconds < 86400:
            return f"{seconds / 3600:.1f} h"
        else:
            return f"{seconds / 86400:.1f} d"
    except Exception:
        return str(seconds)


def format_gb_value(raw: Any) -> Decimal:
    """Format a raw value in GB to a Decimal representation."""
    if raw is None:
        return Decimal(0)
    try:
        mb = Decimal(str(raw).replace(",", "."))
        bytes_val = mb * Decimal(1024 * 1024)
        formatted = format_bytes(float(bytes_val))
        return Decimal(str(round(formatted[0], 2))) if formatted else Decimal(0)
    except Exception:
        return Decimal(0)


def format_temperature(raw: Any) -> Decimal:
    """Format a raw temperature value to a Decimal representation."""
    if raw is None:
        return Decimal(0)
    try:
        return Decimal(str(round(float(raw), 1)))
    except Exception:
        return Decimal(0)


def format_percentage(raw: Any) -> Decimal:
    """Format a raw percentage value to a Decimal representation."""
    if raw is None:
        return Decimal(0)
    try:
        return Decimal(str(round(float(raw), 1)))
    except Exception:
        return Decimal(0)


def format_speed(raw: Any) -> Decimal:
    """Format a raw speed value to a Decimal representation."""
    if raw is None:
        return Decimal(0)
    try:
        return Decimal(str(round(float(raw), 2)))
    except Exception:
        return Decimal(0)


def format_timestamp(raw: Any) -> str:
    """Format a raw timestamp value to a human-readable string."""
    if raw is None:
        return "N/A"
    try:
        dt = datetime.fromtimestamp(float(raw))
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return "Invalid timestamp"


def format_status_code(raw: Any, status_map: dict[int, str]) -> str:
    """Format a raw status code to a human-readable string."""
    try:
        return status_map.get(int(raw), f"Unknown status: {raw}")
    except (ValueError, TypeError):
        return f"Invalid value: {raw}"


def format_frequency_mhz(raw: Any) -> Any:
    """Convert a string like '4800 MHz' or '4800MHz' to an integer."""
    if isinstance(raw, str) and "MHz" in raw:
        cleaned = raw.replace("MHz", "").strip()
        if cleaned.isdigit():
            return int(cleaned)
    return raw


def convert_string_to_number(value: Union[str, int, float, Decimal], decimal_places: int) -> Union[int, float, Decimal, str]:
    """Convert a string to a number (int, float, or Decimal) if possible."""
    if isinstance(value, str):
        value = value.strip().replace(",", ".")
        if not value:
            return value 
        try:
            if '.' in value:
                return round(float(value), decimal_places)
            else:
                return int(value)
        except ValueError:
            try:
                return round(Decimal(value), decimal_places)
            except Exception:
                return str(value) 
    return str(value)  


def format_sensor_value(raw: Any, endpoint: UgreenEntity) -> Any:
    """Format a raw value based on the endpoint definition."""
    try:
        if endpoint.description.unit_of_measurement is not None and endpoint.description.unit_of_measurement in ("MB", "GB", "TB"):
            return format_gb_value(raw)

        if isinstance(endpoint.description.name, str) and "Timestamp" in endpoint.description.name:
            return format_timestamp(raw)

        if "server_status" in endpoint.description.key:
            return format_status_code(raw, {
                2: "Normal",
            })

        if "disk" in endpoint.description.key and "status" in endpoint.description.key:
            return format_status_code(raw, {
                1: "Normal",
            })
            
        if "status" in endpoint.description.key:
            return format_status_code(raw, {
                0: "Normal",
            })
            
        if "disk" in endpoint.description.key and not "interface" in endpoint.description.key and "type" in endpoint.description.key:
            return format_status_code(raw, {
                0: "HDD",
                1: "SSD",
                2: "NVMe",
            })
            
        if "volume" in endpoint.description.key and "health" in endpoint.description.key:
            return format_status_code(raw, {
                0: "Normal",
            })

        if endpoint.description.unit_of_measurement is not None and endpoint.description.unit_of_measurement == "%":
            return format_percentage(raw)

        if endpoint.description.unit_of_measurement is not None and endpoint.description.unit_of_measurement == "°C":
            return format_temperature(raw)

        if endpoint.description.unit_of_measurement is not None and endpoint.description.unit_of_measurement in ("MB/s", "KB/s", "GB/s"):
            return format_speed(raw)

        if endpoint.description.unit_of_measurement is not None and endpoint.description.unit_of_measurement == "MHz":
            return format_frequency_mhz(raw)

        if endpoint.path == "_dummy_total_ram":
            mem_list = raw.get("data", {}).get("hardware", {}).get("mem", [])
            if isinstance(mem_list, list):
                total_size_bytes = sum(
                    module.get("size", 0)
                    for module in mem_list
                    if isinstance(module, dict)
                )
                return int(round(total_size_bytes / 1024 / 1024 / 1024))
            return 0

        return convert_string_to_number(raw, endpoint.decimal_places)

    except Exception:
        return Decimal(0)
