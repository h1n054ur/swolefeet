from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

# Create a single console instance to be used across the application
console = Console()

def clear_screen():
    """Clear the terminal screen."""
    console.clear()

def print_header(title, emoji=""):
    """Print a header panel with a title and optional emoji.
    
    Args:
        title (str): The title text to display
        emoji (str): Optional emoji to display before the title
    """
    console.print(Panel.fit(f"[bold cyan]{emoji} {title}[/bold cyan]", title=f"{title} Menu"))

def prompt_choice(prompt_text, choices, default="0"):
    """Prompt the user to make a choice from a list of options.
    
    Args:
        prompt_text (str): The text to display for the prompt
        choices (list): List of valid choices
        default (str): Default choice if user presses enter
    
    Returns:
        str: The user's selected choice
    """
    return Prompt.ask(prompt_text, choices=choices, default=default)

def print_panel(text, title=None):
    """Print text in a panel with an optional title.
    
    Args:
        text (str): The text to display in the panel
        title (str, optional): The title for the panel
    """
    console.print(Panel.fit(text, title=title))