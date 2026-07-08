from app.services.camera_management.camera_service import camera_service

class StreamMonitor:
    @staticmethod
    def get_status_summary() -> dict:
        cams = camera_service.list_cameras()
        online = sum(1 for c in cams if c["status"] == "Online")
        recording = sum(1 for c in cams if c["recording_enabled"])
        return {
            "total_cameras": len(cams),
            "online_cameras": online,
            "offline_cameras": len(cams) - online,
            "recording_cameras": recording
        }
