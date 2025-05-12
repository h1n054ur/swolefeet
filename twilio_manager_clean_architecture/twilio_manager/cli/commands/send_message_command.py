from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from twilio_manager.core.messaging import send_message

console = Console()

def handle_send_message_command():
    console.clear()
    console.print(Panel.fit("[bold cyan]✉️ Send a Message[/bold cyan]"))

    from_number = Prompt.ask("From (your Twilio number, e.g., +14155552671)")
    to_number = Prompt.ask("To (recipient's number, e.g., +14155559876)")
    body = Prompt.ask("Message body")

    confirm = Confirm.ask(f"Send message to [bold green]{to_number}[/bold green]?")
    if not confirm:
        console.print("[yellow]Message not sent.[/yellow]")
        return

    success = send_message(from_number, to_number, body)

    if success:
        console.print(f"[green]✅ Message sent successfully to {to_number}![/green]")
    else:
        console.print(f"[red]❌ Failed to send message to {to_number}.[/red]")

    Prompt.ask("\nPress Enter to return")
