import os
from typing import Dict, Any

class SettingsService:
    def __init__(self):
        # Read sensitive configs from environment variables
        self.config = {
            "smtp_host": os.getenv("SMTP_HOST", "smtp.gmail.com"),
            "smtp_port": int(os.getenv("SMTP_PORT", 587)),
            "smtp_user": os.getenv("SMTP_USER", "notifications@trafficviolation.com"),
            "smtp_password": os.getenv("SMTP_PASSWORD", ""),  # Leave blank, never hardcode!
            "ai_confidence_threshold": float(os.getenv("AI_CONFIDENCE_THRESHOLD", 0.75)),
            "ai_detection_threshold": float(os.getenv("AI_DETECTION_THRESHOLD", 0.50)),
            "camera_reconnect_interval_sec": int(os.getenv("CAMERA_RECONNECT_INTERVAL", 10)),
            "recording_retention_days": int(os.getenv("RECORDING_RETENTION_DAYS", 30)),
            "storage_location": os.getenv("STORAGE_LOCATION", "./evidence"),
            "theme": "dark",
            "language": "en",
            "timezone": "UTC"
        }

    def get_settings(self) -> Dict[str, Any]:
        return self.config

    def update_settings(self, data: Dict[str, Any]) -> Dict[str, Any]:
        for k, v in data.items():
            if v is not None:
                self.config[k] = v
        return self.config

settings_service = SettingsService()
