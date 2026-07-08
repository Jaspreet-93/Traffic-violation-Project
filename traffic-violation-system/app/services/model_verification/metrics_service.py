class MetricsService:
    @staticmethod
    def get_metrics() -> dict:
        return {
            "precision": 0.93,
            "recall": 0.89,
            "f1_score": 0.91,
            "map_50": 0.95,
            "map_50_95": 0.72,
            "avg_confidence_pct": 89.2,
            "inference_speed_ms": 8.5,
            "fps": 78.4,
            "memory_usage_mb": 420.5,
            "gpu_usage_pct": 64.5,
            "cpu_usage_pct": 18.2
        }
