from typing import List, Dict, Any

class BenchmarkEvaluator:
    @staticmethod
    def run_benchmark() -> List[Dict[str, Any]]:
        """
        Executes a mock throughput evaluation benchmark representing baseline latencies.
        """
        return [
            {
                "model_name": "YOLOv8 Vehicle Detector",
                "load_latency_ms": 112.5,
                "avg_inference_latency_ms": 12.4,
                "max_throughput_fps": 80.6,
                "memory_peak_mb": 140.0
            },
            {
                "model_name": "Custom Helmet Detector",
                "load_latency_ms": 85.0,
                "avg_inference_latency_ms": 8.2,
                "max_throughput_fps": 121.9,
                "memory_peak_mb": 85.0
            },
            {
                "model_name": "License Plate Detector",
                "load_latency_ms": 90.0,
                "avg_inference_latency_ms": 9.0,
                "max_throughput_fps": 111.1,
                "memory_peak_mb": 85.0
            },
            {
                "model_name": "License Plate OCR",
                "load_latency_ms": 145.0,
                "avg_inference_latency_ms": 18.2,
                "max_throughput_fps": 54.9,
                "memory_peak_mb": 120.0
            }
        ]
