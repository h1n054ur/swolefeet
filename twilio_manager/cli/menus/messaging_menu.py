from twilio_manager.cli.menus.base_menu import BaseMenu
from twilio_manager.cli.commands.send_message_command import handle_send_message_command
from twilio_manager.cli.commands.view_logs_command import handle_view_message_logs_command
# from cli.commands.delete_message_command import handle_delete_message_command  # Optional

class MessagingMenu(BaseMenu):
    def __init__(self):
        super().__init__("📨 Messaging Management", "Messaging Menu")

    def _setup_options(self):
        self.add_option("1", "Send a Message", handle_send_message_command, "✉️")
        self.add_option("2", "View Message Logs", handle_view_message_logs_command, "📄")
        # self.add_option("3", "Delete a Message", handle_delete_message_command, "🗑")  # Optional
        self.add_option("0", "Back", True, "🔙")

def show_messaging_menu():
    menu = MessagingMenu()
    menu.show()
