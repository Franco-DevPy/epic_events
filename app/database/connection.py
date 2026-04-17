import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv(encoding='utf-8') 

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

if not all([DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT]):
    raise ValueError("Database configuration is incomplete. Please check your .env file.")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL, echo=False)

def get_db_connection():
    return engine.connect()


if __name__ == "__main__":    
    try:
        with get_db_connection() as connection:
            print("Database connection successful!")
    except Exception as e:
        print(f"Database connection failed: {e}")