import numpy as np
from app.services.traffic_light.traffic_light_detector import traffic_light_detector
from app.utils.traffic_light_utils import draw_traffic_light_detections
from app.core.logger import logger

class TrafficLightService:
    def __init__(self):
        self.is_running = False
        self.latest_traffic_light_state = "green" # Default to green

    def start_traffic_light_detection(self):
        """
        Enables the traffic light detection state.
        """
        self.is_running = True
        logger.info("Real-time traffic light signal detection started.")

    def stop_traffic_light_detection(self):
        """
        Disables the traffic light detection state.
        """
        self.is_running = False
        logger.info("Real-time traffic light signal detection stopped.")

    def get_status(self) -> bool:
        """
        Returns the active running state of the traffic light detection system.
        """
        return self.is_running

    def process_frame(self, frame: np.ndarray) -> np.ndarray:
        """
        Intercepts camera frame, runs traffic light detection, and draws signal boxes.
        """
        if not self.is_running:
            return frame

        try:
            detections = traffic_light_detector.detect_traffic_lights(frame)
            if not detections:
                return frame

            # Determine global signal state
            state = "green"
            for det in detections:
                if det['class_id'] == 0: # red
                    state = "red"
                    break
                elif det['class_id'] == 1 and state != "red":
                    state = "yellow"
            self.latest_traffic_light_state = state

            frame = draw_traffic_light_detections(frame, detections)
        except Exception as e:
            logger.error(f"Error during real-time frame traffic light processing: {e}")

        return frame

traffic_light_service = TrafficLightService()
