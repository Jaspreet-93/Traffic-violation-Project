import unittest
import numpy as np
import cv2
import os
import uuid
from app.services.upload_detection.video_detector import VideoDetector, jobs_registry

class TestVideoDetectorPipeline(unittest.TestCase):
    def setUp(self):
        # Create a dummy video file
        self.filepath = "test_dummy_video.mp4"
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(self.filepath, fourcc, 30.0, (640, 480))
        for _ in range(30):  # 1 second of video
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(frame, "TEST VIDEO", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
            out.write(frame)
        out.release()
        self.job_id = str(uuid.uuid4())

    def tearDown(self):
        if os.path.exists(self.filepath):
            os.remove(self.filepath)
        processed_path = f"processed_{self.filepath}"
        if os.path.exists(processed_path):
            os.remove(processed_path)

    def test_analyze_video_characteristics(self):
        cap = cv2.VideoCapture(self.filepath)
        self.assertTrue(cap.isOpened())
        res = VideoDetector._analyze_video_characteristics(cap, self.filepath)
        cap.release()
        
        self.assertEqual(res["fps"], 30.0)
        self.assertEqual(res["width"], 640)
        self.assertEqual(res["height"], 480)
        self.assertIn("motion_level", res)
        self.assertIn("traffic_density", res)

    def test_assess_and_preprocess_frame(self):
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        info = {"motion_level": "low"}
        prep_frame, is_valid, score = VideoDetector._assess_and_preprocess_frame(frame, info)
        # Low brightness (0) -> should reject black frame
        self.assertFalse(is_valid)

if __name__ == "__main__":
    unittest.main()
