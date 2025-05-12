# flows/helpers/account_mgmt/voice_inbound_settings.py

from twilio.rest import Client
from config.settings import ACCOUNT_SID, API_KEY_SID, API_KEY_SECRET
from utils.ui import console, clear_screen
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.console import Group
from rich.align import Align

client = Client(API_KEY_SID, API_KEY_SECRET, ACCOUNT_SID)

def handle_inbound_call_settings():
    clear_screen()
    console.print("[bold cyan]📥 Inbound Call Settings[/bold cyan]")

    try:
        numbers = client.incoming_phone_numbers.list(limit=20)

        if not numbers:
            console.print("[yellow]No phone numbers found on your account.[/yellow]")
            console.input("Press Enter to return...")
            return

        table = Table(title="Inbound Numbers", header_style="bold green")
        table.add_column("Phone Number", style="cyan")
        table.add_column("Voice URL", style="magenta", overflow="fold")
        table.add_column("TwiML App SID", style="white", overflow="fold")

        for number in numbers:
            table.add_row(
                number.phone_number,
                number.voice_url or "(not set)",
                number.voice_application_sid or "(none)"
            )

        console.print(table)

    except Exception as e:
        console.print(f"[red]Error fetching phone number settings: {e}[/red]")

    console.input("Press Enter to return...")
