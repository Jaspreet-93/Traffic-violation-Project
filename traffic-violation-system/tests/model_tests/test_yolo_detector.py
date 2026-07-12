import os
import unittest
import numpy as np
from app.services.detection.yolo_detector import yolo_detector

class TestYoloDetectorUpgrade(unittest.TestCase):
    def test_predict_vehicles_detailed(self):
        # Create dummy image frame
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        
        # Test detailed detection API
        res = yolo_detector.predict_vehicles_detailed(frame)
        
        self.assertIn("fps", res)
        self.assertIn("latency_ms", res)
        self.assertIn("average_confidence", res)
        self.assertIn("detections", res)
        
        self.assertIsInstance(res["fps"], float)
        self.assertIsInstance(res["latency_ms"], float)
        self.assertIsInstance(res["average_confidence"], float)
        self.assertIsInstance(res["detections"], list)

if __name__ == "__main__":
    unittest.main()
