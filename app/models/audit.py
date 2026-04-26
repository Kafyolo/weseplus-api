from sqlalchemy import Column, String, DateTime, ForeignKey, JSON, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True) # Nullable for unauthenticated actions if any
    action = Column(String, nullable=False) # e.g., 'LOGIN', 'LOAN_REQUEST', 'QR_VALIDATE'
    metadata_json = Column(JSON, nullable=True) # Using metadata_json to avoid reserved keyword conflicts if any
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="audit_logs")
