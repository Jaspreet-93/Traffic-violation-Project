import os
from ultralytics import YOLO
from app.core.logger import logger

class HelmetModel:
    def __init__(self):
        self.model = None
        # Locate models/helmet/helmet_model.pt relative to the app/models directory
        self.model_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), "..", "..", "models", "helmet", "helmet_model.pt"
        ))

    def load_model(self):
        """
        Loads the custom helmet YOLOv8 model weights lazily.
        """
        if self.model is None:
            logger.info(f"Loading custom helmet model from: {self.model_path}")
            if not os.path.exists(self.model_path):
                logger.error(f"Helmet model weights not found at: {self.model_path}")
                raise FileNotFoundError(f"Helmet model weights file not found: {self.model_path}")
            try:
                self.model = YOLO(self.model_path)
                logger.info("Custom helmet YOLOv8 model loaded successfully.")
            except Exception as e:
                logger.error(f"Error loading custom helmet YOLOv8 model: {e}")
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
        imgsz = 640
        return self.model(frame, verbose=False, device=device, half=half, imgsz=imgsz)

helmet_model = HelmetModel()
