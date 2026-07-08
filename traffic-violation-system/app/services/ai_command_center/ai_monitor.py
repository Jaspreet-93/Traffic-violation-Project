from datetime import datetime, time as dt_time, timezone
from app.services.ai_command_center.model_validator import ModelValidator
from app.services.ai_command_center.system_monitor import SystemMonitor
from app.services.ai_command_center.confidence_monitor import ConfidenceMonitor
from app.utils.performance_utils import performance_tracker
from app.database.connection import SessionLocal
from app.database.models.violation import Violation
from app.core.logger import logger

class AIMonitor:
    @staticmethod
    def get_overview_metrics() -> dict:
        """
        Compiles high-level status aggregates for the AI Command Center overview.
        """
        models = ModelValidator.get_all_models_health()
        system = SystemMonitor.get_system_overview()
        confidence = ConfidenceMonitor.get_confidence_metrics()

        total_models = len(models)
        running = sum(1 for m in models if m["status"] == "Running")
        offline = total_models - running

        # Determine overall system health category
        health = "Healthy"
        if offline > 0:
            health = "Warning"
        if offline > 2:
            health = "Critical"

        # Query total violations registered today
        violations_today = 0
        db = SessionLocal()
        try:
            today_start = datetime.combine(datetime.today(), dt_time.min).replace(tzinfo=timezone.utc)
            violations_today = db.query(Violation).filter(Violation.timestamp >= today_start).count()
        except Exception as e:
            logger.warning(f"Failed to query database for today's violations count, using cache: {e}")
            from app.services.violation.violation_service import violation_service
            violations_today = len(violation_service.recorded_violations)
        finally:
            db.close()

        # Estimation default counts
        vehicles_detected = violations_today * 8 + 42

        return {
            "system_health": health,
            "total_models": total_models,
            "running_models": running,
            "offline_models": offline,
            "average_confidence": confidence["overall_violation"],
            "fps": round(performance_tracker.get_current_fps(), 1),
            "violations_today": violations_today,
            "vehicles_detected_today": vehicles_detected,
            "active_cameras": 1,
            "cpu_usage": system["cpu_usage"],
            "gpu_usage": system["gpu_usage"],
            "ram_usage": system["ram_usage"],
            "storage_usage": system["storage_usage"],
            "system_uptime": system["system_uptime"]
        }
