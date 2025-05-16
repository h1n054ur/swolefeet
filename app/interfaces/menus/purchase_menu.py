"""Menu for purchasing new phone numbers."""

import logging
from typing import Dict, Callable
from .base_menu import BaseMenu

logger = logging.getLogger(__name__)

class PurchaseMenu(BaseMenu):
    """Menu for purchasing new phone numbers."""
    
    def show(self) -> None:
        """Display the purchase menu."""
        self.clear_screen()
        self.render_header("Purchase Phone Numbers")
        
        options: Dict[str, Callable] = {
            '1': self.search_numbers,
            '2': self.purchase_number,
            '3': self.bulk_purchase
        }
        
        while self.prompt_choice(options):
            self.clear_screen()
            self.render_header("Purchase Phone Numbers")
    
    def search_numbers(self) -> bool:
        """Search for available numbers."""
        self.console.print("[yellow]Search functionality coming soon![/yellow]")
        return True
    
    def purchase_number(self) -> bool:
        """Purchase a specific number."""
        self.console.print("[yellow]Purchase functionality coming soon![/yellow]")
        return True
    
    def bulk_purchase(self) -> bool:
        """Purchase multiple numbers at once."""
        self.console.print("[yellow]Bulk purchase functionality coming soon![/yellow]")
        return True