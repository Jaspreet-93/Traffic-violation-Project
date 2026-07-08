from pydantic import BaseModel
from typing import List, Dict, Any

class StatDailyItem(BaseModel):
    date: str
    vehicles: int
    violations: int

class StatWeeklyItem(BaseModel):
    week: str
    vehicles: int
    violations: int

class StatMonthlyItem(BaseModel):
    month: str
    vehicles: int
    violations: int

class StatisticsResponse(BaseModel):
    total_vehicles: int
    total_violations: int
    detection_accuracy_pct: float
    avg_confidence_pct: float
    avg_inference_time_ms: float
    avg_detection_speed_fps: float
    system_uptime_sec: int

class DailyStatsResponse(BaseModel):
    daily: List[StatDailyItem]

class WeeklyStatsResponse(BaseModel):
    weekly: List[StatWeeklyItem]

class MonthlyStatsResponse(BaseModel):
    monthly: List[StatMonthlyItem]

class PerformanceStatsResponse(BaseModel):
    uptime_percentage: float
    gpu_utilization_pct: float
    memory_utilization_pct: float
    disk_write_speed_mbps: float
    model_inference_latencies_ms: Dict[str, float]
