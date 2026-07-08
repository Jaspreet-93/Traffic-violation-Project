from app.services.ai_command_center.confidence_monitor import ConfidenceMonitor

class ConfidenceService:
    @staticmethod
    def get_live_confidence() -> dict:
        """
        Gathers model inference confidence ratings.
        """
        metrics = ConfidenceMonitor.get_confidence_metrics()
        
        # Format values to strings with percent signs if they are floats
        formatted = {}
        for k, v in metrics.items():
            if isinstance(v, float):
                formatted[k] = f"{v * 100:.1f}%"
            else:
                formatted[k] = str(v)
                
        return formatted
