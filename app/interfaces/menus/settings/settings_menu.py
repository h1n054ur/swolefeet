"""Menu for managing settings and admin functions."""

import logging
from typing import Dict, Callable
from ..base_menu import BaseMenu
from .billing_menu import BillingMenu
from .security_menu import SecurityMenu
from .subaccount_menu import SubaccountMenu
from .dev_tools_menu import DevToolsMenu
from .account_logs_menu import AccountLogsMenu
from .advanced_search_menu import AdvancedSearchMenu
from .config_mgmt_menu import ConfigMgmtMenu
from .diagnostics_menu import DiagnosticsMenu

logger = logging.getLogger(__name__)

class SettingsMenu(BaseMenu):
    """Menu for managing settings and admin functions."""
    
    def show(self) -> None:
        """Display the settings menu."""
        self.clear_screen()
        self.render_header("Settings & Admin")
        
        options: Dict[str, Callable] = {
            '1': self.show_billing,
            '2': self.show_security,
            '3': self.show_subaccounts,
            '4': self.show_dev_tools,
            '5': self.show_account_logs,
            '6': self.show_advanced_search,
            '7': self.show_config_mgmt,
            '8': self.show_diagnostics
        }
        
        while self.prompt_choice(options):
            self.clear_screen()
            self.render_header("Settings & Admin")
    
    def show_billing(self) -> bool:
        """Show billing information and usage."""
        menu = BillingMenu(parent=self)
        menu.show()
        return True
    
    def show_security(self) -> bool:
        """Show security settings."""
        menu = SecurityMenu(parent=self)
        menu.show()
        return True
    
    def show_subaccounts(self) -> bool:
        """Show subaccount management."""
        menu = SubaccountMenu(parent=self)
        menu.show()
        return True
    
    def show_dev_tools(self) -> bool:
        """Show developer tools."""
        menu = DevToolsMenu(parent=self)
        menu.show()
        return True
    
    def show_account_logs(self) -> bool:
        """Show account-wide logs."""
        menu = AccountLogsMenu(parent=self)
        menu.show()
        return True
    
    def show_advanced_search(self) -> bool:
        """Show advanced search interface."""
        menu = AdvancedSearchMenu(parent=self)
        menu.show()
        return True
    
    def show_config_mgmt(self) -> bool:
        """Show configuration management."""
        menu = ConfigMgmtMenu(parent=self)
        menu.show()
        return True
    
    def show_diagnostics(self) -> bool:
        """Show system diagnostics."""
        menu = DiagnosticsMenu(parent=self)
        menu.show()
        return True