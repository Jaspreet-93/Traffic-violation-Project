from datetime import datetime, timedelta
from typing import List

class DecisionService:
    @staticmethod
    def get_latest_decision() -> dict:
        return {
            "violation_id": "violation-latest-101",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "violation_type": "No Helmet",
            "decision": "Rider safety gear absent. Action: Log violation ticket and send notification.",
            "status": "Flagged",
            "confidence_score": 0.92
        }

    @classmethod
    def get_decision_by_id(cls, violation_id: str) -> dict:
        return {
            "violation_id": violation_id,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "violation_type": "No Helmet",
            "decision": "Rider safety gear absent. Action: Log violation ticket.",
            "status": "Flagged",
            "confidence_score": 0.92
        }

    @classmethod
    def get_history(cls) -> List[dict]:
        now = datetime.now()
        types = ["No Helmet", "No Seat Belt", "Speed Limit Violation"]
        history = []
        for i in range(5):
            t = (now - timedelta(minutes=i*15)).strftime("%Y-%m-%d %H:%M:%S")
            history.append({
                "violation_id": f"violation-job-{i}",
                "timestamp": t,
                "violation_type": types[i % len(types)],
                "decision": f"Violation verified. Action: Auto-flagged.",
                "status": "Approved" if i % 2 == 0 else "Flagged",
                "confidence_score": 0.94 - (i * 0.015)
            })
        return history
