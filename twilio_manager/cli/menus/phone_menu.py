from twilio_manager.cli.menus.base_menu import BaseMenu, with_loading
from twilio_manager.cli.commands.search_command import handle_search_command
from twilio_manager.cli.commands.purchase_command import handle_purchase_command
from twilio_manager.cli.commands.configure_command import handle_configure_command
from twilio_manager.cli.commands.release_command import handle_release_command

class PhoneMenu(BaseMenu):
    def __init__(self):
        super().__init__("📞 Phone Number Management", "Phone Menu")
        
        # Add menu options
        self.add_option("1", "Search Available Numbers", self.search_numbers, "phone")
        self.add_option("2", "Purchase a Number", self.purchase_number, "phone")
        self.add_option("3", "Configure a Number", self.configure_number, "phone")
        self.add_option("4", "Release a Number", self.release_number, "phone")
        self.add_back_option()

    @with_loading("Searching for available numbers...")
    def search_numbers(self):
        handle_search_command()
        return True

    @with_loading("Processing purchase...")
    def purchase_number(self):
        handle_purchase_command()
        return True

    @with_loading("Loading configuration...")
    def configure_number(self):
        handle_configure_command()
        return True

    @with_loading("Processing number release...")
    def release_number(self):
        handle_release_command()
        return True

def show_phone_menu():
    menu = PhoneMenu()
    menu.show()
