from app.crud.crud_client import (
    create_client,
    get_all_clients,
    get_client_by_id,
    update_client,
    delete_client
)
from colorama import Fore, Style
from app.models.user import EnumRole
from app.services.auth_service import get_current_user
import sentry_sdk


# CREATE CLIENT
def create_client_service(full_name, email, phone, company_name, token):
    current_user = get_current_user(token)
    if not current_user:
        return None

    if not full_name or not email:
        print(
            Fore.RED +
            "Error: Name and email are required." +
            Style.RESET_ALL)
        return None
    try:
        # raise Exception("Test Sentry capture Create Client")
        if current_user.role != EnumRole.commercial.value:
            print(Fore.RED + "Permission denied." + Style.RESET_ALL)
            return None
        client = create_client(
            full_name=full_name,
            email=email,
            phone=phone,
            company_name=company_name,
            commercial_id=current_user.id
        )
        if client:
            print(
                Fore.GREEN +
                "Client created successfully." +
                Style.RESET_ALL)
            return client
    except Exception as e:
        sentry_sdk.capture_exception(e)
        print(Fore.RED + f"Error: {e}" + Style.RESET_ALL)
        return None


# READ ALL CLIENTS
def get_all_clients_service(token):
    current_user = get_current_user(token)
    if not current_user:
        return []

    try:
        clients = get_all_clients(current_user)  
        if current_user.role == EnumRole.management.value:
            return clients
        if current_user.role == EnumRole.commercial.value:
            filtered = [
                c for c in clients if c.commercial_id == current_user.id]
            if not filtered:
                print(Fore.YELLOW + "No clients found." + Style.RESET_ALL)
            return filtered
        if current_user.role == EnumRole.support.value:
            print(
                Fore.YELLOW +
                "Support role has no access to clients." +
                Style.RESET_ALL)
            return []
    except Exception as e:
        sentry_sdk.capture_exception(e)
        print(Fore.RED + f"Error retrieving clients: {e}" + Style.RESET_ALL)
        return []


# UPDATE CLIENT
def update_client_service(client_id, full_name, email, phone, token):
    current_user = get_current_user(token)
    if not current_user:
        return None

    try:
        client = get_client_by_id(client_id)
        if not client:
            print(Fore.RED + "Client not found." + Style.RESET_ALL)
            return None
        if current_user.role == EnumRole.commercial.value and client.commercial_id != current_user.id:
            print(
                Fore.RED +
                "Permission denied: You can only update your own clients." +
                Style.RESET_ALL)
            return None
        updated_client = update_client(
            client_id=client_id,
            full_name=full_name,
            email=email,
            phone=phone
        )
        if updated_client:
            print(
                Fore.GREEN +
                "Client updated successfully." +
                Style.RESET_ALL)
            return updated_client
        else:
            print(Fore.RED + "Failed to update client." + Style.RESET_ALL)
            return None
    except Exception as e:
        sentry_sdk.capture_exception(e)
        print(Fore.RED + f"Error updating client: {e}" + Style.RESET_ALL)
        return None


# DELETE CLIENT
def delete_client_service(client_id, token):
    current_user = get_current_user(token)
    if not current_user:
        return False

    try:
        client = get_client_by_id(client_id)
        if not client:
            print(Fore.RED + "Client not found." + Style.RESET_ALL)
            return False
        if current_user.role != EnumRole.management.value:
            print(
                Fore.RED +
                "Permission denied: Only management can delete clients." +
                Style.RESET_ALL)
            return False
        success = delete_client(client_id)
        if success:
            print(
                Fore.GREEN +
                "Client deleted successfully." +
                Style.RESET_ALL)
            return True
        else:
            print(Fore.RED + "Failed to delete client." + Style.RESET_ALL)
            return False
    except Exception as e:
        sentry_sdk.capture_exception(e)
        print(Fore.RED + f"Error deleting client: {e}" + Style.RESET_ALL)
        return False
