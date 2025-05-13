from functools import wraps
from typing import Callable, Optional

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.spinner import Spinner
from rich.live import Live

from twilio_manager.shared.styles import StyleConfig

console = Console(theme=StyleConfig.get_theme())

def with_loading(message: str = None):
    """Decorator to show loading spinner while executing a function."""
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            spinner = Spinner("dots", text=message or StyleConfig.LOADING_MESSAGES["default"])
            try:
                with Live(spinner, refresh_per_second=10):
                    result = func(*args, **kwargs)
                return result
            except Exception as e:
                console.clear()
                console.print(f"[error]Error: {str(e)}[/error]")
                console.input("\nPress Enter to continue...")
                return True  # Continue showing menu
        return wrapper
    return decorator

class BaseMenu:
    """Base class for all menus with standardized styling and behavior."""
    
    def __init__(self, title: str, menu_type: str):
        self.title = title
        self.menu_type = menu_type
        self.options = []
        self.has_back = False
    
    def add_option(self, key: str, text: str, handler: Callable, icon: str = None) -> None:
        """Add a menu option with handler."""
        self.options.append({
            "key": key,
            "text": text,
            "handler": handler,
            "icon": icon
        })
    
    def add_back_option(self) -> None:
        """Add a back option to the menu."""
        self.has_back = True
        self.add_option("0", "Back", lambda: True, "back")
    
    def clear_screen(self) -> None:
        """Clear the screen properly."""
        console.clear()
        console.print("\033[2J\033[H", end="")  # ANSI escape codes for full screen clear

    def render_menu(self) -> None:
        """Render the menu with consistent styling."""
        self.clear_screen()
        console.print(Panel.fit(
            StyleConfig.format_menu_title(self.title, self.menu_type),
            title=self.menu_type
        ))
        
        for option in self.options:
            console.print(StyleConfig.format_menu_option(
                option["key"],
                option["text"],
                option["icon"]
            ))
        console.print()
    
    def get_choice(self) -> str:
        """Get user choice with validation."""
        valid_choices = [opt["key"] for opt in self.options]
        return Prompt.ask(
            "Choose an option",
            choices=valid_choices,
            default="0" if self.has_back else valid_choices[0]
        )
    
    def handle_choice(self, choice: str) -> bool:
        """Handle menu choice and return whether to continue."""
        for option in self.options:
            if option["key"] == choice:
                try:
                    self.clear_screen()  # Clear screen before executing handler
                    console.print(Panel.fit(
                        StyleConfig.format_menu_title(self.title, self.menu_type),
                        title=self.menu_type
                    ))
                    console.print()  # Add spacing
                    result = option["handler"]()
                    if result is False:  # Only exit if explicitly False
                        return False
                    return True
                except Exception as e:
                    console.clear()
                    console.print(f"[error]Error: {str(e)}[/error]")
                    console.input("\nPress Enter to continue...")
                    return True
        return True
    
    def show(self) -> None:
        """Show the menu and handle user input."""
        while True:
            try:
                self.render_menu()
                choice = self.get_choice()
                
                if not self.handle_choice(choice):
                    self.clear_screen()  # Clear screen before exiting
                    break
            except Exception as e:
                console.clear()
                console.print(f"[error]Error: {str(e)}[/error]")
                console.input("\nPress Enter to continue...")
                continue