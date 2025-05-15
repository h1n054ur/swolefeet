"""Menu for viewing billing information and usage."""

import logging
from typing import Dict, Callable
from datetime import datetime, timedelta
from rich.table import Table
from ..base_menu import BaseMenu
from ....services.account_service import AccountService

logger = logging.getLogger(__name__)

class BillingMenu(BaseMenu):
    """Menu for viewing billing information and usage."""
    
    def __init__(self, parent: BaseMenu = None):
        """Initialize the menu.
        
        Args:
            parent: Optional parent menu for navigation.
        """
        super().__init__(parent)
        self.account_service = AccountService()
    
    def show(self) -> None:
        """Display the billing menu."""
        self.clear_screen()
        self.render_header("Billing & Usage")
        
        options: Dict[str, Callable] = {
            '1': self.show_current_usage,
            '2': self.show_billing_info,
            '3': self.show_usage_history
        }
        
        while self.prompt_choice(options):
            self.clear_screen()
            self.render_header("Billing & Usage")
    
    def show_current_usage(self) -> bool:
        """Show current billing period usage.
        
        Returns:
            True to continue menu loop.
        """
        try:
            usage = self.account_service.get_usage()
            
            # Create usage table
            table = Table(show_header=True, header_style="bold blue")
            table.add_column("Category")
            table.add_column("Usage")
            table.add_column("Cost")
            
            for category in usage.categories:
                table.add_row(
                    category.name,
                    str(category.usage),
                    f"${category.cost:.2f}"
                )
            
            self.console.print("\n[bold]Current Billing Period Usage[/bold]")
            self.console.print(f"Period: {usage.start_date} to {usage.end_date}")
            self.console.print(table)
            self.console.print(f"\nTotal Cost: ${usage.total_cost:.2f}")
            
            return True
            
        except Exception as e:
            logger.exception("Error getting usage information")
            self.console.print(f"[red]Error: {str(e)}[/red]")
            return True
    
    def show_billing_info(self) -> bool:
        """Show billing account information.
        
        Returns:
            True to continue menu loop.
        """
        try:
            billing = self.account_service.get_billing()
            
            self.console.print("\n[bold]Billing Information[/bold]")
            self.console.print(f"Account Type: {billing.type}")
            self.console.print(f"Payment Method: {billing.payment_method}")
            self.console.print(f"Billing Email: {billing.email}")
            self.console.print(f"Tax ID: {billing.tax_id or 'Not set'}")
            
            if billing.address:
                self.console.print("\n[bold]Billing Address:[/bold]")
                self.console.print(f"Street: {billing.address.street}")
                self.console.print(f"City: {billing.address.city}")
                self.console.print(f"State: {billing.address.state}")
                self.console.print(f"Country: {billing.address.country}")
                self.console.print(f"Postal Code: {billing.address.postal_code}")
            
            return True
            
        except Exception as e:
            logger.exception("Error getting billing information")
            self.console.print(f"[red]Error: {str(e)}[/red]")
            return True
    
    def show_usage_history(self) -> bool:
        """Show historical usage data.
        
        Returns:
            True to continue menu loop.
        """
        try:
            # Get date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=30)
            
            history = self.account_service.get_usage_history(
                start_date=start_date,
                end_date=end_date
            )
            
            # Create history table
            table = Table(show_header=True, header_style="bold blue")
            table.add_column("Date")
            table.add_column("Voice Minutes")
            table.add_column("SMS Count")
            table.add_column("Total Cost")
            
            for day in history:
                table.add_row(
                    day.date.strftime("%Y-%m-%d"),
                    str(day.voice_minutes),
                    str(day.sms_count),
                    f"${day.total_cost:.2f}"
                )
            
            self.console.print("\n[bold]Usage History[/bold]")
            self.console.print(
                f"Period: {start_date.strftime('%Y-%m-%d')} to "
                f"{end_date.strftime('%Y-%m-%d')}"
            )
            self.console.print(table)
            
            return True
            
        except Exception as e:
            logger.exception("Error getting usage history")
            self.console.print(f"[red]Error: {str(e)}[/red]")
            return True