from sqlalchemy import Column, String, DateTime, ForeignKey, Numeric, func, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import enum
from app.core.database import Base

class LoanStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    USED = "USED"
    PAID = "PAID"

class FuelLoan(Base):
    __tablename__ = "fuel_loans"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    vehicle_id = Column(UUID(as_uuid=True), ForeignKey("vehicles.id"), nullable=False)
    litres = Column(Numeric(10, 2), nullable=False)
    price_per_litre = Column(Numeric(10, 2), nullable=False)
    loan_amount = Column(Numeric(10, 2), nullable=False)
    service_fee = Column(Numeric(10, 2), nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    status = Column(Enum(LoanStatus), default=LoanStatus.PENDING)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="loans")
    vehicle = relationship("Vehicle", back_populates="loans")
    coupon = relationship("QRCode", back_populates="loan", uselist=False)
    transactions = relationship("Transaction", back_populates="loan")
