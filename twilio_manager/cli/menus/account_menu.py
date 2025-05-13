from twilio_manager.cli.menus.base_menu import BaseMenu
from twilio_manager.cli.commands.manage_account_command import (
    handle_view_account_info,
    handle_subaccount_management,
    handle_api_key_management
)

class AccountMenu(BaseMenu):
    def get_title(self):
        return "🧾 Account Management"

    def get_menu_name(self):
        return "Account Menu"

    def get_options(self):
        return [
            ("1", "View Account Info / Balance", "👤"),
            ("2", "Manage Subaccounts", "👥"),
            ("3", "Manage API Keys", "🔑"),
            ("0", "Back", "🔙")
        ]

    def handle_choice(self, choice):
        if choice == "1":
            handle_view_account_info()
        elif choice == "2":
            handle_subaccount_management()
        elif choice == "3":
            handle_api_key_management()
        elif choice == "0":
            return True
        return False

def show_account_menu():
    AccountMenu().show()
