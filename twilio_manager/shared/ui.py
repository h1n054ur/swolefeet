from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

def print_title(text):
    console.print(Panel.fit(f"[bold cyan]{text}[/bold cyan]", title="Twilio CLI", border_style="blue"))

def print_success(message):
    console.print(f"[green]✅ {message}[/green]")

def print_error(message):
    console.print(f"[red]❌ {message}[/red]")

def print_warning(message):
    console.print(f"[yellow]⚠️ {message}[/yellow]")

def print_divider():
    console.rule("[dim]────────────────────────────")
