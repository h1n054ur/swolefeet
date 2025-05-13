from twilio_manager.cli.menus.base_menu import BaseMenu
from twilio_manager.shared.ui.styling import console
from twilio_manager.cli.menus.phone_menu import PhoneMenu
from twilio_manager.cli.menus.messaging_menu import MessagingMenu
from twilio_manager.cli.menus.voice_menu import VoiceMenu
from twilio_manager.cli.menus.account_menu import AccountMenu
from twilio_manager.cli.menus.advanced_menu import AdvancedMenu

class MainMenu(BaseMenu):
    def show(self):
        """Display the main menu."""
        self.display("Twilio CLI Manager", "📘", {
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
            console.print("\n[green]Goodbye![/green]")
