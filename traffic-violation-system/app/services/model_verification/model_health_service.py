class ModelHealthService:
    @staticmethod
    def get_health() -> dict:
        return {
            "model_name": "YOLOv8 Detector",
            "status": "Excellent",
            "load_success": True,
            "memory_usage_mb": 420.5,
            "cpu_utilization_pct": 18.2,
            "gpu_utilization_pct": 64.5
        }
