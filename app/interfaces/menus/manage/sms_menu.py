"""Menu for sending SMS messages."""

import logging
import re
from typing import Dict, Callable
from ..base_menu import BaseMenu
from ....models.phone_number_model import NumberRecord
from ....services.messaging_service import MessagingService

logger = logging.getLogger(__name__)

class SmsMenu(BaseMenu):
    """Menu for sending SMS messages."""
    
    def __init__(self, number: NumberRecord, parent: BaseMenu = None):
        """Initialize the menu.
        
        Args:
            number: The phone number to send from.
            parent: Optional parent menu for navigation.
        """
        super().__init__(parent)
        self.number = number
        self.messaging_service = MessagingService()
    
    def show(self) -> None:
        """Display the SMS menu."""
        self.clear_screen()
        self.render_header(f"Send SMS from {self.number.number}")
        
        # Get destination number
        dest = self.prompt_input(
            "Enter destination number (E.164 format): ",
            self.validate_phone_number
        )
        
        if not dest:
            return
        
        # Get message body
        body = self.prompt_input(
            "\nEnter message (max 1600 chars): ",
            lambda x: len(x) <= 1600 and len(x) > 0
        )
        
        if not body:
            return
        
        try:
            # Send the message
            message = self.messaging_service.send_sms(
                from_number=self.number.number,
                to_number=dest,
                body=body
            )
            
            self.console.print(f"\n[green]Message sent! SID: {message.sid}[/green]")
            self.console.print(f"Status: {message.status}")
            
            # Show options
            options: Dict[str, Callable] = {
                '1': lambda: self.refresh_status(message.sid)
            }
            
            while self.prompt_choice(options):
                self.clear_screen()
                self.render_header(f"Message to {dest}")
        
        except Exception as e:
            logger.exception("Error sending message")
            self.console.print(f"[red]Error: {str(e)}[/red]")
    
    def validate_phone_number(self, number: str) -> bool:
        """Validate E.164 phone number format.
        
        Args:
            number: Phone number to validate.
            
        Returns:
            True if valid, False otherwise.
        """
        pattern = r'^\+[1-9]\d{1,14}$'
        return bool(re.match(pattern, number))
    
    def refresh_status(self, message_sid: str) -> bool:
        """Refresh message status.
        
        Args:
            message_sid: The message SID to check.
            
        Returns:
            True to continue menu loop, False to exit.
        """
        try:
            message = self.messaging_service.get_message(message_sid)
            self.console.print(f"\nStatus: {message.status}")
            return True
        except Exception as e:
            logger.exception("Error refreshing message status")
            self.console.print(f"[red]Error: {str(e)}[/red]")
            return False