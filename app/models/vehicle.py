from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    vehicle_number = Column(String, unique=True, index=True, nullable=False)
    verified = Column(Boolean, default=False)

    owner = relationship("User", back_populates="vehicles")
    loans = relationship("FuelLoan", back_populates="vehicle")
