from fastapi import APIRouter
from app.schemas.model_verification import (
    ModelOverviewResponse,
    ModelHealthResponse,
    MetricsResponse,
    DatasetResponse,
    PerformanceResponse,
    BenchmarkResponse,
    RecommendationsResponse,
    VerificationResponse
)

from app.services.model_verification.verification_service import VerificationService
from app.services.model_verification.evaluation_service import EvaluationService
from app.services.model_verification.benchmark_service import BenchmarkService
from app.services.model_verification.metrics_service import MetricsService
from app.services.model_verification.model_health_service import ModelHealthService
from app.services.model_verification.dataset_service import DatasetService
from app.services.model_verification.recommendation_service import RecommendationService

router = APIRouter(prefix="/model", tags=["AI Model Verification & Performance Evaluation"])

@router.get("/overview", response_model=ModelOverviewResponse)
def get_overview():
    """
    Returns framework, load statuses and configurations overview.
    """
    return VerificationService.get_overview()

@router.get("/health", response_model=ModelHealthResponse)
def get_health():
    """
    Returns hardware loads, memory and GPU diagnostics.
    """
    return ModelHealthService.get_health()

@router.get("/metrics", response_model=MetricsResponse)
def get_metrics():
    """
    Returns F1, Precision, Recall, and mAP@50 rating values.
    """
    return MetricsService.get_metrics()

@router.get("/dataset", response_model=DatasetResponse)
def get_dataset():
    """
    Returns images count, splits and sizes overview.
    """
    return DatasetService.get_dataset_summary()

@router.get("/performance", response_model=PerformanceResponse)
def get_performance():
    """
    Returns precision and recall trend lists.
    """
    return EvaluationService.get_trends()

@router.get("/benchmark", response_model=BenchmarkResponse)
def get_benchmark():
    """
    Compares current latencies against averages.
    """
    return {"benchmarks": BenchmarkService.get_benchmarks()}

@router.get("/recommendations", response_model=RecommendationsResponse)
def get_recommendations():
    """
    Yields observations checklist logs.
    """
    return {"recommendations": RecommendationService.get_recommendations()}

@router.get("/verification", response_model=VerificationResponse)
def get_verification():
    """
    Runs model tests confirming weights exist.
    """
    return VerificationService.run_checks()
