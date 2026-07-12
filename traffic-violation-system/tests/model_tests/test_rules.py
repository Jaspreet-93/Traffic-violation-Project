import unittest
from app.services.rule_engine.rule_intelligence import rule_intelligence

class TestRuleIntelligence(unittest.TestCase):
    def test_rules_check(self):
        # City centre rules: Speed limit 50, restricted truck, helmet & seat belt true
        violations = rule_intelligence.check_rule_violation(
            location_name="City Centre",
            vehicle_type="heavy truck",
            speed=60,
            lane_type="normal",
            helmet_worn=True,
            seat_belt_worn=False
        )
        
        types = [v["type"] for v in violations]
        self.assertIn("speeding", types)
        self.assertIn("restricted_vehicle_entry", types)
        self.assertIn("no seat belt", types)

        # Highway rules: Speed limit 100, allowed lanes emergency/normal
        violations_hw = rule_intelligence.check_rule_violation(
            location_name="Highway",
            vehicle_type="car",
            speed=80,
            lane_type="emergency",
            helmet_worn=True,
            seat_belt_worn=True
        )
        types_hw = [v["type"] for v in violations_hw]
        self.assertIn("emergency_lane_violation", types_hw)

if __name__ == "__main__":
    unittest.main()
