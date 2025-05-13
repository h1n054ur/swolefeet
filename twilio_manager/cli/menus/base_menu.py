from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from rich.prompt import Prompt

from twilio_manager.shared.styles import (
    console, COLORS, ICONS,
    show_title as show_styled_title,
    print_success, print_error, print_warning
)

class BaseMenu(ABC):
    def __init__(self, title: str, menu_title: str = "Menu"):
        self.console = console  # Use shared console instance
        self.title = title
        self.menu_title = menu_title
        self._options: Dict[str, tuple[str, Any]] = {}
        self._setup_options()

    @abstractmethod
    def _setup_options(self) -> None:
        """Setup menu options. Must be implemented by subclasses."""
        pass

    def add_option(self, key: str, label: str, handler: Any, emoji: str = "") -> None:
        """Add a menu option with its handler."""
        self._options[key] = (f"{emoji} {label}" if emoji else label, handler)

    def _display_menu(self) -> None:
        """Display the menu with consistent styling."""
        self.clear_screen()
        show_styled_title(self.title, self.menu_title)
        
        for key, (label, _) in self._options.items():
            self.console.print(f"[{COLORS['header']}]{key}.[/{COLORS['header']}] {label}")
        self.console.print()

    def _get_valid_choices(self) -> List[str]:
        """Get list of valid choice keys."""
        return list(self._options.keys())

    def show(self) -> None:
        """Display the menu and handle user input."""
        while True:
            self._display_menu()
            
            choice = Prompt.ask(
                "Choose an option",
                choices=self._get_valid_choices(),
                default="0"
            )
            
            if choice in self._options:
                _, handler = self._options[choice]
                if callable(handler):
                    result = handler()
                    if result is True:  # Explicit return to previous menu
                        break
                elif handler is True:  # Return to previous menu
                    break
                elif handler is False:  # Exit application
                    return False

    def clear_screen(self) -> None:
        """Clear the screen."""
        self.console.clear()

    def show_title(self, subtitle: Optional[str] = None) -> None:
        """Show a title panel with optional subtitle."""
        show_styled_title(self.title, subtitle)

    def prompt_enter(self, message: str = "Press Enter to continue") -> None:
        """Show a prompt to press Enter."""
        Prompt.ask(f"\n{message}")

    def print_success(self, message: str) -> None:
        """Print a success message."""
        print_success(message)

    def print_error(self, message: str) -> None:
        """Print an error message."""
        print_error(message)

    def print_warning(self, message: str) -> None:
        """Print a warning message."""
        print_warning(message)