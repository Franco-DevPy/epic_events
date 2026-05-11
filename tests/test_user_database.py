from app.models.user import User, EnumRole
from app.services.auth_service import hash_password


def test_create_user_in_db(db_session):
    user = User(
        full_name="John Doe",
        email="john@example.com",
        password_hash=hash_password("password123"),
        role=EnumRole.commercial
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    assert user.id is not None
    assert user.email == "john@example.com"
    print(f"USER CREATED {user.full_name} (ID: {user.id})")


def test_read_user_from_db(db_session, management_user):
    found = db_session.query(User).filter_by(
        email="manager@test.com"
    ).first()

    assert found is not None
    assert found.id == management_user.id
    assert found.role == "management"
    print(f"USER FOUND {found.full_name} (ID: {found.id})")


def test_update_user_in_db(db_session, management_user):
    management_user.full_name = "Updated Name"
    db_session.commit()

    db_session.refresh(management_user)
    assert management_user.full_name == "Updated Name"

    found = db_session.query(User).filter_by(
        id=management_user.id
    ).first()
    assert found.full_name == "Updated Name"
    print(f"USER UPDATED {found.full_name} (ID: {found.id})")


def test_delete_user_from_db(db_session, management_user):
    user_id = management_user.id

    db_session.delete(management_user)
    db_session.commit()

    found = db_session.query(User).filter_by(id=user_id).first()
    assert found is None
    print(f"USER DELETED (ID: {user_id})")


def test_list_all_users(db_session, management_user):
    user2 = User(
        full_name="User 2",
        email="user2@test.com",
        password_hash=hash_password("pass"),
        role=EnumRole.commercial
    )
    user3 = User(
        full_name="User 3",
        email="user3@test.com",
        password_hash=hash_password("pass"),
        role=EnumRole.support
    )

    db_session.add(user2)
    db_session.add(user3)
    db_session.commit()

    all_users = db_session.query(User).all()
    assert len(all_users) == 3

    emails = [u.email for u in all_users]
    assert "manager@test.com" in emails
    assert "user2@test.com" in emails
    assert "user3@test.com" in emails

    print(f"TOTAL USERS: {len(all_users)}")
