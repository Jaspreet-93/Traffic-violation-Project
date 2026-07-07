import os
import json
from app.core.logger import logger

class RuleEngine:
    def __init__(self):
        self.rules_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), "..", "..", "..", "rules", "violation_rules.json"
        ))
        self.rules = {}
        self.load_rules()

    def load_rules(self):
        """
        Loads traffic violation rules dynamically.
        """
        if not os.path.exists(self.rules_path):
            # Write default rules if not found
            os.makedirs(os.path.dirname(self.rules_path), exist_ok=True)
            self.rules = {
                "helmet_required": True,
                "seat_belt_required": True,
                "red_light_violation": True,
                "phone_usage_violation": True
            }
            with open(self.rules_path, "w") as f:
                json.dump(self.rules, f, indent=4)
            logger.info(f"Default violation rules written to: {self.rules_path}")
        else:
            try:
                with open(self.rules_path, "r") as f:
                    self.rules = json.load(f)
                logger.info(f"Violation rules loaded successfully from: {self.rules_path}")
            except Exception as e:
                logger.error(f"Error loading rules from {self.rules_path}: {e}")
                # Fallback
                self.rules = {
                    "helmet_required": True,
                    "seat_belt_required": True,
                    "red_light_violation": True,
                    "phone_usage_violation": True
                }

    def check_helmet_violation(self, helmet_status: str) -> bool:
        """
        Checks if a helmet violation occurred based on current rules.
        """
        self.load_rules()
        if not self.rules.get("helmet_required", True):
            return False
        return helmet_status == "no helmet"

    def check_seat_belt_violation(self, seat_belt_status: str) -> bool:
        """
        Checks if a seat belt violation occurred based on current rules.
        """
        self.load_rules()
        if not self.rules.get("seat_belt_required", True):
            return False
        return seat_belt_status == "no seatbelt" or seat_belt_status == "unbelted"

    def check_red_light_violation(self, traffic_light_state: str) -> bool:
        """
        Checks if a red light violation occurred based on current rules.
        """
        self.load_rules()
        if not self.rules.get("red_light_violation", True):
            return False
        return traffic_light_state == "red"

    def check_behavior_violation(self, behavior_label: str) -> bool:
        """
        Checks if driver behavior violates current rules (e.g. phone usage).
        """
        self.load_rules()
        if behavior_label == "phone" and self.rules.get("phone_usage_violation", True):
            return True
        return False

rule_engine = RuleEngine()
