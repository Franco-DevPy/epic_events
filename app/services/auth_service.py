from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from app.models.user import User
from app.services.token_service import decode_token
from app.database.session import get_db_session
from colorama import Fore, Style
import sentry_sdk

ph = PasswordHasher()


def hash_password(password: str) -> str:
    return ph.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    try:
        ph.verify(password_hash, password)
        return True
    except VerifyMismatchError as e:
        sentry_sdk.capture_exception(e)
        return False


def get_current_user(token: str):
    payload = decode_token(token)
    if not payload:
        print(Fore.RED + "Invalid token." + Style.RESET_ALL)
        return None

    user_id = payload.get("user_id")
    if not user_id:
        print(Fore.RED + "Invalid token payload." + Style.RESET_ALL)
        return None
    session = get_db_session()
    try:
        current_user = session.get(User, user_id)
        if not current_user:
            print(Fore.RED + "User not found." + Style.RESET_ALL)
            return None
        return current_user
    except Exception as e:
        print(Fore.RED + f"Error retrieving user: {e}" + Style.RESET_ALL)
        return None
    finally:
        session.close()
