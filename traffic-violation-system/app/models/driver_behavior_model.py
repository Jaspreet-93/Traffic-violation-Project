import os
from ultralytics import YOLO
from app.core.logger import logger

class DriverBehaviorModel:
    def __init__(self):
        self.model = None
        # Locate models/driver_behavior/driver_behavior_model.pt relative to the app/models directory
        self.model_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), "..", "..", "models", "driver_behavior", "driver_behavior_model.pt"
        ))

    def load_model(self):
        """
        Loads the custom driver behavior YOLOv8 model weights lazily.
        """
        if self.model is None:
            logger.info(f"Loading custom driver behavior model from: {self.model_path}")
            if not os.path.exists(self.model_path):
                logger.error(f"Driver behavior detector weights not found at: {self.model_path}")
                raise FileNotFoundError(f"Driver behavior model weights file not found: {self.model_path}")
            try:
                self.model = YOLO(self.model_path)
                logger.info("Custom driver behavior YOLOv8 model loaded successfully.")
            except Exception as e:
                logger.error(f"Error loading custom driver behavior YOLOv8 model: {e}")
                raise

    def predict(self, frame):
        """
        Runs model inference on the frame and returns raw YOLO results.
        """
        self.load_model()
        if self.model is None:
            return None
        return self.model(frame, verbose=False)

driver_behavior_model = DriverBehaviorModel()
