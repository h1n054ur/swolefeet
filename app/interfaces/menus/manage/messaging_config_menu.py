"""Menu for configuring messaging settings."""

import logging
from typing import Dict, Callable, Optional
from rich.table import Table
from ..base_menu import BaseMenu
from ....models.phone_number_model import NumberRecord
from ....services.number_service import NumberService
from ....services.messaging_service import MessagingService

logger = logging.getLogger(__name__)

class MessagingConfigMenu(BaseMenu):
    """Menu for configuring messaging settings."""
    
    def __init__(self, number: NumberRecord, parent: BaseMenu = None):
        """Initialize the menu.
        
        Args:
            number: The phone number to configure.
            parent: Optional parent menu for navigation.
        """
        super().__init__(parent)
        self.number = number
        self.number_service = NumberService()
        self.messaging_service = MessagingService()
    
    def show(self) -> None:
        """Display the messaging configuration menu."""
        self.clear_screen()
        self.render_header(f"Messaging Configuration - {self.number.number}")
        
        options: Dict[str, Callable] = {
            '1': self.configure_webhook,
            '2': self.select_messaging_service,
            '3': self.clear_config
        }
        
        while self.prompt_choice(options):
            self.clear_screen()
            self.render_header(f"Messaging Configuration - {self.number.number}")
    
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
                sms_url=url,
                sms_method=method,
                messaging_service_sid=None  # Clear service when setting webhook
            )
            self.console.print("[green]Messaging webhook updated successfully![/green]")
            return True
            
        except Exception as e:
            logger.exception("Error updating messaging webhook")
            self.console.print(f"[red]Error: {str(e)}[/red]")
            return True
    
    def select_messaging_service(self) -> bool:
        """Select a messaging service.
        
        Returns:
            True to continue menu loop.
        """
        try:
            # Get available services
            services = self.messaging_service.list_services()
            
            if not services:
                self.console.print("[yellow]No messaging services found![/yellow]")
                return True
            
            # Display services
            table = Table(show_header=True, header_style="bold blue")
            table.add_column("#")
            table.add_column("SID")
            table.add_column("Name")
            table.add_column("Status")
            
            for i, service in enumerate(services, 1):
                table.add_row(
                    str(i),
                    service.sid,
                    service.friendly_name,
                    service.status
                )
            
            self.console.print(table)
            
            # Get selection
            choice = self.prompt_input(
                "\nSelect service number (empty to cancel): ",
                lambda x: not x or x.isdigit() and 1 <= int(x) <= len(services)
            )
            
            if not choice:
                return True
            
            # Update number
            service = services[int(choice) - 1]
            self.number = self.number_service.update_number(
                self.number.number,
                messaging_service_sid=service.sid,
                sms_url=None,  # Clear webhook when setting service
                sms_method=None
            )
            
            self.console.print("[green]Messaging service updated successfully![/green]")
            return True
            
        except Exception as e:
            logger.exception("Error selecting messaging service")
            self.console.print(f"[red]Error: {str(e)}[/red]")
            return True
    
    def clear_config(self) -> bool:
        """Clear all messaging configuration.
        
        Returns:
            True to continue menu loop.
        """
        try:
            self.number = self.number_service.update_number(
                self.number.number,
                sms_url=None,
                sms_method=None,
                messaging_service_sid=None
            )
            self.console.print("[green]Messaging configuration cleared successfully![/green]")
            return True
            
        except Exception as e:
            logger.exception("Error clearing messaging configuration")
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