import os
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
from app.core.logger import logger
from app.utils.deletion_registry import load_deleted_ids, record_deleted_id

DB_PATH = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "uploads", "cameras.json"
))

class CameraService:
    def __init__(self):
        self.default_cameras = [
            {
                "id": 1,
                "name": "North Intersection Camera",
                "url": "rtsp://192.168.1.101/live",
                "resolution": "1920x1080",
                "fps": 30,
                "enabled": True,
                "recording_enabled": True,
                "status": "Online",
                "health": "Excellent",
                "last_active": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            {
                "id": 2,
                "name": "South Expressway Camera",
                "url": "rtsp://192.168.1.102/live",
                "resolution": "1280x720",
                "fps": 25,
                "enabled": True,
                "recording_enabled": False,
                "status": "Online",
                "health": "Good",
                "last_active": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        ]
        self.cameras = []
        self._load_db()

    def _load_db(self):
        if not os.path.exists(DB_PATH):
            self.cameras = list(self.default_cameras)
            self._save_db()
            return
        try:
            with open(DB_PATH, 'r') as f:
                self.cameras = json.load(f)
        except Exception as e:
            logger.error(f"Error loading cameras DB: {e}")
            self.cameras = list(self.default_cameras)

    def _save_db(self):
        try:
            os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
            with open(DB_PATH, 'w') as f:
                json.dump(self.cameras, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving cameras DB: {e}")

    def list_cameras(self) -> List[Dict[str, Any]]:
        self._load_db()
        deleted_ids = load_deleted_ids("cameras")
        return [c for c in self.cameras if c["id"] not in deleted_ids]

    def create_camera(self, data: Dict[str, Any]) -> Dict[str, Any]:
        self._load_db()
        new_id = max([c["id"] for c in self.cameras], default=0) + 1
        cam = {
            "id": new_id,
            "name": data["name"],
            "url": data["url"],
            "resolution": data.get("resolution", "1920x1080"),
            "fps": data.get("fps", 30),
            "enabled": True,
            "recording_enabled": data.get("recording_enabled", True),
            "status": "Online",
            "health": "Excellent",
            "last_active": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.cameras.append(cam)
        self._save_db()
        return cam

    def update_camera(self, camera_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        self._load_db()
        for c in self.cameras:
            if c["id"] == camera_id:
                for k, v in data.items():
                    if v is not None:
                        c[k] = v
                self._save_db()
                return c
        return None

    def delete_camera(self, camera_id: int) -> bool:
        self._load_db()
        record_deleted_id("cameras", camera_id)
        
        # Database deletion
        from app.database.connection import SessionLocal, check_db_connection
        from app.database.models.camera import Camera
        if check_db_connection():
            db = SessionLocal()
            try:
                r = db.query(Camera).filter(Camera.id == camera_id).first()
                if r:
                    db.delete(r)
                    db.commit()
            except Exception as e_db:
                logger.error(f"Error deleting camera {camera_id} from DB: {e_db}")
                db.rollback()
            finally:
                db.close()
                
        initial_len = len(self.cameras)
        self.cameras = [c for c in self.cameras if c["id"] != camera_id]
        self._save_db()
        return len(self.cameras) < initial_len

camera_service = CameraService()
