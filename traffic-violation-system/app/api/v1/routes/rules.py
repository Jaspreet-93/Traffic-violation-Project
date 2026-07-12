from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from app.services.rule_engine.rule_intelligence import rule_intelligence

router = APIRouter(prefix="/rules", tags=["Traffic Rules Intelligence System"])

class RuleUpdatePayload(BaseModel):
    location: str
    rules: Dict[str, Any]

@router.get("", status_code=status.HTTP_200_OK)
def list_rules():
    """
    Returns list of all active location-based rules.
    """
    return rule_intelligence.rules

@router.get("/{location}", status_code=status.HTTP_200_OK)
def get_rules_for_location(location: str):
    """
    Returns rules configured for target location.
    """
    rules = rule_intelligence.get_rules_for_location(location)
    if not rules:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Rules for location '{location}' are not configured."
        )
    return rules

@router.post("/update", status_code=status.HTTP_200_OK)
def update_rules(payload: RuleUpdatePayload):
    """
    Updates or registers location-based rules configuration.
    """
    rule_intelligence.rules[payload.location] = payload.rules
    rule_intelligence.save_rules()
    return {"success": True, "message": f"Rules for location '{payload.location}' successfully updated."}

@router.post("/reset", status_code=status.HTTP_200_OK)
def reset_rules():
    """
    Resets location-based rules configuration back to default values.
    """
    rule_intelligence.rules = dict(rule_intelligence.default_rules)
    rule_intelligence.save_rules()
    return {"success": True, "message": "Rules configuration reset back to default."}
