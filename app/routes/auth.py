from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.schemas import LoginRequest, VerifyRequest, Token, ProfileUpdate
from app.services.auth_service import auth_service
from app.routes.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    return await auth_service.login_request(db, request.phone)

@router.post("/verify", response_model=Token)
async def verify(request: VerifyRequest, db: Session = Depends(get_db)):
    return await auth_service.verify_otp(db, request.phone, request.otp)

@router.post("/register")
async def register(
    request: ProfileUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await auth_service.update_profile(db, current_user, request)
