from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.violation import ViolationCreate, LegacyViolationResponse
from app.services.violation_service import ViolationService
from typing import List

router = APIRouter(prefix="/violations-legacy", tags=["Violation Legacy"])

@router.post("", response_model=LegacyViolationResponse, status_code=status.HTTP_201_CREATED)
def create_violation(violation_in: ViolationCreate, db: Session = Depends(get_db)):
    """
    Registers a new traffic violation. Ensures the associated camera exists.
    """
    try:
        return ViolationService.create_violation(db=db, violation_in=violation_in)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("", response_model=List[LegacyViolationResponse])
def list_violations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieves all registered traffic violations.
    """
    return ViolationService.get_violations(db=db, skip=skip, limit=limit)

@router.get("/{id}", response_model=LegacyViolationResponse)
def get_violation(id: int, db: Session = Depends(get_db)):
    """
    Retrieves a single traffic violation record by its ID.
    """
    db_violation = ViolationService.get_violation_by_id(db=db, violation_id=id)
    if not db_violation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Violation with ID {id} not found."
        )
    return db_violation
