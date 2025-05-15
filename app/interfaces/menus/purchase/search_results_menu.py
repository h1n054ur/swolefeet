"""Menu for displaying and selecting search results."""

from typing import List, Optional
from textual.widgets import DataTable, Footer, Static
from textual.screen import Screen
from textual.containers import Vertical
from textual.binding import Binding
from textual.coordinate import Coordinate

from ....models.phone_number_model import NumberRecord
from .purchase_confirm_menu import PurchaseConfirmMenu

class SearchResultsMenu(Screen):
    """Menu for displaying and selecting search results."""

    BINDINGS = [
        Binding("escape", "go_back", "Back", show=True),
        Binding("enter", "select_number", "Select", show=True),
        Binding("n", "next_page", "Next Page", show=True),
        Binding("p", "prev_page", "Prev Page", show=True),
        Binding("s", "sort_column", "Sort", show=True),
        Binding("j", "cursor_down", "Down", show=False),
        Binding("k", "cursor_up", "Up", show=False),
        Binding("c", "clear_selection", "Clear", show=True),
        Binding("x", "select_all", "Select All", show=True),
        Binding("b", "bulk_select", "Bulk Select", show=True)
    ]

    def __init__(self, numbers: List[NumberRecord], **kwargs):
        super().__init__(**kwargs)
        self.numbers = numbers
        self.page_size = 10
        self.current_page = 0
        self.total_pages = (len(numbers) - 1) // self.page_size + 1
        self.sort_column = 0
        self.sort_reverse = False
        self.selected_numbers: List[NumberRecord] = []
        self.table: Optional[DataTable] = None
        self.status: Optional[Static] = None

    def compose(self):
        """Create child widgets."""
        # Create table
        table = DataTable()
        table.add_columns("Number", "Type", "Region", "Selected")
        
        # Add status
        status = Static(self._get_status_text(), id="status")
        
        yield Vertical(status, table)

    def _get_status_text(self) -> str:
        """Get current status text."""
        return (
            f"Page {self.current_page + 1} of {self.total_pages} | "
            f"Selected: {len(self.selected_numbers)} numbers"
        )

    def on_mount(self):
        """Initialize widgets when mounted."""
        self.table = self.query_one(DataTable)
        self.status = self.query_one("#status", Static)
        self._update_table()

    def _update_table(self):
        """Update table with current page of numbers."""
        self.table.clear()
        start = self.current_page * self.page_size
        end = min(start + self.page_size, len(self.numbers))
        
        for number in self.numbers[start:end]:
            self.table.add_row(
                number.phone_number,
                number.type,
                number.region or "N/A",
                "✓" if number in self.selected_numbers else ""
            )
        
        self.status.update(self._get_status_text())

    async def action_go_back(self):
        """Handle back action."""
        await self.app.pop_screen()

    async def action_select_number(self):
        """Handle number selection."""
        row = self.table.cursor_coordinate.row
        if row is None:
            return
        
        # Get number from current page
        index = self.current_page * self.page_size + row
        if index >= len(self.numbers):
            return
        
        number = self.numbers[index]
        
        # Toggle selection
        if number in self.selected_numbers:
            self.selected_numbers.remove(number)
        else:
            self.selected_numbers.append(number)
        
        # Update display
        self._update_table()
        
        # If numbers selected, show purchase confirmation
        if self.selected_numbers:
            await self.app.push_screen(
                PurchaseConfirmMenu(numbers=self.selected_numbers)
            )

    async def action_next_page(self):
        """Go to next page."""
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self._update_table()

    async def action_prev_page(self):
        """Go to previous page."""
        if self.current_page > 0:
            self.current_page -= 1
            self._update_table()

    async def action_sort_column(self):
        """Sort by current column."""
        if not self.table.cursor_coordinate:
            return
            
        column = self.table.cursor_coordinate.column
        if column == self.sort_column:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = column
            self.sort_reverse = False
            
        # Sort numbers
        if column == 0:  # Number
            self.numbers.sort(
                key=lambda x: x.phone_number,
                reverse=self.sort_reverse
            )
        elif column == 1:  # Type
            self.numbers.sort(
                key=lambda x: x.type,
                reverse=self.sort_reverse
            )
        elif column == 2:  # Region
            self.numbers.sort(
                key=lambda x: x.region or "",
                reverse=self.sort_reverse
            )
            
        self._update_table()

    async def action_cursor_down(self):
        """Move cursor down."""
        if self.table.cursor_coordinate:
            row = self.table.cursor_coordinate.row
            if row < len(self.table.rows) - 1:
                self.table.move_cursor(row=row + 1)

    async def action_cursor_up(self):
        """Move cursor up."""
        if self.table.cursor_coordinate:
            row = self.table.cursor_coordinate.row
            if row > 0:
                self.table.move_cursor(row=row - 1)

    async def action_clear_selection(self):
        """Clear all selections."""
        self.selected_numbers.clear()
        self._update_table()

    async def action_select_all(self):
        """Select all numbers on current page."""
        start = self.current_page * self.page_size
        end = min(start + self.page_size, len(self.numbers))
        for number in self.numbers[start:end]:
            if number not in self.selected_numbers:
                self.selected_numbers.append(number)
        self._update_table()

    async def action_bulk_select(self):
        """Select a range of numbers."""
        if not self.table.cursor_coordinate:
            return
            
        # Get current row
        current_row = self.table.cursor_coordinate.row
        if current_row is None:
            return
            
        # Calculate range
        start_row = max(0, current_row - 4)  # Select 5 numbers up
        end_row = min(len(self.table.rows), current_row + 5)  # Select 5 numbers down
        
        # Add numbers to selection
        start_idx = self.current_page * self.page_size + start_row
        end_idx = self.current_page * self.page_size + end_row
        for number in self.numbers[start_idx:end_idx]:
            if number not in self.selected_numbers:
                self.selected_numbers.append(number)
        
        self._update_table() (paginated results table)
