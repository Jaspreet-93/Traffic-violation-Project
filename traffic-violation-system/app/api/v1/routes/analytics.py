from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.analytics import AnalyticsSummaryResponse, DailyStatItem, TypeStatItem
from app.services.analytics.analytics_service import analytics_service

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/summary", response_model=AnalyticsSummaryResponse)
def get_analytics_summary():
    """
    Returns metrics summary counts.
    """
    try:
        return analytics_service.get_summary()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/daily", response_model=List[DailyStatItem])
def get_daily_statistics():
    """
    Returns daily violation trends for the past 7 days.
    """
    try:
        raw_list = analytics_service.get_daily_stats()
        return [
            DailyStatItem(date=item["date"], count=item["count"])
            for item in raw_list
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/types", response_model=List[TypeStatItem])
def get_violation_types_statistics():
    """
    Returns aggregate counts grouped by violation categories.
    """
    try:
        raw_list = analytics_service.get_type_stats()
        return [
            TypeStatItem(type=item["type"], count=item["count"])
            for item in raw_list
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
