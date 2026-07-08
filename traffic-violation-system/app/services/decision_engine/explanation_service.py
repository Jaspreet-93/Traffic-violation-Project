from app.services.decision_engine.reasoning_engine import ReasoningEngine
from app.services.decision_engine.confidence_reasoning import ConfidenceReasoning

class ExplanationService:
    @staticmethod
    def get_explanation(violation_id: str, violation_type: str = "No Helmet") -> dict:
        reason = ReasoningEngine.get_reason(violation_type)
        conf = ConfidenceReasoning.get_confidence_values(violation_type)

        supporting = ["Motorcycle Class ID Matched", "Rider Bounding Box Tracked"]
        if violation_type == "No Seat Belt":
            supporting = ["Car Class ID Matched", "Cabin ROI Scanned"]
        elif violation_type == "Speed Limit Violation":
            supporting = ["Car Class ID Matched", "Pixel Displacement Frame Tracker"]

        return {
            "violation_id": violation_id,
            "violation_type": violation_type,
            "reason": reason,
            "supporting_detections": supporting,
            "model_confidence": conf,
            "evidence_generated": [
                f"/uploads/evidence_{violation_id}_crop.jpg",
                f"/uploads/evidence_{violation_id}_full.jpg"
            ],
            "final_decision": f"Violation Logged: {violation_type} verified",
            "overall_trust_score": 93.4
        }
