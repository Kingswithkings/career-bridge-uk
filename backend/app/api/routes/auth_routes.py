from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session

from ...database import get_db
from ...schemas.auth_schema import (
    AuthResponse,
    ForgotPasswordRequest,
    LoginRequest,
    MessageResponse,
    RegisterRequest,
    ResetPasswordRequest,
)
from ...services.auth_service import (
    create_password_reset_code,
    login_user,
    register_user,
    reset_user_password,
)
from ...services.email_service import (
    send_password_reset_code,
    send_registration_confirmation_email,
)

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/register", response_model=AuthResponse)
def register(
    request: RegisterRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    response = register_user(
        db=db,
        email=request.email,
        password=request.password,
        full_name=request.full_name,
    )
    background_tasks.add_task(
        send_registration_confirmation_email,
        response["email"],
        request.full_name,
    )
    return response


@router.post("/login", response_model=AuthResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    return login_user(
        db=db,
        email=request.email,
        password=request.password,
    )


@router.post("/forgot-password", response_model=MessageResponse)
def forgot_password(
    request: ForgotPasswordRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    reset_details = create_password_reset_code(db=db, email=request.email)

    if reset_details:
        background_tasks.add_task(
            send_password_reset_code,
            reset_details["email"],
            reset_details["code"],
            reset_details["full_name"],
        )

    return {
        "message": "If an account exists for this email, a password reset code has been sent.",
    }


@router.post("/reset-password", response_model=MessageResponse)
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    return reset_user_password(
        db=db,
        email=request.email,
        code=request.code,
        new_password=request.new_password,
    )
