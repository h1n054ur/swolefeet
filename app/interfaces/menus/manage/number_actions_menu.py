"""Menu for actions on a specific phone number."""

import logging
from typing import Dict, Callable
from ..base_menu import BaseMenu
from ....models.phone_number_model import NumberRecord
from .call_menu import CallMenu
from .sms_menu import SmsMenu
from .logs_menu import LogsMenu
from .config_menu import ConfigMenu
from .release_menu import ReleaseMenu

logger = logging.getLogger(__name__)

class NumberActionsMenu(BaseMenu):
    """Menu for actions on a specific phone number."""
    
    def __init__(self, number: NumberRecord, parent: BaseMenu = None):
        """Initialize the menu.
        
        Args:
            number: The phone number to manage.
            parent: Optional parent menu for navigation.
        """
        super().__init__(parent)
        self.number = number
    
    def show(self) -> None:
        """Display the number actions menu."""
        self.clear_screen()
        self.render_header(f"Manage {self.number.number}")
        
        # Show current number info
        self.console.print(f"[bold]Friendly Name:[/bold] {self.number.friendly_name or '-'}")
        self.console.print(f"[bold]Region:[/bold] {self.number.country} - {self.number.region}")
        self.console.print(f"[bold]Type:[/bold] {self.number.type}")
        self.console.print(f"[bold]Capabilities:[/bold] {', '.join(self.number.capabilities)}\n")
        
        options: Dict[str, Callable] = {
            '1': self.make_call,
            '2': self.send_sms,
            '3': self.view_logs,
            '4': self.configure,
            '5': self.release
        }
        
        while self.prompt_choice(options):
            self.clear_screen()
            self.render_header(f"Manage {self.number.number}")
    
    def make_call(self) -> bool:
        """Open the call menu."""
        if 'voice' not in self.number.capabilities:
            self.console.print("[red]This number does not support voice calls![/red]")
            return True
        
        menu = CallMenu(self.number, parent=self)
        menu.show()
        return True
    
    def send_sms(self) -> bool:
        """Open the SMS menu."""
        if 'sms' not in self.number.capabilities:
            self.console.print("[red]This number does not support SMS![/red]")
            return True
        
        menu = SmsMenu(self.number, parent=self)
        menu.show()
        return True
    
    def view_logs(self) -> bool:
        """Open the logs menu."""
        menu = LogsMenu(self.number, parent=self)
        menu.show()
        return True
    
    def configure(self) -> bool:
        """Open the configuration menu."""
        menu = ConfigMenu(self.number, parent=self)
        menu.show()
        return True
    
    def release(self) -> bool:
        """Open the release confirmation menu."""
        menu = ReleaseMenu(self.number, parent=self)
        menu.show()
        return True