from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class UploadResponse(BaseModel):
    job_id: str
    filename: str
    file_type: str
    status: str
    created_at: str

class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    progress: float
    error_message: Optional[str] = None
    metrics: Optional[Dict[str, Any]] = None

class DetectionItem(BaseModel):
    label: str
    bbox: List[int]
    confidence: float

class EvidenceSummary(BaseModel):
    violations_count: int
    vehicles_count: int
    processing_time_sec: float
    frame_count: Optional[int] = None
    processed_file_url: Optional[str] = None
    summary_text: str

class DetectionResultResponse(BaseModel):
    job_id: str
    filename: str
    file_type: str
    objects: List[DetectionItem]
    evidence: EvidenceSummary

class HistoryItem(BaseModel):
    job_id: str
    upload_date: str
    filename: str
    file_type: str
    status: str
    summary_text: str
    result_link: str

class HistoryResponse(BaseModel):
    history: List[HistoryItem]

class DeleteHistoryResponse(BaseModel):
    success: bool
    message: str
