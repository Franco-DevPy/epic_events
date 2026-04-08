import questionary
from colorama import Fore, Style

from app.cli.client_menu import client_menu
from app.cli.contract_menu import contract_menu
from app.cli.event_menu import event_menu


from app.models.user import EnumRole


def main_menu(current_user, token):
    while True:
        print(Fore.MAGENTA + f"\n=== Main Menu ({current_user.full_name} - {current_user.role}) ===" + Style.RESET_ALL)

        if current_user.role == EnumRole.commercial.value:
            choices = ["Clients", "Contracts", "Events", "Logout"]

        elif current_user.role == EnumRole.support.value:
            choices = ["Events", "Logout"]

        elif current_user.role == EnumRole.management.value:
            choices = ["Clients", "Contracts", "Events", "Logout"]

        choice = questionary.select(
            "Choose an option:",
            choices=choices
        ).ask()

        if choice == "Clients":
            client_menu(current_user, token)

        elif choice == "Contracts":
            contract_menu(current_user, token)

        elif choice == "Events":
            event_menu(current_user, token)

        elif choice == "Logout":
            print(Fore.YELLOW + "Logging out..." + Style.RESET_ALL)
            break