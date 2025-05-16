"""Menu for making outbound calls."""

import logging
import re
from typing import Dict, Callable
from ..base_menu import BaseMenu
from ....models.phone_number_model import NumberRecord
from ....services.voice_service import VoiceService

logger = logging.getLogger(__name__)

class CallMenu(BaseMenu):
    """Menu for making outbound calls."""
    
    def __init__(self, number: NumberRecord, parent: BaseMenu = None):
        """Initialize the menu.
        
        Args:
            number: The phone number to call from.
            parent: Optional parent menu for navigation.
        """
        super().__init__(parent)
        self.number = number
        self.voice_service = VoiceService()
    
    def show(self) -> None:
        """Display the call menu."""
        self.clear_screen()
        self.render_header(f"Make Call from {self.number.number}")
        
        # Get destination number
        dest = self.prompt_input(
            "Enter destination number (E.164 format): ",
            self.validate_phone_number
        )
        
        if not dest:
            return
        
        try:
            # Make the call
            call = self.voice_service.make_call(
                from_number=self.number.number,
                to_number=dest
            )
            
            self.console.print(f"\n[green]Call initiated! SID: {call.sid}[/green]")
            self.console.print(f"Status: {call.status}")
            
            # Show options
            options: Dict[str, Callable] = {
                '1': lambda: self.refresh_call(call.sid),
                '2': lambda: self.cancel_call(call.sid)
            }
            
            while self.prompt_choice(options):
                self.clear_screen()
                self.render_header(f"Call to {dest}")
        
        except Exception as e:
            logger.exception("Error making call")
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
    
    def refresh_call(self, call_sid: str) -> bool:
        """Refresh call status.
        
        Args:
            call_sid: The call SID to check.
            
        Returns:
            True to continue menu loop, False to exit.
        """
        try:
            call = self.voice_service.get_call(call_sid)
            self.console.print(f"\nStatus: {call.status}")
            return True
        except Exception as e:
            logger.exception("Error refreshing call status")
            self.console.print(f"[red]Error: {str(e)}[/red]")
            return False
    
    def cancel_call(self, call_sid: str) -> bool:
        """Cancel an in-progress call.
        
        Args:
            call_sid: The call SID to cancel.
            
        Returns:
            True to continue menu loop, False to exit.
        """
        try:
            self.voice_service.cancel_call(call_sid)
            self.console.print("\n[green]Call cancelled successfully![/green]")
            return False
        except Exception as e:
            logger.exception("Error cancelling call")
            self.console.print(f"[red]Error: {str(e)}[/red]")
            return True