from twilio_manager.cli.menus.base_menu import BaseMenu
from twilio_manager.cli.commands.manage_account_command import (
    handle_sip_trunk_menu,
    handle_twiml_app_menu
)

class AdvancedMenu(BaseMenu):
    def show(self):
        """Display the advanced voice features menu."""
        self.display("Advanced Voice Features", "🧠", {
            "1": "🔌 SIP Trunks",
            "2": "🧠 TwiML Applications",
            # "3": "📥 Inbound Call Settings",  # Optional
            "0": "🔙 Back"
        })

    def handle_choice(self, choice):
        """Handle the user's menu choice.
        
        Args:
            choice (str): The user's selected option
        """
        if choice == "1":
            handle_sip_trunk_menu()
        elif choice == "2":
            handle_twiml_app_menu()
        # elif choice == "3":
        #     handle_inbound_settings_menu()
