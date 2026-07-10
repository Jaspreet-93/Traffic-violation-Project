import unittest
import numpy as np
from app.services.upload_detection.pipeline_runner import PipelineRunner

class TestSeatBeltSuitability(unittest.TestCase):
    def test_suitability_front_facing_car(self):
        # Front-facing car with sufficient resolution and correct aspect ratio
        crop = np.zeros((300, 300, 3), dtype=np.uint8)
        is_suitable, reason = PipelineRunner.validate_seat_belt_suitability("car", crop, "front_view_car.jpg")
        self.assertTrue(is_suitable)
        self.assertEqual(reason, "Valid windshield/cabin view")

    def test_suitability_rear_facing_car(self):
        crop = np.zeros((300, 300, 3), dtype=np.uint8)
        is_suitable, reason = PipelineRunner.validate_seat_belt_suitability("car", crop, "rear_facing_car.jpg")
        self.assertFalse(is_suitable)
        self.assertIn("Rear/Side view", reason)

    def test_suitability_side_view_car(self):
        # Side view typically has high aspect ratio (wider than tall)
        crop = np.zeros((200, 400, 3), dtype=np.uint8)
        is_suitable, reason = PipelineRunner.validate_seat_belt_suitability("car", crop, "car_side.jpg")
        self.assertFalse(is_suitable)
        self.assertIn("Side view / Angle not suitable", reason)

    def test_suitability_bus(self):
        crop = np.zeros((400, 400, 3), dtype=np.uint8)
        is_suitable, reason = PipelineRunner.validate_seat_belt_suitability("bus", crop, "front_bus.jpg")
        self.assertFalse(is_suitable)
        self.assertIn("Not a passenger car", reason)

    def test_suitability_truck(self):
        crop = np.zeros((400, 400, 3), dtype=np.uint8)
        is_suitable, reason = PipelineRunner.validate_seat_belt_suitability("truck", crop, "front_truck.jpg")
        self.assertFalse(is_suitable)
        self.assertIn("Not a passenger car", reason)

    def test_suitability_motorcycle(self):
        crop = np.zeros((200, 200, 3), dtype=np.uint8)
        is_suitable, reason = PipelineRunner.validate_seat_belt_suitability("motorcycle", crop, "front_motorcycle.jpg")
        self.assertFalse(is_suitable)
        self.assertIn("Not a passenger car", reason)

    def test_suitability_night(self):
        crop = np.zeros((300, 300, 3), dtype=np.uint8)
        is_suitable, reason = PipelineRunner.validate_seat_belt_suitability("car", crop, "car_at_night.jpg")
        self.assertFalse(is_suitable)
        self.assertIn("Low lighting / Rain occlusion", reason)

    def test_suitability_rain(self):
        crop = np.zeros((300, 300, 3), dtype=np.uint8)
        is_suitable, reason = PipelineRunner.validate_seat_belt_suitability("car", crop, "car_in_rain.jpg")
        self.assertFalse(is_suitable)
        self.assertIn("Low lighting / Rain occlusion", reason)

    def test_suitability_low_resolution(self):
        # Low resolution crop (e.g. 100x100)
        crop = np.zeros((100, 100, 3), dtype=np.uint8)
        is_suitable, reason = PipelineRunner.validate_seat_belt_suitability("car", crop, "front_car.jpg")
        self.assertFalse(is_suitable)
        self.assertIn("Far distance / Low resolution", reason)

if __name__ == "__main__":
    unittest.main()
