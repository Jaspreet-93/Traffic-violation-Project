import os
from ultralytics import YOLO
from app.core.logger import logger

class TrafficLightModel:
    def __init__(self):
        self.model = None
        # Locate models/traffic_light/traffic_light_model.pt relative to the app/models directory
        self.model_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), "..", "..", "models", "traffic_light", "traffic_light_model.pt"
        ))

    def load_model(self):
        """
        Loads the custom traffic light YOLOv8 model weights lazily.
        """
        if self.model is None:
            logger.info(f"Loading custom traffic light model from: {self.model_path}")
            if not os.path.exists(self.model_path):
                logger.error(f"Traffic light detector weights not found at: {self.model_path}")
                raise FileNotFoundError(f"Traffic light model weights file not found: {self.model_path}")
            try:
                self.model = YOLO(self.model_path)
                logger.info("Custom traffic light YOLOv8 model loaded successfully.")
            except Exception as e:
                logger.error(f"Error loading custom traffic light YOLOv8 model: {e}")
                raise

    def predict(self, frame):
        """
        Runs model inference on the frame and returns raw YOLO results.
        """
        self.load_model()
        if self.model is None:
            return None
        import torch
        device = 0 if torch.cuda.is_available() else "cpu"
        half = torch.cuda.is_available()
        return self.model(frame, verbose=False, device=device, half=half, imgsz=640)

traffic_light_model = TrafficLightModel()
