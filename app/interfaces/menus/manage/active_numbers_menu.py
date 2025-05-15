"""Menu for listing and selecting active phone numbers."""

import logging
from typing import Dict, Callable, List
from rich.table import Table
from ..base_menu import BaseMenu
from ....services.number_service import NumberService
from ....models.phone_number_model import NumberRecord
from .number_actions_menu import NumberActionsMenu

logger = logging.getLogger(__name__)

class ActiveNumbersMenu(BaseMenu):
    """Menu for listing and selecting active phone numbers."""
    
    def __init__(self, parent: BaseMenu = None):
        """Initialize the menu.
        
        Args:
            parent: Optional parent menu for navigation.
        """
        super().__init__(parent)
        self.number_service = NumberService()
        self.numbers: List[NumberRecord] = []
        
    def show(self) -> None:
        """Display the active numbers menu."""
        self.clear_screen()
        self.render_header("Active Phone Numbers")
        
        try:
            # Fetch active numbers
            self.numbers = self.number_service.list_active_numbers()
            
            if not self.numbers:
                self.console.print("[yellow]No active numbers found![/yellow]")
                return
            
            # Display numbers in a table
            table = Table(show_header=True, header_style="bold blue")
            table.add_column("#", style="dim")
            table.add_column("Phone Number")
            table.add_column("Friendly Name")
            table.add_column("Region")
            table.add_column("Type")
            
            for i, number in enumerate(self.numbers, 1):
                table.add_row(
                    str(i),
                    number.number,
                    number.friendly_name or "-",
                    f"{number.country} - {number.region}",
                    number.type
                )
            
            self.console.print(table)
            self.console.print("\nSelect a number to manage or 'b' to go back.")
            
            # Build options dict
            options: Dict[str, Callable] = {
                str(i): lambda n=number: self.manage_number(n)
                for i, number in enumerate(self.numbers, 1)
            }
            
            while self.prompt_choice(options):
                self.clear_screen()
                self.render_header("Active Phone Numbers")
                self.console.print(table)
                
        except Exception as e:
            logger.exception("Error listing active numbers")
            self.console.print(f"[red]Error: {str(e)}[/red]")
    
    def manage_number(self, number: NumberRecord) -> bool:
        """Open the actions menu for a specific number.
        
        Args:
            number: The number to manage.
            
        Returns:
            True to continue the menu loop, False to exit.
        """
        menu = NumberActionsMenu(number, parent=self)
        menu.show()
        return True