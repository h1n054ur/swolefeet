from twilio_manager.cli.menus.base_menu import BaseMenu
from twilio_manager.cli.menus.phone_menu import show_phone_menu
from twilio_manager.cli.menus.messaging_menu import show_messaging_menu
from twilio_manager.cli.menus.voice_menu import show_voice_menu
from twilio_manager.cli.menus.account_menu import show_account_menu
from twilio_manager.cli.menus.advanced_menu import show_advanced_menu

class MainMenu(BaseMenu):
    def __init__(self):
        super().__init__("📘 Twilio CLI Manager", "Main Menu")

    def _setup_options(self):
        self.add_option("1", "Phone Numbers", show_phone_menu, "📞")
        self.add_option("2", "Messaging", show_messaging_menu, "📨")
        self.add_option("3", "Voice", show_voice_menu, "📞")
        self.add_option("4", "Account", show_account_menu, "🧾")
        self.add_option("5", "Advanced Features", show_advanced_menu, "🧠")
        self.add_option("0", "Exit", self._exit_handler, "❌")

    def _exit_handler(self):
        self.console.print("\n[green]Goodbye![/green]")
        return False

def show_main_menu():
    menu = MainMenu()
    menu.show()
