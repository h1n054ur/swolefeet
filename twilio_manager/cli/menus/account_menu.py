from twilio_manager.cli.menus.base_menu import BaseMenu
from twilio_manager.cli.commands.manage_account_command import (
    handle_view_account_info,
    handle_subaccount_management,
    handle_api_key_management
)

class AccountMenu(BaseMenu):
    def __init__(self):
        super().__init__("🧾 Account Management", "Account Menu")

    def _setup_options(self):
        self.add_option("1", "View Account Info / Balance", handle_view_account_info, "👤")
        self.add_option("2", "Manage Subaccounts", handle_subaccount_management, "👥")
        self.add_option("3", "Manage API Keys", handle_api_key_management, "🔑")
        self.add_option("0", "Back", True, "🔙")

def show_account_menu():
    menu = AccountMenu()
    menu.show()
