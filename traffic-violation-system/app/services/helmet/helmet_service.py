import numpy as np
from app.services.helmet.helmet_detector import helmet_detector
from app.utils.helmet_utils import draw_helmet_detections
from app.core.logger import logger

class HelmetService:
    def __init__(self):
        self.is_running = False
        self.latest_helmet_results = {} # Maps vehicle_id -> {"status": str, "confidence": float}

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
                from app.services.tracking.bytetrack_tracker import bytetrack_tracker
                latest_tracks = getattr(bytetrack_tracker, "latest_tracks", [])
                
                current_results = {}
                for det in detections:
                    x1, y1, x2, y2 = det['bbox']
                    status = det['helmet_status']
                    conf = det['confidence']
                    
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
                        current_results[associated_id] = {
                            "status": status,
                            "confidence": conf
                        }
                self.latest_helmet_results = current_results
                frame = draw_helmet_detections(frame, detections)
        except Exception as e:
            logger.error(f"Error during real-time frame helmet processing: {e}")

        return frame

helmet_service = HelmetService()
