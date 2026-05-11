from pytest import fixture
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from app.database.base import Base
from app.services.token_service import generate_token


load_dotenv(encoding='utf-8')


@fixture(scope="session")
def sqlalchemy_connect_url():
    url = os.getenv("TEST_DATABASE_URL")
    if not url:
        raise ValueError(
            "Test URL not found. Please set TEST_DATABASE_URL in your .env file."
        )
    return url


@fixture(scope="session", autouse=True)
def setup_database(sqlalchemy_connect_url):
    engine = create_engine(sqlalchemy_connect_url, echo=False)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    print("Tables dropped!")


@fixture
def db_session(transaction, dbsession):
    return dbsession


@fixture
def management_user(db_session):
    from app.models.user import User, EnumRole
    from app.services.auth_service import hash_password

    user = User(
        full_name="Admin Manager",
        email="manager@test.com",
        password_hash=hash_password("password123"),
        role=EnumRole.management
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user


@fixture
def commercial_user(db_session):
    from app.models.user import User, EnumRole
    from app.services.auth_service import hash_password

    user = User(
        full_name="John Commercial",
        email="commercial@test.com",
        password_hash=hash_password("password123"),
        role=EnumRole.commercial
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user


@fixture
def support_user(db_session):
    from app.models.user import User, EnumRole
    from app.services.auth_service import hash_password

    user = User(
        full_name="Jane Support",
        email="support@test.com",
        password_hash=hash_password("password123"),
        role=EnumRole.support
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user


@fixture
def management_token(management_user):
    return generate_token(management_user)


@fixture
def commercial_token(commercial_user):
    return generate_token(commercial_user)


@fixture
def support_token(support_user):
    return generate_token(support_user)
