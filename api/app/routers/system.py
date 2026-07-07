from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from app.database import check_db_connection
from app.config import settings

router = APIRouter(tags=["System"])

@router.get("/")
async def root():
    """
    Welcome endpoint returning basic metadata about the API.
    """
    return {
        "message": f"Welcome to the {settings.APP_NAME}",
        "environment": settings.APP_ENV,
        "debug_mode": settings.DEBUG,
        "docs_url": "/docs"
    }

@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """
    System health check. Tests connection to the PostgreSQL database.
    """
    db_healthy = check_db_connection()
    
    health_status = {
        "status": "healthy" if db_healthy else "unhealthy",
        "services": {
            "api": "healthy",
            "database": "healthy" if db_healthy else "unhealthy"
        }
    }
    
    if not db_healthy:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content=health_status
        )
        
    return health_status
