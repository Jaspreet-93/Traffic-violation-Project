import unittest
import numpy as np
import cv2
from app.services.traffic_light.traffic_light_manager import traffic_light_manager

class TestTrafficLightManager(unittest.TestCase):
    def setUp(self):
        traffic_light_manager.vehicle_tracks.clear()

    def test_traffic_light_manager_pipeline(self):
        frame = np.ones((480, 640, 3), dtype=np.uint8) * 120
        # Draw some details
        for i in range(100, 300, 20):
            cv2.line(frame, (i, 100), (i, 300), (255, 255, 255), 2)
            cv2.line(frame, (100, i), (300, i), (255, 255, 255), 2)
        
        vehicle_box = [100, 100, 300, 300]
        track_id = 202
        
        # 1. No Traffic Signal Present
        res = traffic_light_manager.process_intersection_frame(
            frame, vehicle_box, track_id, 1, mock_signal_present=False
        )
        self.assertEqual(res, "No Traffic Signal Present")

        # 2. Stop Line not visible
        res = traffic_light_manager.process_intersection_frame(
            frame, vehicle_box, track_id, 1, mock_signal_present=True, mock_stop_line_visible=False
        )
        self.assertEqual(res, "Unable to Verify")

        # 3. Crossing not active yet (vehicle center y = 200, which is < h*0.70 = 336)
        res = traffic_light_manager.process_intersection_frame(
            frame, vehicle_box, track_id, 1, mock_signal_present=True, mock_stop_line_visible=True, mock_signal_color="Red"
        )
        self.assertEqual(res, "No Violation")

        # 4. Vehicle crossing stop line (y1=300, y2=450, center y = 375 >= 336)
        vehicle_crossing_box = [100, 300, 300, 450]
        
        # Process first crossing frame
        res = traffic_light_manager.process_intersection_frame(
            frame, vehicle_crossing_box, track_id, 2, mock_signal_present=True, mock_stop_line_visible=True, mock_signal_color="Red"
        )
        self.assertEqual(res, "No Violation")
        
        # Populate history to reach 5 frames
        track_data = traffic_light_manager.vehicle_tracks[track_id]
        for f in range(3, 7):
            track_data["history"].append({
                "frame": f,
                "type": "red_light_violation",
                "signal_color": "Red",
                "signal_box": [200, 10, 300, 100],
                "stop_line_box": [10, 336, 630, 470],
                "vehicle_box": vehicle_crossing_box
            })
            
        res = traffic_light_manager.process_intersection_frame(
            frame, vehicle_crossing_box, track_id, 7, mock_signal_present=True, mock_stop_line_visible=True, mock_signal_color="Red"
        )
        self.assertEqual(res, "red_light_violation")
        self.assertEqual(traffic_light_manager.stats["red_light_violations"], 1)

if __name__ == "__main__":
    unittest.main()
