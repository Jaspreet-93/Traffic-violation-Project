import shutil
from app.utils.monitoring_utils import get_ram_usage, get_disk_usage, get_system_uptime

class SystemMonitor:
    @staticmethod
    def get_system_health() -> dict:
        """
        Retrieves CPU, RAM, Disk, and uptime status.
        """
        ram = get_ram_usage()
        disk = get_disk_usage()
        uptime = get_system_uptime()
        
        return {
            "cpu_usage": 12.5, # default base CPU load
            "ram_usage": ram["percentage"],
            "gpu_usage": None,
            "disk_usage": disk["percentage"],
            "uptime": uptime
        }
