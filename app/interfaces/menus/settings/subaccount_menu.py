"""Menu for managing subaccounts."""

import logging
from typing import Dict, Callable
from rich.table import Table
from ..base_menu import BaseMenu
from ....services.account_service import AccountService

logger = logging.getLogger(__name__)

class SubaccountMenu(BaseMenu):
    """Menu for managing subaccounts."""
    
    def __init__(self, parent: BaseMenu = None):
        """Initialize the menu.
        
        Args:
            parent: Optional parent menu for navigation.
        """
        super().__init__(parent)
        self.account_service = AccountService()
    
    def show(self) -> None:
        """Display the subaccount menu."""
        self.clear_screen()
        self.render_header("Subaccount Management")
        
        options: Dict[str, Callable] = {
            '1': self.list_subaccounts,
            '2': self.create_subaccount,
            '3': self.switch_account,
            '4': self.close_subaccount
        }
        
        while self.prompt_choice(options):
            self.clear_screen()
            self.render_header("Subaccount Management")
    
    def list_subaccounts(self) -> bool:
        """List all subaccounts.
        
        Returns:
            True to continue menu loop.
        """
        try:
            # Get subaccounts
            accounts = self.account_service.list_subaccounts()
            
            if not accounts:
                self.console.print("[yellow]No subaccounts found![/yellow]")
                return True
            
            # Display accounts
            table = Table(show_header=True, header_style="bold blue")
            table.add_column("SID")
            table.add_column("Friendly Name")
            table.add_column("Status")
            table.add_column("Created")
            
            for account in accounts:
                table.add_row(
                    account.sid,
                    account.friendly_name,
                    account.status,
                    account.created_at.strftime("%Y-%m-%d")
                )
            
            self.console.print("\n[bold]Subaccounts[/bold]")
            self.console.print(table)
            
            return True
            
        except Exception as e:
            logger.exception("Error listing subaccounts")
            self.console.print(f"[red]Error: {str(e)}[/red]")
            return True
    
    def create_subaccount(self) -> bool:
        """Create a new subaccount.
        
        Returns:
            True to continue menu loop.
        """
        try:
            name = self.prompt_input(
                "\nEnter friendly name for subaccount: ",
                lambda x: bool(x.strip())
            )
            
            if not name:
                return True
            
            account = self.account_service.create_subaccount(name)
            
            self.console.print("\n[green]Subaccount created successfully![/green]")
            self.console.print(f"Account SID: {account.sid}")
            self.console.print(f"Auth Token: {account.auth_token}")
            self.console.print("[bold red]Save these credentials now. The auth token will not be shown again.[/bold red]")
            
            return True
            
        except Exception as e:
            logger.exception("Error creating subaccount")
            self.console.print(f"[red]Error: {str(e)}[/red]")
            return True
    
    def switch_account(self) -> bool:
        """Switch to a different account.
        
        Returns:
            True to continue menu loop.
        """
        try:
            sid = self.prompt_input(
                "\nEnter account SID to switch to: ",
                lambda x: bool(x.startswith('AC'))
            )
            
            if not sid:
                return True
            
            # Get current account info
            current = self.account_service.get_current_account()
            
            # Switch account
            self.account_service.switch_account(sid)
            
            self.console.print("\n[green]Account switched successfully![/green]")
            self.console.print(f"Previous: {current.friendly_name} ({current.sid})")
            
            # Get new account info
            new = self.account_service.get_current_account()
            self.console.print(f"Current: {new.friendly_name} ({new.sid})")
            
            return True
            
        except Exception as e:
            logger.exception("Error switching account")
            self.console.print(f"[red]Error: {str(e)}[/red]")
            return True
    
    def close_subaccount(self) -> bool:
        """Close a subaccount.
        
        Returns:
            True to continue menu loop.
        """
        try:
            sid = self.prompt_input(
                "\nEnter subaccount SID to close: ",
                lambda x: bool(x.startswith('AC'))
            )
            
            if not sid:
                return True
            
            # Get account info
            account = self.account_service.get_account(sid)
            
            # Confirm closure
            self.console.print(f"\nClosing account: {account.friendly_name} ({account.sid})")
            self.console.print("[red]WARNING: This action cannot be undone![/red]")
            
            confirm = self.prompt_input(
                "\nType the account SID to confirm: ",
                lambda x: x == sid
            )
            
            if confirm:
                self.account_service.close_subaccount(sid)
                self.console.print("\n[green]Subaccount closed successfully![/green]")
            
            return True
            
        except Exception as e:
            logger.exception("Error closing subaccount")
            self.console.print(f"[red]Error: {str(e)}[/red]")
            return True