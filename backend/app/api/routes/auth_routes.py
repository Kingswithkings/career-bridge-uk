from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...database import get_db
from ...schemas.auth_schema import AuthResponse, LoginRequest, RegisterRequest
from ...services.auth_service import login_user, register_user

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/register", response_model=AuthResponse)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    return register_user(
        db=db,
        email=request.email,
        password=request.password,
        full_name=request.full_name,
    )


@router.post("/login", response_model=AuthResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    return login_user(
        db=db,
        email=request.email,
        password=request.password,
    )
