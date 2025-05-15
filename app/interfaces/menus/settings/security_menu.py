"""Menu for managing security settings."""

import logging
import re
from typing import Dict, Callable
from rich.table import Table
from ..base_menu import BaseMenu
from ....services.security_service import SecurityService

logger = logging.getLogger(__name__)

class SecurityMenu(BaseMenu):
    """Menu for managing security settings."""
    
    def __init__(self, parent: BaseMenu = None):
        """Initialize the menu.
        
        Args:
            parent: Optional parent menu for navigation.
        """
        super().__init__(parent)
        self.security_service = SecurityService()
    
    def show(self) -> None:
        """Display the security menu."""
        self.clear_screen()
        self.render_header("Security Settings")
        
        options: Dict[str, Callable] = {
            '1': self.manage_api_keys,
            '2': self.manage_ip_whitelist,
            '3': self.show_audit_log
        }
        
        while self.prompt_choice(options):
            self.clear_screen()
            self.render_header("Security Settings")
    
    def manage_api_keys(self) -> bool:
        """Manage API keys.
        
        Returns:
            True to continue menu loop.
        """
        try:
            # Get current API keys
            keys = self.security_service.list_api_keys()
            
            # Display keys
            table = Table(show_header=True, header_style="bold blue")
            table.add_column("#")
            table.add_column("Name")
            table.add_column("Created")
            table.add_column("Last Used")
            table.add_column("Status")
            
            for i, key in enumerate(keys, 1):
                table.add_row(
                    str(i),
                    key.name,
                    key.created_at.strftime("%Y-%m-%d"),
                    key.last_used_at.strftime("%Y-%m-%d") if key.last_used_at else "Never",
                    "Active" if key.active else "Inactive"
                )
            
            self.console.print("\n[bold]API Keys[/bold]")
            self.console.print(table)
            
            # Show options
            key_options: Dict[str, Callable] = {
                'c': self.create_api_key,
                'r': self.revoke_api_key,
                'b': lambda: False
            }
            
            self.console.print("\nOptions:")
            self.console.print("c. Create New Key")
            self.console.print("r. Revoke Key")
            self.console.print("b. Back")
            
            return self.prompt_choice(key_options)
            
        except Exception as e:
            logger.exception("Error managing API keys")
            self.console.print(f"[red]Error: {str(e)}[/red]")
            return True
    
    def create_api_key(self) -> bool:
        """Create a new API key.
        
        Returns:
            True to continue menu loop.
        """
        try:
            name = self.prompt_input(
                "\nEnter key name: ",
                lambda x: bool(x.strip())
            )
            
            key = self.security_service.create_api_key(name)
            
            self.console.print("\n[green]API Key created successfully![/green]")
            self.console.print("[bold red]Save these credentials now. The secret will not be shown again.[/bold red]")
            self.console.print(f"Key SID: {key.sid}")
            self.console.print(f"Key Secret: {key.secret}")
            
            return True
            
        except Exception as e:
            logger.exception("Error creating API key")
            self.console.print(f"[red]Error: {str(e)}[/red]")
            return True
    
    def revoke_api_key(self) -> bool:
        """Revoke an existing API key.
        
        Returns:
            True to continue menu loop.
        """
        try:
            sid = self.prompt_input(
                "\nEnter key SID to revoke: ",
                lambda x: bool(re.match(r'^SK[a-f0-9]{32}$', x))
            )
            
            if not sid:
                return True
            
            confirm = self.prompt_input(
                "\nType 'REVOKE' to confirm: ",
                lambda x: x == 'REVOKE'
            )
            
            if confirm:
                self.security_service.revoke_api_key(sid)
                self.console.print("\n[green]API Key revoked successfully![/green]")
            
            return True
            
        except Exception as e:
            logger.exception("Error revoking API key")
            self.console.print(f"[red]Error: {str(e)}[/red]")
            return True
    
    def manage_ip_whitelist(self) -> bool:
        """Manage IP address whitelist.
        
        Returns:
            True to continue menu loop.
        """
        try:
            # Get current whitelist
            ips = self.security_service.list_ip_whitelist()
            
            # Display IPs
            table = Table(show_header=True, header_style="bold blue")
            table.add_column("#")
            table.add_column("IP/CIDR")
            table.add_column("Added")
            table.add_column("Description")
            
            for i, ip in enumerate(ips, 1):
                table.add_row(
                    str(i),
                    ip.cidr,
                    ip.added_at.strftime("%Y-%m-%d"),
                    ip.description or ""
                )
            
            self.console.print("\n[bold]IP Whitelist[/bold]")
            self.console.print(table)
            
            # Show options
            ip_options: Dict[str, Callable] = {
                'a': self.add_ip,
                'r': self.remove_ip,
                'b': lambda: False
            }
            
            self.console.print("\nOptions:")
            self.console.print("a. Add IP/CIDR")
            self.console.print("r. Remove IP/CIDR")
            self.console.print("b. Back")
            
            return self.prompt_choice(ip_options)
            
        except Exception as e:
            logger.exception("Error managing IP whitelist")
            self.console.print(f"[red]Error: {str(e)}[/red]")
            return True
    
    def add_ip(self) -> bool:
        """Add an IP or CIDR to the whitelist.
        
        Returns:
            True to continue menu loop.
        """
        try:
            cidr = self.prompt_input(
                "\nEnter IP/CIDR (e.g. 192.168.1.0/24): ",
                self.validate_cidr
            )
            
            if not cidr:
                return True
            
            description = self.prompt_input(
                "Enter description (optional): "
            )
            
            self.security_service.add_ip_to_whitelist(
                cidr=cidr,
                description=description
            )
            
            self.console.print("\n[green]IP/CIDR added successfully![/green]")
            return True
            
        except Exception as e:
            logger.exception("Error adding IP to whitelist")
            self.console.print(f"[red]Error: {str(e)}[/red]")
            return True
    
    def remove_ip(self) -> bool:
        """Remove an IP or CIDR from the whitelist.
        
        Returns:
            True to continue menu loop.
        """
        try:
            cidr = self.prompt_input(
                "\nEnter IP/CIDR to remove: ",
                self.validate_cidr
            )
            
            if not cidr:
                return True
            
            confirm = self.prompt_input(
                "\nType 'REMOVE' to confirm: ",
                lambda x: x == 'REMOVE'
            )
            
            if confirm:
                self.security_service.remove_ip_from_whitelist(cidr)
                self.console.print("\n[green]IP/CIDR removed successfully![/green]")
            
            return True
            
        except Exception as e:
            logger.exception("Error removing IP from whitelist")
            self.console.print(f"[red]Error: {str(e)}[/red]")
            return True
    
    def show_audit_log(self) -> bool:
        """Show security audit log.
        
        Returns:
            True to continue menu loop.
        """
        try:
            # Get audit log entries
            entries = self.security_service.get_audit_log()
            
            # Display entries
            table = Table(show_header=True, header_style="bold blue")
            table.add_column("Time")
            table.add_column("Action")
            table.add_column("Actor")
            table.add_column("Details")
            
            for entry in entries:
                table.add_row(
                    entry.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    entry.action,
                    entry.actor,
                    entry.details
                )
            
            self.console.print("\n[bold]Security Audit Log[/bold]")
            self.console.print(table)
            
            return True
            
        except Exception as e:
            logger.exception("Error showing audit log")
            self.console.print(f"[red]Error: {str(e)}[/red]")
            return True
    
    def validate_cidr(self, cidr: str) -> bool:
        """Validate IP/CIDR format.
        
        Args:
            cidr: IP/CIDR to validate.
            
        Returns:
            True if valid, False otherwise.
        """
        if not cidr:
            return True
            
        # Basic CIDR validation
        try:
            ip, prefix = cidr.split('/')
            prefix = int(prefix)
            
            # Validate IP format
            parts = ip.split('.')
            if len(parts) != 4:
                return False
                
            for part in parts:
                num = int(part)
                if num < 0 or num > 255:
                    return False
            
            # Validate prefix
            if prefix < 0 or prefix > 32:
                return False
            
            return True
            
        except ValueError:
            return False