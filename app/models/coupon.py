from sqlalchemy import Column, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base

class QRCode(Base):
    __tablename__ = "qr_coupons"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    loan_id = Column(UUID(as_uuid=True), ForeignKey("fuel_loans.id"), nullable=False)
    qr_code_data = Column(JSON, nullable=False) # Stores the encoded payload
    is_used = Column(Boolean, default=False)
    expiry_time = Column(DateTime(timezone=True), nullable=False)

    loan = relationship("FuelLoan", back_populates="coupon")
