from app.crud.crud_event import (
    create_event,
    get_all_events,
    get_event_by_id,
    update_event,
    delete_event,
    get_events_without_support
)

from app.crud.crud_contract import get_contract_by_id
from app.crud.crud_user import get_users_by_role
from app.models.contract import EnumStatus
from app.models.user import EnumRole, User
from colorama import Fore, Style
import sentry_sdk

# CREATE EVENT
def create_event_service(event_start, event_end, location, attendees, contract_id, support_id, notes, token):
    from datetime import datetime
    current_user = User.get_current_user(token)
    if not current_user:
        return None
    
    if not event_start or not event_end or not location or attendees is None:
        print(Fore.RED + "Error: Event start, event end, location, and attendees are required." + Style.RESET_ALL)
        return None
    try:
        if current_user.role != EnumRole.commercial.value:
            print(Fore.RED + "Permission denied: Only commercial can create events." + Style.RESET_ALL)
            return None
        contract = get_contract_by_id(contract_id)
        if not contract:
            print(Fore.RED + "Contract not found." + Style.RESET_ALL)
            return None
        if contract.status != EnumStatus.signed:
            print(Fore.RED + "Contract is not signed." + Style.RESET_ALL)
            return None        
        if contract.commercial_id != current_user.id:
            print(Fore.RED + "Permission denied." + Style.RESET_ALL)
            return None
        # Validate support user if provided
        if support_id is not None:
            support_users = get_users_by_role("support")
            if not any(user.id == support_id for user in support_users):
                print(Fore.RED + "Support user not found." + Style.RESET_ALL)
                return None
        # Parse datetime strings
        try:
            event_start_dt = datetime.strptime(event_start, "%Y-%m-%d %H:%M")
            event_end_dt = datetime.strptime(event_end, "%Y-%m-%d %H:%M")
        except ValueError as e:
            print(Fore.RED + f"Invalid date format. Use YYYY-MM-DD HH:MM (e.g., 2026-06-01 14:30)" + Style.RESET_ALL)
            print(Fore.RED + f"Ensure day and month have two digits (01-31 for day, 01-12 for month)" + Style.RESET_ALL)
            return None
        event = create_event(
            client_id=contract.client_id,
            contract_id=contract_id,
            support_id=support_id,
            event_start=event_start_dt,
            event_end=event_end_dt,
            location=location,
            attendees=attendees,
            notes=notes
        )
        if event:
            print(Fore.GREEN + "Event created successfully." + Style.RESET_ALL)
            return event
        else:
            print(Fore.RED + "Failed to create event." + Style.RESET_ALL)
            return None

    except Exception as e:
        sentry_sdk.capture_exception(e)
        print(Fore.RED + f"Error creating event: {e}" + Style.RESET_ALL)
        return None
    

# READ ALL EVENTS
def get_all_events_service(token):
    current_user = User.get_current_user(token)
    if not current_user:
        return []
    
    try:
        # raise Exception("Test Sentry capture Get All Events") 

        events = get_all_events()
        if current_user.role == EnumRole.management.value:
            return events
        if current_user.role == EnumRole.commercial.value:
            filtered = [
                e for e in events
                if e.contract and e.contract.commercial_id == current_user.id
            ]
        elif current_user.role == EnumRole.support.value:
            filtered = [
                e for e in events
                if e.support_id == current_user.id
            ]
        else:
            filtered = []
        if not filtered:
            print("No events found.")
        return filtered
    except Exception as e:
        sentry_sdk.capture_exception(e)
        print(Fore.RED + f"Error retrieving events: {e}" + Style.RESET_ALL)
        return []
    

