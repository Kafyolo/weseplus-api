from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.schemas import LoginRequest, VerifyRequest, Token
from app.services.auth_service import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    return await auth_service.login_request(db, request.phone)

@router.post("/verify", response_model=Token)
async def verify(request: VerifyRequest, db: Session = Depends(get_db)):
    return await auth_service.verify_otp(db, request.phone, request.otp)
