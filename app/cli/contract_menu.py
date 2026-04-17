import questionary
from colorama import Fore, Style

from app.services.contract_service import (
    create_contract_service,
    get_all_contracts_service,
    update_contract_service,
    delete_contract_service
)

from app.models.contract import EnumStatus
from app.services.client_service import get_all_clients_service


def contract_menu(token):
    while True:
        print(Fore.YELLOW + "\n=== Contracts Menu ===" + Style.RESET_ALL)
        choice = questionary.select(
            "Choose an action:",
            choices=[
                "Create contract",
                "List contracts",
                "Update contract",
                "Delete contract",
                "Back"
            ]
        ).ask()
        # CREATE CONTRACT
        if choice == "Create contract":
            print(Fore.CYAN + "\n=== Create Contract ===" + Style.RESET_ALL)
            clients = get_all_clients_service(token)
            if not clients:
                print(Fore.RED + "No clients available." + Style.RESET_ALL)
                continue
            client_choice = questionary.select(
                "Select a client:",
                choices=[
                    f"{c.id} - {c.full_name}"
                    for c in clients
                ]
            ).ask()
            client_id = int(client_choice.split(" - ")[0])
            total_amount = questionary.text("Total amount:").ask()
            remaining_amount = questionary.text("Remaining amount:").ask()
            try:
                total_amount = float(total_amount)
                remaining_amount = float(remaining_amount)
            except:
                print(Fore.RED + "Amounts must be numbers." + Style.RESET_ALL)
                continue
            status_choice = questionary.select(
                "Select contract status:",
                choices=["signed", "unsigned"]
            ).ask()
            status = EnumStatus(status_choice)
            create_contract_service(
                client_id=client_id,
                total_amount=total_amount,
                remaining_amount=remaining_amount,
                status=status,
                token=token
            )
        elif choice == "List contracts":
            print(Fore.CYAN + "\n=== Contracts List ===" + Style.RESET_ALL)
            contracts = get_all_contracts_service(token)
            if not contracts:
                print(Fore.YELLOW + "No contracts found." + Style.RESET_ALL)
            else:
                for c in contracts:
                    print(
                        Fore.GREEN +
                        f"[ID {c.id}] Client :  {c.client.full_name} | ({c.client.company_name}) | total: {c.total_amount}€ | remaining: {c.remaining_amount}€ | {c.status.value}"
                        + Style.RESET_ALL
                    )
        elif choice == "Update contract":
            print(Fore.CYAN + "\n=== Update Contract ===" + Style.RESET_ALL)
            contracts = get_all_contracts_service(token)
            if not contracts:
                print(Fore.YELLOW + "No contracts available." + Style.RESET_ALL)
                continue
            contract_choice = questionary.select(
                "Select contract:",
                choices=[
                    f"{c.id} - Client :  {c.client.full_name} | ({c.client.company_name}) | total: {c.total_amount}€ | remaining: {c.remaining_amount}€ | {c.status.value}"
                    for c in contracts
                ]
            ).ask()
            contract_id = int(contract_choice.split(" - ")[0])
            total_amount = questionary.text("New total amount (leave empty):").ask()
            remaining_amount = questionary.text("New remaining amount (leave empty):").ask()
            status_choice = questionary.select(
                "New status:",
                choices=["skip", "signed", "unsigned"]
            ).ask()
            total_amount = float(total_amount) if total_amount else None
            remaining_amount = float(remaining_amount) if remaining_amount else None
            status = EnumStatus(status_choice) if status_choice != "skip" else None
            update_contract_service(
                contract_id=contract_id,
                total_amount=total_amount,
                remaining_amount=remaining_amount,
                status=status,
                token=token
            )
        elif choice == "Delete contract":
            print(Fore.CYAN + "\n=== Delete Contract ===" + Style.RESET_ALL)
            contracts = get_all_contracts_service(token)
            if not contracts:
                print(Fore.YELLOW + "No contracts available." + Style.RESET_ALL)
                continue
            contract_choice = questionary.select(
                "Select contract to delete:",
                choices=[
                    f"{c.id} - Client :  {c.client.full_name} | ({c.client.company_name}) | total: {c.total_amount}€ | remaining: {c.remaining_amount}€ | {c.status.value}"
                    for c in contracts
                ]
            ).ask()
            contract_id = int(contract_choice.split(" - ")[0])
            confirm = questionary.confirm("Are you sure?").ask()
            if confirm:
                delete_contract_service(contract_id, token)
            else:
                print(Fore.YELLOW + "Deletion cancelled." + Style.RESET_ALL)
        elif choice == "Back":
            break