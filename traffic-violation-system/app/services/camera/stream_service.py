import time
from app.services.camera.camera_manager import camera_manager

class StreamService:
    @staticmethod
    def generate_mjpeg_stream():
        """
        FastAPI generator that yields JPEG frame buffers as a multipart stream.
        """
        while True:
            frame_bytes = camera_manager.get_latest_frame()
            
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n"
                b"Content-Length: " + str(len(frame_bytes)).encode() + b"\r\n\r\n" +
                frame_bytes +
                b"\r\n"
            )
            
            # Deliver stream at ~25 FPS to control frame pacing
            time.sleep(0.04)
