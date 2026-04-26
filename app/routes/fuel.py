from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.schemas import FuelRequest, LoanResponse
from app.services.fuel_service import fuel_service
from app.routes.dependencies import get_current_user
from app.models.user import User
from app.models.loan import FuelLoan

router = APIRouter(prefix="/fuel", tags=["fuel"])

@router.post("/request", response_model=LoanResponse)
async def request_fuel(
    request: FuelRequest, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await fuel_service.request_loan(
        db, 
        user_id=str(current_user.id), 
        vehicle_number=request.vehicle_number, 
        litres=request.litres
    )

@router.get("/history", response_model=List[LoanResponse])
async def get_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(FuelLoan).filter(FuelLoan.user_id == current_user.id).order_by(FuelLoan.created_at.desc()).all()
