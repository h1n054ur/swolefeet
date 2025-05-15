"""Menu for configuring phone number settings."""

import logging
from typing import Dict, Callable
from ..base_menu import BaseMenu
from ....models.phone_number_model import NumberRecord
from ....services.number_service import NumberService
from .voice_config_menu import VoiceConfigMenu
from .messaging_config_menu import MessagingConfigMenu

logger = logging.getLogger(__name__)

class ConfigMenu(BaseMenu):
    """Menu for configuring phone number settings."""
    
    def __init__(self, number: NumberRecord, parent: BaseMenu = None):
        """Initialize the menu.
        
        Args:
            number: The phone number to configure.
            parent: Optional parent menu for navigation.
        """
        super().__init__(parent)
        self.number = number
        self.number_service = NumberService()
    
    def show(self) -> None:
        """Display the configuration menu."""
        self.clear_screen()
        self.render_header(f"Configure {self.number.number}")
        
        # Show current configuration
        self.display_current_config()
        
        options: Dict[str, Callable] = {
            '1': self.configure_voice,
            '2': self.configure_messaging,
            '3': self.set_friendly_name
        }
        
        while self.prompt_choice(options):
            self.clear_screen()
            self.render_header(f"Configure {self.number.number}")
            self.display_current_config()
    
    def display_current_config(self) -> None:
        """Display current number configuration."""
        self.console.print("\n[bold]Current Configuration:[/bold]")
        self.console.print(f"Friendly Name: {self.number.friendly_name or '-'}")
        
        if 'voice' in self.number.capabilities:
            self.console.print("\n[bold]Voice Configuration:[/bold]")
            self.console.print(f"Voice URL: {self.number.voice_url or '-'}")
            self.console.print(f"Voice Method: {self.number.voice_method or '-'}")
            self.console.print(f"Voice Application: {self.number.voice_application_sid or '-'}")
        
        if 'sms' in self.number.capabilities:
            self.console.print("\n[bold]Messaging Configuration:[/bold]")
            self.console.print(f"SMS URL: {self.number.sms_url or '-'}")
            self.console.print(f"SMS Method: {self.number.sms_method or '-'}")
            self.console.print(f"Messaging Service: {self.number.messaging_service_sid or '-'}")
    
    def configure_voice(self) -> bool:
        """Open voice configuration menu.
        
        Returns:
            True to continue menu loop.
        """
        if 'voice' not in self.number.capabilities:
            self.console.print("[red]This number does not support voice![/red]")
            return True
        
        menu = VoiceConfigMenu(self.number, parent=self)
        menu.show()
        
        # Refresh number data
        self.number = self.number_service.get_number(self.number.number)
        return True
    
    def configure_messaging(self) -> bool:
        """Open messaging configuration menu.
        
        Returns:
            True to continue menu loop.
        """
        if 'sms' not in self.number.capabilities:
            self.console.print("[red]This number does not support SMS![/red]")
            return True
        
        menu = MessagingConfigMenu(self.number, parent=self)
        menu.show()
        
        # Refresh number data
        self.number = self.number_service.get_number(self.number.number)
        return True
    
    def set_friendly_name(self) -> bool:
        """Set a friendly name for the number.
        
        Returns:
            True to continue menu loop.
        """
        name = self.prompt_input(
            "\nEnter friendly name (empty to clear): "
        )
        
        try:
            self.number = self.number_service.update_number(
                self.number.number,
                friendly_name=name or None
            )
            self.console.print("[green]Friendly name updated successfully![/green]")
            return True
            
        except Exception as e:
            logger.exception("Error updating friendly name")
            self.console.print(f"[red]Error: {str(e)}[/red]")
            return True