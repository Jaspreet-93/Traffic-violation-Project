import unittest
import numpy as np
import cv2
from app.services.driver_behavior.mobile_phone_manager import mobile_phone_manager
from app.services.driver_behavior.behavior_detector import behavior_detector

class TestMobilePhoneManager(unittest.TestCase):
    def setUp(self):
        mobile_phone_manager.vehicle_tracks.clear()

    def test_mobile_phone_manager_pipeline(self):
        frame = np.ones((480, 640, 3), dtype=np.uint8) * 120
        # Draw windshield area
        cv2.rectangle(frame, (100, 100), (540, 200), (255, 255, 255), -1)
        
        vehicle_box = [100, 100, 540, 400]
        track_id = 101
        
        # 1. Non-allowed class should return Unable to Verify immediately
        res = mobile_phone_manager.process_vehicle_frame(frame, vehicle_box, track_id, "motorcycle", 1)
        self.assertEqual(res, "Unable to Verify")

        # 2. Allowed class car
        res = mobile_phone_manager.process_vehicle_frame(frame, vehicle_box, track_id, "car", 1)
        self.assertEqual(res, "Unable to Verify")

        # 3. Simulate 5 consecutive talking on phone detections
        # Mock behavior detector
        original_detect = behavior_detector.detect_behavior
        behavior_detector.detect_behavior = lambda f: [{"bbox": [10, 10, 50, 50], "class_id": 1, "confidence": 0.88}]
        
        try:
            # Process first frame
            res = mobile_phone_manager.process_vehicle_frame(frame, vehicle_box, track_id, "car", 1)
            self.assertEqual(res, "Unable to Verify")
            
            # Populate 4 more frames in history to hit multi-frame validation
            track_data = mobile_phone_manager.vehicle_tracks[track_id]
            for f in range(2, 6):
                track_data["history"].append({
                    "frame": f,
                    "type": "using_phone",
                    "conf": 0.88,
                    "phone_box": [120, 120, 160, 160],
                    "phone_crop": np.zeros((40, 40, 3), dtype=np.uint8),
                    "hand_box": [110, 110, 170, 170],
                    "hand_crop": np.zeros((60, 60, 3), dtype=np.uint8)
                })
                
            res = mobile_phone_manager.process_vehicle_frame(frame, vehicle_box, track_id, "car", 6)
            self.assertEqual(res, "using_phone")
            self.assertEqual(mobile_phone_manager.stats["mobile_phone_violations"], 1)
        finally:
            behavior_detector.detect_behavior = original_detect

if __name__ == "__main__":
    unittest.main()
