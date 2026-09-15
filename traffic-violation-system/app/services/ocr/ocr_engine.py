from app.models.ocr_model import ocr_model_wrapper
from app.utils.ocr_utils import preprocess_plate_image, clean_extracted_text
import easyocr
import torch
import re

class OCREngine:
    def __init__(self):
        self.reader = None
        self._cache = {}

    def get_reader(self):
        if self.reader is None:
            gpu = torch.cuda.is_available()
            self.reader = easyocr.Reader(['en'], gpu=gpu)
        return self.reader

    def clear_cache(self):
        self._cache.clear()

    def extract_text(self, cropped_img, vehicle_id: int) -> dict:
        # Check cache if vehicle already has a recognized high-confidence plate
        if vehicle_id is not None and vehicle_id in self._cache:
            cached = self._cache[vehicle_id]
            if cached.get("confidence", 0.0) >= 0.70 and not cached.get("plate_number", "").startswith("IND-P"):
                return cached

        if cropped_img is None or cropped_img.size == 0:
            return {"plate_number": f"IND-P{vehicle_id:04d}" if vehicle_id >= 0 else "UNREADABLE", "confidence": 0.50}

        h, w = cropped_img.shape[:2]
        # Ignore microscopic or noise crops
        if h < 12 or w < 30:
            return {"plate_number": f"IND-P{vehicle_id:04d}" if vehicle_id >= 0 else "UNREADABLE", "confidence": 0.50}

        preprocessed = preprocess_plate_image(cropped_img)
        
        from app.services.accuracy.accuracy_optimizer import accuracy_optimizer
        import cv2

        # Baseline confidence score from custom PyTorch model
        conf = 0.50
        if preprocessed is not None:
            try:
                conf = ocr_model_wrapper.recognize_text(preprocessed)
            except Exception:
                conf = 0.50
        
        plate_text = ""
        try:
            # Pad and scale crop to optimal CRNN resolution (height ~110-130px)
            pad_y = max(4, int(h * 0.12))
            pad_x = max(8, int(w * 0.12))
            padded = cv2.copyMakeBorder(cropped_img, pad_y, pad_y, pad_x, pad_x, cv2.BORDER_CONSTANT, value=[255, 255, 255])
            
            h_p, w_p = padded.shape[:2]
            if h_p > 160:
                scale = 130.0 / h_p
                scaled = cv2.resize(padded, (int(w_p * scale), 130), interpolation=cv2.INTER_AREA)
            elif h_p < 80:
                scale = 110.0 / h_p
                scaled = cv2.resize(padded, (int(w_p * scale), 110), interpolation=cv2.INTER_CUBIC)
            else:
                scaled = padded

            # Apply contrast and edge enhancement
            enhanced = accuracy_optimizer.enhance_crop_contrast(scaled)
            reader = self.get_reader()
            
            # Fast alphanumeric OCR inference with restricted character allowlist
            ocr_results = reader.readtext(
                enhanced,
                allowlist='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
                paragraph=False,
                batch_size=1
            )
            
            # Fast fallback on grayscale only if contrast was extremely low
            if not ocr_results and np.std(enhanced) < 35:
                gray = cv2.cvtColor(enhanced, cv2.COLOR_BGR2GRAY)
                ocr_results = reader.readtext(
                    gray,
                    allowlist='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
                    paragraph=False,
                    batch_size=1
                )

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
                    # Apply Indian plate syntactic cleaning
                    plate_text = accuracy_optimizer.clean_license_plate(raw_combined)
                    if len(plate_text) >= 4:
                        if scores:
                            conf = float(round(sum(scores) / len(scores), 3))
                    else:
                        plate_text = ""
        except Exception as e:
            from app.core.logger import logger
            logger.debug(f"Fast OCR extraction skipped: {e}")

        # If plate is unreadable from crop or crop was not found, return unverified identifier
        if not plate_text:
            if vehicle_id >= 0:
                plate_text = f"IND-P{vehicle_id:04d}"
                conf = 0.50
            else:
                plate_text = "UNREADABLE"
                conf = 0.0

        res = {
            "plate_number": plate_text,
            "confidence": conf
        }

        # Cache result
        if vehicle_id is not None:
            self._cache[vehicle_id] = res

        return res

ocr_engine = OCREngine()

