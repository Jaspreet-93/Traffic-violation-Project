class DecisionTree:
    @staticmethod
    def get_decision_path(violation_type: str) -> dict:
        """
        Builds the validation branch mapping for rule evaluations.
        """
        paths = {
            "No Helmet": {
                "rule": "Helmet detected is absent on active rider",
                "branches": [
                    "Vehicle Class: Motorcycle",
                    "Helmet Classifier Status: False",
                    "Violations Logged: True"
                ]
            },
            "No Seat Belt": {
                "rule": "Seatbelt detected is absent on driver/passenger",
                "branches": [
                    "Vehicle Class: Car/Truck",
                    "Seatbelt Classifier Status: False",
                    "Violations Logged: True"
                ]
            },
            "Speed Limit Violation": {
                "rule": "Tracked velocity exceeds class bounds threshold",
                "branches": [
                    "Speed estimation: 84 km/h",
                    "Speed limit: 60 km/h",
                    "Violations Logged: True"
                ]
            }
        }
        return paths.get(violation_type, {
            "rule": "General traffic infraction rule evaluation",
            "branches": [
                "Object tracked: True",
                "Anomaly detection: Active",
                "Violations Logged: True"
            ]
        })
