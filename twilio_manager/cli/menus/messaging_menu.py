from twilio_manager.cli.menus.base_menu import BaseMenu, with_loading
from twilio_manager.cli.commands.send_message_command import handle_send_message_command
from twilio_manager.cli.commands.view_logs_command import handle_view_message_logs_command

class MessagingMenu(BaseMenu):
    def __init__(self):
        super().__init__("📨 Messaging Management", "Messaging Menu")
        
        # Add menu options
        self.add_option("1", "Send a Message", self.send_message, "message")
        self.add_option("2", "View Message Logs", self.view_logs, "message")
        self.add_back_option()

    @with_loading("Sending message...")
    def send_message(self):
        handle_send_message_command()
        return True

    @with_loading("Loading message logs...")
    def view_logs(self):
        handle_view_message_logs_command()
        return True

def show_messaging_menu():
    menu = MessagingMenu()
    menu.show()
