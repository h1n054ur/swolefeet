"""Menu for configuring voice settings."""

import logging
from typing import Dict, Callable, Optional
from rich.table import Table
from ..base_menu import BaseMenu
from ....models.phone_number_model import NumberRecord
from ....services.number_service import NumberService
from ....services.voice_service import VoiceService

logger = logging.getLogger(__name__)

class VoiceConfigMenu(BaseMenu):
    """Menu for configuring voice settings."""
    
    def __init__(self, number: NumberRecord, parent: BaseMenu = None):
        """Initialize the menu.
        
        Args:
            number: The phone number to configure.
            parent: Optional parent menu for navigation.
        """
        super().__init__(parent)
        self.number = number
        self.number_service = NumberService()
        self.voice_service = VoiceService()
    
    def show(self) -> None:
        """Display the voice configuration menu."""
        self.clear_screen()
        self.render_header(f"Voice Configuration - {self.number.number}")
        
        options: Dict[str, Callable] = {
            '1': self.configure_webhook,
            '2': self.select_application,
            '3': self.select_sip_trunk,
            '4': self.clear_config
        }
        
        while self.prompt_choice(options):
            self.clear_screen()
            self.render_header(f"Voice Configuration - {self.number.number}")
    
    def configure_webhook(self) -> bool:
        """Configure webhook URL and method.
        
        Returns:
            True to continue menu loop.
        """
        url = self.prompt_input(
            "\nEnter webhook URL (empty to skip): ",
            self.validate_url
        )
        
        if not url:
            return True
        
        method = self.prompt_input(
            "Enter HTTP method (GET/POST): ",
            lambda x: x.upper() in ['GET', 'POST']
        ).upper()
        
        try:
            self.number = self.number_service.update_number(
                self.number.number,
                voice_url=url,
                voice_method=method,
                voice_application_sid=None  # Clear application when setting webhook
            )
            self.console.print("[green]Voice webhook updated successfully![/green]")
            return True
            
        except Exception as e:
            logger.exception("Error updating voice webhook")
            self.console.print(f"[red]Error: {str(e)}[/red]")
            return True
    
    def select_application(self) -> bool:
        """Select a TwiML application.
        
        Returns:
            True to continue menu loop.
        """
        try:
            # Get available applications
            applications = self.voice_service.list_applications()
            
            if not applications:
                self.console.print("[yellow]No TwiML applications found![/yellow]")
                return True
            
            # Display applications
            table = Table(show_header=True, header_style="bold blue")
            table.add_column("#")
            table.add_column("SID")
            table.add_column("Name")
            table.add_column("Voice URL")
            
            for i, app in enumerate(applications, 1):
                table.add_row(
                    str(i),
                    app.sid,
                    app.friendly_name,
                    app.voice_url or '-'
                )
            
            self.console.print(table)
            
            # Get selection
            choice = self.prompt_input(
                "\nSelect application number (empty to cancel): ",
                lambda x: not x or x.isdigit() and 1 <= int(x) <= len(applications)
            )
            
            if not choice:
                return True
            
            # Update number
            app = applications[int(choice) - 1]
            self.number = self.number_service.update_number(
                self.number.number,
                voice_application_sid=app.sid,
                voice_url=None,  # Clear webhook when setting application
                voice_method=None
            )
            
            self.console.print("[green]Voice application updated successfully![/green]")
            return True
            
        except Exception as e:
            logger.exception("Error selecting voice application")
            self.console.print(f"[red]Error: {str(e)}[/red]")
            return True
    
    def select_sip_trunk(self) -> bool:
        """Select a SIP trunk.
        
        Returns:
            True to continue menu loop.
        """
        try:
            # Get available trunks
            trunks = self.voice_service.list_sip_trunks()
            
            if not trunks:
                self.console.print("[yellow]No SIP trunks found![/yellow]")
                return True
            
            # Display trunks
            table = Table(show_header=True, header_style="bold blue")
            table.add_column("#")
            table.add_column("SID")
            table.add_column("Name")
            table.add_column("Domain")
            
            for i, trunk in enumerate(trunks, 1):
                table.add_row(
                    str(i),
                    trunk.sid,
                    trunk.friendly_name,
                    trunk.domain_name
                )
            
            self.console.print(table)
            
            # Get selection
            choice = self.prompt_input(
                "\nSelect trunk number (empty to cancel): ",
                lambda x: not x or x.isdigit() and 1 <= int(x) <= len(trunks)
            )
            
            if not choice:
                return True
            
            # Update number
            trunk = trunks[int(choice) - 1]
            self.number = self.number_service.update_number(
                self.number.number,
                voice_application_sid=trunk.sid,
                voice_url=None,  # Clear webhook when setting trunk
                voice_method=None
            )
            
            self.console.print("[green]SIP trunk updated successfully![/green]")
            return True
            
        except Exception as e:
            logger.exception("Error selecting SIP trunk")
            self.console.print(f"[red]Error: {str(e)}[/red]")
            return True
    
    def clear_config(self) -> bool:
        """Clear all voice configuration.
        
        Returns:
            True to continue menu loop.
        """
        try:
            self.number = self.number_service.update_number(
                self.number.number,
                voice_url=None,
                voice_method=None,
                voice_application_sid=None
            )
            self.console.print("[green]Voice configuration cleared successfully![/green]")
            return True
            
        except Exception as e:
            logger.exception("Error clearing voice configuration")
            self.console.print(f"[red]Error: {str(e)}[/red]")
            return True
    
    def validate_url(self, url: str) -> bool:
        """Validate webhook URL format.
        
        Args:
            url: URL to validate.
            
        Returns:
            True if valid, False otherwise.
        """
        if not url:
            return True
        return url.startswith(('http://', 'https://'))