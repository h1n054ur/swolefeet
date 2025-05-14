from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.style import Style
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.status import Status

# Create a single console instance to be used across the application
console = Console()

# Define consistent styles
STYLES = {
    'success': Style(color="green", bold=True),
    'error': Style(color="red", bold=True),
    'warning': Style(color="yellow", bold=True),
    'info': Style(color="blue"),
    'highlight': Style(color="cyan", bold=True),
    'prompt': Style(color="yellow"),
    'header': Style(color="cyan", bold=True),
    'subheader': Style(color="cyan"),
    'data': Style(color="white"),
    'dim': Style(color="grey70"),
}

def clear_screen():
    """Clear the terminal screen."""
    console.clear()

def print_header(title, emoji=""):
    """Print a header panel with a title and optional emoji.
    
    Args:
        title (str): The title text to display
        emoji (str): Optional emoji to display before the title
    """
    console.print(f"[bold cyan]{emoji} {title}[/bold cyan]\n")

def prompt_choice(prompt_text, choices, default="0"):
    """Prompt the user to make a choice from a list of options.
    
    Args:
        prompt_text (str): The text to display for the prompt
        choices (list): List of valid choices
        default (str): Default choice if user presses enter
    
    Returns:
        str: The user's selected choice
    """
    return Prompt.ask(prompt_text, choices=choices, default=default, show_choices=False)

def print_panel(text, title=None, style='info'):
    """Print text in a panel with an optional title.
    
    Args:
        text (str): The text to display in the panel
        title (str, optional): The title for the panel
        style (str, optional): Style to use from STYLES dict. Defaults to 'info'
    """
    console.print(Panel.fit(text, title=title, style=STYLES[style]))

def print_success(message):
    """Print a success message.
    
    Args:
        message (str): The success message to display
    """
    console.print(f"✅ {message}", style=STYLES['success'])

def print_error(message):
    """Print an error message.
    
    Args:
        message (str): The error message to display
    """
    console.print(f"❌ {message}", style=STYLES['error'])

def print_warning(message):
    """Print a warning message.
    
    Args:
        message (str): The warning message to display
    """
    console.print(f"⚠️ {message}", style=STYLES['warning'])

def print_info(message):
    """Print an info message.
    
    Args:
        message (str): The info message to display
    """
    console.print(f"ℹ️ {message}", style=STYLES['info'])

def create_table(title=None, columns=None):
    """Create a Rich table with consistent styling.
    
    Args:
        title (str, optional): Title for the table
        columns (list, optional): List of column names
    
    Returns:
        Table: A Rich table object
    """
    table = Table(title=title, show_header=True if columns else False)
    if columns:
        for col in columns:
            table.add_column(col, style=STYLES['header'])
    return table

def confirm_action(prompt_text, default=False):
    """Prompt for user confirmation with consistent styling.
    
    Args:
        prompt_text (str): The confirmation prompt text
        default (bool, optional): Default response. Defaults to False
    
    Returns:
        bool: True if confirmed, False otherwise
    """
    return Confirm.ask(prompt_text, default=default)

def create_spinner(message):
    """Create a spinner with message for long-running operations.
    
    Args:
        message (str): Message to display with the spinner
    
    Returns:
        Status: A Rich status object that can be used as context manager
    """
    return Status(message, spinner="dots")