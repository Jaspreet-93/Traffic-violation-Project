import os
import json
from typing import Dict, Any, List, Optional
from app.core.logger import logger

class RuleIntelligence:
    def __init__(self):
        self.rules_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), "..", "..", "..", "rules", "location_rules.json"
        ))
        self.default_rules = {
            "City Centre": {
                "speed_limit_kph": 50,
                "allowed_lanes": ["normal", "bus", "turning"],
                "bus_lane_only": ["bus"],
                "restricted_vehicles": ["heavy truck"],
                "helmet_required": True,
                "seat_belt_required": True
            },
            "Highway": {
                "speed_limit_kph": 100,
                "allowed_lanes": ["normal", "emergency"],
                "emergency_lane_only": ["emergency"],
                "restricted_vehicles": ["bicycle", "auto rickshaw"],
                "helmet_required": True,
                "seat_belt_required": True
            },
            "School Zone": {
                "speed_limit_kph": 30,
                "allowed_lanes": ["normal"],
                "restricted_vehicles": [],
                "helmet_required": True,
                "seat_belt_required": True
            }
        }
        self.rules = {}
        self.load_rules()

    def load_rules(self):
        """
        Loads location rules from configuration file or falls back to defaults.
        """
        if os.path.exists(self.rules_path):
            try:
                with open(self.rules_path, "r") as f:
                    self.rules = json.load(f)
                logger.info(f"Location rules loaded successfully from {self.rules_path}")
            except Exception as e:
                logger.error(f"Error loading location rules from file: {e}")
                self.rules = dict(self.default_rules)
        else:
            self.rules = dict(self.default_rules)
            self.save_rules()

    def save_rules(self):
        """
        Saves rules configuration to local JSON file.
        """
        try:
            os.makedirs(os.path.dirname(self.rules_path), exist_ok=True)
            with open(self.rules_path, "w") as f:
                json.dump(self.rules, f, indent=2)
            logger.info(f"Location rules saved successfully to {self.rules_path}")
        except Exception as e:
            logger.error(f"Error saving location rules to file: {e}")

    def get_rules_for_location(self, location_name: str) -> Optional[dict]:
        return self.rules.get(location_name)

    def check_rule_violation(
        self,
        location_name: str,
        vehicle_type: str,
        speed: float,
        lane_type: str,
        helmet_worn: bool = True,
        seat_belt_worn: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Checks current metrics against location-based rules and returns a list of detected violations.
        """
        violations = []
        loc_rules = self.get_rules_for_location(location_name)
        if not loc_rules:
            return violations

        # 1. Speed check
        limit = loc_rules.get("speed_limit_kph", 50)
        if speed > limit:
            violations.append({
                "type": "speeding",
                "details": f"Vehicle speed {speed} kph exceeded limit of {limit} kph in {location_name} zone"
            })

        # 2. restricted vehicle check
        restricted = loc_rules.get("restricted_vehicles", [])
        if vehicle_type.lower() in [v.lower() for v in restricted]:
            violations.append({
                "type": "restricted_vehicle_entry",
                "details": f"Vehicle type {vehicle_type} is prohibited in {location_name} zone"
            })

        # 3. lane restriction check
        if lane_type == "emergency" and vehicle_type.lower() != "emergency":
            violations.append({
                "type": "emergency_lane_violation",
                "details": f"Non-emergency vehicle driving inside emergency lane"
            })
        elif lane_type == "bus" and vehicle_type.lower() != "bus":
            violations.append({
                "type": "bus_lane_violation",
                "details": f"Non-bus vehicle driving inside designated bus lane"
            })

        # 4. helmet check
        if loc_rules.get("helmet_required", True) and vehicle_type.lower() == "motorcycle" and not helmet_worn:
            violations.append({
                "type": "no helmet",
                "details": "Motorcycle rider not wearing a helmet"
            })

        # 5. seat belt check
        if loc_rules.get("seat_belt_required", True) and any(t in vehicle_type.lower() for t in ["car", "suv", "truck"]) and not seat_belt_worn:
            violations.append({
                "type": "no seat belt",
                "details": "Driver not wearing a seat belt"
            })

        return violations

rule_intelligence = RuleIntelligence()
