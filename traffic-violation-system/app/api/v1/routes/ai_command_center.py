from fastapi import APIRouter
from typing import List

from app.schemas.ai_command_center import (
    AIOverviewResponse,
    AISystemHealthResponse,
    AIModelHealthResponse,
    AIHardwareResponse,
    AIConfidenceResponse,
    AIPerformanceResponse
)

from app.services.ai_command_center.ai_monitor import AIMonitor
from app.services.ai_command_center.system_monitor import SystemMonitor
from app.services.ai_command_center.model_monitor import ModelMonitor
from app.services.ai_command_center.hardware_monitor import HardwareMonitor
from app.services.ai_command_center.confidence_monitor import ConfidenceMonitor
from app.services.ai_command_center.ai_service import AIService

router = APIRouter(prefix="/ai", tags=["AI Command Center"])

@router.get("/overview", response_model=AIOverviewResponse)
def get_ai_overview():
    """
    Returns overview of the system counters.
    """
    return AIMonitor.get_overview_metrics()

@router.get("/system-health", response_model=AISystemHealthResponse)
def get_system_health():
    """
    Returns server load values.
    """
    return SystemMonitor.get_system_health()

@router.get("/model-health", response_model=AIModelHealthResponse)
def get_model_health():
    """
    Returns active classifier models list.
    """
    models = ModelMonitor.get_model_health()
    return {"models": models}

@router.get("/hardware", response_model=AIHardwareResponse)
def get_hardware_status():
    """
    Returns physical hardware properties.
    """
    return HardwareMonitor.get_hardware_status()

@router.get("/confidence", response_model=AIConfidenceResponse)
def get_confidence_metrics():
    """
    Returns confidence scores.
    """
    return ConfidenceMonitor.get_confidence_metrics()

@router.get("/performance", response_model=AIPerformanceResponse)
def get_performance_metrics():
    """
    Returns real-time frames performance stats.
    """
    return AIService.get_performance_metrics()
