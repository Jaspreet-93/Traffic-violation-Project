from app.services.camera_management.camera_service import camera_service

class RecordingService:
    @staticmethod
    def toggle_recording(camera_id: int, recording_enabled: bool) -> bool:
        res = camera_service.update_camera(camera_id, {"recording_enabled": recording_enabled})
        return res is not None
