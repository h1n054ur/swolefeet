from twilio_manager.cli.menus.base_menu import SubMenu
from twilio_manager.cli.commands.search_command import handle_search_command
from twilio_manager.cli.commands.purchase_command import handle_purchase_command
from twilio_manager.cli.commands.configure_command import handle_configure_command
from twilio_manager.cli.commands.release_command import handle_release_command

class PhoneMenu(SubMenu):
    def __init__(self):
        super().__init__("Phone Number Management", "📞")
        self.add_option("1", "Search Available Numbers", lambda: handle_search_command() or False, "🔍")
        self.add_option("2", "Purchase a Number", lambda: handle_purchase_command() or False, "🛒")
        self.add_option("3", "Configure a Number", lambda: handle_configure_command() or False, "⚙️")
        self.add_option("4", "Release a Number", lambda: handle_release_command() or False, "🗑")

def show_phone_menu():
    PhoneMenu().show()
