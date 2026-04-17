from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Enum as SQLAlchemyEnum
from app.database.base import Base
from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from colorama import Fore, Style
from app.services.token_service import decode_token

class EnumRole(str, Enum):
    commercial = "commercial"
    support = "support"
    management = "management"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]
    role: Mapped[str] = mapped_column(SQLAlchemyEnum(
        "commercial", "support", "management",
        name="enumrole",
        create_constraint=True
    ))
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc)
)

    clients = relationship("Client", back_populates="commercial")
    contracts = relationship("Contract", back_populates="commercial")
    events = relationship("Event", back_populates="support")

    @classmethod
    def get_current_user(cls, token: str) :  
        from app.crud.crud_user import get_user_by_id
        
        payload = decode_token(token)
        if not payload:
            print(Fore.RED + "Invalid token." + Style.RESET_ALL)
            return None
        current_user = get_user_by_id(payload["user_id"])
        if not current_user:
            print(Fore.RED + "User not found." + Style.RESET_ALL)
            return None
            
        return current_user