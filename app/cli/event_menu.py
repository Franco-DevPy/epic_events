import questionary
from colorama import Fore, Style

from app.services.event_service import create_event_service
from app.crud.crud_contract import get_all_contracts
from app.crud.crud_user import get_users_by_role
from app.services.event_service import (
    get_all_events_service,
    update_event_service,
    delete_event_service,
    get_events_without_support_service
)

# SIMULAR USER
from app.crud.crud_user import get_user_by_id

def event_menu(token):
    from app.models.user import User
    current_user = User.get_current_user(token)
    if not current_user:
        return
    
    while True:
        print(Fore.CYAN + "\n=== Events Menu ===" + Style.RESET_ALL)

        if current_user.role == "support":
            choices = [
                "List events",
                "Back"
            ]
        else:
            choices = [
                "Create event",
                "List events",
                "Update event",
                "Delete event",
                "Back"
            ]

        choice = questionary.select(
            "Choose an action:",
            choices=choices
        ).ask()

        if choice == "Create event":
            print(Fore.CYAN + "\n=== Create Event ===" + Style.RESET_ALL)
            current_user = get_user_by_id(current_user.id)
            print(Fore.YELLOW + "Date format: YYYY-MM-DD HH:MM (e.g., 2026-06-01 14:30)" + Style.RESET_ALL)
            event_start = questionary.text("Event start (YYYY-MM-DD HH:MM):").ask()
            event_end = questionary.text("Event end (YYYY-MM-DD HH:MM):").ask()
            location = questionary.text("Location:").ask()
            attendees = questionary.text("Number of attendees:").ask()
            notes = questionary.text("Notes (optional):").ask()
            try:
                attendees = int(attendees)
            except:
                print(Fore.RED + "Attendees must be a number." + Style.RESET_ALL)
                return
            # SELECT CONTRACT
            contracts = get_all_contracts()
            
            if not contracts:
                print(Fore.RED + "No contracts available." + Style.RESET_ALL)
                return
            contract_choice = questionary.select(
                "Select a contract:",
                choices=[
                    f"ID {c.id} | Client: {c.client.full_name} ({c.client.company_name}) | Status: {c.status.value}"
                    for c in contracts
                ]
            ).ask()
            contract_id = int(contract_choice.split()[1])
            # SELECT SUPPORT
            support_users = get_users_by_role("support")
            if not support_users:
                print(Fore.RED + "No support users available." + Style.RESET_ALL)
                return
            
            support_choices = [f"{u.id} - {u.full_name}" for u in support_users]
            support_choices.append("No support (assign later)")
            
            support_choice = questionary.select(
                "Select a support user:",
                choices=support_choices
            ).ask()
            
            if support_choice == "No support (assign later)":
                support_id = None
            else:
                support_id = int(support_choice.split(" - ")[0])
            
            create_event_service(
                event_start=event_start,
                event_end=event_end,
                location=location,
                attendees=attendees,
                contract_id=contract_id,
                support_id=support_id,
                notes=notes or None,
                token=token
            )
        elif choice == "List events":
            # Sub-menu for filtering events (Management only)
            if current_user.role == "management":
                while True:
                    print(Fore.MAGENTA + "\n=== Filter Events ===" + Style.RESET_ALL)
                    filter_choice = questionary.select(
                        "Select filter:",
                        choices=[
                            "All events",
                            "Events without support",
                            "Back"
                        ]
                    ).ask()
                    
                    if filter_choice == "All events":
                        print(Fore.CYAN + "\n=== All Events ===" + Style.RESET_ALL)
                        events = get_all_events_service(token)
                        if not events:
                            print(Fore.YELLOW + "No events found." + Style.RESET_ALL)
                        else:
                            for event in events:
                                support_name = event.support.full_name if event.support else "No support assigned"
                                print(
                                    Fore.GREEN +
                                    f"[ID {event.id}] {event.location} | {event.event_start} to {event.event_end} | {event.attendees} attendees | Support: {support_name}"
                                    + Style.RESET_ALL
                                )
                    
                    elif filter_choice == "Events without support":
                        print(Fore.CYAN + "\n=== Events Without Support ===" + Style.RESET_ALL)
                        events = get_events_without_support_service(token)
                        if not events:
                            print(Fore.YELLOW + "No events without support found." + Style.RESET_ALL)
                        else:
                            for event in events:
                                print(
                                    Fore.GREEN +
                                    f"[ID {event.id}] {event.location} | {event.event_start} to {event.event_end} | {event.attendees} attendees | Support: No support assigned"
                                    + Style.RESET_ALL
                                )
                    
                    elif filter_choice == "Back":
                        break
            else:
                # For Support and Commercial, show their events directly
                print(Fore.CYAN + "\n=== Events List ===" + Style.RESET_ALL)
                events = get_all_events_service(token)
                if not events:
                    print(Fore.YELLOW + "No events found." + Style.RESET_ALL)
                else:
                    for event in events:
                        support_name = event.support.full_name if event.support else "No support assigned"
                        print(
                            Fore.GREEN +
                            f"[ID {event.id}] {event.location} | {event.event_start} to {event.event_end} | {event.attendees} attendees | Support: {support_name}"
                            + Style.RESET_ALL
                        )
        elif choice == "Update event":
            print(Fore.CYAN + "\n=== Update Event ===" + Style.RESET_ALL)
            events = get_all_events_service(token)
            if not events:
                print(Fore.YELLOW + "No events available." + Style.RESET_ALL)
                return
            
            event_choices = [f"{e.id} - {e.location} ({e.event_start})" for e in events]
            event_choices.append("Cancel")
            
            event_choice = questionary.select(
                "Select event to update:",
                choices=event_choices
            ).ask()
            
            if event_choice == "Cancel":
                print(Fore.YELLOW + "Update cancelled." + Style.RESET_ALL)
                continue
            
            event_id = int(event_choice.split(" - ")[0])
            event_start = questionary.text("New event start (YYYY-MM-DD HH:MM, leave empty to skip):").ask()
            event_end = questionary.text("New event end (YYYY-MM-DD HH:MM, leave empty to skip):").ask()
            location = questionary.text("New location (leave empty to skip):").ask()
            attendees = questionary.text("New attendees (leave empty to skip):").ask()
            notes = questionary.text("New notes (leave empty to skip):").ask()
            if attendees:
                try:
                    attendees = int(attendees)
                except:
                    print(Fore.RED + "Attendees must be a number." + Style.RESET_ALL)
                    return
            else:
                attendees = None
            update_event_service(
                event_id=event_id,
                event_start=event_start or None,
                event_end=event_end or None,
                location=location or None,
                attendees=attendees,
                notes=notes or None,
                token=token
            )
        elif choice == "Delete event":
            print(Fore.CYAN + "\n=== Delete Event ===" + Style.RESET_ALL)
            events = get_all_events_service(token)
            if not events:
                print(Fore.YELLOW + "No events available." + Style.RESET_ALL)
                return
            
            event_choices = [f"{e.id} - {e.location} ({e.event_start})" for e in events]
            event_choices.append("Cancel")
            
            event_choice = questionary.select(
                "Select event to delete:",
                choices=event_choices
            ).ask()
            
            if event_choice == "Cancel":
                print(Fore.YELLOW + "Deletion cancelled." + Style.RESET_ALL)
                continue
            
            event_id = int(event_choice.split(" - ")[0])
            confirm = questionary.confirm("Are you sure?").ask()
            if confirm:
                delete_event_service(event_id, token)
            else:
                print(Fore.YELLOW + "Deletion cancelled." + Style.RESET_ALL)
        elif choice == "Back":
            break