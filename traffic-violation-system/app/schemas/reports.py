from pydantic import BaseModel
from typing import List, Optional

class ReportGenerateRequest(BaseModel):
    report_type: str  # "daily", "weekly", "monthly", "violation", "camera", "ai_performance"
    export_format: str # "pdf", "excel", "csv"
    camera_id: Optional[int] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class ReportResponse(BaseModel):
    id: int
    name: str
    report_type: str
    export_format: str
    generated_at: str
    file_size_kb: float
    download_url: str

    model_config = {
        "from_attributes": True
    }

class ReportGenerateResponse(BaseModel):
    success: bool
    report: ReportResponse
    message: str

class DeleteReportResponse(BaseModel):
    success: bool
    message: str
