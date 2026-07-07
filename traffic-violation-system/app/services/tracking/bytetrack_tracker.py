import os
from typing import List, Dict, Any
from app.services.detection.yolo_detector import yolo_detector
from app.core.logger import logger

class ByteTrackTracker:
    def __init__(self):
        # Reuses existing model loading state from the yolo_detector singleton
        self.latest_tracks = []

    def update(self, frame) -> List[Dict[str, Any]]:
        """
        Updates the ByteTrack tracker with the current frame and returns tracked vehicles.
        """
        yolo_detector.load_model()
        if yolo_detector.model is None:
            self.latest_tracks = []
            return []

        # Run tracking using Ultralytics built-in ByteTrack
        results = yolo_detector.model.track(frame, persist=True, tracker="bytetrack.yaml", verbose=False)
        if not results:
            self.latest_tracks = []
            return []

        tracked_detections = []
        for result in results:
            boxes = result.boxes
            # Check if boxes have track IDs assigned (IDs won't exist on frames with no tracks)
            if boxes is None or not hasattr(boxes, "id") or boxes.id is None:
                continue
                
            for box in boxes:
                # Class ID is a float in Ultralytics box property
                cls_id = int(box.cls[0].item())
                if cls_id in yolo_detector.vehicle_classes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                    conf = float(box.conf[0].item())
                    # Get tracking ID
                    track_id = int(box.id[0].item())
                    tracked_detections.append({
                        'box': [x1, y1, x2, y2],
                        'class_id': cls_id,
                        'conf': conf,
                        'id': track_id
                    })
        self.latest_tracks = tracked_detections
        return tracked_detections

bytetrack_tracker = ByteTrackTracker()
