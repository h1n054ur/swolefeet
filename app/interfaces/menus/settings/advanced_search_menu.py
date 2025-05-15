"""Menu for advanced search functionality."""

import logging
from typing import Dict, Callable, List
from datetime import datetime
from rich.table import Table
from ..base_menu import BaseMenu
from ....services.search_service import SearchService, SearchFilter

logger = logging.getLogger(__name__)

class AdvancedSearchMenu(BaseMenu):
    """Menu for advanced search functionality."""
    
    def __init__(self, parent: BaseMenu = None):
        """Initialize the menu.
        
        Args:
            parent: Optional parent menu for navigation.
        """
        super().__init__(parent)
        self.search_service = SearchService()
        self.page_size = 20
        self.current_page = 1
        self.filters: List[SearchFilter] = []
    
    def show(self) -> None:
        """Display the advanced search menu."""
        self.clear_screen()
        self.render_header("Advanced Search")
        
        options: Dict[str, Callable] = {
            '1': self.add_filter,
            '2': self.clear_filters,
            '3': self.execute_search,
            'n': self.next_page,
            'p': self.prev_page
        }
        
        while self.prompt_choice(options):
            self.clear_screen()
            self.render_header("Advanced Search")
            self.display_filters()
    
    def display_filters(self) -> None:
        """Display current search filters."""
        if not self.filters:
            self.console.print("[yellow]No filters set![/yellow]")
        else:
            table = Table(show_header=True, header_style="bold blue")
            table.add_column("#")
            table.add_column("Field")
            table.add_column("Operator")
            table.add_column("Value")
            
            for i, filter in enumerate(self.filters, 1):
                table.add_row(
                    str(i),
                    filter.field,
                    filter.operator,
                    str(filter.value)
                )
            
            self.console.print("\n[bold]Current Filters[/bold]")
            self.console.print(table)
        
        self.console.print("\nOptions:")
        self.console.print("1. Add Filter")
        self.console.print("2. Clear Filters")
        self.console.print("3. Execute Search")
        self.console.print("n. Next Page")
        self.console.print("p. Previous Page")
        self.console.print("b. Back")
    
    def add_filter(self) -> bool:
        """Add a search filter.
        
        Returns:
            True to continue menu loop.
        """
        try:
            # Show available fields
            fields = self.search_service.get_searchable_fields()
            
            self.console.print("\n[bold]Available Fields:[/bold]")
            for i, field in enumerate(fields, 1):
                self.console.print(f"{i}. {field.name} ({field.type})")
            
            # Get field selection
            field_choice = self.prompt_input(
                "\nSelect field number: ",
                lambda x: x.isdigit() and 1 <= int(x) <= len(fields)
            )
            
            if not field_choice:
                return True
            
            field = fields[int(field_choice) - 1]
            
            # Show operators for field type
            operators = self.search_service.get_operators_for_type(field.type)
            
            self.console.print("\n[bold]Available Operators:[/bold]")
            for i, op in enumerate(operators, 1):
                self.console.print(f"{i}. {op}")
            
            # Get operator selection
            op_choice = self.prompt_input(
                "\nSelect operator number: ",
                lambda x: x.isdigit() and 1 <= int(x) <= len(operators)
            )
            
            if not op_choice:
                return True
            
            operator = operators[int(op_choice) - 1]
            
            # Get value
            value = self.prompt_input(
                "\nEnter value: ",
                lambda x: self.validate_value(x, field.type)
            )
            
            if not value:
                return True
            
            # Add filter
            self.filters.append(SearchFilter(
                field=field.name,
                operator=operator,
                value=self.convert_value(value, field.type)
            ))
            
            self.console.print("\n[green]Filter added successfully![/green]")
            return True
            
        except Exception as e:
            logger.exception("Error adding filter")
            self.console.print(f"[red]Error: {str(e)}[/red]")
            return True
    
    def clear_filters(self) -> bool:
        """Clear all search filters.
        
        Returns:
            True to continue menu loop.
        """
        self.filters = []
        self.console.print("\n[green]All filters cleared![/green]")
        return True
    
    def execute_search(self) -> bool:
        """Execute search with current filters.
        
        Returns:
            True to continue menu loop.
        """
        try:
            if not self.filters:
                self.console.print("[yellow]No filters set! Add at least one filter.[/yellow]")
                return True
            
            # Execute search
            results = self.search_service.search_advanced(
                filters=self.filters,
                page=self.current_page,
                page_size=self.page_size
            )
            
            if not results:
                self.console.print("[yellow]No results found![/yellow]")
                return True
            
            # Display results
            table = Table(show_header=True, header_style="bold blue")
            table.add_column("Type")
            table.add_column("SID")
            table.add_column("Created")
            table.add_column("Details")
            
            for result in results:
                table.add_row(
                    result.resource_type,
                    result.sid,
                    result.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    result.details[:50] + "..." if len(result.details) > 50 else result.details
                )
            
            self.console.print(f"\n[bold]Search Results (Page {self.current_page})[/bold]")
            self.console.print(table)
            
            return True
            
        except Exception as e:
            logger.exception("Error executing search")
            self.console.print(f"[red]Error: {str(e)}[/red]")
            return True
    
    def next_page(self) -> bool:
        """Go to next page of results.
        
        Returns:
            True to continue menu loop.
        """
        self.current_page += 1
        return self.execute_search()
    
    def prev_page(self) -> bool:
        """Go to previous page of results.
        
        Returns:
            True to continue menu loop.
        """
        if self.current_page > 1:
            self.current_page -= 1
            return self.execute_search()
        return True
    
    def validate_value(self, value: str, field_type: str) -> bool:
        """Validate input value against field type.
        
        Args:
            value: Value to validate.
            field_type: Expected field type.
            
        Returns:
            True if valid, False otherwise.
        """
        if not value:
            return True
            
        try:
            self.convert_value(value, field_type)
            return True
        except ValueError:
            return False
    
    def convert_value(self, value: str, field_type: str) -> any:
        """Convert string value to appropriate type.
        
        Args:
            value: Value to convert.
            field_type: Target field type.
            
        Returns:
            Converted value.
            
        Raises:
            ValueError: If value cannot be converted.
        """
        if field_type == 'string':
            return value
        elif field_type == 'number':
            return float(value)
        elif field_type == 'integer':
            return int(value)
        elif field_type == 'boolean':
            return value.lower() in ['true', 'yes', '1']
        elif field_type == 'date':
            return datetime.strptime(value, '%Y-%m-%d')
        elif field_type == 'datetime':
            return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        else:
            raise ValueError(f"Unsupported field type: {field_type}")