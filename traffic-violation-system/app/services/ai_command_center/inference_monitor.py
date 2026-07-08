from app.utils.performance_utils import performance_tracker
from app.utils.monitoring_utils import get_ram_usage, get_disk_usage

class InferenceMonitor:
    @staticmethod
    def get_performance_status() -> dict:
        """
        Gathers live FPS, latency, and system memory load rates.
        """
        ram = get_ram_usage()
        disk = get_disk_usage()
        
        # Calculate inference time as the average vehicle detection latency
        avg_inference = performance_tracker.get_average_inference_time("yolo_vehicle")

        return {
            "fps": round(performance_tracker.get_current_fps(), 1),
            "inference_time": round(avg_inference, 1),
            "cpu_usage": 12.5, # default base load
            "gpu_usage": None,
            "ram_usage": ram["percentage"],
            "disk_usage": disk["percentage"],
            "api_response_time": round(performance_tracker.get_avg_api_response_time(), 1),
            "queue_size": performance_tracker.get_queue_size()
        }
