"""Menu for searching numbers by digits."""

from typing import Dict, Optional, Set
from textual.widgets import Input, Static, Button
from textual.screen import Screen
from textual.containers import Vertical, Horizontal
from textual.binding import Binding

from ....services.number_service import NumberService
from .search_progress_menu import SearchProgressMenu

class ByDigitsMenu(Screen):
    """Menu for searching numbers by digits."""

    BINDINGS = [
        Binding("escape", "go_back", "Back", show=True),
        Binding("enter", "search_numbers", "Search", show=True)
    ]

    def __init__(self, country_code: str, number_type: str, **kwargs):
        super().__init__(**kwargs)
        self.country_code = country_code
        self.number_type = number_type
        self.number_service = NumberService()
        self.digits_input: Optional[Input] = None
        self.status: Optional[Static] = None
        self.area_codes: Set[str] = set()

    def compose(self):
        """Create child widgets."""
        # Create input
        digits = Input(
            placeholder="Enter 3-10 digits to search",
            id="digits"
        )
        
        # Create status
        status = Static(
            "Enter digits to search for in phone numbers",
            id="status"
        )
        
        # Create buttons
        buttons = Horizontal(
            Button("Search", id="search_btn"),
            Button("Cancel", id="cancel_btn")
        )
        
        yield Vertical(digits, status, buttons)

    async def on_mount(self):
        """Initialize widgets when mounted."""
        self.digits_input = self.query_one("#digits", Input)
        self.status = self.query_one("#status", Static)
        
        # Set up button handlers
        self.query_one("#search_btn", Button).on_click = self.action_search_numbers
        self.query_one("#cancel_btn", Button).on_click = self.action_go_back
        
        # Load area codes for US
        if self.country_code == "US":
            self.area_codes = await self.number_service.get_area_codes()
            self.status.update(
                "Enter 3 digits for area code search, or 4-10 digits for number search"
            )

    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle digit input changes."""
        if event.input.id != "digits":
            return
            
        digits = event.value
        
        # Validate input
        if not digits.isdigit():
            self.status.update("Please enter only digits")
            return
            
        if len(digits) < 3 or len(digits) > 10:
            self.status.update("Please enter between 3 and 10 digits")
            return
            
        # Special handling for US area codes
        if self.country_code == "US" and len(digits) == 3:
            if digits in self.area_codes:
                self.status.update(f"Valid area code: {digits}")
            else:
                self.status.update(f"Unknown area code: {digits}")
        else:
            self.status.update("Ready to search")

    async def action_go_back(self):
        """Handle back action."""
        await self.app.pop_screen()

    async def action_search_numbers(self):
        """Handle number search."""
        if not self.digits_input or not self.digits_input.value:
            return
            
        digits = self.digits_input.value
        
        # Validate input
        if not digits.isdigit():
            self.status.update("Please enter only digits")
            return
            
        if len(digits) < 3 or len(digits) > 10:
            self.status.update("Please enter between 3 and 10 digits")
            return
            
        # Start search
        await self.app.push_screen(
            SearchProgressMenu(
                country_code=self.country_code,
                number_type=self.number_type,
                search_pattern=digits
            )
        )