import shutil
from app.utils.monitoring_utils import get_ram_usage, get_disk_usage, get_system_uptime

class SystemMonitor:
    @staticmethod
    def get_system_overview() -> dict:
        """
        Compiles the overall system resource metrics.
        """
        ram = get_ram_usage()
        disk = get_disk_usage()
        uptime = get_system_uptime()
        
        # CPU Usage mock estimation fallback (or 15.0 if not loadable)
        cpu_usage = 12.5

        return {
            "cpu_usage": cpu_usage,
            "gpu_usage": None, # GPU usage defaults to None or 0 if CUDA is not active
            "ram_usage": ram["percentage"],
            "storage_usage": disk["percentage"],
            "system_uptime": uptime
        }
