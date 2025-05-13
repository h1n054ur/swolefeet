"""Shared styling constants and utilities for consistent UI appearance."""
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# Shared console instance
console = Console()

# Color schemes
COLORS = {
    'title': 'bold cyan',
    'header': 'bold magenta',
    'success': 'green',
    'error': 'red',
    'warning': 'yellow',
    'info': 'cyan',
    'dim': 'dim',
    'highlight': 'bold green',
    'normal': 'white'
}

# Icons
ICONS = {
    'success': '✅',
    'error': '❌',
    'warning': '⚠️',
    'info': 'ℹ️',
    'back': '🔙',
    'phone': '📞',
    'message': '✉️',
    'settings': '⚙️',
    'search': '🔍',
    'delete': '🗑',
    'user': '👤',
    'users': '👥',
    'key': '🔑',
    'brain': '🧠',
    'docs': '📄'
}

def create_table(title: str = None, show_lines: bool = True) -> Table:
    """Create a consistently styled table."""
    table = Table(
        title=title,
        show_lines=show_lines,
        header_style=COLORS['header']
    )
    return table

def show_title(title: str, subtitle: str = None) -> None:
    """Display a consistently styled title panel."""
    title_text = f"[{COLORS['title']}]{title}[/{COLORS['title']}]"
    if subtitle:
        title_text += f"\n[{COLORS['dim']}]{subtitle}[/{COLORS['dim']}]"
    console.print(Panel.fit(title_text))

def print_success(message: str) -> None:
    """Print a success message."""
    console.print(f"[{COLORS['success']}]{ICONS['success']} {message}[/{COLORS['success']}]")

def print_error(message: str) -> None:
    """Print an error message."""
    console.print(f"[{COLORS['error']}]{ICONS['error']} {message}[/{COLORS['error']}]")

def print_warning(message: str) -> None:
    """Print a warning message."""
    console.print(f"[{COLORS['warning']}]{ICONS['warning']} {message}[/{COLORS['warning']}]")

def print_info(message: str) -> None:
    """Print an info message."""
    console.print(f"[{COLORS['info']}]{ICONS['info']} {message}[/{COLORS['info']}]")

def format_phone_number(number: str) -> str:
    """Format a phone number for display."""
    return f"[{COLORS['highlight']}]{number}[/{COLORS['highlight']}]"

def format_status(status: str) -> str:
    """Format a status message with appropriate color."""
    if status.lower() in ['success', 'completed', 'active']:
        return f"[{COLORS['success']}]{status}[/{COLORS['success']}]"
    elif status.lower() in ['error', 'failed', 'inactive']:
        return f"[{COLORS['error']}]{status}[/{COLORS['error']}]"
    else:
        return f"[{COLORS['normal']}]{status}[/{COLORS['normal']}]"