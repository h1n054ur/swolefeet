"""Menu for developer tools and settings."""

import logging
from typing import Dict, Callable
from rich.table import Table
from ..base_menu import BaseMenu
from ....services.dev_service import DevService

logger = logging.getLogger(__name__)

class DevToolsMenu(BaseMenu):
    """Menu for developer tools and settings."""
    
    def __init__(self, parent: BaseMenu = None):
        """Initialize the menu.
        
        Args:
            parent: Optional parent menu for navigation.
        """
        super().__init__(parent)
        self.dev_service = DevService()
    
    def show(self) -> None:
        """Display the developer tools menu."""
        self.clear_screen()
        self.render_header("Developer Tools")
        
        options: Dict[str, Callable] = {
            '1': self.show_webhook_url,
            '2': self.toggle_sandbox,
            '3': self.show_test_credentials,
            '4': self.show_api_explorer
        }
        
        while self.prompt_choice(options):
            self.clear_screen()
            self.render_header("Developer Tools")
    
    def show_webhook_url(self) -> bool:
        """Show webhook URL and configuration.
        
        Returns:
            True to continue menu loop.
        """
        try:
            # Get webhook info
            webhook = self.dev_service.get_webhook_info()
            
            self.console.print("\n[bold]Webhook Configuration[/bold]")
            self.console.print(f"URL: {webhook.url}")
            self.console.print(f"Method: {webhook.method}")
            self.console.print(f"Fallback URL: {webhook.fallback_url or 'Not set'}")
            
            # Show recent requests
            table = Table(show_header=True, header_style="bold blue")
            table.add_column("Time")
            table.add_column("Status")
            table.add_column("Response Time")
            table.add_column("Error")
            
            for request in webhook.recent_requests:
                table.add_row(
                    request.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    str(request.status_code),
                    f"{request.response_time_ms}ms",
                    request.error or ""
                )
            
            self.console.print("\n[bold]Recent Webhook Requests[/bold]")
            self.console.print(table)
            
            return True
            
        except Exception as e:
            logger.exception("Error showing webhook info")
            self.console.print(f"[red]Error: {str(e)}[/red]")
            return True
    
    def toggle_sandbox(self) -> bool:
        """Toggle sandbox mode.
        
        Returns:
            True to continue menu loop.
        """
        try:
            # Get current status
            is_sandbox = self.dev_service.is_sandbox_enabled()
            
            self.console.print("\n[bold]Sandbox Mode[/bold]")
            self.console.print(f"Current Status: {'Enabled' if is_sandbox else 'Disabled'}")
            
            # Confirm toggle
            action = "disable" if is_sandbox else "enable"
            confirm = self.prompt_input(
                f"\nType '{action.upper()}' to {action} sandbox mode: ",
                lambda x: x == action.upper()
            )
            
            if confirm:
                self.dev_service.set_sandbox_mode(not is_sandbox)
                self.console.print(f"\n[green]Sandbox mode {action}d successfully![/green]")
            
            return True
            
        except Exception as e:
            logger.exception("Error toggling sandbox mode")
            self.console.print(f"[red]Error: {str(e)}[/red]")
            return True
    
    def show_test_credentials(self) -> bool:
        """Show test credentials.
        
        Returns:
            True to continue menu loop.
        """
        try:
            # Get test credentials
            creds = self.dev_service.get_test_credentials()
            
            self.console.print("\n[bold]Test Credentials[/bold]")
            self.console.print("[yellow]Use these credentials for testing only![/yellow]")
            self.console.print(f"Account SID: {creds.account_sid}")
            self.console.print(f"Auth Token: {creds.auth_token}")
            
            self.console.print("\n[bold]Test Phone Numbers[/bold]")
            for number in creds.test_numbers:
                self.console.print(f"- {number.number} ({number.capabilities})")
            
            return True
            
        except Exception as e:
            logger.exception("Error showing test credentials")
            self.console.print(f"[red]Error: {str(e)}[/red]")
            return True
    
    def show_api_explorer(self) -> bool:
        """Show API explorer interface.
        
        Returns:
            True to continue menu loop.
        """
        try:
            # Get available endpoints
            endpoints = self.dev_service.list_api_endpoints()
            
            # Display endpoints
            table = Table(show_header=True, header_style="bold blue")
            table.add_column("Method")
            table.add_column("Path")
            table.add_column("Description")
            
            for endpoint in endpoints:
                table.add_row(
                    endpoint.method,
                    endpoint.path,
                    endpoint.description
                )
            
            self.console.print("\n[bold]Available API Endpoints[/bold]")
            self.console.print(table)
            
            # Show options
            api_options: Dict[str, Callable] = {
                't': self.test_endpoint,
                'b': lambda: False
            }
            
            self.console.print("\nOptions:")
            self.console.print("t. Test Endpoint")
            self.console.print("b. Back")
            
            return self.prompt_choice(api_options)
            
        except Exception as e:
            logger.exception("Error showing API explorer")
            self.console.print(f"[red]Error: {str(e)}[/red]")
            return True
    
    def test_endpoint(self) -> bool:
        """Test an API endpoint.
        
        Returns:
            True to continue menu loop.
        """
        try:
            method = self.prompt_input(
                "\nEnter HTTP method (GET/POST/PUT/DELETE): ",
                lambda x: x.upper() in ['GET', 'POST', 'PUT', 'DELETE']
            ).upper()
            
            if not method:
                return True
            
            path = self.prompt_input(
                "Enter API path: ",
                lambda x: bool(x.strip())
            )
            
            if not path:
                return True
            
            # Make test request
            response = self.dev_service.test_endpoint(method, path)
            
            self.console.print("\n[bold]API Response[/bold]")
            self.console.print(f"Status: {response.status_code}")
            self.console.print("Headers:")
            for key, value in response.headers.items():
                self.console.print(f"  {key}: {value}")
            self.console.print("\nBody:")
            self.console.print(response.body)
            
            return True
            
        except Exception as e:
            logger.exception("Error testing endpoint")
            self.console.print(f"[red]Error: {str(e)}[/red]")
            return True