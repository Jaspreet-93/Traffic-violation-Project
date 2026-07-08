from typing import List, Dict, Any

class FrameService:
    @staticmethod
    def get_frame_details(violation_id: str, frame_number: int) -> dict:
        """
        Retrieves processed outputs at frame offsets.
        """
        return {
            "frame_number": frame_number,
            "image_url": f"/uploads/frame_{violation_id}_{frame_number}.jpg",
            "objects": [
                {"label": "motorcycle", "bbox": [120, 180, 240, 380], "confidence": 0.94},
                {"label": "no helmet", "bbox": [150, 120, 210, 178], "confidence": 0.92}
            ]
        }
