import unittest
import numpy as np
import cv2
from app.services.helmet.helmet_manager import helmet_manager
from app.services.helmet.helmet_detector import helmet_detector

class TestHelmetManager(unittest.TestCase):
    def setUp(self):
        helmet_manager.motorcycle_tracks.clear()
        helmet_manager.total_helmet_violations = 0

    def test_helmet_temporal_verification_and_filters(self):
        # Mock helmet detector to return a simulated "no helmet" box
        original_detect = helmet_detector.detect_helmets
        helmet_detector.detect_helmets = lambda f: [{"bbox": [10, 10, 80, 80], "helmet_status": "no helmet", "confidence": 0.85}]

        try:
            frame = np.ones((480, 640, 3), dtype=np.uint8) * 120
            # Put bright texture to prevent dark/blur rejection
            cv2.putText(frame, "MOTORCYCLE TEST FRAME FOR HELMET", (110, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            vehicle_box = [100, 100, 400, 400]
            track_id = 99
            
            # 1. First frame: should return "Unable to Verify" since we need at least 5 frames for No Helmet
            res = helmet_manager.process_motorcycle_frame(frame, vehicle_box, track_id, 1)
            self.assertEqual(res, "Unable to Verify")

            # 2. Simulate 4 more frames without helmet in history
            track_data = helmet_manager.motorcycle_tracks[track_id]
            for f in range(2, 6):
                track_data["history"].append({
                    "frame": f,
                    "type": "no helmet",
                    "conf": 0.85,
                    "head_box": [110, 110, 180, 180],
                    "head_crop": np.zeros((70, 70, 3), dtype=np.uint8)
                })

            # Process a No Helmet frame: should trigger No Helmet violation now!
            res = helmet_manager.process_motorcycle_frame(frame, vehicle_box, track_id, 6)
            self.assertEqual(res, "no helmet")
            self.assertEqual(helmet_manager.total_helmet_violations, 1)

            # 3. If helmet is seen in later frame, it must reject the "No Helmet" violation!
            track_data["helmet_seen"] = True
            res = helmet_manager.process_motorcycle_frame(frame, vehicle_box, track_id, 7)
            self.assertEqual(res, "helmet")
        finally:
            helmet_detector.detect_helmets = original_detect

if __name__ == "__main__":
    unittest.main()
