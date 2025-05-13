from twilio_manager.cli.menus.base_menu import BaseMenu
from twilio_manager.cli.menus.phone_menu import PhoneMenu
from twilio_manager.cli.menus.messaging_menu import MessagingMenu
from twilio_manager.cli.menus.voice_menu import VoiceMenu
from twilio_manager.cli.menus.account_menu import AccountMenu
from twilio_manager.cli.menus.advanced_menu import AdvancedMenu

class MainMenu(BaseMenu):
    def get_title(self):
        return "📘 Twilio CLI Manager"

    def get_menu_name(self):
        return "Main Menu"

    def get_options(self):
        return [
            ("1", "Phone Numbers", "📞"),
            ("2", "Messaging", "📨"),
            ("3", "Voice", "📞"),
            ("4", "Account", "🧾"),
            ("5", "Advanced Features", "🧠"),
            ("0", "Exit", "❌")
        ]

    def handle_choice(self, choice):
        if choice == "1":
            PhoneMenu().show()
        elif choice == "2":
            MessagingMenu().show()
        elif choice == "3":
            VoiceMenu().show()
        elif choice == "4":
            AccountMenu().show()
        elif choice == "5":
            AdvancedMenu().show()
        elif choice == "0":
            self.show_success("Goodbye!")
            return True
        return False

def show_main_menu():
    MainMenu().show()
