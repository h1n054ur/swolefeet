from twilio_manager.cli.menus.base_menu import BaseMenu
from twilio_manager.shared.constants import MENU_TITLES
from twilio_manager.cli.commands.send_message_command import handle_send_message_command
from twilio_manager.cli.commands.view_logs_command import handle_view_message_logs_command
# from cli.commands.delete_message_command import handle_delete_message_command  # Optional

class MessagingMenu(BaseMenu):
    def show(self):
        """Display the messaging management menu."""
        title, emoji = MENU_TITLES["messaging"]
        self.display(title, emoji, {
            "1": "✉️ Send a Message",
            "2": "📄 View Message Logs",
            # "3": "🗑 Delete a Message",  # Optional
            "0": "🔙 Back"
        })

    def handle_choice(self, choice):
        """Handle the user's menu choice.
        
        Args:
            choice (str): The user's selected option
        """
        if choice == "1":
            handle_send_message_command()
        elif choice == "2":
            handle_view_message_logs_command()
        # elif choice == "3":
        #     handle_delete_message_command()
