from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.style import Style
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.status import Status
from twilio_manager.shared.utils.logger import get_logger

logger = get_logger(__name__)

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
    try:
        console.clear()
    except Exception as e:
        logger.warning(f"Failed to clear screen: {str(e)}")
        # Fallback to printing newlines
        console.print("\n" * 100)

def print_header(title, emoji=""):
    """Print a header panel with a title and optional emoji.
    
    Args:
        title (str): The title text to display
        emoji (str): Optional emoji to display before the title
    """
    try:
        console.print(f"[bold cyan]{emoji} {title}[/bold cyan]\n")
    except Exception as e:
        logger.error(f"Error printing header: {str(e)}")
        # Fallback to simple print
        print(f"{emoji} {title}\n")

def prompt_choice(prompt_text, choices, default="0"):
    """Prompt the user to make a choice from a list of options.
    
    Args:
        prompt_text (str): The text to display for the prompt
        choices (list): List of valid choices
        default (str): Default choice if user presses enter
    
    Returns:
        str: The user's selected choice
    """
    try:
        return Prompt.ask(prompt_text, choices=choices, default=default)
    except Exception as e:
        logger.error(f"Error in prompt: {str(e)}")
        # Fallback to basic input
        while True:
            choice = input(f"{prompt_text} [{'/'.join(choices)}] ").strip() or default
            if choice in choices:
                return choice

def print_panel(text, title=None, style='info'):
    """Print text in a panel with an optional title.
    
    Args:
        text (str): The text to display in the panel
        title (str, optional): The title for the panel
        style (str, optional): Style to use from STYLES dict. Defaults to 'info'
    """
    try:
        console.print(Panel.fit(text, title=title, style=STYLES[style]))
    except Exception as e:
        logger.error(f"Error printing panel: {str(e)}")
        # Fallback to simple print
        if title:
            print(f"\n{title}")
        print(text)

def print_success(message):
    """Print a success message.
    
    Args:
        message (str): The success message to display
    """
    try:
        console.print(f"✅ {message}", style=STYLES['success'])
    except Exception as e:
        logger.error(f"Error printing success: {str(e)}")
        print(f"SUCCESS: {message}")

def print_error(message):
    """Print an error message.
    
    Args:
        message (str): The error message to display
    """
    try:
        console.print(f"❌ {message}", style=STYLES['error'])
    except Exception as e:
        logger.error(f"Error printing error: {str(e)}")
        print(f"ERROR: {message}")

def print_warning(message):
    """Print a warning message.
    
    Args:
        message (str): The warning message to display
    """
    try:
        console.print(f"⚠️ {message}", style=STYLES['warning'])
    except Exception as e:
        logger.error(f"Error printing warning: {str(e)}")
        print(f"WARNING: {message}")

def print_info(message):
    """Print an info message.
    
    Args:
        message (str): The info message to display
    """
    try:
        console.print(f"ℹ️ {message}", style=STYLES['info'])
    except Exception as e:
        logger.error(f"Error printing info: {str(e)}")
        print(f"INFO: {message}")

def create_table(title=None, columns=None, width=None):
    """Create a Rich table with consistent styling.
    
    Args:
        title (str, optional): Title for the table
        columns (list, optional): List of column names
        width (int, optional): Maximum width for the table
    
    Returns:
        Table: A Rich table object
    """
    try:
        # Get terminal width if not specified
        if width is None:
            width = console.width or 80
            width = min(width - 2, 120)  # Leave some margin
        
        # Create table with proper width and border style
        table = Table(
            title=title,
            show_header=True if columns else False,
            width=width,
            box=None,  # Use simpler box style for better compatibility
            padding=(0, 1),  # Reduce padding for better space usage
            show_edge=False  # Hide outer edges for cleaner look
        )
        
        if columns:
            # Calculate default column widths
            num_cols = len(columns)
            default_width = max(10, (width - (num_cols * 2)) // num_cols)
            
            for col in columns:
                table.add_column(
                    col,
                    style=STYLES['header'],
                    width=default_width,
                    overflow='ellipsis'
                )
        
        return table
        
    except Exception as e:
        logger.error(f"Error creating table: {str(e)}", exc_info=True)
        # Fallback to basic table
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
    try:
        return Confirm.ask(prompt_text, default=default)
    except Exception as e:
        logger.error(f"Error in confirmation: {str(e)}")
        # Fallback to basic input
        while True:
            choice = input(f"{prompt_text} (y/n) ").strip().lower()
            if choice in ('y', 'yes'):
                return True
            if choice in ('n', 'no'):
                return False
            if not choice and default is not None:
                return default

def create_spinner(message):
    """Create a spinner with message for long-running operations.
    
    Args:
        message (str): Message to display with the spinner
    
    Returns:
        Status: A Rich status object that can be used as context manager
    """
    try:
        return Status(message, spinner="dots")
    except Exception as e:
        logger.error(f"Error creating spinner: {str(e)}")
        # Return a dummy context manager
        class DummyStatus:
            def __enter__(self):
                print(message + "...")
                return self
            def __exit__(self, *args):
                pass
        return DummyStatus()