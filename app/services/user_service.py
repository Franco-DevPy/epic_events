from app.crud.crud_user import create_user, get_user_by_email
from app.models.user import EnumRole

from colorama import Fore, Style
from colorama import Fore, Style
from app.crud.crud_user import get_user_by_email
from app.services.auth_service import verify_password



def register_user_service(full_name, email, password, role):
    if not full_name or not email or not password:
        print(Fore.RED + "Error: All fields are required." + Style.RESET_ALL)
        return None
    try:
        existing_user = get_user_by_email(email)
        if existing_user:
            print(Fore.YELLOW + "User already exists with this email." + Style.RESET_ALL)
            return None
        user = create_user(
            full_name=full_name,
            email=email,
            password=password,
            role=role
        )
        if user:
            print(Fore.GREEN + "User registered successfully." + Style.RESET_ALL)
            return user
        else :
            print(Fore.RED + "Failed to register user." + Style.RESET_ALL)
            return None
    except Exception as e:
        print(Fore.RED + f"Error registering user: {e}" + Style.RESET_ALL)
        return None
    

def login_user_service(email, password):
    if not email or not password:
        print(Fore.RED + "Error: Email and password are required." + Style.RESET_ALL)
        return None
    try:
        user = get_user_by_email(email)
        if not user:
            print(Fore.RED + "User not found." + Style.RESET_ALL)
            return None

        if verify_password(password, user.password_hash):
            print(Fore.GREEN +f"Welcome {user.full_name}! You are logged in as {user.role}."+ Style.RESET_ALL)
            return user
        else:
            print(Fore.RED + "Invalid password." + Style.RESET_ALL)
            return None
    except Exception as e:
        print(Fore.RED + f"Error during login: {e}" + Style.RESET_ALL)
        return None