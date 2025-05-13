from twilio_manager.cli.menus.base_menu import BaseMenu, with_loading
from twilio_manager.cli.commands.manage_account_command import (
    handle_view_account_info,
    handle_subaccount_management,
    handle_api_key_management
)

class AccountMenu(BaseMenu):
    def __init__(self):
        super().__init__("🧾 Account Management", "Account Menu")
        
        # Add menu options
        self.add_option("1", "View Account Info / Balance", self.view_account_info, "account")
        self.add_option("2", "Manage Subaccounts", self.manage_subaccounts, "account")
        self.add_option("3", "Manage API Keys", self.manage_api_keys, "account")
        self.add_back_option()

    @with_loading("Loading account information...")
    def view_account_info(self):
        handle_view_account_info()
        return True

    @with_loading("Loading subaccount management...")
    def manage_subaccounts(self):
        handle_subaccount_management()
        return True

    @with_loading("Loading API key management...")
    def manage_api_keys(self):
        handle_api_key_management()
        return True

def show_account_menu():
    menu = AccountMenu()
    menu.show()
# Placeholder for account_menu.py
