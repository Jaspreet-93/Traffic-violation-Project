from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class AIOverviewResponse(BaseModel):
    system_health: str
    total_models: int
    running_models: int
    loaded_models: int
    average_confidence: float
    system_uptime: str
    fps: float
    pipeline_status: str

class AISystemHealthResponse(BaseModel):
    cpu_usage: float
    ram_usage: float
    gpu_usage: Optional[float] = None
    disk_usage: float
    uptime: str

class AIModelHealthDetail(BaseModel):
    name: str
    status: str
    exists: bool
    loads_successfully: bool
    device: str
    framework: str
    classes: List[str]

class AIModelHealthResponse(BaseModel):
    models: List[AIModelHealthDetail]

class AIHardwareResponse(BaseModel):
    cpu_cores: int
    ram_total_gb: float
    ram_used_gb: float
    disk_total_gb: float
    disk_used_gb: float
    gpu_name: Optional[str] = None
    gpu_memory_total_mb: Optional[float] = None

class AIConfidenceResponse(BaseModel):
    vehicle_detection: str
    vehicle_tracking: str
    helmet_detection: str
    ocr: str
    seat_belt: str
    traffic_light: str
    driver_behavior: str
    overall_violation: str

class AIPerformanceResponse(BaseModel):
    fps: float
    inference_time_ms: float
    api_response_time_ms: float
    queue_size: int
