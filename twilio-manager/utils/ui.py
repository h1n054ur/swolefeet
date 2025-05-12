# utils/ui.py

from rich.console import Console
from rich.panel import Panel
from rich.align import Align
import os

console = Console()


def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(title: str):
    """Print a centered header panel with a given title."""
    panel = Panel(f"[bold cyan]{title}[/bold cyan]", border_style="bright_blue", expand=False)
    console.print(Align.center(panel))


def print_main_menu():
    """Display the main menu options."""
    menu = "\n".join([
        "[bold cyan]1.[/] Search for new numbers",
        "[bold cyan]2.[/] Manage active numbers",
        "[bold cyan]3.[/] Exit"
    ])
    panel = Panel.fit(menu, title="[bold]Main Menu[/bold]", border_style="green")
    console.print(Align.center(panel))


def print_error(message: str):
    """Display an error message in red."""
    console.print(f"[red]❌ {message}[/red]")


def print_success(message: str):
    """Display a success message in green."""
    console.print(f"[green]✅ {message}[/green]")


def print_info(message: str):
    """Display an informational message in cyan."""
    console.print(f"[cyan]{message}[/cyan]")


def print_warning(message: str):
    """Display a warning message in yellow."""
    console.print(f"[yellow]⚠️ {message}[/yellow]")
