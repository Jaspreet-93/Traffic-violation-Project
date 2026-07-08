from typing import List, Dict, Any, Optional
from datetime import datetime

class CameraService:
    def __init__(self):
        # In-memory store for cameras to fallback on database downtime
        self.cameras = [
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

    def list_cameras(self) -> List[Dict[str, Any]]:
        return self.cameras

    def create_camera(self, data: Dict[str, Any]) -> Dict[str, Any]:
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
        return cam

    def update_camera(self, camera_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        for c in self.cameras:
            if c["id"] == camera_id:
                for k, v in data.items():
                    if v is not None:
                        c[k] = v
                return c
        return None

    def delete_camera(self, camera_id: int) -> bool:
        initial_len = len(self.cameras)
        self.cameras = [c for c in self.cameras if c["id"] != camera_id]
        return len(self.cameras) < initial_len

camera_service = CameraService()
