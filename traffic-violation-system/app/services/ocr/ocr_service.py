import numpy as np
from app.services.ocr.ocr_engine import ocr_engine
from app.utils.ocr_utils import draw_ocr_results
from app.services.number_plate.plate_detector import plate_detector
from app.services.tracking.bytetrack_tracker import bytetrack_tracker
from app.core.logger import logger

class OCRService:
    def __init__(self):
        self.is_running = False
        self.latest_ocr_results = {} # Maps vehicle_id -> {"plate_number": str, "confidence": float}

    def start_ocr(self):
        """
        Enables the OCR text extraction processing state.
        """
        self.is_running = True
        logger.info("Real-time vehicle number plate OCR text extraction started.")

    def stop_ocr(self):
        """
        Disables the OCR text extraction processing state.
        """
        self.is_running = False
        logger.info("Real-time vehicle number plate OCR text extraction stopped.")

    def get_status(self) -> bool:
        """
        Returns the active running state of the OCR processing pipeline.
        """
        return self.is_running

    def process_frame(self, frame: np.ndarray) -> np.ndarray:
        """
        Intercepts camera frame, crops number plate boxes, extracts text characters, and overlays labels.
        """
        if not self.is_running:
            return frame

        try:
            detections = plate_detector.detect_plates(frame)
            if not detections:
                return frame

            # Query latest tracked vehicles
            latest_tracks = getattr(bytetrack_tracker, "latest_tracks", [])
            ocr_associations = []

            for det in detections:
                px1, py1, px2, py2 = det['bbox']
                
                # Bounding box bounds checks
                h, w = frame.shape[:2]
                px1 = max(0, px1)
                py1 = max(0, py1)
                px2 = min(w, px2)
                py2 = min(h, py2)
                
                if px2 <= px1 or py2 <= py1:
                    continue
                    
                # Crop the number plate sub-region
                cropped_img = frame[py1:py2, px1:px2]
                if cropped_img.size == 0:
                    continue
                    
                # Centroid of the plate bounding box
                cx = (px1 + px2) / 2.0
                cy = (py1 + py2) / 2.0
                
                associated_id = -1
                for track in latest_tracks:
                    vx1, vy1, vx2, vy2 = track['box']
                    vehicle_id = track['id']
                    if vx1 <= cx <= vx2 and vy1 <= cy <= vy2:
                        associated_id = vehicle_id
                        break
                
                # Extract text using OCR engine
                ocr_res = ocr_engine.extract_text(cropped_img, associated_id)
                plate_number = ocr_res["plate_number"]
                ocr_conf = ocr_res["confidence"]
                
                # Cache results if vehicle ID is matched
                if associated_id != -1:
                    self.latest_ocr_results[associated_id] = {
                        "plate_number": plate_number,
                        "confidence": ocr_conf
                    }
                
                ocr_associations.append({
                    "vehicle_id": associated_id,
                    "plate_bbox": [px1, py1, px2, py2],
                    "plate_number": plate_number,
                    "confidence": ocr_conf
                })

            frame = draw_ocr_results(frame, ocr_associations)
        except Exception as e:
            logger.error(f"Error during real-time frame OCR processing: {e}")

        return frame

ocr_service = OCRService()
