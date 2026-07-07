import os
import time
import unittest
from ultralytics import YOLO

class TestModelInference(unittest.TestCase):
    def test_model_loading_and_speed(self):
        # Locate yolov8n.pt or use fallback model name
        model_path = "models/yolo/yolov8n.pt"
        if not os.path.exists(model_path):
            print(f"Model path {model_path} not found on local disk. Loading remote yolov8n model...")
            model_path = "yolov8n.pt" # downloads dynamically

        print("Testing model loading...")
        start_time = time.time()
        try:
            model = YOLO(model_path)
            load_duration = time.time() - start_time
            print(f"Model loaded successfully in {load_duration:.4f} seconds.")
            self.assertIsNotNone(model)
        except Exception as e:
            self.fail(f"Failed to load YOLO model: {e}")

        # Check basic properties
        print("Checking model properties...")
        self.assertEqual(model.overrides.get('task'), 'detect')

if __name__ == "__main__":
    unittest.main()
