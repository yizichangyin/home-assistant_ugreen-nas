from typing import Optional, Any, Union
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from typing import Any, Optional
from .api import UgreenEntity

def format_dynamic_size(
    raw: Any,
    input_unit: str = 'B',
    decimal_places: int = 2
) -> Optional[Decimal]:
    """Format bytes into a human-readable format with configurable decimal places."""
    try:
        if raw is None or input_unit not in ("B", "KB", "MB", "GB", "TB", "PB"):
            return None
        
        size = Decimal(str(raw).replace(",", "."))
        exponent_map = {'B': 0, 'KB': 1, 'MB': 2, 'GB': 3, 'TB': 4, 'PB': 5}
        exponent = exponent_map[input_unit]

        size_bytes = size * (Decimal(1024) ** exponent)
        
        for _ in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
            if size_bytes < 1024:
                quantize_str = f'1.{"0" * decimal_places}'
                return size_bytes.quantize(Decimal(quantize_str), rounding=ROUND_HALF_UP)
            size_bytes /= Decimal(1024)

        quantize_str = f'1.{"0" * decimal_places}'
        return size_bytes.quantize(Decimal(quantize_str), rounding=ROUND_HALF_UP)

    except Exception:
        return None

def determine_unit(
    raw: Any,
    input_unit: str = 'B',
    per_second: bool = False
) -> str:
    """Determine the appropriate unit for a given size in bytes."""
        
    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    
    if per_second:
        input_unit = input_unit.replace("/s", "") if input_unit.endswith("/s") else input_unit

    if input_unit not in units:
        return "Unknown unit"

    unit_index = units.index(input_unit)

    try:
        size = Decimal(raw) if isinstance(raw, (int, float, Decimal)) else Decimal(str(raw).replace(",", "."))
    except Exception:
        size = Decimal(0)

    while unit_index < len(units) - 1 and size >= 1024:
        size /= Decimal(1024)
        unit_index += 1

    unit_str = f"{units[unit_index]}/s" if per_second else units[unit_index]
    return unit_str

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
        # return Decimal(str(round(float(raw), 1)))
        # changed, temps are reported in full °C
        return int(round(float(raw)))
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
#    return str(value)
    return value

def format_sensor_value(raw: Any, endpoint: UgreenEntity) -> Any:
    """Format a raw value based on the endpoint definition."""
    try:
        if endpoint.description.unit_of_measurement is not None and endpoint.description.unit_of_measurement in ("B", "KB", "MB", "GB", "TB"):
            return format_dynamic_size(raw, endpoint.description.unit_of_measurement, endpoint.decimal_places)

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
            

        if "fan" in endpoint.description.key and "overall" in endpoint.description.key:
            return format_status_code(raw, {
                0: "Normal",
            })

        if "fan" in endpoint.description.key and "status" in endpoint.description.key:
            return format_status_code(raw, {
                0: "ERROR!",
                1: "Normal",
            })

        if "disk" in endpoint.description.key and not "interface" in endpoint.description.key and "type" in endpoint.description.key:
            return format_status_code(raw, {
                0: "HDD",
                1: "SSD",
                2: "M.2",
            })
            
        if "volume" in endpoint.description.key and "health" in endpoint.description.key:
            return format_status_code(raw, {
                0: "Normal",
            })
            
        if "usb_device_type" in endpoint.description.key:
            return format_status_code(raw, {
                0: "Generic USB Device",   # 0 = External HDD?
            })

        # if "status" in endpoint.description.key:
        #     return format_status_code(raw, {
        #         0: "Normal",
        #     })

        if endpoint.description.unit_of_measurement is not None and endpoint.description.unit_of_measurement == "%":
            return format_percentage(raw)

        if endpoint.description.unit_of_measurement is not None and endpoint.description.unit_of_measurement == "°C":
            return format_temperature(raw)

        if endpoint.description.unit_of_measurement is not None and endpoint.description.unit_of_measurement in ("KB/s", "MB/s", "GB/s"):
            return format_dynamic_size(raw, endpoint.description.unit_of_measurement, endpoint.decimal_places)

        if endpoint.description.unit_of_measurement is not None and endpoint.description.unit_of_measurement == "MHz":
            return format_frequency_mhz(raw)
        
        return convert_string_to_number(raw, endpoint.decimal_places)

    except Exception:
        return Decimal(0)

#########

def scale_bytes_per_second(raw: Any) -> Optional[str]:
    # Convert raw Bps value to a human-readable string like '316.45 MB/s'.
    # Normally, transfer speeds are specified in bps / bits per second, e.g. 10Gbps.
    # However, the UGOS API is actually reporting in *Bytes* per second.
    # This has been tested/verified in Windows Explorer by copying huge files.
    # Also, the UGOS web interface displays values in **BYTES** ("B", not "b") per second.
    try:
        if raw is None:
            return None
        bytes_per_second = Decimal(str(raw).replace(",", "."))
        units = ["B/s", "kB/s", "MB/s", "GB/s", "TB/s"]
        unit_index = 0
        while bytes_per_second >= 1024 and unit_index < len(units) - 1:
            bytes_per_second /= 1024
            unit_index += 1
        value = int(bytes_per_second.to_integral_value(rounding=ROUND_HALF_UP))
        return f"{value} {units[unit_index]}"
    except Exception:
        return None


def extract_value_from_path(data: dict, path: str) -> Any:
    # Extract a value from nested dictionary/list structure using dot and index notation.
    try:
        parts = path.split(".")
        value: Any = data
        for part in parts:
            if "[" in part and "]" in part:
                part_name, index = part[:-1].split("[")
                value = value.get(part_name, []) if isinstance(value, dict) else []
                value = value[int(index)] if isinstance(value, list) else None
            else:
                value = value.get(part) if isinstance(value, dict) else None
        return value
    except Exception:
        return None
