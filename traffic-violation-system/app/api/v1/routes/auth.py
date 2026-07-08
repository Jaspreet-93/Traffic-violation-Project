from fastapi import APIRouter, HTTPException, Body
from app.schemas.auth import UserRegister, UserLogin, UserUpdate, PasswordChange, ForgotPassword, UserResponse
from app.services.auth.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["User Authentication & Accounts"])

@router.post("/register", response_model=UserResponse)
def register(payload: UserRegister):
    """
    Registers a new authorized user.
    """
    try:
        return AuthService.register_user(
            full_name=payload.full_name,
            email_address=payload.email_address,
            phone_number=payload.phone_number,
            password=payload.password,
            confirm_password=payload.confirm_password
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=UserResponse)
def login(payload: UserLogin):
    """
    Authenticates user using email and password.
    """
    try:
        return AuthService.login_user(
            email_address=payload.email_address,
            password=payload.password
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/profile/{user_id}", response_model=UserResponse)
def update_profile(user_id: str, payload: UserUpdate):
    """
    Updates user profile properties (full name, phone number).
    """
    try:
        return AuthService.update_profile(
            user_id=user_id,
            full_name=payload.full_name,
            phone_number=payload.phone_number
        )
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/change-password/{user_id}", response_model=UserResponse)
def change_password(user_id: str, payload: PasswordChange):
    """
    Changes user account password securely.
    """
    try:
        return AuthService.change_password(
            user_id=user_id,
            old_password=payload.old_password,
            new_password=payload.new_password,
            confirm_new_password=payload.confirm_new_password
        )
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/forgot-password")
def forgot_password(payload: ForgotPassword):
    """
    Triggers simulated forgot password email reset notification.
    """
    try:
        msg = AuthService.forgot_password(payload.email_address)
        return {"status": "success", "message": msg}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
