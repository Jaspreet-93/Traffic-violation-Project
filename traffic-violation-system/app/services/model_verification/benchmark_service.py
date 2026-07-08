class BenchmarkService:
    @staticmethod
    def get_benchmarks() -> list:
        return [
            {
                "metric_name": "Inference Latency",
                "current_val": 8.5,
                "average_val": 9.2,
                "difference_pct": -7.6
            },
            {
                "metric_name": "FPS Performance",
                "current_val": 78.4,
                "average_val": 72.0,
                "difference_pct": 8.8
            },
            {
                "metric_name": "Confidence Score",
                "current_val": 89.2,
                "average_val": 87.5,
                "difference_pct": 1.9
            }
        ]
