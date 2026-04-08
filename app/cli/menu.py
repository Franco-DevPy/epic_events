from prompt_toolkit import choice
import questionary
from colorama import Fore, Style

from app.cli.main_menu import main_menu
from app.services.user_service import register_user_service
from app.models.user import EnumRole
from app.services.login_service import login_user_service
from app.services.token_service import generate_token, decode_token
from app.crud.crud_user import get_user_by_id


def start_menu():
    while True:
        print(Fore.CYAN + "\n=== Epic Events CRM ===" + Style.RESET_ALL)

        choice = questionary.select(
            "Welcome! Choose an option:",
            choices=[
                "Login Alice Commercial",
                "Login Charliee Support",
                "Login Eve Management",
                "Login",
                "Register",
                "Exit"
            ]
        ).ask()

        ## SIMULAR USER ALICE

        if choice == "Login Alice Commercial":

            while True:
                print(Fore.CYAN + "\n=== Login ===" + Style.RESET_ALL)

                email = "alice@epic.com"
                password = "123456"

                user = login_user_service(email, password)

                if user:
                    token = generate_token(user)
                    payload = decode_token(token)
                    if payload:
                        user_id = payload["user_id"]
                        current_user = get_user_by_id(user_id)
                        main_menu(current_user, token)
                        break 
                else:
                    retry = questionary.confirm("Try again?").ask()
                    if not retry:
                        break

        if choice == "Login Charliee Support":

            while True:
                print(Fore.CYAN + "\n=== Login ===" + Style.RESET_ALL)

                email = "charlie@epic.com"
                password = "123456"

                user = login_user_service(email, password)

                if user:
                    token = generate_token(user)
                    payload = decode_token(token)
                    if payload:
                        user_id = payload["user_id"]
                        current_user = get_user_by_id(user_id)
                        main_menu(current_user, token)
                        break 
                else:
                    retry = questionary.confirm("Try again?").ask()
                    if not retry:
                        break

            if choice == "Login Eve Management":

                while True:
                    print(Fore.CYAN + "\n=== Login ===" + Style.RESET_ALL)

                    email = "eve@epic.com"
                    password = "123456"

                    user = login_user_service(email, password)

                    if user:
                        token = generate_token(user)
                        payload = decode_token(token)
                        if payload:
                            user_id = payload["user_id"]
                            current_user = get_user_by_id(user_id)
                            main_menu(current_user, token)
                            break 
                    else:
                        retry = questionary.confirm("Try again?").ask()
                        if not retry:
                            break

        if choice == "Login":

            while True:
                print(Fore.CYAN + "\n=== Login ===" + Style.RESET_ALL)

                email = questionary.text("Email:").ask()
                password = questionary.password("Password:").ask()

                user = login_user_service(email, password)

                if user:
                    token = generate_token(user)
                    payload = decode_token(token)
                    if payload:
                        user_id = payload["user_id"]
                        current_user = get_user_by_id(user_id)
                        main_menu(current_user, token)
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