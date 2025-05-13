from twilio_manager.cli.menus.base_menu import BaseMenu, with_loading
from twilio_manager.cli.commands.manage_account_command import (
    handle_sip_trunk_menu,
    handle_twiml_app_menu
)

class AdvancedMenu(BaseMenu):
    def __init__(self):
        super().__init__("🧠 Advanced Voice Features", "Advanced Menu")
        
        # Add menu options
        self.add_option("1", "SIP Trunks", self.manage_sip_trunks, "advanced")
        self.add_option("2", "TwiML Applications", self.manage_twiml_apps, "advanced")
        self.add_back_option()

    @with_loading("Loading SIP trunk management...")
    def manage_sip_trunks(self):
        handle_sip_trunk_menu()
        return True

    @with_loading("Loading TwiML application management...")
    def manage_twiml_apps(self):
        handle_twiml_app_menu()
        return True

def show_advanced_menu():
    menu = AdvancedMenu()
    menu.show()
# Placeholder for advanced_menu.py
