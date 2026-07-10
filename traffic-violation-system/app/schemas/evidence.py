from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class EvidenceResponse(BaseModel):
    evidence_id: int
    violation_id: int
    vehicle_id: Optional[int] = Field(None, description="ID of the tracked vehicle")
    violation: str = Field(..., description="Violation classification label")
    image_path: str = Field(..., description="Relative path to captured snapshot image proof")
    video_path: Optional[str] = None
    timestamp: str = Field(..., description="Standard UTC format timestamp")

    # Real Media Verification Fields
    original_image_path: Optional[str] = None
    original_video_path: Optional[str] = None
    processed_image_path: Optional[str] = None
    processed_video_path: Optional[str] = None
    thumbnail_path: Optional[str] = None
    capture_time: Optional[str] = None
    camera_id: Optional[str] = None
    violation_type: Optional[str] = None
    confidence: Optional[float] = None
    vehicle_number: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    model_config = {
        "from_attributes": True
    }

class EvidenceDetail(BaseModel):
    evidence_id: int
    violation_id: int
    vehicle_id: Optional[int] = None
    plate_number: Optional[str] = None
    violation: str
    image_path: Optional[str] = None
    video_path: Optional[str] = None
    timestamp: str

    # Real Media Verification Fields
    original_image_path: Optional[str] = None
    original_video_path: Optional[str] = None
    processed_image_path: Optional[str] = None
    processed_video_path: Optional[str] = None
    thumbnail_path: Optional[str] = None
    capture_time: Optional[str] = None
    camera_id: Optional[str] = None
    violation_type: Optional[str] = None
    confidence: Optional[float] = None
    vehicle_number: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    model_config = {
        "from_attributes": True
    }

class EvidenceMetadataResponse(BaseModel):
    evidence_id: int
    detection_time: str
    processing_time_ms: float
    vehicle_type: str
    violation_type: str
    confidence: float
    model_version: str
    evidence_size_kb: float
    resolution: str

class EvidenceIntegrityResponse(BaseModel):
    evidence_id: int
    checksum_sha256: str
    integrity_verified: bool
    status: str

class DeleteEvidenceResponse(BaseModel):
    success: bool
    message: str
