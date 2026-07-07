import numpy as np
from app.services.helmet.helmet_detector import helmet_detector
from app.utils.helmet_utils import draw_helmet_detections
from app.core.logger import logger

class HelmetService:
    def __init__(self):
        self.is_running = False

    def start_helmet_detection(self):
        """
        Enables the helmet detection processing state.
        """
        self.is_running = True
        logger.info("Real-time helmet detection started.")

    def stop_helmet_detection(self):
        """
        Disables the helmet detection processing state.
        """
        self.is_running = False
        logger.info("Real-time helmet detection stopped.")

    def get_status(self) -> bool:
        """
        Returns the active running state of the helmet detection system.
        """
        return self.is_running

    def process_frame(self, frame: np.ndarray) -> np.ndarray:
        """
        Intercepts raw camera frame and overlays custom helmet detections if enabled.
        """
        if not self.is_running:
            return frame

        try:
            detections = helmet_detector.detect_helmets(frame)
            if detections:
                frame = draw_helmet_detections(frame, detections)
        except Exception as e:
            logger.error(f"Error during real-time frame helmet processing: {e}")

        return frame

helmet_service = HelmetService()
