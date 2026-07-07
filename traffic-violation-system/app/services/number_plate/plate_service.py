import numpy as np
from app.services.number_plate.plate_detector import plate_detector
from app.utils.plate_utils import draw_plate_detections
from app.services.tracking.bytetrack_tracker import bytetrack_tracker
from app.core.logger import logger

class PlateService:
    def __init__(self):
        self.is_running = False

    def start_plate_detection(self):
        """
        Enables the number plate detection processing state.
        """
        self.is_running = True
        logger.info("Real-time vehicle number plate detection started.")

    def stop_plate_detection(self):
        """
        Disables the number plate detection processing state.
        """
        self.is_running = False
        logger.info("Real-time vehicle number plate detection stopped.")

    def get_status(self) -> bool:
        """
        Returns the active running state of the number plate detection system.
        """
        return self.is_running

    def process_frame(self, frame: np.ndarray) -> np.ndarray:
        """
        Intercepts camera frame, runs plate detection, maps centroids to vehicle IDs, and overlays boxes.
        """
        if not self.is_running:
            return frame

        try:
            detections = plate_detector.detect_plates(frame)
            if not detections:
                return frame

            # Query latest tracked vehicles
            latest_tracks = getattr(bytetrack_tracker, "latest_tracks", [])
            plate_associations = []

            for det in detections:
                px1, py1, px2, py2 = det['bbox']
                conf = det['confidence']
                
                # Centroid of the plate bounding box
                cx = (px1 + px2) / 2.0
                cy = (py1 + py2) / 2.0
                
                associated_id = -1
                # Check spatial containment inside tracked vehicle boxes
                for track in latest_tracks:
                    vx1, vy1, vx2, vy2 = track['box']
                    vehicle_id = track['id']
                    if vx1 <= cx <= vx2 and vy1 <= cy <= vy2:
                        associated_id = vehicle_id
                        break
                
                plate_associations.append({
                    "vehicle_id": associated_id,
                    "plate_bbox": [px1, py1, px2, py2],
                    "confidence": conf
                })

            frame = draw_plate_detections(frame, plate_associations)
        except Exception as e:
            logger.error(f"Error during real-time frame number plate processing: {e}")

        return frame

plate_service = PlateService()
