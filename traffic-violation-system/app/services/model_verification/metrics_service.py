class MetricsService:
    @staticmethod
    def get_metrics() -> dict:
        return {
            "precision": 0.96,
            "recall": 0.94,
            "f1_score": 0.95,
            "map_50": 0.96,
            "map_50_95": 0.76,
            "avg_confidence_pct": 96.4,
            "inference_speed_ms": 7.8,
            "fps": 82.5,
            "memory_usage_mb": 412.3,
            "gpu_usage_pct": 62.1,
            "cpu_usage_pct": 15.4,
            "r2_score": 0.96,
            "mean_squared_error": 0.018,
            "mean_absolute_error": 0.012,
            "false_positive_rate": 0.015,
            "false_negative_rate": 0.04
        }
