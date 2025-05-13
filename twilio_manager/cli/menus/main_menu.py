from twilio_manager.cli.menus.base_menu import BaseMenu
from twilio_manager.shared.ui.styling import console
from twilio_manager.shared.constants import MENU_TITLES, APP_TITLE, APP_EMOJI
from twilio_manager.cli.menus.phone_menu import PhoneMenu
from twilio_manager.cli.menus.messaging_menu import MessagingMenu
from twilio_manager.cli.menus.voice_menu import VoiceMenu
from twilio_manager.cli.menus.account_menu import AccountMenu
from twilio_manager.cli.menus.advanced_menu import AdvancedMenu

class MainMenu(BaseMenu):
    def __init__(self, parent=None):
        """Initialize main menu.
        
        Args:
            parent (BaseMenu, optional): Parent menu to return to
        """
        super().__init__(parent)

    def show(self):
        """Display the main menu."""
        self.display(APP_TITLE, APP_EMOJI, {
            "1": "📞 Phone Numbers",
            "2": "📨 Messaging",
            "3": "📞 Voice",
            "4": "🧾 Account",
            "5": "🧠 Advanced Features",
            "0": "❌ Exit"
        })

    def handle_choice(self, choice):
        """Handle the user's menu choice.
        
        Args:
            choice (str): The user's selected option
        """
        if choice == "1":
            PhoneMenu(parent=self).show()
        elif choice == "2":
            MessagingMenu(parent=self).show()
        elif choice == "3":
            VoiceMenu(parent=self).show()
        elif choice == "4":
            AccountMenu(parent=self).show()
        elif choice == "5":
            AdvancedMenu(parent=self).show()
        elif choice == "0":
            self.clear()
            console.print("\n[green]Goodbye![/green]")
            exit(0)  # Only use exit() in main menu
