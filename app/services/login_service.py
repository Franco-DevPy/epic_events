from app.crud.crud_user import create_user, get_user_by_email
from app.models.user import EnumRole
from colorama import Fore, Style
from app.crud.crud_user import get_user_by_id
import sentry_sdk



#login services

def login_user_service(email, password):
    from app.crud.crud_user import get_user_by_email
    from app.services.auth_service import verify_password
    if not email or not password:
        print("Email and password are required.")
        return None
    try:
        user = get_user_by_email(email)
        if user and verify_password(password, user.password_hash):
            return user
        else:
            print("Invalid email or password.")
            return None
    except Exception as e:
        sentry_sdk.capture_exception(e)
        print(f"Error during login: {e}")
        return None