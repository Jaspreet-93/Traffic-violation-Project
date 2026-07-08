import os
import platform
import shutil
import time
import sys
from app.core.logger import logger

START_TIME = time.time()

def get_system_uptime() -> str:
    """
    Returns system uptime duration formatted as string.
    """
    diff_sec = int(time.time() - START_TIME)
    hours, remainder = divmod(diff_sec, 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    if days > 0:
        return f"{days}d {hours}h {minutes}m {seconds}s"
    return f"{hours}h {minutes}m {seconds}s"

def get_cpu_cores() -> int:
    """
    Returns the total number of physical CPU cores.
    """
    try:
        return os.cpu_count() or 1
    except Exception:
        return 1

def get_disk_usage() -> dict:
    """
    Returns disk storage metrics (total_gb, used_gb, percentage).
    """
    try:
        total, used, free = shutil.disk_usage("/")
        total_gb = round(total / (1024 ** 3), 1)
        used_gb = round(used / (1024 ** 3), 1)
        percentage = round((used / total) * 100, 1)
        return {
            "total_gb": total_gb,
            "used_gb": used_gb,
            "percentage": percentage
        }
    except Exception as e:
        logger.error(f"Error reading disk usage: {e}")
        return {
            "total_gb": 0.0,
            "used_gb": 0.0,
            "percentage": 0.0
        }

def get_ram_usage() -> dict:
    """
    Returns RAM memory usage metrics.
    """
    # Fallback default values
    ram_total_gb = 16.0
    ram_used_gb = 4.0
    percentage = 25.0

    try:
        if sys.platform == "win32":
            # Using ctypes to get memory info on Windows
            import ctypes
            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [
                    ("dwLength", ctypes.c_ulong),
                    ("dwMemoryLoad", ctypes.c_ulong),
                    ("ullTotalPhys", ctypes.c_uint64),
                    ("ullAvailPhys", ctypes.c_uint64),
                    ("ullTotalPageFile", ctypes.c_uint64),
                    ("ullAvailPageFile", ctypes.c_uint64),
                    ("ullTotalVirtual", ctypes.c_uint64),
                    ("ullAvailVirtual", ctypes.c_uint64),
                    ("ullAvailExtendedVirtual", ctypes.c_uint64)
                ]
            stat = MEMORYSTATUSEX()
            stat.dwLength = ctypes.sizeof(stat)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
            
            ram_total_gb = round(stat.ullTotalPhys / (1024 ** 3), 1)
            avail_gb = stat.ullAvailPhys / (1024 ** 3)
            ram_used_gb = round(ram_total_gb - avail_gb, 1)
            percentage = float(stat.dwMemoryLoad)
        else:
            # Unix /proc/meminfo parsing
            with open('/proc/meminfo', 'r') as f:
                lines = f.readlines()
            mem_total = 0
            mem_free = 0
            mem_cached = 0
            mem_buffers = 0
            for line in lines:
                if 'MemTotal' in line:
                    mem_total = int(line.split()[1])
                elif 'MemFree' in line:
                    mem_free = int(line.split()[1])
                elif 'Cached' in line:
                    mem_cached = int(line.split()[1])
                elif 'Buffers' in line:
                    mem_buffers = int(line.split()[1])
            if mem_total > 0:
                ram_total_gb = round(mem_total / (1024 * 1024), 1)
                actual_free = mem_free + mem_cached + mem_buffers
                ram_used_gb = round((mem_total - actual_free) / (1024 * 1024), 1)
                percentage = round(((mem_total - actual_free) / mem_total) * 100, 1)
    except Exception as e:
        logger.warning(f"Failed to read real RAM info, using mock fallbacks: {e}")
        
    return {
        "total_gb": ram_total_gb,
        "used_gb": ram_used_gb,
        "percentage": percentage
    }
