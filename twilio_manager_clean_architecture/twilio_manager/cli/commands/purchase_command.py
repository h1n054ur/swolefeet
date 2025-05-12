from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from twilio_manager.core.phone_numbers import purchase_number

console = Console()

def handle_purchase_command():
    console.clear()
    console.print(Panel.fit("[bold cyan]🛒 Purchase a Phone Number[/bold cyan]"))

    number = Prompt.ask("Enter phone number to purchase (E.164 format, e.g., +14155552671)")

    confirm = Confirm.ask(f"Are you sure you want to purchase [bold green]{number}[/bold green]?")
    if not confirm:
        console.print("[yellow]Purchase cancelled.[/yellow]")
        return

    success = purchase_number(number)

    if success:
        console.print(f"[green]✅ Number {number} purchased successfully![/green]")
    else:
        console.print(f"[red]❌ Failed to purchase number {number}.[/red]")

    Prompt.ask("\nPress Enter to return")
