from pydantic import BaseModel
from typing import List, Dict, Any

class ModelOverviewResponse(BaseModel):
    model_name: str
    framework: str
    version: str
    status: str
    device: str
    inference_time_ms: float
    avg_confidence_pct: float
    total_classes: int
    loaded_models: List[str]

class ModelHealthResponse(BaseModel):
    model_name: str
    status: str # "Excellent", "Good", "Warning", "Critical"
    load_success: bool
    memory_usage_mb: float
    cpu_utilization_pct: float
    gpu_utilization_pct: float

class MetricsResponse(BaseModel):
    precision: float
    recall: float
    f1_score: float
    map_50: float
    map_50_95: float
    avg_confidence_pct: float
    inference_speed_ms: float
    fps: float
    memory_usage_mb: float
    gpu_usage_pct: float
    cpu_usage_pct: float

class DatasetResponse(BaseModel):
    dataset_name: str
    dataset_size_mb: float
    images_count: int
    videos_count: int
    classes_count: int
    annotations_count: int
    training_split: float
    validation_split: float
    test_split: float

class PerformanceResponse(BaseModel):
    precision_trend: List[float]
    recall_trend: List[float]
    map_trend: List[float]

class BenchmarkItem(BaseModel):
    metric_name: str
    current_val: float
    average_val: float
    difference_pct: float

class BenchmarkResponse(BaseModel):
    benchmarks: List[BenchmarkItem]

class RecommendationsResponse(BaseModel):
    recommendations: List[str]

class VerificationCheckItem(BaseModel):
    check_name: str
    passed: bool
    details: str

class VerificationResponse(BaseModel):
    overall_passed: bool
    checks: List[VerificationCheckItem]
