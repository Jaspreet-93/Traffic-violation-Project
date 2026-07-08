from datetime import datetime
from app.services.decision_engine.confidence_reasoning import ConfidenceReasoning

class AuditService:
    @staticmethod
    def get_audit_trail(violation_id: str, violation_type: str = "No Helmet") -> dict:
        conf = ConfidenceReasoning.get_confidence_values(violation_type)
        
        models = ["YOLOv8 Vehicle Detector", "ByteTrack Tracker"]
        if violation_type == "No Helmet":
            models.append("Helmet Classifier Model")
        elif violation_type == "No Seat Belt":
            models.append("Seatbelt Classifier Model")

        return {
            "decision_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "models_used": models,
            "confidence_values": conf,
            "evidence_reference": f"REF-EVID-{violation_id}",
            "processing_time_ms": 12.8,
            "pipeline_status": "Execution Completed Successfully"
        }
