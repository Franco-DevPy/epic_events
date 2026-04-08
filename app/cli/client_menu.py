import questionary
from colorama import Fore, Style

from app.services.client_service import (
    create_client_service,
    get_all_clients_service,
    update_client_service,
    delete_client_service
)


def client_menu(current_user, token):
    while True:
        print(Fore.BLUE + "\n=== Clients Menu ===" + Style.RESET_ALL)
        choice = questionary.select(
            "Choose an action:",
            choices=[
                "Create client",
                "List clients",
                "Update client",
                "Delete client",
                "Back"
            ]
        ).ask()
        #CREATE CLIENT
        if choice == "Create client":
            print(Fore.CYAN + "\n=== Create Client ===" + Style.RESET_ALL)
            full_name = questionary.text("Full name:").ask()
            email = questionary.text("Email:").ask()
            phone = questionary.text("Phone:").ask()
            company_name = questionary.text("Company name:").ask()
            create_client_service(
                full_name=full_name,
                email=email,
                phone=phone,
                company_name=company_name,
                token_user=token
            )
        #LIST CLIENTS
        elif choice == "List clients":
            print(Fore.CYAN + "\n=== Clients List ===" + Style.RESET_ALL)
            clients = get_all_clients_service(current_user)
            if not clients:
                print(Fore.YELLOW + "No clients found." + Style.RESET_ALL)
            else:
                for c in clients:
                    print(
                        Fore.GREEN +
                        f"[ID {c.id}] {c.full_name} | {c.email} | {c.company_name}"
                        + Style.RESET_ALL
                    )
        # UPDATE CLIENT
        elif choice == "Update client":
            print(Fore.CYAN + "\n=== Update Client ===" + Style.RESET_ALL)
            clients = get_all_clients_service(current_user)
            if not clients:
                print(Fore.YELLOW + "No clients available." + Style.RESET_ALL)
                continue
            client_choice = questionary.select(
                "Select client:",
                choices=[
                    f"{c.id} - {c.full_name}"
                    for c in clients
                ]
            ).ask()
            client_id = int(client_choice.split(" - ")[0])
            full_name = questionary.text("New name (leave empty):").ask()
            email = questionary.text("New email (leave empty):").ask()
            phone = questionary.text("New phone (leave empty):").ask()
            update_client_service(
                client_id=client_id,
                full_name=full_name or None,
                email=email or None,
                phone=phone or None,
                token_user=token
            )
        # DELETE CLIENT
        elif choice == "Delete client":
            print(Fore.CYAN + "\n=== Delete Client ===" + Style.RESET_ALL)
            clients = get_all_clients_service(current_user)
            if not clients:
                print(Fore.YELLOW + "No clients available." + Style.RESET_ALL)
                continue
            client_choice = questionary.select(
                "Select client to delete:",
                choices=[
                    f"{c.id} - {c.full_name}"
                    for c in clients
                ]
            ).ask()
            client_id = int(client_choice.split(" - ")[0])
            confirm = questionary.confirm("Are you sure?").ask()
            if confirm:
                delete_client_service(client_id, token)
            else:
                print(Fore.YELLOW + "Deletion cancelled." + Style.RESET_ALL)
        elif choice == "Back":
            break