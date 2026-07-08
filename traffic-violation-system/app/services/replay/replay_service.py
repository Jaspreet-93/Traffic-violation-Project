from datetime import datetime, timedelta
from typing import List, Dict, Any
from app.services.upload_detection.upload_service import UploadService

class ReplayService:
    @staticmethod
    def list_replays() -> List[Dict[str, Any]]:
        """
        Scans upload history to compile active replay lists.
        """
        history_items = UploadService.load_history()
        results = []

        for item in history_items:
            if item.get("status") == "Completed" and item.get("file_type") == "video":
                results.append({
                    "violation_id": item["job_id"],
                    "filename": item["filename"],
                    "violation_type": "No Helmet",
                    "timestamp": item["upload_date"],
                    "duration_sec": 15.0
                })

        # Default fallback items if list is empty
        if not results:
            now = datetime.now()
            results.append({
                "violation_id": "violation-mock-1",
                "filename": "camera_feed_intersection_12.mp4",
                "violation_type": "No Helmet",
                "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
                "duration_sec": 24.5
            })
            results.append({
                "violation_id": "violation-mock-2",
                "filename": "highway_monitoring_clip.mp4",
                "violation_type": "No Seat Belt",
                "timestamp": (now - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S"),
                "duration_sec": 18.0
            })

        return results

    @classmethod
    def get_replay(cls, violation_id: str) -> dict:
        replays = cls.list_replays()
        target = None
        for r in replays:
            if r["violation_id"] == violation_id:
                target = r
                break
                
        if not target:
            target = replays[0]

        return {
            "violation_id": violation_id,
            "original_video_url": f"/uploads/processed_{target['filename']}",
            "processed_video_url": f"/uploads/processed_{target['filename']}",
            "violation_type": target["violation_type"],
            "timestamp": target["timestamp"],
            "processing_time_sec": 4.82,
            "overall_trust_score": 93.4
        }
