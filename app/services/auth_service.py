from sqlalchemy.orm import Session
from app.models.user import User
from app.models.audit import AuditLog
from app.core import security
from .firebase_service import firebase_service
from fastapi import HTTPException, status
from datetime import timedelta
from app.core.config import settings

class AuthService:
    # In-memory OTP storage for simplicity in this version. 
    # In production, use Redis with TTL.
    _otp_storage = {}

    async def login_request(self, db: Session, phone: str):
        # Normalize: Take last 9 digits to prevent duplicates like +255 vs 0
        phone = phone.replace("+", "").replace(" ", "")
        if phone.startswith("255"): phone = phone[3:]
        if phone.startswith("0"): phone = phone[1:]
        
        print(f"DEBUG: login_request for normalized phone=[{phone}]")
        otp = security.generate_otp()
        self._otp_storage[phone] = otp
        
        firebase_service.send_sms_otp(phone, otp)
        
        # Log the attempt
        audit_entry = AuditLog(
            action="LOGIN_REQUEST",
            metadata_json={"phone": phone}
        )
        db.add(audit_entry)
        db.commit()
        
        return {"message": "OTP sent successfully"}

    async def verify_otp(self, db: Session, phone: str, otp: str):
        # Normalize: Take last 9 digits
        phone = phone.replace("+", "").replace(" ", "")
        if phone.startswith("255"): phone = phone[3:]
        if phone.startswith("0"): phone = phone[1:]

        print(f"DEBUG: verifying phone=[{phone}] otp=[{otp}] storage={self._otp_storage}")
        # Allow master code for testing/development
        is_master_code = (otp == "123456")
        
        if not is_master_code and (phone not in self._otp_storage or self._otp_storage[phone] != otp):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Namba ya siri sio sahihi"
            )

        # Clear OTP if it was in storage
        if phone in self._otp_storage:
            del self._otp_storage[phone]

        # Get or create user
        user = db.query(User).filter(User.phone == phone).first()
        if not user:
            user = User(phone=phone)
            db.add(user)
            db.commit()
            db.refresh(user)

        # Generate token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = security.create_access_token(
            data={"sub": user.phone, "id": str(user.id)},
            expires_delta=access_token_expires
        )

        # Log success
        audit_entry = AuditLog(
            user_id=user.id,
            action="LOGIN_SUCCESS",
            metadata_json={"phone": phone}
        )
        db.add(audit_entry)
        db.commit()
        
        firebase_service.log_analytics_event("login_success", {"phone": phone})
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": str(user.id),
                "phone": user.phone
            }
        }

auth_service = AuthService()
