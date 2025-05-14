from twilio_manager.cli.menus.base_menu import BaseMenu
from twilio_manager.shared.constants import MENU_TITLES
from twilio_manager.cli.menus.send_message_menu import SendMessageMenu
from twilio_manager.cli.menus.view_message_logs_menu import ViewMessageLogsMenu

class MessagingMenu(BaseMenu):
    def show(self):
        """Display the messaging management menu."""
        title, emoji = MENU_TITLES["messaging"]
        self.display(title, emoji, {
            "1": "✉️ Send a Message",
            "2": "📄 View Message Logs",
            "0": "🔙 Back"
        })

    def handle_choice(self, choice):
        """Handle the user's menu choice.
        
        Args:
            choice (str): The user's selected option
        """
        if choice == "1":
            SendMessageMenu().show()
        elif choice == "2":
            ViewMessageLogsMenu().show()
