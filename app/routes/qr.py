from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.schemas import QRResponse
from app.services.qr_service import qr_service
from app.routes.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/qr", tags=["qr"])

@router.post("/generate/{loan_id}", response_model=QRResponse)
async def generate_qr(
    loan_id: str, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await qr_service.generate_qr(db, loan_id)

@router.post("/validate")
async def validate_qr(
    qr_id: str = Query(...), 
    db: Session = Depends(get_db)
):
    # Agents would typically validate this. For now, it's public entry with id.
    return await qr_service.validate_qr(db, qr_id)
