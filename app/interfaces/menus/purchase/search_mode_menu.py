"""Menu for selecting number search mode."""

from typing import Dict, Optional
from textual.widgets import Button, Static
from textual.screen import Screen
from textual.containers import Vertical, Horizontal
from textual.binding import Binding

from .by_digits_menu import ByDigitsMenu
from .locality_input_menu import LocalityInputMenu

class SearchModeMenu(Screen):
    """Menu for selecting number search mode."""

    BINDINGS = [
        Binding("escape", "go_back", "Back", show=True),
        Binding("d", "search_digits", "Search by Digits", show=True),
        Binding("l", "search_locality", "Search by Locality", show=True)
    ]

    def __init__(self, country_code: str, number_type: str, **kwargs):
        super().__init__(**kwargs)
        self.country_code = country_code
        self.number_type = number_type

    def compose(self):
        """Create child widgets."""
        yield Vertical(
            Static("Choose Search Mode", id="title"),
            Horizontal(
                Button("Search by Digits [d]", id="digits_btn"),
                Button("Search by Locality [l]", id="locality_btn")
            )
        )

    def on_mount(self):
        """Initialize button handlers."""
        self.query_one("#digits_btn", Button).on_click = self.action_search_digits
        self.query_one("#locality_btn", Button).on_click = self.action_search_locality

    async def action_go_back(self):
        """Handle back action."""
        await self.app.pop_screen()

    async def action_search_digits(self):
        """Switch to digits search mode."""
        await self.app.push_screen(
            ByDigitsMenu(
                country_code=self.country_code,
                number_type=self.number_type
            )
        )

    async def action_search_locality(self):
        """Switch to locality search mode."""
        await self.app.push_screen(
            LocalityInputMenu(country_code=self.country_code)
        )