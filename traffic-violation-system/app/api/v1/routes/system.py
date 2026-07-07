from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from app.database.connection import check_db_connection
from app.core.config import settings

router = APIRouter(tags=["System"])

@router.get("/")
async def root():
    """
    Welcome endpoint returning basic metadata about the API.
    """
    return {
        "message": "Traffic Violation Detection Backend Running"
    }

@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """
    Checks database connection health and overall API status.
    """
    db_healthy = check_db_connection()
    
    if not db_healthy:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "Unhealthy"}
        )
        
    return {"status": "Healthy"}
