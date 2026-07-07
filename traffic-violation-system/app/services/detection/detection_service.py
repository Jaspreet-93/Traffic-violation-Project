import numpy as np
from app.services.detection.yolo_detector import yolo_detector
from app.utils.image_utils import draw_detections
from app.core.logger import logger

class DetectionService:
    def __init__(self):
        self.is_running = False

    def start_detection(self):
        """
        Enables vehicle detection processing.
        """
        self.is_running = True
        logger.info("Real-time vehicle detection engine started.")

    def stop_detection(self):
        """
        Disables vehicle detection processing.
        """
        self.is_running = False
        logger.info("Real-time vehicle detection engine stopped.")

    def get_status(self) -> bool:
        """
        Returns the active running state of the vehicle detection system.
        """
        return self.is_running

    def process_frame(self, frame: np.ndarray) -> np.ndarray:
        """
        Annotates the frame with YOLOv8 vehicle detections if the service is running.
        """
        if not self.is_running:
            return frame

        try:
            detections = yolo_detector.predict_vehicles(frame)
            if detections:
                frame = draw_detections(
                    frame, 
                    detections, 
                    yolo_detector.vehicle_classes
                )
        except Exception as e:
            logger.error(f"Error during real-time frame detection processing: {e}")
        
        return frame

detection_service = DetectionService()
