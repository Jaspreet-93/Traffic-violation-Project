import cv2
import os

class ThumbnailGenerator:
    @staticmethod
    def generate_video_thumbnail(video_path: str, thumbnail_path: str) -> bool:
        """
        Extracts the first frame from the video file and saves it as a JPEG image.
        """
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return False
            
        ret, frame = cap.read()
        cap.release()
        
        if ret and frame is not None:
            os.makedirs(os.path.dirname(thumbnail_path), exist_ok=True)
            cv2.imwrite(thumbnail_path, frame)
            return True
            
        return False
