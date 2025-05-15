"""Base menu class that all menus will extend."""

import os
import platform
from typing import Callable, Dict, Optional, TypeVar, Any
from rich.console import Console
from rich.panel import Panel
from rich.style import Style

T = TypeVar('T')

class BaseMenu:
    """Base class for all menus in the application."""
    
    # Shared console instance
    console = Console()
    
    # Common styles
    STYLES = {
        'header': Style(color="blue", bold=True),
        'error': Style(color="red", bold=True),
        'success': Style(color="green"),
        'prompt': Style(color="yellow"),
        'option': Style(color="cyan"),
    }
    
    def __init__(self, parent: Optional['BaseMenu'] = None):
        """Initialize the menu.
        
        Args:
            parent: Optional parent menu for navigation.
        """
        self.parent = parent
    
    def clear_screen(self) -> None:
        """Clear the terminal screen."""
        os.system('cls' if platform.system() == 'Windows' else 'clear')
    
    def render_header(self, title: str) -> None:
        """Render a header with the given title.
        
        Args:
            title: The title to display in the header.
        """
        self.console.print(Panel(
            title,
            style=self.STYLES['header'],
            expand=False
        ))
    
    def prompt_choice(self, options: Dict[str, Callable]) -> bool:
        """Prompt for a choice from the given options.
        
        Args:
            options: Dictionary mapping option keys to their handler functions.
            
        Returns:
            True if the menu should continue, False to exit.
        """
        # Add back option if we have a parent
        if self.parent is not None:
            options['b'] = lambda: False
        
        # Add exit option
        options['q'] = lambda: False
        
        while True:
            # Display options
            self.console.print("\nOptions:", style=self.STYLES['prompt'])
            for key, func in options.items():
                # Get function name or docstring for display
                name = func.__name__.replace('_', ' ').title()
                if func.__doc__:
                    name = func.__doc__.split('\n')[0]
                
                # Special cases for navigation
                if key == 'b':
                    name = "Back"
                elif key == 'q':
                    name = "Exit"
                
                self.console.print(
                    f"[{key}] {name}",
                    style=self.STYLES['option']
                )
            
            # Get choice
            choice = self.prompt_input(
                "\nEnter your choice: ",
                lambda x: x.lower() in options
            )
            
            if choice.lower() == 'q':
                return False
            
            if choice.lower() == 'b' and self.parent is not None:
                return False
            
            # Execute the chosen option
            result = options[choice.lower()]()
            if result is False:
                return False
            
            # Continue the menu loop
            return True
    
    def prompt_input(
        self,
        label: str,
        validator: Optional[Callable[[str], bool]] = None,
        error_msg: str = "Invalid input"
    ) -> str:
        """Prompt for input with optional validation.
        
        Args:
            label: The prompt label to display.
            validator: Optional function to validate the input.
            error_msg: Message to display on validation failure.
            
        Returns:
            The validated input string.
        """
        while True:
            value = input(label)
            if validator is None or validator(value):
                return value
            self.console.print(error_msg, style=self.STYLES['error'])
    
    def show(self) -> None:
        """Display the menu and handle input.
        
        This should be overridden by subclasses to implement
        specific menu behavior.
        """
        raise NotImplementedError(
            "Subclasses must implement show()"
        )
