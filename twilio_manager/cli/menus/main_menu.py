from twilio_manager.cli.menus.base_menu import BaseMenu, with_loading
from twilio_manager.cli.menus.phone_menu import show_phone_menu
from twilio_manager.cli.menus.messaging_menu import show_messaging_menu
from twilio_manager.cli.menus.voice_menu import show_voice_menu
from twilio_manager.cli.menus.account_menu import show_account_menu
from twilio_manager.cli.menus.advanced_menu import show_advanced_menu

class MainMenu(BaseMenu):
    def __init__(self):
        super().__init__("📘 Twilio CLI Manager", "Main Menu")
        
        # Add menu options
        self.add_option("1", "Phone Numbers", self.show_phone_menu, "phone")
        self.add_option("2", "Messaging", self.show_messaging_menu, "message")
        self.add_option("3", "Voice", self.show_voice_menu, "voice")
        self.add_option("4", "Account", self.show_account_menu, "account")
        self.add_option("5", "Advanced Features", self.show_advanced_menu, "advanced")
        self.add_option("0", "Exit", self.exit_app, "exit")

    def show_phone_menu(self):
        show_phone_menu()
        return True

    def show_messaging_menu(self):
        show_messaging_menu()
        return True

    def show_voice_menu(self):
        show_voice_menu()
        return True

    def show_account_menu(self):
        show_account_menu()
        return True

    def show_advanced_menu(self):
        show_advanced_menu()
        return True

    def exit_app(self):
        self.console.print("\n[success]Goodbye![/success]")
        return False

def show_main_menu():
    menu = MainMenu()
    menu.show()
