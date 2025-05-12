from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from twilio_manager.core.phone_numbers import release_number

console = Console()

def handle_release_command():
    console.clear()
    console.print(Panel.fit("[bold cyan]🗑 Release a Phone Number[/bold cyan]"))

    sid_or_number = Prompt.ask("Enter phone number SID or E.164 format (e.g., +14155552671)")

    confirm = Confirm.ask(
        f"[red]Are you sure you want to release number {sid_or_number}? This action is irreversible.[/red]"
    )
    if not confirm:
        console.print("[yellow]Release cancelled.[/yellow]")
        return

    success = release_number(sid_or_number)

    if success:
        console.print(f"[green]✅ Number {sid_or_number} released successfully.[/green]")
    else:
        console.print(f"[red]❌ Failed to release number {sid_or_number}.[/red]")

    Prompt.ask("\nPress Enter to return")
