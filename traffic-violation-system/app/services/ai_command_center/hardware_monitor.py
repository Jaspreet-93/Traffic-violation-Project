import time
from app.utils.monitoring_utils import get_cpu_cores, get_ram_usage, get_disk_usage, START_TIME

class HardwareMonitor:
    @staticmethod
    def get_hardware_status() -> dict:
        """
        Retrieves hardware parameters including cores, RAM, and Disk storage metrics.
        """
        ram = get_ram_usage()
        disk = get_disk_usage()
        uptime_sec = time.time() - START_TIME

        return {
            "overall_status": "Healthy",
            "uptime_seconds": round(uptime_sec, 1),
            "cpu_cores": get_cpu_cores(),
            "ram_total_gb": ram["total_gb"],
            "ram_used_gb": ram["used_gb"],
            "disk_total_gb": disk["total_gb"],
            "disk_used_gb": disk["used_gb"],
            "gpu_name": None,
            "gpu_memory_total_mb": None
        }
