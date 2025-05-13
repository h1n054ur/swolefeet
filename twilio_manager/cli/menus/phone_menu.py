from twilio_manager.cli.menus.base_menu import BaseMenu
from twilio_manager.cli.commands.search_command import handle_search_command
from twilio_manager.cli.commands.purchase_command import handle_purchase_command
from twilio_manager.cli.commands.configure_command import handle_configure_command
from twilio_manager.cli.commands.release_command import handle_release_command

class PhoneMenu(BaseMenu):
    def __init__(self):
        super().__init__("📞 Phone Number Management", "Phone Menu")

    def _setup_options(self):
        self.add_option("1", "Search Available Numbers", handle_search_command, "🔍")
        self.add_option("2", "Purchase a Number", handle_purchase_command, "🛒")
        self.add_option("3", "Configure a Number", handle_configure_command, "⚙️")
        self.add_option("4", "Release a Number", handle_release_command, "🗑")
        self.add_option("0", "Back", True, "🔙")

def show_phone_menu():
    menu = PhoneMenu()
    menu.show()
