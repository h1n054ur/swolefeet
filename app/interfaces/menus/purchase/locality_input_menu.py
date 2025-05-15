"""Menu for selecting locality for number search."""

from typing import Dict, List, Optional
from textual.widgets import Input, DataTable, Static
from textual.screen import Screen
from textual.containers import Vertical
from textual.binding import Binding
from textual.message import Message

from ....services.number_service import NumberService

class LocalityInputMenu(Screen):
    """Menu for selecting locality for number search."""

    BINDINGS = [
        Binding("escape", "go_back", "Back", show=True),
        Binding("enter", "select_locality", "Select", show=True),
        Binding("n", "next_page", "Next Page", show=True),
        Binding("p", "prev_page", "Prev Page", show=True)
    ]

    def __init__(self, country_code: str, **kwargs):
        super().__init__(**kwargs)
        self.country_code = country_code
        self.number_service = NumberService()
        self.localities: List[Dict] = []
        self.filtered_localities: List[Dict] = []
        self.page_size = 10
        self.current_page = 0
        self.search_input: Optional[Input] = None
        self.table: Optional[DataTable] = None
        self.status: Optional[Static] = None

    def compose(self):
        """Create child widgets."""
        # Create search input
        search = Input(
            placeholder="Search localities...",
            id="search"
        )
        
        # Create table
        table = DataTable()
        table.add_columns("Region", "State/Province", "Postal Code")
        
        # Create status
        status = Static("Loading localities...", id="status")
        
        yield Vertical(search, status, table)

    async def on_mount(self):
        """Initialize widgets when mounted."""
        self.search_input = self.query_one("#search", Input)
        self.table = self.query_one(DataTable)
        self.status = self.query_one("#status", Static)
        
        # Load localities
        self.localities = await self.number_service.get_localities(self.country_code)
        self.filtered_localities = self.localities.copy()
        self._update_table()

    def _get_status_text(self) -> str:
        """Get current status text."""
        total_pages = (len(self.filtered_localities) - 1) // self.page_size + 1
        return f"Page {self.current_page + 1} of {total_pages}"

    def _update_table(self):
        """Update table with current page of localities."""
        self.table.clear()
        start = self.current_page * self.page_size
        end = min(start + self.page_size, len(self.filtered_localities))
        
        for locality in self.filtered_localities[start:end]:
            self.table.add_row(
                locality.get("region", "N/A"),
                locality.get("state", "N/A"),
                locality.get("postal_code", "N/A")
            )
        
        self.status.update(self._get_status_text())

    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle search input changes."""
        if event.input.id != "search":
            return
            
        search_text = event.value.lower()
        
        # Filter localities
        self.filtered_localities = [
            loc for loc in self.localities
            if any(
                str(val).lower().find(search_text) != -1
                for val in loc.values()
            )
        ]
        
        # Reset to first page and update
        self.current_page = 0
        self._update_table()

    async def action_go_back(self):
        """Handle back action."""
        await self.app.pop_screen()

    async def action_select_locality(self):
        """Handle locality selection."""
        row = self.table.cursor_coordinate.row
        if row is None:
            return
        
        # Get locality from current page
        index = self.current_page * self.page_size + row
        if index >= len(self.filtered_localities):
            return
        
        locality = self.filtered_localities[index]
        await self.app.pop_screen(locality)

    async def action_next_page(self):
        """Go to next page."""
        total_pages = (len(self.filtered_localities) - 1) // self.page_size + 1
        if self.current_page < total_pages - 1:
            self.current_page += 1
            self._update_table()

    async def action_prev_page(self):
        """Go to previous page."""
        if self.current_page > 0:
            self.current_page -= 1
            self._update_table()
