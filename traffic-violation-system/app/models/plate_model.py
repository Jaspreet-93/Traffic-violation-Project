import os
from ultralytics import YOLO
from app.core.logger import logger

class PlateModel:
    def __init__(self):
        self.model = None
        self.model_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), "..", "..", "models", "number_plate", "plate_yolo11.pt"
        ))
        if not os.path.exists(self.model_path):
            self.model_path = os.path.abspath(os.path.join(
                os.path.dirname(__file__), "..", "..", "models", "number_plate", "plate_detector.pt"
            ))

    def load_model(self):
        """
        Loads the custom number plate YOLOv8 model weights lazily.
        """
        if self.model is None:
            logger.info(f"Loading custom number plate model from: {self.model_path}")
            if not os.path.exists(self.model_path):
                logger.error(f"Plate detector weights not found at: {self.model_path}")
                raise FileNotFoundError(f"Plate detector weights file not found: {self.model_path}")
            try:
                self.model = YOLO(self.model_path)
                logger.info("Custom number plate YOLOv8 model loaded successfully.")
            except Exception as e:
                logger.error(f"Error loading custom number plate YOLOv8 model: {e}")
                raise

    def predict(self, frame):
        """
        Runs model inference on the frame and returns raw YOLO results.
        """
        self.load_model()
        if self.model is None:
            return None
        return self.model(frame, verbose=False)

plate_model = PlateModel()
