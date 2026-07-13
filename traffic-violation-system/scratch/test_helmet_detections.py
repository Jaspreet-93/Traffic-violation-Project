import cv2
import sys
import os
from ultralytics import YOLO

# Add parent path to import app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.models.plate_model import plate_model

def main():
    img_path = "uploads/violation images_8532058e.jpeg"
    if not os.path.exists(img_path):
        print(f"File not found: {img_path}")
        return

    frame = cv2.imread(img_path)
    plate_model.load_model()
    
    print("\n--- Running Plate Model on Full Frame with conf=0.001 ---")
    results = plate_model.model(frame, conf=0.001, verbose=False)
    for res in results:
        print("Predictions found:", len(res.boxes))
        if len(res.boxes) > 0:
            print("Boxes:", res.boxes.xyxy.tolist()[:10])
            print("Confidences:", res.boxes.conf.tolist()[:10])

if __name__ == "__main__":
    main()
