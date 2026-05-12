import sentry_sdk
from colorama import Fore, Style


def login_user_service(email, password):
    from app.crud.crud_user import get_user_by_email
    from app.services.auth_service import verify_password
    if not email or not password:
        print(Fore.RED + "Email and password are required." + Style.RESET_ALL)
        return None
    try:
        user = get_user_by_email(email)
        if user and verify_password(password, user.password_hash):
            return user
        else:
            print(Fore.RED + "Invalid email or password." + Style.RESET_ALL)
            return None
    except Exception as e:
        sentry_sdk.capture_exception(e)
        print(Fore.RED + f"Error during login: {e}" + Style.RESET_ALL)
        return None
