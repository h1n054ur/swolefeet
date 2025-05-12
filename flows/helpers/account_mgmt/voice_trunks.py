# flows/helpers/account_mgmt/voice_trunks.py

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

def handle_sip_trunks_menu():
    while True:
        clear_screen()
        content = Group(
            Text("📡 SIP Trunks", style="bold cyan", justify="center"),
            Text("Manage and configure your SIP trunks.", style="green"),
            Text(""),
            Text("1. View SIP Trunks"),
            Text("2. Configure SIP Trunks"),
            Text("3. Back"),
            Text(""),
            Text("Enter your choice (1-3):", justify="center")
        )
        panel = Panel(content, border_style="green", padding=(1, 4))
        console.print(Align.center(panel, vertical="middle"))

        choice = console.input("\n> ").strip()

        if choice == "1":
            view_sip_trunks()
        elif choice == "2":
            configure_sip_trunk()
        elif choice == "3":
            return
        else:
            console.print("[red]Invalid choice. Please try again.[/red]")
            console.input("Press Enter to continue...")

def view_sip_trunks():
    clear_screen()
    console.print("[bold cyan]📡 SIP Trunks Overview[/bold cyan]")

    try:
        trunks = client.trunking.v1.trunks.list(limit=10)

        if not trunks:
            console.print("[yellow]No SIP trunks found.[/yellow]")
            console.input("Press Enter to return...")
            return

        table = Table(title="SIP Trunks", header_style="bold green")
        table.add_column("Friendly Name", style="cyan")
        table.add_column("SID", style="magenta", overflow="fold")

        for trunk in trunks:
            table.add_row(trunk.friendly_name or "(unnamed)", trunk.sid)

        console.print(table)

    except Exception as e:
        console.print(f"[red]Error fetching SIP trunks: {e}[/red]")

    console.input("Press Enter to return...")

def configure_sip_trunk():
    clear_screen()
    console.print("[bold green]🛠 Create a New SIP Trunk[/bold green]")

    try:
        friendly_name = Prompt.ask("Enter a name for the SIP trunk")
        trunk = client.trunking.v1.trunks.create(friendly_name=friendly_name)

        console.print(f"\n[green]✅ SIP Trunk created! SID: {trunk.sid}[/green]")
        console.input("Press Enter to return...")

    except Exception as e:
        console.print(f"[red]Error creating SIP trunk: {e}[/red]")
        console.input("Press Enter to return...")
