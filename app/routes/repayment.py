from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.schemas import RepaymentRequest
from app.models.loan import FuelLoan, LoanStatus
from app.models.transaction import Transaction, TransactionType, TransactionStatus
from app.models.audit import AuditLog
from app.routes.dependencies import get_current_user
from app.models.user import User
from app.services.firebase_service import firebase_service

router = APIRouter(prefix="/repayment", tags=["repayment"])

@router.post("/pay")
async def pay_loan(
    request: RepaymentRequest, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    loan = db.query(FuelLoan).filter(FuelLoan.id == request.loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Mkopo haukupatikana")

    if loan.status == LoanStatus.PAID:
        raise HTTPException(status_code=400, detail="Mkopo huu tayari umelipwa")

    # In a real system, verify external payment (M-Pesa etc) here
    
    # 1. Update Loan status
    loan.status = LoanStatus.PAID
    
    # 2. Log Transaction
    payment_transaction = Transaction(
        loan_id=loan.id,
        amount=request.amount,
        type=TransactionType.REPAYMENT,
        status=TransactionStatus.SUCCESS
    )
    db.add(payment_transaction)
    
    # 3. Audit Log
    audit_entry = AuditLog(
        user_id=current_user.id,
        action="REPAYMENT_SUCCESS",
        metadata_json={
            "loan_id": str(loan.id),
            "amount": float(request.amount),
            "transaction_id": str(payment_transaction.id)
        }
    )
    db.add(audit_entry)
    db.commit()

    firebase_service.log_analytics_event("repayment_done", {"loan_id": str(loan.id), "amount": float(request.amount)})
    
    firebase_service.send_notification(
        phone=current_user.phone,
        title="Malipo Yamepokelewa",
        body=f"Asante kwa kulipia mkopo wako wa {float(request.amount)} TZS. Kikomo chako cha mkopo kimeongezwa."
    )

    return {"message": "Malipo yamefanikiwa", "loan_id": str(loan.id)}
