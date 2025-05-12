from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from twilio_manager.core.voice import make_call

console = Console()

def handle_make_call_command():
    console.clear()
    console.print(Panel.fit("[bold cyan]📞 Make a Voice Call[/bold cyan]"))

    from_number = Prompt.ask("From (your Twilio number, e.g., +14155552671)")
    to_number = Prompt.ask("To (recipient number, e.g., +14155559876)")
    voice_url = Prompt.ask("Voice URL (TwiML/Webhook)", default="https://handler.twilio.com/twiml/EHxxxxx")

    confirm = Confirm.ask(f"Place call from [green]{from_number}[/green] to [cyan]{to_number}[/cyan]?")
    if not confirm:
        console.print("[yellow]Call cancelled.[/yellow]")
        return

    success = make_call(from_number, to_number, voice_url)

    if success:
        console.print(f"[green]✅ Call initiated successfully![/green]")
    else:
        console.print(f"[red]❌ Failed to place the call.[/red]")

    Prompt.ask("\nPress Enter to return")
