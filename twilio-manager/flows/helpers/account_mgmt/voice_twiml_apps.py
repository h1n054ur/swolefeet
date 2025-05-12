# flows/helpers/account_mgmt/voice_twiml_apps.py

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

def handle_twiml_apps_menu():
    while True:
        clear_screen()
        content = Group(
            Text("🧩 TwiML Apps", style="bold cyan", justify="center"),
            Text("Manage and view TwiML applications linked to your numbers.", style="green"),
            Text(""),
            Text("1. View TwiML Apps"),
            Text("2. Configure TwiML Apps"),
            Text("3. Back"),
            Text(""),
            Text("Enter your choice (1-3):", justify="center")
        )
        panel = Panel(content, border_style="green", padding=(1, 4))
        console.print(Align.center(panel, vertical="middle"))

        choice = console.input("\n> ").strip()

        if choice == "1":
            view_twiml_apps()
        elif choice == "2":
            configure_twiml_app()
        elif choice == "3":
            return
        else:
            console.print("[red]Invalid choice. Please try again.[/red]")
            console.input("Press Enter to continue...")

def view_twiml_apps():
    clear_screen()
    console.print("[bold cyan]🧩 TwiML Applications[/bold cyan]")

    try:
        apps = client.applications.list(limit=20)

        if not apps:
            console.print("[yellow]No TwiML applications found.[/yellow]")
            console.input("Press Enter to return...")
            return

        table = Table(title="TwiML Apps", header_style="bold green")
        table.add_column("Name", style="cyan")
        table.add_column("SID", style="magenta", overflow="fold")
        table.add_column("Voice URL", style="white", overflow="fold")

        for app in apps:
            table.add_row(app.friendly_name, app.sid, app.voice_url or "(none)")

        console.print(table)

    except Exception as e:
        console.print(f"[red]Error fetching TwiML Apps: {e}[/red]")

    console.input("Press Enter to return...")

def configure_twiml_app():
    clear_screen()
    console.print("[bold green]🛠 Create a New TwiML App[/bold green]")

    try:
        name = Prompt.ask("Enter a name for the TwiML app")
        voice_url = Prompt.ask("Enter the Voice Request URL (e.g. https://handler.twilio.com/twiml/XYZ)")

        app = client.applications.create(
            friendly_name=name,
            voice_url=voice_url
        )

        console.print(
            f"\n[green]✅ TwiML App created![/green]\n"
            f"[white]SID: [bold]{app.sid}[/bold][/white]"
        )

    except Exception as e:
        console.print(f"[red]Error creating TwiML App: {e}[/red]")

    console.input("Press Enter to return...")
