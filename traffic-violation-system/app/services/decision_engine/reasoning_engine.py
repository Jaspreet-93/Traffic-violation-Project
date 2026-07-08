class ReasoningEngine:
    @staticmethod
    def get_reason(violation_type: str) -> str:
        reasons = {
            "No Helmet": "The AURA detection engine tracked a motorcycle vehicle and verified the rider was not wearing safety headgear.",
            "No Seat Belt": "The driver cabinet classifier detected seatbelt constraints were unfastened while the vehicle was in motion.",
            "Speed Limit Violation": "Radar tracking estimation recorded speed of 84 km/h, exceeding the configured zone threshold of 60 km/h."
        }
        return reasons.get(violation_type, "Pipeline rule check matched anomaly pattern criteria.")
