from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey
from app.database.base import Base
from datetime import datetime, timezone


class Client(Base):
    __tablename__ = "clients"
    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    phone: Mapped[str]
    company_name: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )
    commercial_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    commercial = relationship("User", back_populates="clients")
    contracts = relationship("Contract", back_populates="client")
    events = relationship("Event", back_populates="client")