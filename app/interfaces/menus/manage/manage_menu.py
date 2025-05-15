"""Menu for managing existing phone numbers."""

import logging
from typing import Dict, Callable
from ..base_menu import BaseMenu
from .active_numbers_menu import ActiveNumbersMenu

logger = logging.getLogger(__name__)

class ManageMenu(BaseMenu):
    """Menu for managing existing phone numbers."""
    
    def show(self) -> None:
        """Display the management menu."""
        self.clear_screen()
        self.render_header("Manage Phone Numbers")
        
        options: Dict[str, Callable] = {
            '1': self.list_active_numbers,
            '2': self.search_numbers,
            '3': self.view_logs
        }
        
        while self.prompt_choice(options):
            self.clear_screen()
            self.render_header("Manage Phone Numbers")
    
    def list_active_numbers(self) -> bool:
        """List and manage active phone numbers."""
        menu = ActiveNumbersMenu(parent=self)
        menu.show()
        return True
    
    def search_numbers(self) -> bool:
        """Search through phone numbers."""
        self.console.print("[yellow]Search functionality coming soon![/yellow]")
        return True
    
    def view_logs(self) -> bool:
        """View global logs for all numbers."""
        self.console.print("[yellow]Global log viewer coming soon![/yellow]")
        return True