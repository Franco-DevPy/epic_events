from app.database.session import get_db_session
from app.models.user import User, EnumRole
from app.services.auth_service import hash_password

# CRUD operations CREATE
def create_user(full_name: str, email: str, password: str, role: EnumRole):
    session = get_db_session()
    try:
        new_user = User(
            full_name=full_name,
            email=email,
            password_hash=hash_password(password),
            role=role
        )
        session.add(new_user)
        session.commit()
        print(f"User '{full_name}' created successfully.")
        return new_user
    except Exception as e:
        session.rollback()
        print(f"Error creating user: {e}")

    finally:
        session.close()


# CRUD operations READ
def get_user_by_email(email: str):
    session = get_db_session()
    try:
        user = session.query(User).filter_by(email=email).first()
        print(f"User with email '{email}' retrieved successfully.")
        return user
    except Exception as e:
        print(f"Error retrieving user: {e}")
    finally:
        session.close()



def get_user_by_id(user_id: int):
    session = get_db_session()
    try:
        user = session.get(User, user_id)
        print(f"User with ID '{user_id}' retrieved successfully.")
        return user
    except Exception as e:
        print(f"Error retrieving user: {e}")
    finally:
        session.close()

# CRUD operations UPDATE
def update_user(user_id: int, full_name: str = None, email: str = None, password: str = None, role: EnumRole = None):
    session = get_db_session()
    try:
        user = session.get(User, user_id)
        if not user:
            print(f"User with ID {user_id} not found.")
            return None

        if full_name:
            user.full_name = full_name
        if email:
            user.email = email
        if password:
            user.password_hash = hash_password(password)
        if role:
            user.role = role

        session.commit()
        print(f"User with ID {user_id} updated successfully.")
        return user
    except Exception as e:
        session.rollback()
        print(f"Error updating user: {e}")
    finally:
        session.close()


# CRUD GET USER BY ROLE
def get_users_by_role(role: EnumRole):
    session = get_db_session()
    try:
        users = session.query(User).filter_by(role=role).all()
        print(f"Users with role '{role}' retrieved successfully.")
        return users
    except Exception as e:
        print(f"Error retrieving users by role: {e}")
    finally:
        session.close()


# CRUD operations DELETE
def delete_user(user_id: int):
    session = get_db_session()
    try:
        user = session.get(User, user_id)
        if not user:
            print(f"User with ID {user_id} not found.")
            return False

        session.delete(user)
        session.commit()
        print(f"User with ID {user_id} deleted successfully.")
        return True
    except Exception as e:
        session.rollback()
        print(f"Error deleting user: {e}")
    finally:
        session.close()



