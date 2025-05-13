from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from abc import ABC, abstractmethod

class BaseMenu(ABC):
    def __init__(self):
        self.console = Console()
        self._setup_styles()

    def _setup_styles(self):
        """Define common styling properties"""
        self.styles = {
            'title_style': "[bold cyan]",
            'option_style': "[bold magenta]",
            'back_option': "0",
            'back_text': "🔙 Back",
            'exit_text': "❌ Exit",
            'panel_border_style': "cyan",
        }

    def clear_screen(self):
        """Clear the screen and show the menu title"""
        self.console.clear()
        self.console.print(Panel.fit(
            f"{self.styles['title_style']}{self.get_title()}[/]",
            title=self.get_menu_name(),
            border_style=self.styles['panel_border_style']
        ))

    def print_option(self, key, text, emoji=""):
        """Print a menu option with consistent styling"""
        emoji_str = f"{emoji} " if emoji else ""
        self.console.print(f"{self.styles['option_style']}{key}.[/] {emoji_str}{text}")

    def get_choice(self, choices, default="0", show_choices=True):
        """Get user choice with consistent styling"""
        return Prompt.ask("\nChoose an option", choices=choices, default=default, show_choices=show_choices)

    def show_error(self, message):
        """Show error message with consistent styling"""
        self.console.print(f"\n[red]{message}[/red]")

    def show_success(self, message):
        """Show success message with consistent styling"""
        self.console.print(f"\n[green]{message}[/green]")

    def show_info(self, message):
        """Show info message with consistent styling"""
        self.console.print(f"\n[blue]{message}[/blue]")

    def wait_for_input(self, message="Press Enter to continue"):
        """Wait for user input with consistent styling"""
        Prompt.ask(f"\n{message}")

    @abstractmethod
    def get_title(self):
        """Return the menu title with emoji"""
        pass

    @abstractmethod
    def get_menu_name(self):
        """Return the menu name for the panel title"""
        pass

    @abstractmethod
    def get_options(self):
        """Return a list of tuples (key, text, emoji) for menu options"""
        pass

    @abstractmethod
    def handle_choice(self, choice):
        """Handle the user's menu choice"""
        pass

    def show(self):
        """Display the menu and handle user input"""
        while True:
            self.clear_screen()
            
            # Print menu options
            for key, text, emoji in self.get_options():
                self.print_option(key, text, emoji)
            
            self.console.print("")  # Add spacing
            
            # Get valid choices
            choices = [opt[0] for opt in self.get_options()]
            choice = self.get_choice(choices)
            
            # Handle the choice
            should_exit = self.handle_choice(choice)
            if should_exit:
                break