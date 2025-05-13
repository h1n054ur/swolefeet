from rich.table import Table
from twilio_manager.core.account import (
    get_account_info,
    list_subaccounts,
    list_api_keys,
    list_sip_trunks,
    list_twiml_apps
)
from twilio_manager.shared.ui.styling import (
    console,
    clear_screen,
    print_header,
    print_panel,
    prompt_choice
)

def handle_view_account_info():
    """Display account information and balance."""
    clear_screen()
    print_header("Account Info / Balance", "👤")

    info = get_account_info()
    if not info:
        print_panel("[red]Failed to retrieve account information.[/red]")
    else:
        table = Table(title="Account Info")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="white")

        for key, value in info.items():
            table.add_row(key, str(value))
        console.print(table)

    prompt_choice("\nPress Enter to return", choices=[""], default="")


def handle_subaccount_management():
    """Display list of subaccounts."""
    clear_screen()
    print_header("Subaccount List", "👥")

    subs = list_subaccounts()
    if not subs:
        print_panel("[yellow]No subaccounts found.[/yellow]")
    else:
        table = Table(title="Subaccounts", show_lines=True)
        table.add_column("SID", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("Status", style="magenta")

        for sub in subs:
            table.add_row(sub["sid"], sub["friendly_name"], sub["status"])

        console.print(table)

    prompt_choice("\nPress Enter to return", choices=[""], default="")


def handle_api_key_management():
    """Display list of API keys."""
    clear_screen()
    print_header("API Key List", "🔑")

    keys = list_api_keys()
    if not keys:
        print_panel("[yellow]No API keys found.[/yellow]")
    else:
        table = Table(title="API Keys", show_lines=True)
        table.add_column("SID", style="cyan")
        table.add_column("Friendly Name", style="green")

        for key in keys:
            table.add_row(key["sid"], key["friendly_name"])

        console.print(table)

    prompt_choice("\nPress Enter to return", choices=[""], default="")


def handle_sip_trunk_menu():
    """Display list of SIP trunks."""
    clear_screen()
    print_header("SIP Trunks", "🔌")

    trunks = list_sip_trunks()
    if not trunks:
        print_panel("[yellow]No SIP trunks found.[/yellow]")
    else:
        table = Table(title="SIP Trunks", show_lines=True)
        table.add_column("SID", style="cyan")
        table.add_column("Friendly Name", style="green")
        table.add_column("Voice Region", style="magenta")

        for trunk in trunks:
            table.add_row(trunk["sid"], trunk["friendly_name"], trunk.get("voice_region", "—"))

        console.print(table)

    prompt_choice("\nPress Enter to return", choices=[""], default="")


def handle_twiml_app_menu():
    """Display list of TwiML applications."""
    clear_screen()
    print_header("TwiML Applications", "🧠")

    apps = list_twiml_apps()
    if not apps:
        print_panel("[yellow]No TwiML applications found.[/yellow]")
    else:
        table = Table(title="TwiML Apps", show_lines=True)
        table.add_column("SID", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("Voice URL", style="magenta")

        for app in apps:
            table.add_row(app["sid"], app["friendly_name"], app.get("voice_url", "—"))

        console.print(table)

    prompt_choice("\nPress Enter to return", choices=[""], default="")
