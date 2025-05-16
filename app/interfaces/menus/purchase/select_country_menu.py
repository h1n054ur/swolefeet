"""Menu for selecting country for number purchase."""

from typing import Dict, Optional
from textual.widgets import Select, Input, Static
from textual.screen import Screen
from textual.containers import Vertical, Horizontal
from textual.binding import Binding

from ....models.country_data import COUNTRY_CODES
from .select_type_menu import SelectTypeMenu

COMMON_COUNTRIES = {
    "US": "United States",
    "CA": "Canada",
    "GB": "United Kingdom",
    "AU": "Australia"
}

class SelectCountryMenu(Screen):
    """Menu for selecting the country for number purchase."""

    BINDINGS = [
        Binding("escape", "go_back", "Back", show=True),
        Binding("enter", "select_country", "Select", show=True),
        Binding("tab", "toggle_mode", "Toggle Mode", show=True)
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.country_select: Optional[Select] = None
        self.country_input: Optional[Input] = None
        self.status: Optional[Static] = None
        self.use_common = True

    def compose(self):
        """Create child widgets."""
        # Common countries selector
        common_select = Select(
            options=[
                (f"{code} - {name}", code)
                for code, name in COMMON_COUNTRIES.items()
            ],
            prompt="Select Common Country",
            id="common_select"
        )
        
        # Other country input
        other_input = Input(
            placeholder="Enter ISO country code (e.g., FR, DE)",
            id="other_input",
            disabled=True
        )
        
        # Status text
        status = Static(
            "Select from common countries or press [TAB] to enter another country code",
            id="status"
        )
        
        yield Vertical(
            common_select,
            other_input,
            status
        )

    def on_mount(self):
        """Initialize widgets when mounted."""
        self.country_select = self.query_one("#common_select", Select)
        self.country_input = self.query_one("#other_input", Input)
        self.status = self.query_one("#status", Static)

    async def action_go_back(self):
        """Handle back action."""
        await self.app.pop_screen()

    async def action_toggle_mode(self):
        """Toggle between common and other country input."""
        self.use_common = not self.use_common
        self.country_select.disabled = not self.use_common
        self.country_input.disabled = self.use_common
        
        if self.use_common:
            self.status.update(
                "Select from common countries or press [TAB] to enter another country code"
            )
        else:
            self.status.update(
                "Enter ISO country code or press [TAB] to select from common countries"
            )

    async def action_select_country(self):
        """Handle country selection."""
        country_code = None
        
        if self.use_common:
            if not self.country_select.value:
                return
            country_code = self.country_select.value
        else:
            if not self.country_input.value:
                return
            # Validate ISO code
            code = self.country_input.value.upper()
            if code in COUNTRY_CODES:
                country_code = code
            else:
                self.status.update("Invalid country code. Please try again.")
                return
        
        if country_code:
            await self.app.push_screen(SelectTypeMenu(country_code=country_code))