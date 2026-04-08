from http import client

from app.crud.crud_contract import (
    create_contract,
    get_all_contracts,
    get_contract_by_id,
    update_contract,
    delete_contract
)

from app.crud.crud_client import get_client_by_id
from colorama import Fore, Style
from app.models.user import EnumRole
from app.models.contract import EnumStatus
from app.services.token_service import decode_token
from app.crud.crud_user import get_user_by_id


# CREATE CONTRACT
def create_contract_service(client_id, total_amount, remaining_amount, status, token_user):
    payload = decode_token(token_user)
    if not payload:
        print(Fore.RED + "Invalid token." + Style.RESET_ALL)
        return None
    
    current_user = get_user_by_id(payload["user_id"])
    
    if not client_id or total_amount is None:
        print(Fore.RED + "Error: Client and total amount are required." + Style.RESET_ALL)
        return None
    try:
        if current_user.role not in [EnumRole.commercial.value, EnumRole.management.value]:
            print(Fore.RED + "Permission denied: Only commercial or management users can create contracts." + Style.RESET_ALL)
            return None
        client = get_client_by_id(client_id)
        if not client:
            print(Fore.RED + "Client not found." + Style.RESET_ALL)
            return None
        if client.commercial_id != current_user.id:
            print(Fore.RED + "Permission denied: This client is not yours." + Style.RESET_ALL)
            return None
        contract = create_contract(
            client_id=client_id,
            commercial_id=client.commercial_id,
            total_amount=total_amount,
            remaining_amount=remaining_amount,
            status=status  
        )
        if contract:
            print(Fore.GREEN + "Contract created successfully." + Style.RESET_ALL)
            return contract
        else:
            print(Fore.RED + "Failed to create contract." + Style.RESET_ALL)
            return None
    except Exception as e:
        print(Fore.RED + f"Error creating contract: {e}" + Style.RESET_ALL)
        return None


def get_all_contracts_service(current_user):
    try:
        contracts = get_all_contracts()
        if current_user.role == EnumRole.management.value:
            return contracts
        elif current_user.role == EnumRole.commercial.value:
            filtered = [c for c in contracts if c.commercial_id == current_user.id]
            if not filtered:
                print(Fore.YELLOW + "No contracts found." + Style.RESET_ALL)
            return filtered
        elif current_user.role == EnumRole.support.value:
            print(Fore.YELLOW + "Support role has no access to contracts." + Style.RESET_ALL)
            return []
        return []

    except Exception as e:
        print(Fore.RED + f"Error retrieving contracts: {e}" + Style.RESET_ALL)
        return []

# UPDATE CONTRACT
def update_contract_service(contract_id, total_amount, remaining_amount, status, token_user):
    payload = decode_token(token_user)
    if not payload:
        print(Fore.RED + "Invalid token." + Style.RESET_ALL)
        return None
    
    current_user = get_user_by_id(payload["user_id"])
    
    try:
        contract = get_contract_by_id(contract_id)
        if not contract:
            print(Fore.RED + "Contract not found." + Style.RESET_ALL)
            return None
        if current_user.role == EnumRole.commercial.value and contract.commercial_id != current_user.id:
            print(Fore.RED + "Permission denied: You can only update your own contracts." + Style.RESET_ALL)
            return None
        updated_contract = update_contract(
            contract_id=contract_id,
            total_amount=total_amount,
            remaining_amount=remaining_amount,
            status=status  # EnumStatus
        )
        if updated_contract:
            print(Fore.GREEN + "Contract updated successfully." + Style.RESET_ALL)
            return updated_contract
        else:
            print(Fore.RED + "Failed to update contract." + Style.RESET_ALL)
            return None
    except Exception as e:
        print(Fore.RED + f"Error updating contract: {e}" + Style.RESET_ALL)
        return None


# DELETE CONTRACT
def delete_contract_service(contract_id, token_user):
    payload = decode_token(token_user)
    if not payload:
        print(Fore.RED + "Invalid token." + Style.RESET_ALL)
        return False
    
    current_user = get_user_by_id(payload["user_id"])
    
    try:
        contract = get_contract_by_id(contract_id)
        if not contract:
            print(Fore.RED + "Contract not found." + Style.RESET_ALL)
            return False

        if current_user.role != EnumRole.management.value:
            print(Fore.RED + "Permission denied: Only management can delete contracts." + Style.RESET_ALL)
            return False
        success = delete_contract(contract_id)
        if success:
            print(Fore.GREEN + "Contract deleted successfully." + Style.RESET_ALL)
            return True
        else:
            print(Fore.RED + "Failed to delete contract." + Style.RESET_ALL)
            return False
    except Exception as e:
        print(Fore.RED + f"Error deleting contract: {e}" + Style.RESET_ALL)
        return False