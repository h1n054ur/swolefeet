"""Main menu implementation."""

import logging
from typing import Dict, Callable
from .base_menu import BaseMenu

logger = logging.getLogger(__name__)

class MainMenu(BaseMenu):
    """Main menu of the application."""
    
    def show(self) -> None:
        """Display the main menu."""
        self.clear_screen()
        self.render_header("Twilio Manager CLI")
        
        options: Dict[str, Callable] = {
            '1': self.purchase_numbers,
            '2': self.manage_numbers,
            '3': self.settings
        }
        
        while self.prompt_choice(options):
            self.clear_screen()
            self.render_header("Twilio Manager CLI")
    
    def purchase_numbers(self) -> bool:
        """Purchase new phone numbers."""
        from .purchase.purchase_menu import PurchaseMenu
        menu = PurchaseMenu(parent=self)
        menu.show()
        return True
    
    def manage_numbers(self) -> bool:
        """Manage existing phone numbers."""
        from .manage.manage_menu import ManageMenu
        menu = ManageMenu(parent=self)
        menu.show()
        return True
    
    def settings(self) -> bool:
        """Settings and administration."""
        from .settings.settings_menu import SettingsMenu
        menu = SettingsMenu(parent=self)
        menu.show()
        return True
