from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta
from app.models.coupon import QRCode
from app.models.loan import FuelLoan, LoanStatus
from app.models.audit import AuditLog
from app.core.config import settings
from fastapi import HTTPException, status
import json
from .firebase_service import firebase_service

class QRService:
    async def generate_qr(self, db: Session, loan_id: str):
        loan = db.query(FuelLoan).filter(FuelLoan.id == loan_id).first()
        if not loan:
            raise HTTPException(status_code=404, detail="Loan not found")

        # Expiry: 2 hours from now
        expiry = datetime.now(timezone.utc) + timedelta(hours=settings.QR_EXPIRY_HOURS)
        
        qr_data = {
            "loan_id": str(loan.id),
            "user_id": str(loan.user_id),
            "vehicle": loan.vehicle.vehicle_number,
            "litres": float(loan.litres),
            "expiry": expiry.isoformat()
        }

        qr_coupon = QRCode(
            loan_id=loan.id,
            qr_code_data=qr_data,
            expiry_time=expiry
        )
        db.add(qr_coupon)
        db.commit()
        db.refresh(qr_coupon)

        # Audit
        audit_entry = AuditLog(
            user_id=loan.user_id,
            action="QR_GENERATED",
            metadata_json={"loan_id": str(loan.id), "coupon_id": str(qr_coupon.id)}
        )
        db.add(audit_entry)
        db.commit()

        firebase_service.log_analytics_event("qr_generated", {"loan_id": str(loan.id)})

        return qr_coupon

    async def validate_qr(self, db: Session, qr_id: str):
        coupon = db.query(QRCode).filter(QRCode.id == qr_id).first()
        if not coupon:
            raise HTTPException(status_code=404, detail="Kuponi haipatikani")

        if coupon.is_used:
            # firebase_service.log_analytics_event("qr_reuse_attempt", {"qr_id": qr_id})
            raise HTTPException(status_code=400, detail="Kuponi tayari imetumika")

        if datetime.now(timezone.utc) > coupon.expiry_time.replace(tzinfo=timezone.utc):
            raise HTTPException(status_code=400, detail="Kuponi imeisha muda wake")

        # Mark as used
        coupon.is_used = True
        
        # Update loan status
        loan = coupon.loan
        loan.status = LoanStatus.USED
        
        db.commit()

        # Audit
        audit_entry = AuditLog(
            user_id=loan.user_id,
            action="QR_USED",
            metadata_json={"qr_id": qr_id, "loan_id": str(loan.id)}
        )
        db.add(audit_entry)
        db.commit()

        firebase_service.log_analytics_event("qr_used", {"loan_id": str(loan.id)})

        return {"message": "Kuponi imethibitishwa", "loan_id": str(loan.id)}

qr_service = QRService()