# UPDATE EVENT
def update_event_service(event_id, event_start=None, event_end=None, location=None, attendees=None, notes=None, support_id=None, token=None):
    from datetime import datetime
    
    current_user = User.get_current_user(token)
    if not current_user:
        return None
    
    try:
        event = get_event_by_id(event_id)
        if not event:
            print(Fore.RED + f"Event with ID {event_id} not found." + Style.RESET_ALL)
            return None
        if current_user.role == EnumRole.support.value:
            if event.support_id != current_user.id:
                print(Fore.RED + "Permission denied: You can only update your own events." + Style.RESET_ALL)
                return None
        if current_user.role == EnumRole.commercial.value:
            contract = get_contract_by_id(event.contract_id)
            if contract.commercial_id != current_user.id:
                print(Fore.RED + "Permission denied: You can only update your clients' events." + Style.RESET_ALL)
                return None
        if support_id:
            support_users = get_users_by_role("support")
            if not any(user.id == support_id for user in support_users):
                print(Fore.RED + "Support user not found." + Style.RESET_ALL)
                return None
        
        # Parse datetime strings if provided
        event_start_dt = None
        event_end_dt = None
        if event_start:
            try:
                event_start_dt = datetime.strptime(event_start, "%Y-%m-%d %H:%M")
            except ValueError:
                print(Fore.RED + f"Invalid event start format. Use YYYY-MM-DD HH:MM (e.g., 2026-06-01 14:30)" + Style.RESET_ALL)
                print(Fore.RED + f"Ensure day and month have two digits (01-31 for day, 01-12 for month)" + Style.RESET_ALL)
                return None
        if event_end:
            try:
                event_end_dt = datetime.strptime(event_end, "%Y-%m-%d %H:%M")
            except ValueError:
                print(Fore.RED + f"Invalid event end format. Use YYYY-MM-DD HH:MM (e.g., 2026-06-02 18:00)" + Style.RESET_ALL)
                print(Fore.RED + f"Ensure day and month have two digits (01-31 for day, 01-12 for month)" + Style.RESET_ALL)
                return None
        
        updated_event = update_event(
            event_id=event_id,
            event_start=event_start_dt,
            event_end=event_end_dt,
            location=location,
            attendees=attendees,
            notes=notes,
            support_id=support_id
        )
        if updated_event:
            print(Fore.GREEN + "Event updated successfully." + Style.RESET_ALL)
            return updated_event
        else:
            print(Fore.RED + "Failed to update event." + Style.RESET_ALL)
            return None

    except Exception as e:
        sentry_sdk.capture_exception(e)
        print(Fore.RED + f"Error updating event: {e}" + Style.RESET_ALL)
        return None

# DELETE EVENT
def delete_event_service(event_id, token):
    current_user = User.get_current_user(token)
    if not current_user:
        return False
    
    try:
        event = get_event_by_id(event_id)

        if not event:
            print(Fore.RED + f"Event with ID {event_id} not found." + Style.RESET_ALL)
            return False
        if current_user.role == EnumRole.support.value:
            if event.support_id != current_user.id:
                print(Fore.RED + "Permission denied." + Style.RESET_ALL)
                return False
        if current_user.role == EnumRole.commercial.value:
            contract = get_contract_by_id(event.contract_id)
            if contract.commercial_id != current_user.id:
                print(Fore.RED + "Permission denied." + Style.RESET_ALL)
                return False
        if delete_event(event_id):
            print(Fore.GREEN + "Event deleted successfully." + Style.RESET_ALL)
            return True
        else:
            print(Fore.RED + "Failed to delete event." + Style.RESET_ALL)
            return False

    except Exception as e:
        sentry_sdk.capture_exception(e)
        print(Fore.RED + f"Error deleting event: {e}" + Style.RESET_ALL)
        return False


# GET EVENTS WITHOUT SUPPORT (Management only)
def get_events_without_support_service(token):
    current_user = User.get_current_user(token)
    if not current_user:
        return []
    
    if current_user.role != EnumRole.management.value:
        print(Fore.RED + "Permission denied: Only management can view events without support." + Style.RESET_ALL)
        return []
    
    try:
        events = get_events_without_support()
        if not events:
            print(Fore.YELLOW + "No events without support found." + Style.RESET_ALL)
        return events
    except Exception as e:
        sentry_sdk.capture_exception(e)
        print(Fore.RED + f"Error retrieving events without support: {e}" + Style.RESET_ALL)
        return []