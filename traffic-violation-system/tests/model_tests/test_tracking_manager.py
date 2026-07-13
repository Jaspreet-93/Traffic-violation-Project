import unittest
import numpy as np
from app.services.tracking.track_manager import track_manager

class TestTrackManager(unittest.TestCase):
    def setUp(self):
        track_manager.tracks.clear()
        track_manager.total_vehicles_tracked = 0
        track_manager.lost_tracks_count = 0
        track_manager.id_switch_count = 0

    def test_track_lifecycle_and_stats(self):
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        
        # 1. Simulate new detection
        detections = [
            {"id": 1, "box": [100, 100, 200, 250], "conf": 0.95, "class_id": 2}
        ]
        track_manager.update_tracks(frame, detections, 1)
        
        self.assertEqual(track_manager.total_vehicles_tracked, 1)
        details = track_manager.get_track_by_id(1)
        self.assertIsNotNone(details)
        self.assertEqual(details["vehicle_class"], "car")
        self.assertEqual(details["status"], "active")
        
        # 2. Update track
        detections_update = [
            {"id": 1, "box": [105, 105, 205, 255], "conf": 0.96, "class_id": 2}
        ]
        track_manager.update_tracks(frame, detections_update, 2)
        
        details = track_manager.get_track_by_id(1)
        self.assertEqual(details["frames_tracked"], 2)
        self.assertEqual(details["average_confidence"], 0.955)
        
        # 3. Test history endpoint format
        history = track_manager.get_track_history(1)
        self.assertIsNotNone(history)
        self.assertEqual(len(history["center_coordinates"]), 2)
        self.assertEqual(len(history["detection_history"]), 2)
        
        # 4. Test active tracks list
        active_list = track_manager.get_active_tracks()
        self.assertEqual(len(active_list), 1)
        self.assertEqual(active_list[0]["track_id"], 1)

if __name__ == "__main__":
    unittest.main()
