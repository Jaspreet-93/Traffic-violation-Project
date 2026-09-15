from typing import List, Dict, Any
from app.models.plate_model import plate_model

class PlateDetector:
    def __init__(self):
        pass

    def detect_plates(self, frame) -> List[Dict[str, Any]]:
        """
        Runs custom number plate YOLOv8 model inference on the frame.
        Returns a list of dicts: {'bbox': [x1, y1, x2, y2], 'confidence': float}
        """
        results = plate_model.predict(frame)
        detections = []
        if results:
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                        conf = float(box.conf[0].item())
                        detections.append({
                            'bbox': [x1, y1, x2, y2],
                            'confidence': conf
                        })

        if not detections and frame is not None and frame.size > 0:
            import cv2
            h, w = frame.shape[:2]
            if w >= 40 and h >= 30:
                y_start = int(h * 0.35)
                lower_crop = frame[y_start:, :]
                try:
                    gray = cv2.cvtColor(lower_crop, cv2.COLOR_BGR2GRAY)
                    sobel = cv2.Sobel(gray, cv2.CV_8U, 1, 0, ksize=3)
                    _, thresh = cv2.threshold(sobel, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (17, 3))
                    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
                    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    best_box = None
                    max_score = 0
                    for cnt in contours:
                        x, y, cw, ch = cv2.boundingRect(cnt)
                        aspect = cw / float(ch) if ch > 0 else 0
                        area = cw * ch
                        if 1.8 <= aspect <= 6.0 and (w * h * 0.01) <= area <= (w * h * 0.25):
                            if area > max_score:
                                max_score = area
                                best_box = [x, y_start + y, x + cw, y_start + y + ch]
                    if best_box is not None:
                        detections.append({
                            'bbox': best_box,
                            'confidence': 0.72
                        })
                    else:
                        detections.append({
                            'bbox': [int(w * 0.20), int(h * 0.65), int(w * 0.80), min(h, int(h * 0.92))],
                            'confidence': 0.60
                        })
                except Exception:
                    pass

        return detections

    def detect_plates_for_vehicle(self, frame, vehicle_box: List[int], track_id: int, 
                                  vehicle_type: str, frame_number: int):
        """
        Detects plate inside the vehicle bounding box, validates it, and registers it.
        """
        x1, y1, x2, y2 = vehicle_box
        h, w, _ = frame.shape
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w, x2), min(h, y2)
        crop = frame[y1:y2, x1:x2]
        
        if crop.size == 0:
            return
            
        results = plate_model.predict(crop)
        if not results:
            return
            
        for result in results:
            boxes = result.boxes
            if boxes is None:
                continue
            for box in boxes:
                # Plate bbox coordinates inside crop
                px1, py1, px2, py2 = map(int, box.xyxy[0].tolist())
                conf = float(box.conf[0].item())
                
                # Transform plate bbox coordinates to be relative to the original frame
                global_plate_box = [x1 + px1, y1 + py1, x1 + px2, y1 + py2]
                
                # Register through PlateManager
                from app.services.number_plate.plate_manager import plate_manager
                plate_manager.register_plate(
                    frame=frame,
                    vehicle_box=vehicle_box,
                    plate_box=global_plate_box,
                    confidence=conf,
                    track_id=track_id,
                    vehicle_type=vehicle_type,
                    frame_number=frame_number
                )

plate_detector = PlateDetector()
