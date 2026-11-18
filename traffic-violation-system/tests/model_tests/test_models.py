import os
import time
import unittest
from ultralytics import YOLO

class TestModelInference(unittest.TestCase):
    def test_model_loading_and_speed(self):
        # Locate yolov8n.pt or use fallback model name
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        candidate_paths = [
            os.path.join(base_dir, "models", "yolo", "yolov8n.pt"),
            os.path.join(base_dir, "traffic-violation-system", "models", "yolo", "yolov8n.pt"),
            "traffic-violation-system/models/yolo/yolov8n.pt",
            "models/yolo/yolov8n.pt",
            "yolov8n.pt"
        ]
        model_path = next((p for p in candidate_paths if os.path.exists(p)), "yolov8n.pt")

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
