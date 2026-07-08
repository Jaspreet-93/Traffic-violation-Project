from fastapi import APIRouter, HTTPException, status
from typing import List

from app.schemas.replay import (
    ReplayListResponse,
    ReplayDetailResponse,
    ReplayTimelineResponse,
    FrameViewerResponse
)

from app.services.replay.replay_service import ReplayService
from app.services.replay.timeline_service import TimelineService
from app.services.replay.frame_service import FrameService
from app.services.replay.replay_validator import ReplayValidator

router = APIRouter(prefix="/replay", tags=["Violation Replay Center"])

@router.get("/list", response_model=ReplayListResponse)
def list_replays():
    """
    Returns index of logs files supporting violation replay.
    """
    items = ReplayService.list_replays()
    return {"replays": items}

@router.get("/{violation_id}", response_model=ReplayDetailResponse)
def get_replay_details(violation_id: str):
    """
    Retrieves video resolution parameters and url path links.
    """
    ReplayValidator.validate_violation_id(violation_id)
    return ReplayService.get_replay(violation_id)

@router.get("/timeline/{violation_id}", response_model=ReplayTimelineResponse)
def get_timeline(violation_id: str):
    """
    Returns markers mapping models predictions at frame offsets.
    """
    ReplayValidator.validate_violation_id(violation_id)
    events = TimelineService.get_timeline_markers(violation_id)
    return {
        "violation_id": violation_id,
        "events": events
    }

@router.get("/frame/{violation_id}/{frame_number}", response_model=FrameViewerResponse)
def get_frame(violation_id: str, frame_number: int):
    """
    Returns overlay bounding boxes for frame review.
    """
    ReplayValidator.validate_violation_id(violation_id)
    return FrameService.get_frame_details(violation_id, frame_number)
