from fastapi import APIRouter, HTTPException, status
from typing import List

from app.schemas.decision_engine import (
    DecisionResponse,
    DecisionHistoryResponse,
    ExplanationResponse,
    AuditResponse
)

from app.services.decision_engine.decision_service import DecisionService
from app.services.decision_engine.explanation_service import ExplanationService
from app.services.decision_engine.audit_service import AuditService

router = APIRouter(prefix="/decision", tags=["Explainable AI Decision Engine"])

@router.get("/latest", response_model=DecisionResponse)
def get_latest_decision():
    """
    Returns the latest logged explainable decision trace.
    """
    return DecisionService.get_latest_decision()

@router.get("/history", response_model=DecisionHistoryResponse)
def get_decision_history():
    """
    Returns index of recent processed decision logs.
    """
    items = DecisionService.get_history()
    return {"history": items}

@router.get("/{violation_id}", response_model=DecisionResponse)
def get_decision_by_id(violation_id: str):
    """
    Retrieves decision by unique violation ID.
    """
    return DecisionService.get_decision_by_id(violation_id)

@router.get("/explanation/{violation_id}", response_model=ExplanationResponse)
def get_explanation(violation_id: str):
    """
    Generates structured explainable AI logical explanation.
    """
    # Look up decision to check type
    dec = DecisionService.get_decision_by_id(violation_id)
    return ExplanationService.get_explanation(violation_id, dec.get("violation_type", "No Helmet"))

@router.get("/audit/{violation_id}", response_model=AuditResponse)
def get_audit(violation_id: str):
    """
    Compiles models usage and pipeline execution speeds audits.
    """
    dec = DecisionService.get_decision_by_id(violation_id)
    return AuditService.get_audit_trail(violation_id, dec.get("violation_type", "No Helmet"))
