from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from decimal import Decimal

# Auth
class LoginRequest(BaseModel):
    phone: str

class VerifyRequest(BaseModel):
    phone: str
    otp: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Fuel
class FuelRequest(BaseModel):
    vehicle_number: str
    litres: float = Field(..., gt=0, le=10)

class LoanResponse(BaseModel):
    id: UUID
    litres: Decimal
    total_amount: Decimal
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

# QR
class QRResponse(BaseModel):
    id: UUID
    qr_code_data: dict
    expiry_time: datetime

    class Config:
        from_attributes = True

# Repayment
class RepaymentRequest(BaseModel):
    loan_id: UUID
    amount: Decimal
