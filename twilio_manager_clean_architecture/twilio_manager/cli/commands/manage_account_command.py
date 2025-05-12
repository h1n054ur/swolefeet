from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.panel import Panel

from twilio_manager.core.account import (
    get_account_info,
    list_subaccounts,
    list_api_keys,
    list_sip_trunks,
    list_twiml_apps
)

console = Console()

def handle_view_account_info():
    console.clear()
    console.print(Panel.fit("[bold cyan]👤 Account Info / Balance[/bold cyan]"))

    info = get_account_info()
    if not info:
        console.print("[red]Failed to retrieve account information.[/red]")
    else:
        table = Table(title="Account Info")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="white")

        for key, value in info.items():
            table.add_row(key, str(value))
        console.print(table)

    Prompt.ask("\nPress Enter to return")


def handle_subaccount_management():
    console.clear()
    console.print(Panel.fit("[bold cyan]👥 Subaccount List[/bold cyan]"))

    subs = list_subaccounts()
    if not subs:
        console.print("[yellow]No subaccounts found.[/yellow]")
    else:
        table = Table(title="Subaccounts", show_lines=True)
        table.add_column("SID", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("Status", style="magenta")

        for sub in subs:
            table.add_row(sub["sid"], sub["friendly_name"], sub["status"])

        console.print(table)

    Prompt.ask("\nPress Enter to return")


def handle_api_key_management():
    console.clear()
    console.print(Panel.fit("[bold cyan]🔑 API Key List[/bold cyan]"))

    keys = list_api_keys()
    if not keys:
        console.print("[yellow]No API keys found.[/yellow]")
    else:
        table = Table(title="API Keys", show_lines=True)
        table.add_column("SID", style="cyan")
        table.add_column("Friendly Name", style="green")

        for key in keys:
            table.add_row(key["sid"], key["friendly_name"])

        console.print(table)

    Prompt.ask("\nPress Enter to return")


def handle_sip_trunk_menu():
    console.clear()
    console.print(Panel.fit("[bold cyan]🔌 SIP Trunks[/bold cyan]"))

    trunks = list_sip_trunks()
    if not trunks:
        console.print("[yellow]No SIP trunks found.[/yellow]")
    else:
        table = Table(title="SIP Trunks", show_lines=True)
        table.add_column("SID", style="cyan")
        table.add_column("Friendly Name", style="green")
        table.add_column("Voice Region", style="magenta")

        for trunk in trunks:
            table.add_row(trunk["sid"], trunk["friendly_name"], trunk.get("voice_region", "—"))

        console.print(table)

    Prompt.ask("\nPress Enter to return")


def handle_twiml_app_menu():
    console.clear()
    console.print(Panel.fit("[bold cyan]🧠 TwiML Applications[/bold cyan]"))

    apps = list_twiml_apps()
    if not apps:
        console.print("[yellow]No TwiML applications found.[/yellow]")
    else:
        table = Table(title="TwiML Apps", show_lines=True)
        table.add_column("SID", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("Voice URL", style="magenta")

        for app in apps:
            table.add_row(app["sid"], app["friendly_name"], app.get("voice_url", "—"))

        console.print(table)

    Prompt.ask("\nPress Enter to return")
