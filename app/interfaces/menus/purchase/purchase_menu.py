"""Main menu for the number purchase guided flow."""

from typing import Dict, Optional
from textual.widgets import Select, Static
from textual.screen import Screen
from textual.containers import Container, Vertical
from textual.binding import Binding

from ....models.country_data import COUNTRY_CODES
from ....services.number_service import NumberService
from .search_progress_menu import SearchProgressMenu

class PurchaseMenu(Screen):
    """Main menu for purchasing phone numbers."""

    BINDINGS = [
        Binding("escape", "go_back", "Back", show=True),
        Binding("enter", "next_step", "Next", show=True)
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.country_select: Optional[Select] = None
        self.type_select: Optional[Select] = None
        self.number_service = NumberService()
        self.current_step = 1
        self.total_steps = 4
        self.selected_country: Optional[str] = None
        self.selected_type: Optional[str] = None

    def compose(self):
        """Create child widgets."""
        yield Vertical(
            Static(f"Step {self.current_step} of {self.total_steps}: Select Country", id="step_label"),
            Select(
                options=[
                    (f"{code} - {name}", code)
                    for code, name in COUNTRY_CODES.items()
                ],
                prompt="Select Country",
                id="country_select"
            ),
            Select(
                options=[],  # Will be populated when country is selected
                prompt="Select Number Type",
                id="type_select",
                disabled=True
            ),
            id="purchase_container"
        )

    async def on_select_changed(self, event: Select.Changed) -> None:
        """Handle selection changes."""
        if event.select.id == "country_select":
            self.selected_country = event.value
            await self._update_type_options()
        elif event.select.id == "type_select":
            self.selected_type = event.value

    async def _update_type_options(self) -> None:
        """Update number type options based on selected country."""
        if not self.selected_country:
            return

        type_select = self.query_one("#type_select", Select)
        types = await self.number_service.get_available_types(self.selected_country)
        type_select.disabled = False
        type_select.options = [
            (type_name.title(), type_code)
            for type_code, type_name in types.items()
        ]

    async def action_go_back(self) -> None:
        """Handle back action."""
        await self.app.pop_screen()

    async def action_next_step(self) -> None:
        """Handle next step action."""
        if not self.selected_country or not self.selected_type:
            return

        # Move to search progress menu
        await self.app.push_screen(
            SearchProgressMenu(
                country_code=self.selected_country,
                number_type=self.selected_type
            )
        )
