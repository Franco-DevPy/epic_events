import questionary
from colorama import Fore, Style

from app.services.user_service import (
    create_user_service,
    get_all_users_service,
    update_user_service,
    delete_user_service
)
from app.models.user import EnumRole


def user_menu(token):
    while True:
        print(Fore.MAGENTA + "\n=== Users Management Menu ===" + Style.RESET_ALL)
        choice = questionary.select(
            "Choose an action:",
            choices=[
                "Create user",
                "List users",
                "Update user",
                "Delete user",
                "Back"
            ]
        ).ask()
        
        # CREATE USER
        if choice == "Create user":
            print(Fore.CYAN + "\n=== Create User ===" + Style.RESET_ALL)
            full_name = questionary.text("Full name:").ask()
            email = questionary.text("Email:").ask()
            password = questionary.password("Password:").ask()
            role_choice = questionary.select(
                "Select role:",
                choices=["commercial", "support", "management"]
            ).ask()
            role = EnumRole(role_choice)
            
            create_user_service(
                full_name=full_name,
                email=email,
                password=password,
                role=role,
                token=token
            )
        
        # LIST USERS
        elif choice == "List users":
            print(Fore.CYAN + "\n=== Users List ===" + Style.RESET_ALL)
            users = get_all_users_service(token)
            if not users:
                print(Fore.YELLOW + "No users found." + Style.RESET_ALL)
            else:
                for u in users:
                    print(
                        Fore.GREEN +
                        f"[ID {u.id}] {u.full_name} | {u.email} | Role: {u.role}"
                        + Style.RESET_ALL
                    )
        
        # UPDATE USER
        elif choice == "Update user":
            print(Fore.CYAN + "\n=== Update User ===" + Style.RESET_ALL)
            users = get_all_users_service(token)
            if not users:
                print(Fore.YELLOW + "No users available." + Style.RESET_ALL)
                continue
            
            user_choices = [f"{u.id} - {u.full_name} ({u.role})" for u in users]
            user_choices.append("Cancel")
            
            user_choice = questionary.select(
                "Select user to update:",
                choices=user_choices
            ).ask()
            
            if user_choice == "Cancel":
                print(Fore.YELLOW + "Update cancelled." + Style.RESET_ALL)
                continue
            
            user_id = int(user_choice.split(" - ")[0])
            
            full_name = questionary.text("New full name (leave empty to skip):").ask()
            email = questionary.text("New email (leave empty to skip):").ask()
            password = questionary.password("New password (leave empty to skip):").ask()
            role_choice = questionary.select(
                "New role:",
                choices=["skip", "commercial", "support", "management"]
            ).ask()
            
            role = EnumRole(role_choice) if role_choice != "skip" else None
            
            update_user_service(
                user_id=user_id,
                full_name=full_name or None,
                email=email or None,
                password=password or None,
                role=role,
                token=token
            )
        
        # DELETE USER
        elif choice == "Delete user":
            print(Fore.CYAN + "\n=== Delete User ===" + Style.RESET_ALL)
            users = get_all_users_service(token)
            if not users:
                print(Fore.YELLOW + "No users available." + Style.RESET_ALL)
                continue
            
            user_choices = [f"{u.id} - {u.full_name} ({u.role})" for u in users]
            user_choices.append("Cancel")
            
            user_choice = questionary.select(
                "Select user to delete:",
                choices=user_choices
            ).ask()
            
            if user_choice == "Cancel":
                print(Fore.YELLOW + "Deletion cancelled." + Style.RESET_ALL)
                continue
            
            user_id = int(user_choice.split(" - ")[0])
            
            confirm = questionary.confirm("Are you sure you want to delete this user?").ask()
            if confirm:
                delete_user_service(user_id, token)
            else:
                print(Fore.YELLOW + "Deletion cancelled." + Style.RESET_ALL)
        
        elif choice == "Back":
            break
