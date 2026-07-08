from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class LiveConfidenceResponse(BaseModel):
    vehicle_detection: str
    vehicle_tracking: str
    helmet_detection: str
    ocr: str
    seat_belt: str
    traffic_light: str
    driver_behavior: str
    overall_violation: str

class ConfidenceHistoryItem(BaseModel):
    job_id: str
    timestamp: str
    confidence_score: float
    model_name: str

class ConfidenceHistoryResponse(BaseModel):
    history: List[ConfidenceHistoryItem]

class ModelConfidenceDetail(BaseModel):
    name: str
    status: str
    framework: str
    classes: List[str]
    avg_confidence: str

class ModelsConfidenceResponse(BaseModel):
    models: List[ModelConfidenceDetail]

class TrustScoreResponse(BaseModel):
    overall_trust_score: float
    trust_level: str

class ChartDataPoint(BaseModel):
    time: str
    value: float

class ComparisonDataPoint(BaseModel):
    model_name: str
    value: float

class ConfidenceStatisticsResponse(BaseModel):
    confidence_trend: List[ChartDataPoint]
    average_confidence: float
    model_comparison: List[ComparisonDataPoint]
    daily_confidence: List[ChartDataPoint]
    accuracy_trend: List[ChartDataPoint]
    processing_time_trend: List[ChartDataPoint]
