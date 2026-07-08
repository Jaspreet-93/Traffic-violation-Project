from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class ReplayListItem(BaseModel):
    violation_id: str
    filename: str
    violation_type: str
    timestamp: str
    duration_sec: float

class ReplayListResponse(BaseModel):
    replays: List[ReplayListItem]

class ReplayDetailResponse(BaseModel):
    violation_id: str
    original_video_url: str
    processed_video_url: str
    violation_type: str
    timestamp: str
    processing_time_sec: float
    overall_trust_score: float

class TimelineEventItem(BaseModel):
    time_offset_sec: float
    event_name: str
    description: str
    confidence: Optional[float] = None

class ReplayTimelineResponse(BaseModel):
    violation_id: str
    events: List[TimelineEventItem]

class FrameViewerResponse(BaseModel):
    frame_number: int
    image_url: str
    objects: List[Dict[str, Any]]
