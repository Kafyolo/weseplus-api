from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timezone, timedelta
from app.models.loan import FuelLoan, LoanStatus
from app.models.vehicle import Vehicle
from app.models.audit import AuditLog
from app.core.config import settings
from fastapi import HTTPException, status
from decimal import Decimal
from .firebase_service import firebase_service

class FuelService:
    async def request_loan(self, db: Session, user_id: str, vehicle_number: str, litres: float):
        # 1. Validate vehicle
        vehicle = db.query(Vehicle).filter(Vehicle.vehicle_number == vehicle_number).first()
        if not vehicle:
            # For this demo, we create a vehicle if it doesn't exist. In prod, check verification.
            vehicle = Vehicle(user_id=user_id, vehicle_number=vehicle_number, verified=True)
            db.add(vehicle)
            db.commit()
            db.refresh(vehicle)
        
        # 2. Check for active loan on this vehicle (DISABLED FOR TESTING)
        """
        active_loan = db.query(FuelLoan).filter(
            FuelLoan.vehicle_id == vehicle.id,
            FuelLoan.status.in_([LoanStatus.PENDING, LoanStatus.APPROVED, LoanStatus.USED])
        ).first()
        
        if active_loan:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Vehicle ana mkopo unaoendelea. Lipia kwanza."
            )
        """

        # 3. Check daily limit (DISABLED FOR TESTING)
        """
        today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        daily_litres = db.query(func.sum(FuelLoan.litres)).filter(
            FuelLoan.vehicle_id == vehicle.id,
            FuelLoan.created_at >= today
        ).scalar() or 0
        
        if Decimal(str(daily_litres)) + Decimal(str(litres)) > Decimal(str(settings.MAX_LITRES_PER_DAY)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Umevuka kikomo cha lita {settings.MAX_LITRES_PER_DAY} kwa siku."
            )
        """

        # 4. Mandatory Backend Calculation
        price = Decimal(str(settings.PRICE_PER_LITRE))
        litres_dec = Decimal(str(litres))
        
        loan_amount = litres_dec * price
        service_fee = loan_amount * Decimal(str(settings.SERVICE_FEE_PERCENTAGE))
        total_amount = loan_amount + service_fee

        # 5. Create Loan Record
        new_loan = FuelLoan(
            user_id=user_id,
            vehicle_id=vehicle.id,
            litres=litres_dec,
            price_per_litre=price,
            loan_amount=loan_amount,
            service_fee=service_fee,
            total_amount=total_amount,
            status=LoanStatus.APPROVED # Approved automatically for this demo
        )
        db.add(new_loan)
        db.commit()
        db.refresh(new_loan)

        # 6. Audit & Analytics
        audit_entry = AuditLog(
            user_id=user_id,
            action="LOAN_REQUESTED",
            metadata_json={
                "loan_id": str(new_loan.id),
                "amount": float(total_amount),
                "vehicle": vehicle_number
            }
        )
        db.add(audit_entry)
        db.commit()

        firebase_service.log_analytics_event("loan_requested", {
            "user_id": str(user_id),
            "amount": float(total_amount)
        })
        
        firebase_service.send_notification(
            phone=vehicle.owner.phone,
            title="Mkopo Umeidhinishwa",
            body=f"Umepokea mkopo wa lita {litres}. Rejea yako: {str(new_loan.id)[:8]}"
        )

        return new_loan

fuel_service = FuelService()
