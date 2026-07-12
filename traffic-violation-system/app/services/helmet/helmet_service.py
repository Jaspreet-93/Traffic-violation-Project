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
            from app.services.tracking.bytetrack_tracker import bytetrack_tracker
            latest_tracks = getattr(bytetrack_tracker, "latest_tracks", [])
            
            from app.services.helmet.helmet_manager import helmet_manager
            current_results = {}
            
            for track in latest_tracks:
                cls_id = track.get("class_id")
                # Class 3 is Motorcycle
                if cls_id == 3:
                    box = track["box"]
                    t_id = track["id"]
                    
                    # Run State 5 high-accuracy verified manager
                    status = helmet_manager.process_motorcycle_frame(
                        frame=frame,
                        vehicle_box=box,
                        track_id=t_id,
                        frame_number=0 # live processing
                    )
                    
                    current_results[t_id] = {
                        "status": status,
                        "confidence": 0.88
                    }
                    
                    # Draw annotations
                    if status == "no helmet":
                        x1, y1, x2, y2 = box
                        cv2 = draw_helmet_detections.__globals__["cv2"]
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                        cv2.putText(frame, f"No Helmet | ID:{t_id}", (x1, max(0, y1 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                        
            self.latest_helmet_results = current_results
        except Exception as e:
            logger.error(f"Error during real-time frame helmet processing: {e}")

        return frame

helmet_service = HelmetService()
