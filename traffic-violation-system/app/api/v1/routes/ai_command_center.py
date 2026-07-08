from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from app.schemas.ai_command_center import (
    AIOverviewResponse,
    AIModelHealthResponse,
    AITrainingMetricsResponse,
    AIDatasetHealthResponse,
    AIConfidenceResponse,
    AIPerformanceResponse,
    AIBenchmarkResponse,
    AISystemHealthResponse,
    AIDiagnosticsResponse,
    AIRecommendationsResponse,
    AIReportResponse
)

from app.services.ai_command_center.ai_monitor import AIMonitor
from app.services.ai_command_center.model_validator import ModelValidator
from app.services.ai_command_center.training_metrics import TrainingMetricsService
from app.services.ai_command_center.dataset_validator import DatasetValidator
from app.services.ai_command_center.confidence_monitor import ConfidenceMonitor
from app.services.ai_command_center.inference_monitor import InferenceMonitor
from app.services.ai_command_center.benchmark import BenchmarkEvaluator
from app.services.ai_command_center.hardware_monitor import HardwareMonitor
from app.services.ai_command_center.diagnostics import DiagnosticsEngine
from app.services.ai_command_center.recommendation_engine import RecommendationEngine
from app.services.ai_command_center.report_generator import ReportGenerator

router = APIRouter(prefix="/ai", tags=["AI Command Center"])

class ExportRequest(BaseModel):
    format: str = "pdf"

@router.get("/overview", response_model=AIOverviewResponse)
def get_ai_overview():
    """
    Returns high-level system aggregates and AI system health categories.
    """
    return AIMonitor.get_overview_metrics()

@router.get("/models")
def get_ai_models():
    """
    Returns registered pipeline AI model details.
    """
    return ModelValidator.get_all_models_health()

@router.get("/model-health")
def get_model_health_status():
    """
    Detailed model execution checks.
    """
    return ModelValidator.get_all_models_health()

@router.get("/training-metrics")
def get_training_metrics_status():
    """
    Returns available YOLO or custom training parameters mAP curves if exists.
    """
    metrics = TrainingMetricsService.get_training_metrics()
    if not metrics:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Training metrics not available."
        )
    return metrics

@router.get("/datasets", response_model=List[AIDatasetHealthResponse])
def get_datasets_status():
    """
    Validates classes, splits volumes, and file anomalies for datasets.
    """
    return DatasetValidator.get_datasets_health()

@router.get("/confidence", response_model=AIConfidenceResponse)
def get_live_confidence():
    """
    Collects average inference confidence scores.
    """
    return ConfidenceMonitor.get_confidence_metrics()

@router.get("/performance", response_model=AIPerformanceResponse)
def get_live_performance():
    """
    Current inference latency, FPS, API speeds, and frame queue logs.
    """
    return InferenceMonitor.get_performance_status()

@router.get("/benchmark", response_model=List[AIBenchmarkResponse])
def run_ai_benchmarks():
    """
    Calculates max throughput capacity and load latencies.
    """
    return BenchmarkEvaluator.run_benchmark()

@router.get("/system-health", response_model=AISystemHealthResponse)
def get_system_hardware_health():
    """
    Detailed server CPU, memory, and CUDA specifications.
    """
    return HardwareMonitor.get_hardware_status()

@router.get("/diagnostics", response_model=AIDiagnosticsResponse)
def run_system_diagnostics():
    """
    Auto-detects missing models, corrupt files, configuration warnings, or slow speeds.
    """
    issues = DiagnosticsEngine.run_diagnostics()
    return {"issues": issues}

@router.get("/recommendations")
def get_system_recommendations():
    """
    Dynamic troubleshooting recommendations derived from active system warnings.
    """
    recs = RecommendationEngine.generate_recommendations()
    return {"recommendations": recs}

@router.get("/report", response_model=AIReportResponse)
def get_compiled_report():
    """
    Consolidates validation health statuses into a single summary report.
    """
    return ReportGenerator.compile_full_report()

@router.post("/report/export", response_model=AIReportResponse)
def export_ai_report(payload: ExportRequest):
    """
    Compiles and exports the health report to the specified file format (PDF or Excel/CSV).
    """
    try:
        return ReportGenerator.export_report(payload.format)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Report compile failure: {str(e)}"
        )
