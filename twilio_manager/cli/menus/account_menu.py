from twilio_manager.cli.menus.base_menu import BaseMenu
from twilio_manager.shared.constants import MENU_TITLES
from twilio_manager.cli.commands.manage_account_command import (
    handle_view_account_info,
    handle_subaccount_management,
    handle_api_key_management
)

class AccountMenu(BaseMenu):
    def show(self):
        """Display the account management menu."""
        title, emoji = MENU_TITLES["account"]
        self.display(title, emoji, {
            "1": "👤 View Account Info / Balance",
            "2": "👥 Manage Subaccounts",
            "3": "🔑 Manage API Keys",
            "0": "🔙 Back"
        })

    def handle_choice(self, choice):
        """Handle the user's menu choice.
        
        Args:
            choice (str): The user's selected option
        """
        if choice == "1":
            handle_view_account_info()
        elif choice == "2":
            handle_subaccount_management()
        elif choice == "3":
            handle_api_key_management()
