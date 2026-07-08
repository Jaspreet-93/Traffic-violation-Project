from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class DecisionResponse(BaseModel):
    violation_id: str
    timestamp: str
    violation_type: str
    decision: str
    status: str
    confidence_score: float

class DecisionHistoryResponse(BaseModel):
    history: List[DecisionResponse]

class ExplanationResponse(BaseModel):
    violation_id: str
    violation_type: str
    reason: str
    supporting_detections: List[str]
    model_confidence: Dict[str, str]
    evidence_generated: List[str]
    final_decision: str
    overall_trust_score: float

class AuditResponse(BaseModel):
    decision_time: str
    models_used: List[str]
    confidence_values: Dict[str, str]
    evidence_reference: str
    processing_time_ms: float
    pipeline_status: str
