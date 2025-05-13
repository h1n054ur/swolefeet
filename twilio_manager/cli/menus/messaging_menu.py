from twilio_manager.cli.menus.base_menu import BaseMenu
from twilio_manager.cli.commands.send_message_command import handle_send_message_command
from twilio_manager.cli.commands.view_logs_command import handle_view_message_logs_command
# from cli.commands.delete_message_command import handle_delete_message_command  # Optional

class MessagingMenu(BaseMenu):
    def get_title(self):
        return "📨 Messaging Management"

    def get_menu_name(self):
        return "Messaging Menu"

    def get_options(self):
        return [
            ("1", "Send a Message", "✉️"),
            ("2", "View Message Logs", "📄"),
            # ("3", "Delete a Message", "🗑"),  # Optional
            ("0", "Back", "🔙")
        ]

    def handle_choice(self, choice):
        if choice == "1":
            handle_send_message_command()
        elif choice == "2":
            handle_view_message_logs_command()
        # elif choice == "3":
        #     handle_delete_message_command()
        elif choice == "0":
            return True
        return False

def show_messaging_menu():
    MessagingMenu().show()
