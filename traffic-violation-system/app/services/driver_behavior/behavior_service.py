import numpy as np
from app.services.driver_behavior.behavior_detector import behavior_detector
from app.utils.behavior_utils import draw_behavior_detections
from app.services.tracking.bytetrack_tracker import bytetrack_tracker
from app.core.logger import logger

class BehaviorService:
    def __init__(self):
        self.is_running = False

    def start_behavior_detection(self):
        """
        Enables the driver behavior detection state.
        """
        self.is_running = True
        logger.info("Real-time driver behavior detection started.")

    def stop_behavior_detection(self):
        """
        Disables the driver behavior detection state.
        """
        self.is_running = False
        logger.info("Real-time driver behavior detection stopped.")

    def get_status(self) -> bool:
        """
        Returns the active running state of the driver behavior detection system.
        """
        return self.is_running

    def process_frame(self, frame: np.ndarray) -> np.ndarray:
        """
        Intercepts camera frame, runs behavior detection, associates vehicle ID, and draws bounding boxes.
        """
        if not self.is_running:
            return frame

        try:
            detections = behavior_detector.detect_behavior(frame)
            if not detections:
                return frame

            # Query latest tracked vehicles
            latest_tracks = getattr(bytetrack_tracker, "latest_tracks", [])
            annotated_detections = []

            for det in detections:
                x1, y1, x2, y2 = det['bbox']
                cls_id = det['class_id']
                conf = det['confidence']
                
                # Centroid of the driver behavior detection bounding box
                cx = (x1 + x2) / 2.0
                cy = (y1 + y2) / 2.0
                
                associated_id = -1
                for track in latest_tracks:
                    vx1, vy1, vx2, vy2 = track['box']
                    vehicle_id = track['id']
                    if vx1 <= cx <= vx2 and vy1 <= cy <= vy2:
                        associated_id = vehicle_id
                        break
                
                annotated_detections.append({
                    "vehicle_id": associated_id,
                    "class_id": cls_id,
                    "bbox": [x1, y1, x2, y2],
                    "confidence": conf
                })

            frame = draw_behavior_detections(frame, annotated_detections)
        except Exception as e:
            logger.error(f"Error during real-time frame behavior processing: {e}")

        return frame

behavior_service = BehaviorService()
