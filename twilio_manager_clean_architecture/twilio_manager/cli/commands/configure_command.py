from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from twilio_manager.core.phone_numbers import configure_number

console = Console()

def handle_configure_command():
    console.clear()
    console.print(Panel.fit("[bold cyan]⚙️ Configure a Phone Number[/bold cyan]"))

    sid_or_number = Prompt.ask("Enter phone number SID or E.164 number (e.g., +14155552671)")

    friendly_name = Prompt.ask("Friendly name (optional)", default="")
    voice_url = Prompt.ask("Voice webhook URL (optional)", default="")
    sms_url = Prompt.ask("SMS webhook URL (optional)", default="")

    confirm = Confirm.ask("[bold yellow]Apply these settings?[/bold yellow]")
    if not confirm:
        console.print("[yellow]Configuration cancelled.[/yellow]")
        return

    success = configure_number(
        sid_or_number,
        friendly_name=friendly_name or None,
        voice_url=voice_url or None,
        sms_url=sms_url or None
    )

    if success:
        console.print(f"[green]✅ Number configured successfully![/green]")
    else:
        console.print(f"[red]❌ Failed to update number settings.[/red]")

    Prompt.ask("\nPress Enter to return")
