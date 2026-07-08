class StatisticsService:
    @staticmethod
    def get_overview_statistics() -> dict:
        return {
            "total_vehicles": 14205,
            "total_violations": 843,
            "detection_accuracy_pct": 96.5,
            "avg_confidence_pct": 89.2,
            "avg_inference_time_ms": 12.8,
            "avg_detection_speed_fps": 78.4,
            "system_uptime_sec": 86400 * 5 # 5 days uptime
        }
