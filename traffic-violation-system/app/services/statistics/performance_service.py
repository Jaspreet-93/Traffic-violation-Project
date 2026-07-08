class PerformanceService:
    @staticmethod
    def get_performance_metrics() -> dict:
        return {
            "uptime_percentage": 99.98,
            "gpu_utilization_pct": 64.5,
            "memory_utilization_pct": 42.1,
            "disk_write_speed_mbps": 185.4,
            "model_inference_latencies_ms": {
                "yolov8n": 8.5,
                "helmet_classifier": 4.2,
                "ocr_reader": 12.4
            }
        }
