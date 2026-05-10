from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session

from ...database import get_db
from ...schemas.auth_schema import AuthResponse, LoginRequest, RegisterRequest
from ...services.auth_service import login_user, register_user
from ...services.email_service import send_registration_confirmation_email

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
