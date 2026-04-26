from sqlalchemy import Column, String, DateTime, ForeignKey, Numeric, func, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import enum
from app.core.database import Base

class TransactionType(str, enum.Enum):
    LOAN = "LOAN"
    REPAYMENT = "REPAYMENT"

class TransactionStatus(str, enum.Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    PENDING = "PENDING"

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    loan_id = Column(UUID(as_uuid=True), ForeignKey("fuel_loans.id"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    type = Column(Enum(TransactionType), nullable=False)
    status = Column(Enum(TransactionStatus), default=TransactionStatus.SUCCESS)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    loan = relationship("FuelLoan", back_populates="transactions")
