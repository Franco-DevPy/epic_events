from app.database.base import Base
from app.database.connection import engine
# noqa: F401
from app.models.user import User 
from app.models.client import Client  
from app.models.contract import Contract  
from app.models.event import Event  


def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")


if __name__ == "__main__":
    init_db()
