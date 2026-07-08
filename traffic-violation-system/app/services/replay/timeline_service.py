from typing import List, Dict, Any

class TimelineService:
    @staticmethod
    def get_timeline_markers(violation_id: str) -> List[Dict[str, Any]]:
        """
        Builds the playback seekbar events metadata timeline.
        """
        return [
            {"time_offset_sec": 1.5, "event_name": "Vehicle Detected", "description": "Motorcycle bounding box initialized", "confidence": 0.96},
            {"time_offset_sec": 3.0, "event_name": "Vehicle Tracked", "description": "ByteTrack tracker registered trajectory", "confidence": 0.94},
            {"time_offset_sec": 4.5, "event_name": "Helmet Detection Check", "description": "Rider head region mapped", "confidence": 0.92},
            {"time_offset_sec": 6.0, "event_name": "OCR Plate Scan", "description": "Plate characters identified", "confidence": 0.93},
            {"time_offset_sec": 7.5, "event_name": "Seat Belt Scanner", "description": "Skipped for vehicle type", "confidence": None},
            {"time_offset_sec": 8.0, "event_name": "Traffic Light Scan", "description": "Signal green light detected", "confidence": 0.98},
            {"time_offset_sec": 9.0, "event_name": "Driver Behaviour Scan", "description": "Alert status tracked", "confidence": 0.91},
            {"time_offset_sec": 10.0, "event_name": "Violation Generated", "description": "Rule violation decision matches", "confidence": 0.92},
            {"time_offset_sec": 11.5, "event_name": "Evidence Saved", "description": "Snapshot saved to storage", "confidence": None},
            {"time_offset_sec": 13.0, "event_name": "Email Sent", "description": "SMTP message sent to owner", "confidence": None}
        ]
