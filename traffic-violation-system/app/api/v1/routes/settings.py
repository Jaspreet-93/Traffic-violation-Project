from fastapi import APIRouter
from app.schemas.settings import SettingsRequest, SettingsResponse
from app.services.settings.settings_service import settings_service

router = APIRouter(prefix="/settings", tags=["System Settings"])

@router.get("", response_model=SettingsResponse)
def get_settings():
    """
    Retrieves currently active configurations.
    """
    return settings_service.get_settings()

@router.put("", response_model=SettingsResponse)
def update_settings(payload: SettingsRequest):
    """
    Modifies system environment configs.
    """
    return settings_service.update_settings(payload.model_dump())
