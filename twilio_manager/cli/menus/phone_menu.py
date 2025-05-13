from twilio_manager.cli.menus.base_menu import BaseMenu
from twilio_manager.cli.commands.search_command import handle_search_command
from twilio_manager.cli.commands.purchase_command import handle_purchase_command
from twilio_manager.cli.commands.configure_command import handle_configure_command
from twilio_manager.cli.commands.release_command import handle_release_command

class PhoneMenu(BaseMenu):
    def get_title(self):
        return "📞 Phone Number Management"

    def get_menu_name(self):
        return "Phone Menu"

    def get_options(self):
        return [
            ("1", "Search Available Numbers", "🔍"),
            ("2", "Purchase a Number", "🛒"),
            ("3", "Configure a Number", "⚙️"),
            ("4", "Release a Number", "🗑"),
            ("0", "Back", "🔙")
        ]

    def handle_choice(self, choice):
        if choice == "1":
            handle_search_command()
        elif choice == "2":
            handle_purchase_command()
        elif choice == "3":
            handle_configure_command()
        elif choice == "4":
            handle_release_command()
        elif choice == "0":
            return True
        return False

def show_phone_menu():
    PhoneMenu().show()
