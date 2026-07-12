import cv2
import numpy as np
from app.services.tracking.bytetrack_tracker import bytetrack_tracker
from app.services.tracking.track_manager import track_manager
from app.services.detection.yolo_detector import yolo_detector
from app.core.logger import logger

class TrackingService:
    def __init__(self):
        self.is_running = False
        self.frame_counter = 0

    def start_tracking(self):
        """
        Enables vehicle tracking workflow.
        """
        self.is_running = True
        self.frame_counter = 0
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

        self.frame_counter += 1
        try:
            tracked_vehicles = bytetrack_tracker.update(frame)
            if tracked_vehicles:
                # Update tracked state in TrackManager
                track_manager.update_tracks(frame, tracked_vehicles, self.frame_counter)
                
                # Draw custom boundaries: Box + Class | ID:XX and Plate details if found
                for det in tracked_vehicles:
                    x1, y1, x2, y2 = det["box"]
                    t_id = det["id"]
                    conf = det["conf"]
                    cls_id = det["class_id"]
                    
                    # Resolve class label name
                    cls_name = yolo_detector.vehicle_classes.get(cls_id, "car")
                    
                    # 1. Run High-Accuracy Plate Detector (Stage 3)
                    from app.services.number_plate.plate_detector import plate_detector
                    plate_detector.detect_plates_for_vehicle(
                        frame=frame,
                        vehicle_box=[x1, y1, x2, y2],
                        track_id=t_id,
                        vehicle_type=cls_name,
                        frame_number=self.frame_counter
                    )
                    
                    # Draw vehicle bounding box
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    
                    # Check if plate was successfully detected
                    from app.services.number_plate.plate_manager import plate_manager
                    plate_record = plate_manager.get_plate_by_track(t_id)
                    
                    # Draw vehicle label: Car | ID:17
                    vehicle_label = f"{cls_name.capitalize()} | ID:{t_id}"
                    (w_label, h_label), _ = cv2.getTextSize(vehicle_label, cv2.FONT_HERSHEY_SIMPLEX, 0.4, 1)
                    cv2.rectangle(frame, (x1, max(0, y1 - h_label - 8)), (x1 + w_label + 10, y1), (0, 255, 0), -1)
                    cv2.putText(frame, vehicle_label, (x1 + 5, max(12, y1 - 4)), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1, cv2.LINE_AA)
                    
                    # Draw plate box if available: Plate: 96%
                    if plate_record and plate_record.get("plate_bbox"):
                        px1, py1, px2, py2 = plate_record["plate_bbox"]
                        p_conf = plate_record["confidence"]
                        
                        cv2.rectangle(frame, (px1, py1), (px2, py2), (0, 0, 255), 2)
                        plate_label = f"Plate: {int(p_conf * 100)}%"
                        (wp_label, hp_label), _ = cv2.getTextSize(plate_label, cv2.FONT_HERSHEY_SIMPLEX, 0.4, 1)
                        cv2.rectangle(frame, (px1, max(0, py1 - hp_label - 8)), (px1 + wp_label + 10, py1), (0, 0, 255), -1)
                        cv2.putText(frame, plate_label, (px1 + 5, max(12, py1 - 4)), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
        except Exception as e:
            logger.error(f"Error during real-time frame tracking processing: {e}")

        return frame

tracking_service = TrackingService()
