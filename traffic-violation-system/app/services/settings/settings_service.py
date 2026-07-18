import os
import json
from typing import Dict, Any

SETTINGS_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "uploads", "system_settings.json"))

class SettingsService:
    def __init__(self):
        self.defaults = {
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
        self.config = self._load_settings()

    def _load_settings(self) -> Dict[str, Any]:
        if not os.path.exists(SETTINGS_FILE):
            os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
            with open(SETTINGS_FILE, 'w') as f:
                json.dump(self.defaults, f, indent=4)
            return self.defaults.copy()
        try:
            with open(SETTINGS_FILE, 'r') as f:
                data = json.load(f)
                res = self.defaults.copy()
                for k, v in data.items():
                    if v is not None:
                        res[k] = v
                return res
        except Exception:
            return self.defaults.copy()

    def _save_settings(self) -> None:
        try:
            os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
            with open(SETTINGS_FILE, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            from app.core.logger import logger
            logger.error(f"Error saving system settings file: {e}")

    def get_settings(self) -> Dict[str, Any]:
        return self.config

    def update_settings(self, data: Dict[str, Any]) -> Dict[str, Any]:
        for k, v in data.items():
            if v is not None:
                self.config[k] = v
        self._save_settings()
        return self.config

settings_service = SettingsService()
