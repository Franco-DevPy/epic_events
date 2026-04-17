import questionary
from colorama import Fore, Style

from app.cli.client_menu import client_menu
from app.cli.contract_menu import contract_menu
from app.cli.event_menu import event_menu
from app.cli.user_menu import user_menu

from app.models.user import EnumRole, User


def main_menu(token):
    current_user = User.get_current_user(token)
    if not current_user:
        return
    
    while True:
        print(Fore.MAGENTA + f"\n=== Main Menu ({current_user.full_name} - {Fore.CYAN}{current_user.role.upper()}{Fore.MAGENTA}) ===" + Style.RESET_ALL)
        if current_user.role == EnumRole.commercial.value:
            choices = ["Clients", "Contracts", "Events", "Logout"]

        elif current_user.role == EnumRole.support.value:
            choices = ["Events", "Logout"]

        elif current_user.role == EnumRole.management.value:
            choices = ["Users", "Clients", "Contracts", "Events", "Logout"]

        choice = questionary.select(
            "Choose an option:",
            choices=choices
        ).ask()
        if choice == "Users":
            user_menu(token)
        elif choice == "Clients":
            client_menu(token)
        elif choice == "Contracts":
            contract_menu(token)
        elif choice == "Events":
            event_menu(token)
        elif choice == "Logout":
            print(Fore.YELLOW + "Logging out..." + Style.RESET_ALL)
            break