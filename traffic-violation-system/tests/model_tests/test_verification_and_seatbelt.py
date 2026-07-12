import unittest
import numpy as np
import cv2
from app.services.verification.verification_engine import verification_engine
from app.services.seat_belt.seat_belt_manager import seat_belt_manager

class TestVerificationAndSeatBelt(unittest.TestCase):
    def setUp(self):
        verification_engine.verifications.clear()
        seat_belt_manager.vehicle_tracks.clear()

    def test_verification_engine_multi_frame(self):
        # Mock VLM call to simulate "No Violation" consensus
        original_vlm = verification_engine.call_gemini_vision
        verification_engine.call_gemini_vision = lambda crop, q: {
            "verification": "Seat Belt Present",
            "confidence": 0.95,
            "reason": "Seat belt observed clearly",
            "manual_review": False
        }

        try:
            # 5 identical dummy frames
            frames = [np.ones((100, 100, 3), dtype=np.uint8) * 150 for _ in range(5)]
            
            # Test VLM multi frame verification mode
            res = verification_engine.verify_multi_frame_infraction(
                frames=frames,
                violation_type="seatbelt",
                question="Is the driver's seat belt clearly visible?"
            )
            
            self.assertEqual(res["decision"], "No Violation")
            self.assertFalse(res["manual_review"])
            self.assertGreater(res["confidence"], 0.70)
        finally:
            verification_engine.call_gemini_vision = original_vlm

    def test_seat_belt_manager_pipeline(self):
        frame = np.ones((480, 640, 3), dtype=np.uint8) * 120
        # Draw some features for windshield area
        cv2.rectangle(frame, (100, 100), (540, 200), (255, 255, 255), -1)
        
        vehicle_box = [100, 100, 540, 400]
        track_id = 101
        
        # 1. Non-allowed class should return Unable to Verify immediately
        res = seat_belt_manager.process_vehicle_frame(frame, vehicle_box, track_id, "motorcycle", 1)
        self.assertEqual(res, "Unable to Verify")

        # 2. Allowed class car
        res = seat_belt_manager.process_vehicle_frame(frame, vehicle_box, track_id, "car", 1)
        self.assertEqual(res, "Unable to Verify")

if __name__ == "__main__":
    unittest.main()
