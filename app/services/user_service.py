from app.crud.crud_user import (
    create_user, 
    get_user_by_email, 
    get_all_users,
    get_user_by_id,
    update_user,
    delete_user
)
from app.models.user import EnumRole
from colorama import Fore, Style
from app.services.auth_service import verify_password, get_current_user
import sentry_sdk



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
        sentry_sdk.capture_exception(e)
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
        sentry_sdk.capture_exception(e)
        print(Fore.RED + f"Error during login: {e}" + Style.RESET_ALL)
        return None


# Management only - CREATE USER
def create_user_service(full_name, email, password, role, token):
    current_user = get_current_user(token)
    if not current_user:
        return None
    
    if current_user.role != EnumRole.management.value:
        print(Fore.RED + "Permission denied: Only management can create users." + Style.RESET_ALL)
        return None
    
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
            print(Fore.GREEN + "User created successfully." + Style.RESET_ALL)
            return user
        else:
            print(Fore.RED + "Failed to create user." + Style.RESET_ALL)
            return None
    except Exception as e:
        sentry_sdk.capture_exception(e)
        print(Fore.RED + f"Error creating user: {e}" + Style.RESET_ALL)
        return None


# Management only - GET ALL USERS
def get_all_users_service(token):
    current_user = get_current_user(token)
    if not current_user:
        return []
    
    if current_user.role != EnumRole.management.value:
        print(Fore.RED + "Permission denied: Only management can view all users." + Style.RESET_ALL)
        return []
    
    try:
        users = get_all_users()
        return users
    except Exception as e:
        sentry_sdk.capture_exception(e)
        print(Fore.RED + f"Error retrieving users: {e}" + Style.RESET_ALL)
        return []


# Management only - UPDATE USER
def update_user_service(user_id, full_name, email, password, role, token):
    current_user = get_current_user(token)
    if not current_user:
        return None
    
    if current_user.role != EnumRole.management.value:
        print(Fore.RED + "Permission denied: Only management can update users." + Style.RESET_ALL)
        return None
    
    try:
        user = get_user_by_id(user_id)
        if not user:
            print(Fore.RED + "User not found." + Style.RESET_ALL)
            return None
        
        updated_user = update_user(
            user_id=user_id,
            full_name=full_name,
            email=email,
            password=password,
            role=role
        )
        if updated_user:
            print(Fore.GREEN + "User updated successfully." + Style.RESET_ALL)
            return updated_user
        else:
            print(Fore.RED + "Failed to update user." + Style.RESET_ALL)
            return None
    except Exception as e:
        sentry_sdk.capture_exception(e)
        print(Fore.RED + f"Error updating user: {e}" + Style.RESET_ALL)
        return None


# Management only - DELETE USER
def delete_user_service(user_id, token):
    current_user = get_current_user(token)
    if not current_user:
        return False
    
    if current_user.role != EnumRole.management.value:
        print(Fore.RED + "Permission denied: Only management can delete users." + Style.RESET_ALL)
        return False
    
    try:
        user = get_user_by_id(user_id)
        if not user:
            print(Fore.RED + "User not found." + Style.RESET_ALL)
            return False
        
        success = delete_user(user_id)
        if success:
            print(Fore.GREEN + "User deleted successfully." + Style.RESET_ALL)
            return True
        else:
            print(Fore.RED + "Failed to delete user." + Style.RESET_ALL)
            return False
    except Exception as e:
        sentry_sdk.capture_exception(e)
        print(Fore.RED + f"Error deleting user: {e}" + Style.RESET_ALL)
        return False