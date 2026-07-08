from fastapi import APIRouter, HTTPException, Body
from typing import List, Dict, Any, Optional
from app.schemas.officer_email import OfficerEmailCreate, OfficerEmailUpdate, OfficerEmailResponse
from app.services.officer_email.officer_email_service import OfficerEmailService

router = APIRouter(prefix="/officer-emails", tags=["Officer Email Management"])

@router.get("", response_model=List[OfficerEmailResponse])
def get_emails():
    """
    Returns list of officer email addresses.
    """
    return OfficerEmailService.get_emails()

@router.post("", response_model=OfficerEmailResponse)
def add_email(payload: OfficerEmailCreate):
    """
    Registers a new officer email address.
    """
    try:
        return OfficerEmailService.add_email(
            email_address=payload.email_address,
            active=payload.active,
            primary=payload.primary
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{email_id}", response_model=OfficerEmailResponse)
def update_email(email_id: str, payload: OfficerEmailUpdate):
    """
    Edits registered officer email details.
    """
    try:
        return OfficerEmailService.update_email(
            email_id=email_id,
            email_address=payload.email_address,
            active=payload.active,
            primary=payload.primary
        )
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{email_id}")
def delete_email(email_id: str):
    """
    Deletes an officer email address.
    """
    try:
        OfficerEmailService.delete_email(email_id)
        return {"status": "success", "message": "Officer email deleted."}
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{email_id}/status", response_model=OfficerEmailResponse)
def update_status(email_id: str, active: bool = Body(..., embed=True)):
    """
    Enables or disables an email address.
    """
    try:
        return OfficerEmailService.update_status(email_id, active)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{email_id}/primary", response_model=OfficerEmailResponse)
def set_primary(email_id: str):
    """
    Marks one email address as the primary recipient.
    """
    try:
        return OfficerEmailService.set_primary(email_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
