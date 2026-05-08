from app.database.base import Base
from app.database.connection import engine
# Imports necesarios para que SQLAlchemy registre los modelos
from app.models.user import User  # noqa: F401
from app.models.client import Client  # noqa: F401
from app.models.contract import Contract  # noqa: F401
from app.models.event import Event  # noqa: F401


def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")


if __name__ == "__main__":
    init_db()
