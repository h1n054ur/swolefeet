from twilio_manager.cli.menus.base_menu import BaseMenu
from twilio_manager.cli.commands.manage_account_command import (
    handle_sip_trunk_menu,
    handle_twiml_app_menu
)

class AdvancedMenu(BaseMenu):
    def get_title(self):
        return "🧠 Advanced Voice Features"

    def get_menu_name(self):
        return "Advanced Menu"

    def get_options(self):
        return [
            ("1", "SIP Trunks", "🔌"),
            ("2", "TwiML Applications", "🧠"),
            # ("3", "Inbound Call Settings", "📥"),  # Optional
            ("0", "Back", "🔙")
        ]

    def handle_choice(self, choice):
        if choice == "1":
            handle_sip_trunk_menu()
        elif choice == "2":
            handle_twiml_app_menu()
        # elif choice == "3":
        #     handle_inbound_settings_menu()
        elif choice == "0":
            return True
        return False

def show_advanced_menu():
    AdvancedMenu().show()
