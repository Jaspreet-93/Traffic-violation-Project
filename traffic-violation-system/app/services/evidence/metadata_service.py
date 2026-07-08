from datetime import datetime

class MetadataService:
    @staticmethod
    def get_metadata(evidence_id: int, violation_type: str = "No Helmet") -> dict:
        """
        Retrieves hardware and resolution parameters.
        """
        return {
            "evidence_id": evidence_id,
            "detection_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "processing_time_ms": 14.5,
            "vehicle_type": "Motorcycle" if violation_type == "No Helmet" else "Car",
            "violation_type": violation_type,
            "confidence": 0.93,
            "model_version": "AURA-YOLOv8-v1.2",
            "evidence_size_kb": 245.8,
            "resolution": "1920x1080"
        }
