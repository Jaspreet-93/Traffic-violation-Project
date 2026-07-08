from fastapi import APIRouter
from typing import List

from app.schemas.confidence import (
    LiveConfidenceResponse,
    ConfidenceHistoryResponse,
    ModelsConfidenceResponse,
    TrustScoreResponse,
    ConfidenceStatisticsResponse
)

from app.services.confidence.confidence_service import ConfidenceService
from app.services.confidence.confidence_history import ConfidenceHistoryService
from app.services.confidence.trust_score_service import TrustScoreService
from app.services.confidence.confidence_statistics import ConfidenceStatisticsService
from app.services.ai_command_center.model_monitor import ModelMonitor

router = APIRouter(prefix="/confidence", tags=["AI Confidence Dashboard"])

@router.get("/live", response_model=LiveConfidenceResponse)
def get_live_confidence():
    """
    Returns live model confidence ratings.
    """
    return ConfidenceService.get_live_confidence()

@router.get("/history", response_model=ConfidenceHistoryResponse)
def get_confidence_history():
    """
    Returns historical confidence score logs.
    """
    items = ConfidenceHistoryService.get_history()
    return {"history": items}

@router.get("/models", response_model=ModelsConfidenceResponse)
def get_models_confidence():
    """
    Returns registered models list.
    """
    models = ModelMonitor.get_model_health()
    formatted = []
    for m in models:
        formatted.append({
            "name": m["name"],
            "status": m["status"],
            "framework": m["framework"],
            "classes": m["classes"],
            "avg_confidence": "93.4%" # default average baseline
        })
    return {"models": formatted}

@router.get("/trust-score", response_model=TrustScoreResponse)
def get_ai_trust_score():
    """
    Returns Overall AI Trust Score calculated from available inputs.
    """
    live_conf = ConfidenceService.get_live_confidence()
    return TrustScoreService.calculate_trust_score(live_conf)

@router.get("/statistics", response_model=ConfidenceStatisticsResponse)
def get_statistics():
    """
    Returns stats charts trend data points.
    """
    return ConfidenceStatisticsService.get_statistics()
