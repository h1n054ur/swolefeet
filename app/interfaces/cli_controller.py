"""CLI Controller for the Twilio Manager application."""

import logging
from typing import Optional
from rich.console import Console
from ..gateways.config import load_settings
from ..shared.logging import configure_logging

logger = logging.getLogger(__name__)

class CLIController:
    """Main CLI controller that coordinates services and menus."""
    
    def __init__(self):
        """Initialize the CLI controller."""
        self.settings = load_settings()
        configure_logging(self.settings)
        self.console = Console()
        
        # Services will be initialized here in future phases
        self.services = {}
        
        # Menus will be initialized here in future phases
        self.menus = {}
        
        logger.info("CLI Controller initialized")
    
    def run(self) -> None:
        """Run the main CLI loop."""
        try:
            self.console.print("[bold blue]Twilio Manager CLI[/bold blue]")
            self.console.print("Loading...\n")
            
            # Menu system will be implemented in future phases
            self.console.print("[green]Main Menu[/green]")
            self.console.print("1. 📞 Purchase Numbers")
            self.console.print("2. 📟 Manage Numbers")
            self.console.print("3. 🧾 Settings & Admin")
            
            # Temporary placeholder for menu system
            self.console.print("\n[yellow]Menu system coming in future phases![/yellow]")
            
        except Exception as e:
            logger.exception("Fatal error in CLI controller")
            self.console.print(f"[red]Error: {str(e)}[/red]")
            raise
