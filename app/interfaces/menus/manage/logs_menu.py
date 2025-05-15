"""Menu for viewing number logs."""

import logging
from typing import Dict, Callable, List
from datetime import datetime, timedelta
from rich.table import Table
from ..base_menu import BaseMenu
from ....models.phone_number_model import NumberRecord
from ....models.log_model import LogEntry
from ....services.log_service import LogService

logger = logging.getLogger(__name__)

class LogsMenu(BaseMenu):
    """Menu for viewing number logs."""
    
    def __init__(self, number: NumberRecord, parent: BaseMenu = None):
        """Initialize the menu.
        
        Args:
            number: The phone number to view logs for.
            parent: Optional parent menu for navigation.
        """
        super().__init__(parent)
        self.number = number
        self.log_service = LogService()
        self.page_size = 10
        self.current_page = 1
        self.log_type = 'all'  # 'all', 'voice', 'messaging'
    
    def show(self) -> None:
        """Display the logs menu."""
        self.clear_screen()
        self.render_header(f"Logs for {self.number.number}")
        
        options: Dict[str, Callable] = {
            '1': lambda: self.set_type('voice'),
            '2': lambda: self.set_type('messaging'),
            '3': lambda: self.set_type('all'),
            'n': self.next_page,
            'p': self.prev_page
        }
        
        while True:
            try:
                # Get logs for current page
                logs = self.log_service.get_logs(
                    number=self.number.number,
                    log_type=self.log_type,
                    page=self.current_page,
                    page_size=self.page_size
                )
                
                self.display_logs(logs)
                
                if not self.prompt_choice(options):
                    break
                
                self.clear_screen()
                self.render_header(f"Logs for {self.number.number}")
            
            except Exception as e:
                logger.exception("Error viewing logs")
                self.console.print(f"[red]Error: {str(e)}[/red]")
                break
    
    def display_logs(self, logs: List[LogEntry]) -> None:
        """Display logs in a table.
        
        Args:
            logs: List of log entries to display.
        """
        # Show current filter
        self.console.print(
            f"\nShowing [bold]{self.log_type.title()}[/bold] logs "
            f"(Page {self.current_page})"
        )
        
        if not logs:
            self.console.print("[yellow]No logs found![/yellow]")
            return
        
        # Create table
        table = Table(show_header=True, header_style="bold blue")
        table.add_column("Time")
        table.add_column("Type")
        table.add_column("Status")
        table.add_column("Details")
        
        for log in logs:
            table.add_row(
                log.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                log.operation,
                log.status,
                log.details[:50] + "..." if len(log.details) > 50 else log.details
            )
        
        self.console.print(table)
        self.console.print("\nOptions:")
        self.console.print("1. Show Voice Logs")
        self.console.print("2. Show Messaging Logs")
        self.console.print("3. Show All Logs")
        self.console.print("n. Next Page")
        self.console.print("p. Previous Page")
        self.console.print("b. Back")
    
    def set_type(self, log_type: str) -> bool:
        """Set the log type filter.
        
        Args:
            log_type: Type of logs to show ('voice', 'messaging', 'all').
            
        Returns:
            True to continue menu loop.
        """
        self.log_type = log_type
        self.current_page = 1
        return True
    
    def next_page(self) -> bool:
        """Go to next page of logs.
        
        Returns:
            True to continue menu loop.
        """
        self.current_page += 1
        return True
    
    def prev_page(self) -> bool:
        """Go to previous page of logs.
        
        Returns:
            True to continue menu loop.
        """
        if self.current_page > 1:
            self.current_page -= 1
        return True