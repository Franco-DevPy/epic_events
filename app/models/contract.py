from app.database.base import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import ForeignKey, event
from datetime import datetime, timezone
from enum import Enum

from app.models.client import Client
from app.models.user import User


class EnumStatus(str, Enum):
    signed = "signed"
    unsigned = "unsigned"


class Contract(Base):
    __tablename__ = "contracts"
    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(
        ForeignKey("clients.id"),
        nullable=False
    )
    commercial_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )
    total_amount: Mapped[float]
    remaining_amount: Mapped[float]
    status: Mapped[EnumStatus] = mapped_column(
        SQLAlchemyEnum(EnumStatus)
    )
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )
    
    client = relationship("Client", back_populates="contracts")
    commercial = relationship("User", back_populates="contracts")
    events = relationship("Event", back_populates="contract")