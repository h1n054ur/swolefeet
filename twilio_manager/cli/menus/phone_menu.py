from twilio_manager.cli.menus.base_menu import BaseMenu
from twilio_manager.shared.constants import MENU_TITLES
from twilio_manager.cli.menus.search.search_menu import SearchMenu
from twilio_manager.cli.menus.purchase_menu import PurchaseMenu
from twilio_manager.cli.menus.configure_menu import ConfigureMenu
from twilio_manager.cli.menus.release_menu import ReleaseMenu

class PhoneMenu(BaseMenu):
    def __init__(self, parent=None):
        """Initialize phone menu.
        
        Args:
            parent (BaseMenu, optional): Parent menu to return to
        """
        super().__init__(parent)

    def show(self):
        """Display the phone number management menu."""
        title, emoji = MENU_TITLES["phone"]
        self.display(title, emoji, {
            "1": "🔍 Search Available Numbers",
            "2": "🛒 Purchase a Number",
            "3": "⚙️  Configure a Number",
            "4": "🗑 Release a Number",
            "0": "🔙 Back"
        })

    def handle_choice(self, choice):
        """Handle the user's menu choice.
        
        Args:
            choice (str): The user's selected option
        """
        if choice == "1":
            SearchMenu(parent=self).show()
        elif choice == "2":
            PurchaseMenu(parent=self).show()
        elif choice == "3":
            ConfigureMenu(parent=self).show()
        elif choice == "4":
            ReleaseMenu(parent=self).show()
