from app.models.ocr_model import ocr_model_wrapper
from app.utils.ocr_utils import preprocess_plate_image, clean_extracted_text
import easyocr
import torch
import re

class OCREngine:
    def __init__(self):
        self.reader = None

    def get_reader(self):
        if self.reader is None:
            gpu = torch.cuda.is_available()
            self.reader = easyocr.Reader(['en'], gpu=gpu)
        return self.reader

    def extract_text(self, cropped_img, vehicle_id: int) -> dict:
        preprocessed = preprocess_plate_image(cropped_img)
        
        from app.services.accuracy.accuracy_optimizer import accuracy_optimizer
        import cv2

        # Run inference through PyTorch model to get baseline confidence score
        conf = 0.0
        if preprocessed is not None:
            try:
                conf = ocr_model_wrapper.recognize_text(preprocessed)
            except Exception:
                conf = 0.50
        
        plate_text = ""
        # Try to run real OCR using EasyOCR on the enhanced cropped image
        if cropped_img is not None and cropped_img.size > 0:
            try:
                h, w = cropped_img.shape[:2]
                # Pad and scale up small plate crops so characters are sharp and clear
                pad_y = max(8, int(h * 0.15))
                pad_x = max(12, int(w * 0.15))
                padded = cv2.copyMakeBorder(cropped_img, pad_y, pad_y, pad_x, pad_x, cv2.BORDER_CONSTANT, value=[255, 255, 255])
                
                h_p, w_p = padded.shape[:2]
                if h_p < 100:
                    scale = 120.0 / h_p
                    scaled = cv2.resize(padded, (int(w_p * scale), 120), interpolation=cv2.INTER_CUBIC)
                else:
                    scaled = padded

                # Apply contrast and edge enhancement
                enhanced = accuracy_optimizer.enhance_crop_contrast(scaled)
                reader = self.get_reader()
                
                # First attempt: Enhanced BGR
                ocr_results = reader.readtext(enhanced)
                if not ocr_results:
                    # Second attempt: CLAHE grayscale
                    gray = cv2.cvtColor(enhanced, cv2.COLOR_BGR2GRAY)
                    ocr_results = reader.readtext(gray)

                if ocr_results:
                    texts = []
                    scores = []
                    for bbox, text, score in ocr_results:
                        clean = re.sub(r'[^A-Za-z0-9]', '', text)
                        if clean:
                            texts.append(clean)
                            scores.append(float(score))
                    if texts:
                        raw_combined = "".join(texts).upper()
                        # Apply Indian plate syntactic cleaning (resolving O/0, I/1, Z/2, S/5, B/8 confusion)
                        plate_text = accuracy_optimizer.clean_license_plate(raw_combined)
                        if len(plate_text) >= 4:
                            if scores:
                                conf = float(round(sum(scores) / len(scores), 3))
                        else:
                            plate_text = ""
            except Exception as e:
                from app.core.logger import logger
                logger.error(f"EasyOCR extraction failed: {e}")

        # If plate is unreadable from crop or crop was not found, return unverified identifier
        if not plate_text:
            if vehicle_id >= 0:
                plate_text = f"IND-P{vehicle_id:04d}"
                conf = 0.50
            else:
                plate_text = "UNREADABLE"
                conf = 0.0

        return {
            "plate_number": plate_text,
            "confidence": conf
        }

ocr_engine = OCREngine()

