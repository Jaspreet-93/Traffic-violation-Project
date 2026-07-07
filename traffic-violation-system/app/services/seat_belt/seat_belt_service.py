import numpy as np
from app.services.seat_belt.seat_belt_detector import seat_belt_detector
from app.utils.seat_belt_utils import draw_seat_belt_detections
from app.services.tracking.bytetrack_tracker import bytetrack_tracker
from app.core.logger import logger

class SeatBeltService:
    def __init__(self):
        self.is_running = False
        self.latest_seat_belt_results = {} # Maps vehicle_id -> {"status": str, "confidence": float}

    def start_seat_belt_detection(self):
        """
        Enables the seat belt detection state.
        """
        self.is_running = True
        logger.info("Real-time seat belt detection started.")

    def stop_seat_belt_detection(self):
        """
        Disables the seat belt detection state.
        """
        self.is_running = False
        logger.info("Real-time seat belt detection stopped.")

    def get_status(self) -> bool:
        """
        Returns the active running state of the seat belt detection system.
        """
        return self.is_running

    def process_frame(self, frame: np.ndarray) -> np.ndarray:
        """
        Intercepts camera frame, runs seat belt detection, associates vehicle ID, and draws bounding boxes.
        """
        if not self.is_running:
            return frame

        try:
            detections = seat_belt_detector.detect_seat_belt(frame)
            if not detections:
                return frame

            # Query latest tracked vehicles
            latest_tracks = getattr(bytetrack_tracker, "latest_tracks", [])
            annotated_detections = []
            current_results = {}

            for det in detections:
                x1, y1, x2, y2 = det['bbox']
                cls_id = det['class_id']
                conf = det['confidence']
                
                # Centroid of the seat belt bounding box
                cx = (x1 + x2) / 2.0
                cy = (y1 + y2) / 2.0
                
                associated_id = -1
                for track in latest_tracks:
                    vx1, vy1, vx2, vy2 = track['box']
                    vehicle_id = track['id']
                    if vx1 <= cx <= vx2 and vy1 <= cy <= vy2:
                        associated_id = vehicle_id
                        break
                
                if associated_id != -1:
                    status = "no seatbelt" if cls_id == 1 else "seatbelt"
                    current_results[associated_id] = {
                        "status": status,
                        "confidence": conf
                    }

                annotated_detections.append({
                    "vehicle_id": associated_id,
                    "class_id": cls_id,
                    "bbox": [x1, y1, x2, y2],
                    "confidence": conf
                })

            self.latest_seat_belt_results = current_results
            frame = draw_seat_belt_detections(frame, annotated_detections)
        except Exception as e:
            logger.error(f"Error during real-time frame seat belt processing: {e}")

        return frame

seat_belt_service = SeatBeltService()
