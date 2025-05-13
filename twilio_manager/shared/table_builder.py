"""Table builder for consistent table styling across the application."""
from typing import List, Dict, Any, Optional
from rich.table import Table
from twilio_manager.shared.styles import COLORS, create_table

class TableBuilder:
    """Builder class for creating consistently styled tables."""

    def __init__(self, title: Optional[str] = None):
        self.table = create_table(title=title)
        self._formatters: Dict[str, callable] = {}

    def add_index_column(self) -> 'TableBuilder':
        """Add an index column (#)."""
        self.table.add_column("#", style=COLORS['dim'], justify="right")
        return self

    def add_column(self, header: str, style: Optional[str] = None,
                  justify: str = "left", formatter: Optional[callable] = None) -> 'TableBuilder':
        """Add a column with optional style and formatter."""
        self.table.add_column(header, style=style or COLORS['normal'], justify=justify)
        if formatter:
            self._formatters[header] = formatter
        return self

    def add_phone_column(self, header: str = "Phone Number") -> 'TableBuilder':
        """Add a phone number column."""
        return self.add_column(header, style=COLORS['info'])

    def add_name_column(self, header: str = "Name") -> 'TableBuilder':
        """Add a name column."""
        return self.add_column(header, style=COLORS['highlight'])

    def add_status_column(self, header: str = "Status") -> 'TableBuilder':
        """Add a status column."""
        return self.add_column(header, style=COLORS['success'])

    def add_date_column(self, header: str = "Date") -> 'TableBuilder':
        """Add a date column."""
        return self.add_column(header, style=COLORS['dim'])

    def add_rows(self, data: List[Dict[str, Any]], with_index: bool = True) -> 'TableBuilder':
        """Add multiple rows from a list of dictionaries."""
        for idx, item in enumerate(data, 1):
            row = []
            if with_index:
                row.append(str(idx))
            
            for column in self.table.columns[1 if with_index else 0:]:
                value = item.get(column.header.lower().replace(' ', '_'), 'N/A')
                if column.header in self._formatters:
                    value = self._formatters[column.header](value)
                row.append(str(value))
            
            self.table.add_row(*row)
        return self

    def build(self) -> Table:
        """Return the built table."""
        return self.table