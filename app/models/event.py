from app.database.base import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship, validates
from sqlalchemy import ForeignKey
from datetime import datetime, timezone


class Event(Base):
    __tablename__ = "events"
    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(
        ForeignKey("clients.id"),
        nullable=False
    )
    contract_id: Mapped[int] = mapped_column(
        ForeignKey("contracts.id"),
        nullable=False
    )
    support_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )
    event_start: Mapped[datetime]
    event_end: Mapped[datetime]
    location: Mapped[str]
    attendees: Mapped[int]
    notes: Mapped[str | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    client = relationship("Client", back_populates="events")
    contract = relationship("Contract", back_populates="events")
    support = relationship("User", back_populates="events")

    @validates('attendees')
    def validate_attendees(self, key, value):
        if value < 0:
            raise ValueError("Attendees must be a positive number")
        return value

    def __repr__(self):
        return f"<Event(id={
            self.id}, contract_id={
            self.contract_id}, location='{
            self.location}', start={
                self.event_start})>"
