from fastapi import APIRouter
from app.schemas.statistics import (
    StatisticsResponse,
    DailyStatsResponse,
    WeeklyStatsResponse,
    MonthlyStatsResponse,
    PerformanceStatsResponse
)
from app.services.statistics.statistics_service import StatisticsService
from app.services.statistics.analytics_service import AnalyticsService
from app.services.statistics.performance_service import PerformanceService

router = APIRouter(prefix="/statistics", tags=["AI Statistics Dashboard"])

@router.get("", response_model=StatisticsResponse)
def get_overview():
    """
    Returns runtime total vehicles, average confidence and inference times.
    """
    return StatisticsService.get_overview_statistics()

@router.get("/daily", response_model=DailyStatsResponse)
def get_daily():
    """
    Returns daily violation trends.
    """
    return {"daily": AnalyticsService.get_daily_statistics()}

@router.get("/weekly", response_model=WeeklyStatsResponse)
def get_weekly():
    """
    Returns weekly aggregated metric logs.
    """
    return {"weekly": AnalyticsService.get_weekly_statistics()}

@router.get("/monthly", response_model=MonthlyStatsResponse)
def get_monthly():
    """
    Returns monthly comparison indices.
    """
    return {"monthly": AnalyticsService.get_monthly_statistics()}

@router.get("/performance", response_model=PerformanceStatsResponse)
def get_performance():
    """
    Returns hardware performance load, memory and disk speeds.
    """
    return PerformanceService.get_performance_metrics()
