"""Menu for releasing phone numbers."""

import logging
from typing import Dict, Callable
from ..base_menu import BaseMenu
from ....models.phone_number_model import NumberRecord
from ....services.number_service import NumberService

logger = logging.getLogger(__name__)

class ReleaseMenu(BaseMenu):
    """Menu for releasing phone numbers."""
    
    def __init__(self, number: NumberRecord, parent: BaseMenu = None):
        """Initialize the menu.
        
        Args:
            number: The phone number to release.
            parent: Optional parent menu for navigation.
        """
        super().__init__(parent)
        self.number = number
        self.number_service = NumberService()
    
    def show(self) -> None:
        """Display the release confirmation menu."""
        self.clear_screen()
        self.render_header(f"Release {self.number.number}")
        
        # Show warning
        self.console.print("\n[red]WARNING:[/red] This action cannot be undone!")
        self.console.print(
            "Releasing this number will:\n"
            "1. Remove all configurations\n"
            "2. Stop all active calls and messages\n"
            "3. Make the number available for others to purchase"
        )
        
        # Show number details
        self.console.print(f"\n[bold]Number:[/bold] {self.number.number}")
        self.console.print(f"[bold]Friendly Name:[/bold] {self.number.friendly_name or '-'}")
        self.console.print(f"[bold]Region:[/bold] {self.number.country} - {self.number.region}")
        
        # Get confirmation
        confirm = self.prompt_input(
            "\nType the number to confirm release: ",
            lambda x: x == self.number.number
        )
        
        if not confirm:
            return
        
        try:
            # Release the number
            self.number_service.release_number(self.number.number)
            self.console.print("\n[green]Number released successfully![/green]")
            
        except Exception as e:
            logger.exception("Error releasing number")
            self.console.print(f"[red]Error: {str(e)}[/red]")