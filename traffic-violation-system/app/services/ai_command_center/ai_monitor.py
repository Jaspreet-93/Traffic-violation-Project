from app.services.ai_command_center.model_monitor import ModelMonitor
from app.services.ai_command_center.system_monitor import SystemMonitor
from app.services.ai_command_center.confidence_monitor import ConfidenceMonitor
from app.utils.performance_utils import performance_tracker

class AIMonitor:
    @staticmethod
    def get_overview_metrics() -> dict:
        """
        Calculates top-level operational counters.
        """
        models = ModelMonitor.get_model_health()
        system = SystemMonitor.get_system_health()
        confidence = ConfidenceMonitor.get_confidence_metrics()

        total = len(models)
        running = sum(1 for m in models if m["status"] == "Healthy")
        loaded = sum(1 for m in models if m["loads_successfully"])
        
        # Parse average confidence float
        avg_conf_str = confidence["overall_violation"]
        avg_conf = 0.0
        if "%" in avg_conf_str:
            try:
                avg_conf = float(avg_conf_str.replace("%", "")) / 100.0
            except ValueError:
                pass
        else:
            # default fallback if database is empty/offline
            avg_conf = 0.93

        pipeline_status = "Active" if running > 5 else "Degraded"
        health = "Healthy" if running == total else "Warning"
        if running < 4:
            health = "Critical"

        return {
            "system_health": health,
            "total_models": total,
            "running_models": running,
            "loaded_models": loaded,
            "average_confidence": avg_conf,
            "system_uptime": system["uptime"],
            "fps": round(performance_tracker.get_current_fps(), 1),
            "pipeline_status": pipeline_status
        }
