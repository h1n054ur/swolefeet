from twilio_manager.cli.menus.base_menu import BaseMenu
from twilio_manager.cli.commands.manage_account_command import (
    handle_sip_trunk_menu,
    handle_twiml_app_menu
)

class AdvancedMenu(BaseMenu):
    def __init__(self):
        super().__init__("🧠 Advanced Voice Features", "Advanced Menu")

    def _setup_options(self):
        self.add_option("1", "SIP Trunks", handle_sip_trunk_menu, "🔌")
        self.add_option("2", "TwiML Applications", handle_twiml_app_menu, "🧠")
        # self.add_option("3", "Inbound Call Settings", handle_inbound_settings_menu, "📥")  # Optional
        self.add_option("0", "Back", True, "🔙")

def show_advanced_menu():
    menu = AdvancedMenu()
    menu.show()
