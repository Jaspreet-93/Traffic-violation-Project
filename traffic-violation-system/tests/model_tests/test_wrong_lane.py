import unittest
import numpy as np
import cv2
from app.services.wrong_lane.wrong_lane_manager import wrong_lane_manager

class TestWrongLaneManager(unittest.TestCase):
    def setUp(self):
        wrong_lane_manager.vehicle_tracks.clear()

    def test_wrong_lane_manager_pipeline(self):
        frame = np.ones((480, 640, 3), dtype=np.uint8) * 120
        # Draw some details inside vehicle box to prevent blur rejection
        for i in range(100, 300, 20):
            cv2.line(frame, (i, 100), (i, 300), (255, 255, 255), 2)
            cv2.line(frame, (100, i), (300, i), (255, 255, 255), 2)
        
        vehicle_box = [100, 100, 300, 300]
        track_id = 203
        
        # 1. Correct lane scenario
        res = wrong_lane_manager.process_lane_frame(
            frame, vehicle_box, track_id, 1, mock_lane_type="normal", mock_lane_direction="same"
        )
        self.assertEqual(res, "correct_lane")

        # 2. Opposite direction crossing (first frame -> correct_lane since we need 5 frames)
        res = wrong_lane_manager.process_lane_frame(
            frame, vehicle_box, track_id, 2, mock_lane_type="normal", mock_lane_direction="opposite"
        )
        self.assertEqual(res, "correct_lane")
        
        # Populate history to reach 5 frames of violation
        track_data = wrong_lane_manager.vehicle_tracks[track_id]
        for f in range(3, 7):
            track_data["history"].append({
                "frame": f,
                "type": "wrong_way",
                "lane_type": "normal",
                "lane_direction": "opposite",
                "vehicle_box": vehicle_box
            })
            
        res = wrong_lane_manager.process_lane_frame(
            frame, vehicle_box, track_id, 7, mock_lane_type="normal", mock_lane_direction="opposite"
        )
        self.assertEqual(res, "wrong_way")
        self.assertEqual(wrong_lane_manager.stats["wrong_way_violations"], 1)

if __name__ == "__main__":
    unittest.main()
