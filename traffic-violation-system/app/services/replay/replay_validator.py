from fastapi import HTTPException, status

class ReplayValidator:
    @staticmethod
    def validate_violation_id(violation_id: str):
        if not violation_id or len(violation_id) < 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid violation ID format: '{violation_id}'"
            )
