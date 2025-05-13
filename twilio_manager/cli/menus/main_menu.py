from twilio_manager.cli.menus.base_menu import BaseMenu
from twilio_manager.cli.menus.phone_menu import show_phone_menu
from twilio_manager.cli.menus.messaging_menu import show_messaging_menu
from twilio_manager.cli.menus.voice_menu import show_voice_menu
from twilio_manager.cli.menus.account_menu import show_account_menu
from twilio_manager.cli.menus.advanced_menu import show_advanced_menu

class MainMenu(BaseMenu):
    def __init__(self):
        super().__init__("Twilio CLI Manager", "📘")
        self.add_option("1", "Phone Numbers", lambda: show_phone_menu() or False, "📞")
        self.add_option("2", "Messaging", lambda: show_messaging_menu() or False, "📨")
        self.add_option("3", "Voice", lambda: show_voice_menu() or False, "📞")
        self.add_option("4", "Account", lambda: show_account_menu() or False, "🧾")
        self.add_option("5", "Advanced Features", lambda: show_advanced_menu() or False, "🧠")
        self.add_option("0", "Exit", self.handle_exit, "❌")

    def handle_exit(self) -> bool:
        self.console.print("\n[green]Goodbye![/green]")
        return True

def show_main_menu():
    MainMenu().show()
