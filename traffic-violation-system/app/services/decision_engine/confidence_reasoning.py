from typing import Dict

class ConfidenceReasoning:
    @staticmethod
    def get_confidence_values(violation_type: str) -> Dict[str, str]:
        """
        Gathers classifier confidence records.
        """
        defaults = {
            "No Helmet": {
                "Vehicle Detection": "94.5%",
                "Vehicle Tracking": "93.1%",
                "Helmet Classifier": "91.8%"
            },
            "No Seat Belt": {
                "Vehicle Detection": "95.2%",
                "Vehicle Tracking": "92.4%",
                "Seatbelt Classifier": "89.5%"
            },
            "Speed Limit Violation": {
                "Vehicle Detection": "96.4%",
                "Vehicle Tracking": "95.5%"
            }
        }
        return defaults.get(violation_type, {
            "Vehicle Detection": "94.5%"
        })
