import numpy as np
from app.services.tracking.bytetrack_tracker import bytetrack_tracker
from app.utils.tracking_utils import draw_tracking_detections
from app.services.detection.yolo_detector import yolo_detector
from app.core.logger import logger

class TrackingService:
    def __init__(self):
        self.is_running = False

    def start_tracking(self):
        """
        Enables vehicle tracking workflow.
        """
        self.is_running = True
        logger.info("Real-time vehicle tracking started.")

    def stop_tracking(self):
        """
        Disables vehicle tracking workflow.
        """
        self.is_running = False
        logger.info("Real-time vehicle tracking stopped.")

    def get_status(self) -> bool:
        """
        Returns the active running state of the vehicle tracking system.
        """
        return self.is_running

    def process_frame(self, frame: np.ndarray) -> np.ndarray:
        """
        Intercepts camera frame and applies ByteTrack multi-object vehicle tracking.
        """
        if not self.is_running:
            return frame

        try:
            tracked_vehicles = bytetrack_tracker.update(frame)
            if tracked_vehicles:
                frame = draw_tracking_detections(
                    frame,
                    tracked_vehicles,
                    yolo_detector.vehicle_classes
                )
        except Exception as e:
            logger.error(f"Error during real-time frame tracking processing: {e}")

        return frame

tracking_service = TrackingService()
