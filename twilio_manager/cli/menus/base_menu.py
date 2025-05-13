from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

class BaseMenu(ABC):
    def __init__(self, title: str, menu_title: str = "Menu"):
        self.console = Console()
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
        self.console.clear()
        self.console.print(Panel.fit(f"[bold cyan]{self.title}[/bold cyan]", title=self.menu_title))
        
        for key, (label, _) in self._options.items():
            self.console.print(f"[bold magenta]{key}.[/bold magenta] {label}")
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
        title_text = f"[bold cyan]{self.title}[/bold cyan]"
        if subtitle:
            title_text += f"\n[dim cyan]{subtitle}[/dim cyan]"
        self.console.print(Panel.fit(title_text, title=self.menu_title))

    def prompt_enter(self, message: str = "Press Enter to continue") -> None:
        """Show a prompt to press Enter."""
        Prompt.ask(f"\n{message}")