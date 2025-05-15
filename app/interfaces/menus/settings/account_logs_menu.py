"""Menu for viewing account-wide logs."""

import logging
from typing import Dict, Callable
from datetime import datetime, timedelta
from rich.table import Table
from ..base_menu import BaseMenu
from ....services.log_service import LogService

logger = logging.getLogger(__name__)

class AccountLogsMenu(BaseMenu):
    """Menu for viewing account-wide logs."""
    
    def __init__(self, parent: BaseMenu = None):
        """Initialize the menu.
        
        Args:
            parent: Optional parent menu for navigation.
        """
        super().__init__(parent)
        self.log_service = LogService()
        self.page_size = 20
        self.current_page = 1
        self.log_type = 'all'  # 'all', 'error', 'warning', 'info'
        self.date_range = 'today'  # 'today', 'week', 'month', 'custom'
    
    def show(self) -> None:
        """Display the account logs menu."""
        self.clear_screen()
        self.render_header("Account Logs")
        
        options: Dict[str, Callable] = {
            '1': lambda: self.set_type('all'),
            '2': lambda: self.set_type('error'),
            '3': lambda: self.set_type('warning'),
            '4': lambda: self.set_type('info'),
            '5': self.set_date_range,
            'n': self.next_page,
            'p': self.prev_page,
            'r': self.refresh,
            'e': self.export_logs
        }
        
        while True:
            try:
                # Get logs for current page and filters
                logs = self.log_service.get_account_logs(
                    log_type=self.log_type,
                    start_date=self.get_start_date(),
                    end_date=datetime.now(),
                    page=self.current_page,
                    page_size=self.page_size
                )
                
                self.display_logs(logs)
                
                if not self.prompt_choice(options):
                    break
                
                self.clear_screen()
                self.render_header("Account Logs")
                
            except Exception as e:
                logger.exception("Error viewing logs")
                self.console.print(f"[red]Error: {str(e)}[/red]")
                break
    
    def display_logs(self, logs: list) -> None:
        """Display logs in a table.
        
        Args:
            logs: List of log entries to display.
        """
        # Show current filters
        self.console.print(
            f"\nShowing [bold]{self.log_type.title()}[/bold] logs for "
            f"[bold]{self.date_range}[/bold] "
            f"(Page {self.current_page})"
        )
        
        if not logs:
            self.console.print("[yellow]No logs found![/yellow]")
            return
        
        # Create table
        table = Table(show_header=True, header_style="bold blue")
        table.add_column("Time")
        table.add_column("Level")
        table.add_column("Service")
        table.add_column("Message")
        table.add_column("Resource")
        
        for log in logs:
            table.add_row(
                log.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                log.level,
                log.service,
                log.message[:50] + "..." if len(log.message) > 50 else log.message,
                log.resource_sid or ""
            )
        
        self.console.print(table)
        self.console.print("\nOptions:")
        self.console.print("1. Show All Logs")
        self.console.print("2. Show Errors")
        self.console.print("3. Show Warnings")
        self.console.print("4. Show Info")
        self.console.print("5. Set Date Range")
        self.console.print("n. Next Page")
        self.console.print("p. Previous Page")
        self.console.print("r. Refresh")
        self.console.print("e. Export Logs")
        self.console.print("b. Back")
    
    def set_type(self, log_type: str) -> bool:
        """Set the log type filter.
        
        Args:
            log_type: Type of logs to show.
            
        Returns:
            True to continue menu loop.
        """
        self.log_type = log_type
        self.current_page = 1
        return True
    
    def set_date_range(self) -> bool:
        """Set the date range filter.
        
        Returns:
            True to continue menu loop.
        """
        self.console.print("\nSelect date range:")
        self.console.print("1. Today")
        self.console.print("2. Last 7 days")
        self.console.print("3. Last 30 days")
        self.console.print("4. Custom range")
        
        choice = self.prompt_input(
            "\nEnter choice: ",
            lambda x: x in ['1', '2', '3', '4']
        )
        
        if choice == '1':
            self.date_range = 'today'
        elif choice == '2':
            self.date_range = 'week'
        elif choice == '3':
            self.date_range = 'month'
        elif choice == '4':
            # Get custom date range
            start = self.prompt_input(
                "Enter start date (YYYY-MM-DD): ",
                self.validate_date
            )
            if not start:
                return True
            
            end = self.prompt_input(
                "Enter end date (YYYY-MM-DD): ",
                self.validate_date
            )
            if not end:
                return True
            
            self.date_range = f"custom:{start}:{end}"
        
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
    
    def refresh(self) -> bool:
        """Refresh current page.
        
        Returns:
            True to continue menu loop.
        """
        return True
    
    def export_logs(self) -> bool:
        """Export logs to file.
        
        Returns:
            True to continue menu loop.
        """
        try:
            filename = self.prompt_input(
                "\nEnter filename (empty for default): "
            )
            
            if not filename:
                filename = (
                    f"twilio_logs_{self.log_type}_{datetime.now().strftime('%Y%m%d')}.csv"
                )
            
            # Export logs
            self.log_service.export_logs(
                filename=filename,
                log_type=self.log_type,
                start_date=self.get_start_date(),
                end_date=datetime.now()
            )
            
            self.console.print(f"\n[green]Logs exported to {filename}![/green]")
            return True
            
        except Exception as e:
            logger.exception("Error exporting logs")
            self.console.print(f"[red]Error: {str(e)}[/red]")
            return True
    
    def get_start_date(self) -> datetime:
        """Get start date based on current date range.
        
        Returns:
            Start date for log filtering.
        """
        now = datetime.now()
        
        if self.date_range == 'today':
            return now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif self.date_range == 'week':
            return now - timedelta(days=7)
        elif self.date_range == 'month':
            return now - timedelta(days=30)
        elif self.date_range.startswith('custom:'):
            start_str = self.date_range.split(':')[1]
            return datetime.strptime(start_str, '%Y-%m-%d')
        
        return now
    
    def validate_date(self, date_str: str) -> bool:
        """Validate date string format.
        
        Args:
            date_str: Date string to validate.
            
        Returns:
            True if valid, False otherwise.
        """
        if not date_str:
            return True
            
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False