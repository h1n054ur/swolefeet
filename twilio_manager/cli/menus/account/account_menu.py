from twilio_manager.cli.menus.base_menu import BaseMenu
from twilio_manager.shared.ui.styling import (
    console,
    print_panel,
    prompt_choice,
    STYLES
)
from twilio_manager.cli.menus.account.account_info_menu import AccountInfoMenu
from twilio_manager.cli.menus.account.subaccount_menu import SubaccountMenu
from twilio_manager.cli.menus.account.api_key_menu import ApiKeyMenu
from twilio_manager.cli.menus.account.sip_trunk_menu import SipTrunkMenu
from twilio_manager.cli.menus.account.twiml_app_menu import TwimlAppMenu

class AccountMenu(BaseMenu):
    def show(self):
        """Display account management menu."""
        while True:
            print_panel("Account Management", style='highlight')
            console.print("1. View Account Info", style=STYLES['data'])
            console.print("2. Manage Subaccounts", style=STYLES['data'])
            console.print("3. Manage API Keys", style=STYLES['data'])
            console.print("4. Manage SIP Trunks", style=STYLES['data'])
            console.print("5. Manage TwiML Apps", style=STYLES['data'])
            console.print("0. Return to Main Menu", style=STYLES['data'])

            choice = prompt_choice("\nSelect an option", choices=["0", "1", "2", "3", "4", "5"])

            if choice == "0":
                break
            elif choice == "1":
                AccountInfoMenu().show()
            elif choice == "2":
                SubaccountMenu().show()
            elif choice == "3":
                ApiKeyMenu().show()
            elif choice == "4":
                SipTrunkMenu().show()
            elif choice == "5":
                TwimlAppMenu().show()