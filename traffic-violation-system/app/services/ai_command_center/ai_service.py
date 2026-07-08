from app.utils.performance_utils import performance_tracker

class AIService:
    @staticmethod
    def get_performance_metrics() -> dict:
        """
        Retrieves real-time processing statistics.
        """
        # Fetch current vehicle detector inference time
        avg_inf_ms = performance_tracker.get_average_inference_time("yolo_vehicle")
        avg_api_ms = performance_tracker.get_avg_api_response_time()

        return {
            "fps": round(performance_tracker.get_current_fps(), 1),
            "inference_time_ms": round(avg_inf_ms, 1),
            "api_response_time_ms": round(avg_api_ms, 1),
            "queue_size": performance_tracker.get_queue_size()
        }
