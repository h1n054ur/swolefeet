"""Menu for selecting number capabilities."""

from typing import Dict, List, Optional, Set
from textual.widgets import Checkbox, Static, Button
from textual.screen import Screen
from textual.containers import Vertical, Horizontal
from textual.binding import Binding

from .search_mode_menu import SearchModeMenu

CAPABILITIES = {
    "voice": "Voice",
    "sms": "SMS",
    "mms": "MMS"
}

class SelectCapabilitiesMenu(Screen):
    """Menu for selecting required number capabilities."""

    BINDINGS = [
        Binding("escape", "go_back", "Back", show=True),
        Binding("enter", "confirm_capabilities", "Confirm", show=True),
        Binding("space", "toggle_capability", "Toggle", show=True)
    ]

    def __init__(self, country_code: str, number_type: str, **kwargs):
        super().__init__(**kwargs)
        self.country_code = country_code
        self.number_type = number_type
        self.selected_capabilities: Set[str] = set()
        self.status: Optional[Static] = None
        self.checkboxes: Dict[str, Checkbox] = {}

    def compose(self):
        """Create child widgets."""
        # Create status
        status = Static(
            "Select at least one capability",
            id="status"
        )
        
        # Create checkboxes
        checkboxes = []
        for cap_id, cap_name in CAPABILITIES.items():
            checkbox = Checkbox(cap_name, id=f"cap_{cap_id}")
            self.checkboxes[cap_id] = checkbox
            checkboxes.append(checkbox)
        
        # Create buttons
        buttons = Horizontal(
            Button("Confirm", id="confirm_btn"),
            Button("Cancel", id="cancel_btn")
        )
        
        yield Vertical(
            status,
            *checkboxes,
            buttons
        )

    def on_mount(self):
        """Initialize widgets when mounted."""
        self.status = self.query_one("#status", Static)
        
        # Set up button handlers
        self.query_one("#confirm_btn", Button).on_click = self.action_confirm_capabilities
        self.query_one("#cancel_btn", Button).on_click = self.action_go_back

    def on_checkbox_changed(self, event: Checkbox.Changed) -> None:
        """Handle checkbox changes."""
        cap_id = event.checkbox.id.replace("cap_", "")
        if event.value:
            self.selected_capabilities.add(cap_id)
        else:
            self.selected_capabilities.discard(cap_id)
        
        # Update status
        if self.selected_capabilities:
            caps = ", ".join(CAPABILITIES[cap] for cap in self.selected_capabilities)
            self.status.update(f"Selected: {caps}")
        else:
            self.status.update("Select at least one capability")

    async def action_go_back(self):
        """Handle back action."""
        await self.app.pop_screen()

    async def action_toggle_capability(self):
        """Toggle capability under cursor."""
        focused = self.focused
        if isinstance(focused, Checkbox):
            focused.value = not focused.value

    async def action_confirm_capabilities(self):
        """Handle capability confirmation."""
        if not self.selected_capabilities:
            self.status.update("Please select at least one capability")
            return
        
        # Move to search mode
        await self.app.push_screen(
            SearchModeMenu(
                country_code=self.country_code,
                number_type=self.number_type,
                capabilities=list(self.selected_capabilities)
            )
        )