# flows/helpers/account_mgmt/voice_caller_ids.py

from twilio.rest import Client
from config.settings import ACCOUNT_SID, API_KEY_SID, API_KEY_SECRET
from utils.ui import console, clear_screen
from rich.console import Group
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.table import Table
from rich.prompt import Prompt

client = Client(API_KEY_SID, API_KEY_SECRET, ACCOUNT_SID)

def handle_caller_ids_menu():
    while True:
        clear_screen()
        content = Group(
            Text("📞 Outgoing Caller IDs", style="bold cyan", justify="center"),
            Text("Manage and view verified caller IDs.", style="green"),
            Text(""),
            Text("1. View Caller IDs"),
            Text("2. Configure Caller IDs"),
            Text("3. Back"),
            Text(""),
            Text("Enter your choice (1-3):", justify="center")
        )
        panel = Panel(content, border_style="green", padding=(1, 4))
        console.print(Align.center(panel, vertical="middle"))

        choice = console.input("\n> ").strip()

        if choice == "1":
            view_caller_ids()
        elif choice == "2":
            configure_caller_id()
        elif choice == "3":
            return
        else:
            console.print("[red]Invalid choice. Please try again.[/red]")
            console.input("Press Enter to continue...")

def view_caller_ids():
    clear_screen()
    console.print("[bold cyan]📞 Verified Caller IDs[/bold cyan]")

    try:
        caller_ids = client.outgoing_caller_ids.list(limit=20)

        if not caller_ids:
            console.print("[yellow]No verified caller IDs found.[/yellow]")
            console.input("Press Enter to return...")
            return

        table = Table(title="Caller IDs", header_style="bold green")
        table.add_column("Phone Number", style="cyan")
        table.add_column("Friendly Name", style="magenta")

        for item in caller_ids:
            table.add_row(item.phone_number, item.friendly_name or "(unnamed)")

        console.print(table)

    except Exception as e:
        console.print(f"[red]Error fetching caller IDs: {e}[/red]")

    console.input("Press Enter to return...")

def configure_caller_id():
    clear_screen()
    console.print("[bold green]🛠 Add a New Caller ID[/bold green]")

    try:
        number = Prompt.ask("Enter the phone number to verify (E.164 format, e.g. +1234567890)")
        friendly = Prompt.ask("Enter a friendly name (optional)", default="")

        result = client.outgoing_caller_ids.create(
            phone_number=number,
            friendly_name=friendly or None
        )

        console.print(
            f"\n[green]✅ Caller ID initiated for verification![/green]\n"
            f"[white]Twilio will call [bold]{number}[/bold] with a verification code.[/white]"
        )

    except Exception as e:
        console.print(f"[red]Error adding caller ID: {e}[/red]")

    console.input("Press Enter to return...")
