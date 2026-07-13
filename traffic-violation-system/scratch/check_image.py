import cv2
import os

uploads_dir = r"c:\Users\Jaspreet\OneDrive\Desktop\Traffic violation Project\traffic-violation-system\uploads"
file_path = os.path.join(uploads_dir, "violation images_8532058e.jpeg")

if os.path.exists(file_path):
    print("File exists!")
    img = cv2.imread(file_path)
    if img is not None:
        print(f"Loaded successfully! Shape: {img.shape}")
    else:
        print("Failed to load image with cv2!")
else:
    print("File does NOT exist on disk!")
