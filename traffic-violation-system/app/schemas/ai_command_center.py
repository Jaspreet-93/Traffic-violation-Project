from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class AIOverviewResponse(BaseModel):
    system_health: str = Field(..., description="Overall AI system health status (Healthy/Warning/Critical)")
    total_models: int = Field(..., description="Total registered AI models")
    running_models: int = Field(..., description="Currently active models")
    offline_models: int = Field(..., description="Currently disabled/offline models")
    average_confidence: float = Field(..., description="Average inference confidence across all models")
    fps: float = Field(..., description="Current running FPS of stream processing")
    violations_today: int = Field(..., description="Total infractions logged today")
    vehicles_detected_today: int = Field(..., description="Total vehicles detected today")
    active_cameras: int = Field(..., description="Total active cameras")
    cpu_usage: float = Field(..., description="Current CPU usage percentage")
    gpu_usage: Optional[float] = Field(None, description="Current GPU usage percentage if available")
    ram_usage: float = Field(..., description="Current RAM usage percentage")
    storage_usage: float = Field(..., description="Current disk storage usage percentage")
    system_uptime: str = Field(..., description="System uptime duration formatted string")

class AIModelDetail(BaseModel):
    name: str = Field(..., description="Model descriptor name")
    status: str = Field(..., description="Model health status (Running/Warning/Error)")
    version: str = Field(..., description="Model release version")
    weight_file: str = Field(..., description="Local path or filename of weights")
    framework: str = Field(..., description="Underlying inference framework (e.g. PyTorch/ONNX/YOLO)")
    classes: List[str] = Field(..., description="List of detectable classes")
    input_size: str = Field(..., description="Model input image resolution (e.g. 640x640)")
    device: str = Field(..., description="Target execution device (CPU/CUDA)")
    load_status: str = Field(..., description="Model file load status")
    memory_usage: str = Field(..., description="Memory footprint string")
    fps: float = Field(..., description="Current inference frame rate")
    inference_time: float = Field(..., description="Average inference latency in milliseconds")
    confidence: float = Field(..., description="Current running confidence average")

class AIModelHealthResponse(BaseModel):
    models: List[AIModelDetail]

class AITrainingMetricsResponse(BaseModel):
    dataset_used: str
    epochs: int
    precision: float
    recall: float
    f1_score: float
    map_50: float
    map_50_95: float
    training_loss: float
    validation_loss: float
    best_model: str
    last_training_date: str

class AIDatasetHealthResponse(BaseModel):
    dataset_name: str
    purpose: str
    classes: List[str]
    training_images: int
    validation_images: int
    test_images: int
    missing_labels: int
    corrupted_images: int
    duplicate_images: int
    annotation_format: str
    dataset_health_score: float

class AIConfidenceResponse(BaseModel):
    vehicle_detection: float
    vehicle_tracking: float
    helmet_detection: float
    plate_detection: float
    ocr: float
    seat_belt: float
    traffic_light: float
    driver_behavior: float
    overall_violation: float

class AIPerformanceResponse(BaseModel):
    fps: float
    inference_time: float
    cpu_usage: float
    gpu_usage: Optional[float] = None
    ram_usage: float
    disk_usage: float
    api_response_time: float
    queue_size: int

class AIBenchmarkResponse(BaseModel):
    model_name: str
    load_latency_ms: float
    avg_inference_latency_ms: float
    max_throughput_fps: float
    memory_peak_mb: float

class AISystemHealthResponse(BaseModel):
    overall_status: str
    uptime_seconds: float
    cpu_cores: int
    ram_total_gb: float
    ram_used_gb: float
    disk_total_gb: float
    disk_used_gb: float
    gpu_name: Optional[str] = None
    gpu_memory_total_mb: Optional[float] = None

class AIDiagnosticIssue(BaseModel):
    problem: str
    severity: str = Field(..., description="Critical/Warning/Info")
    recommended_solution: str

class AIDiagnosticsResponse(BaseModel):
    issues: List[AIDiagnosticIssue]

class AIRecommendationsResponse(BaseModel):
    recommendations: List[str]

class AIReportResponse(BaseModel):
    generated_at: str
    report_file: str
    summary: Dict[str, Any]
