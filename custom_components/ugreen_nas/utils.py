from typing import Optional, Tuple, Any, Union
from datetime import datetime
from decimal import Decimal

from .api import UgreenEntity


from decimal import Decimal, ROUND_HALF_UP
from typing import Any, Optional, Tuple

def format_bytes(
    size_bytes: Optional[float], 
    decimal_places: int = 2
) -> Optional[Tuple[Decimal, str]]:
    """Format bytes into a human-readable format with configurable decimal places."""
    try:
        if size_bytes is None:
            return None
        size = Decimal(size_bytes)
        for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
            if size < 1024:
                quantize_str = f'1.{"0" * decimal_places}'
                return size.quantize(Decimal(quantize_str), rounding=ROUND_HALF_UP), unit
            size /= Decimal(1024)
        # Falls größer als PB:
        quantize_str = f'1.{"0" * decimal_places}'
        return size.quantize(Decimal(quantize_str), rounding=ROUND_HALF_UP), 'PB'
    except Exception:
        return None

def format_gb_value(
    raw: Any, 
    decimal_places: int = 2
) -> Decimal:
    """
    Format a raw value in Bytes to GB with configurable decimal places.
    If the input is already in Bytes, divide by 1024^3.
    """
    if raw is None:
        return Decimal(0)
    try:
        bytes_val = Decimal(str(raw).replace(",", "."))
        gb_val = bytes_val / Decimal(1024 ** 3)
        quantize_str = f'1.{"0" * decimal_places}'
        return gb_val.quantize(Decimal(quantize_str), rounding=ROUND_HALF_UP)
    except Exception:
        return Decimal(0)

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

def format_bytes_per_second(
    size_bytes: Optional[float],
    decimal_places: int = 2
) -> Decimal:
    """Convert Bytes to MB/s with configurable decimal places, without unit."""
    if size_bytes is None:
        return Decimal(0)
    try:
        size = Decimal(size_bytes)
        mb_per_s = size / Decimal(1024 ** 2)
        quantize_str = f'1.{"0" * decimal_places}'
        mb_per_s = mb_per_s.quantize(Decimal(quantize_str), rounding=ROUND_HALF_UP)
        return mb_per_s
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
            return format_gb_value(raw, endpoint.decimal_places)

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
            
        if "usb_device_type" in endpoint.description.key:
            return format_status_code(raw, {
                0: "Generic USB Device",   # 0 = External HDD?
            })

        if endpoint.description.unit_of_measurement is not None and endpoint.description.unit_of_measurement == "%":
            return format_percentage(raw)

        if endpoint.description.unit_of_measurement is not None and endpoint.description.unit_of_measurement == "°C":
            return format_temperature(raw)

        if endpoint.description.unit_of_measurement is not None and endpoint.description.unit_of_measurement in ("MB/s", "KB/s", "GB/s"):
            return format_bytes_per_second(raw, endpoint.decimal_places)
        
        if endpoint.description.unit_of_measurement is not None and endpoint.description.unit_of_measurement == "MHz":
            return format_frequency_mhz(raw)

        if "fan" in endpoint.description.key and "status" in endpoint.description.key:
            return format_status_code(raw, {0: "off", 1: "on"})
        
        return convert_string_to_number(raw, endpoint.decimal_places)

    except Exception:
        return Decimal(0)
