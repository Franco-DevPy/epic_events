import questionary
from colorama import Fore, Style

from app.cli.main_menu import main_menu
from app.services.user_service import register_user_service
from app.models.user import EnumRole
from app.services.login_service import login_user_service
from app.services.token_service import generate_token


def start_menu():
    while True:
        print(Fore.CYAN + "\n=== Epic Events CRM ===" + Style.RESET_ALL)

        choice = questionary.select(
            "Welcome! Choose an option:",
            choices=[
                "Login",
                "Register",
                "Exit"
            ]
        ).ask()
        if choice == "Login":
            while True:
                email = questionary.text("Email:").ask()
                password = questionary.password("Password:").ask()
                user = login_user_service(email, password)
                if user:
                    token = generate_token(user)
                    main_menu(token)
                    break
                else:
                    retry = questionary.confirm("Try again?").ask()
                    if not retry:
                        break
        elif choice == "Register":
            print(Fore.CYAN + "\n=== Register User ===" + Style.RESET_ALL)
            full_name = questionary.text("Full name:").ask()
            email = questionary.text("Email:").ask()
            password = questionary.password("Password:").ask()
            role_choice = questionary.select(
                "Select role:",
                choices=[
                    "commercial",
                    "support",
                    "management"
                ]
            ).ask()
            role = EnumRole(role_choice)
            register_user_service(
                full_name,
                email,
                password,
                role
            )
        elif choice == "Exit":
            print(Fore.YELLOW + "Goodbye!" + Style.RESET_ALL)
            break
