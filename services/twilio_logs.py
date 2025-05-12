from config.settings import ACCOUNT_SID
from services.api import twilio_request
from utils.ui import console, clear_screen
from rich.table import Table
from rich.box import SIMPLE


def view_call_logs(phone_number):
    from rich.console import Group
    from rich.text import Text
    from rich.align import Align
    from rich.panel import Panel

    clear_screen()

    endpoint = f"Accounts/{ACCOUNT_SID}/Calls.json"
    params = {"To": phone_number, "PageSize": 20}
    response = twilio_request("GET", endpoint, params=params)

    if not response or response.status_code != 200:
        return console.print("[red]❌ Failed to fetch call logs.[/red]")

    calls = response.json().get("calls", [])
    if not calls:
        return console.print("[yellow]📞 No call logs found.[/yellow]")

    table = Table(box=SIMPLE, header_style="bold magenta")
    table.add_column("Start Time", style="white")
    table.add_column("Direction", style="cyan")
    table.add_column("From", style="white")
    table.add_column("Duration", justify="right", style="green")

    for call in calls:
        table.add_row(
            call.get("start_time") or "(n/a)",
            call.get("direction", "N/A").capitalize(),
            call.get("from") or "(unknown)",
            f"{call.get('duration', '0')}s"
        )

    from rich.console import Group
    from rich.text import Text

    content = Group(
        Align.center(Text("📘 Twilio CLI Manager", style="bold cyan")),
        Align.center(Text(f"Call Logs for {phone_number}", style="bold green")),
        Text(""),
        table,
        Text(""),
        Align.center(Text("Press Enter to return...", style="dim"))
    )

    console.print(Align.center(Panel(content, border_style="green"), vertical="middle"))
    input()


def view_message_logs(phone_number):
    from rich.console import Group
    from rich.text import Text
    from rich.align import Align
    from rich.panel import Panel

    clear_screen()

    endpoint = f"Accounts/{ACCOUNT_SID}/Messages.json"
    params = {"To": phone_number, "PageSize": 20}
    response = twilio_request("GET", endpoint, params=params)

    if not response or response.status_code != 200:
        return console.print("[red]❌ Failed to fetch SMS logs.[/red]")

    messages = response.json().get("messages", [])
    if not messages:
        return console.print("[yellow]📩 No SMS logs found.[/yellow]")

    table = Table(box=SIMPLE, header_style="bold magenta")
    table.add_column("Date Sent", style="white")
    table.add_column("From", style="cyan")
    table.add_column("Body", style="white", overflow="fold")

    for msg in messages:
        table.add_row(
            msg.get("date_sent", "(n/a)"),
            msg.get("from", "(unknown)"),
            msg.get("body", "")[:100]
        )

    content = Group(
        Align.center(Text("📘 Twilio CLI Manager", style="bold cyan")),
        Align.center(Text(f"SMS Logs for {phone_number}", style="bold green")),
        Text(""),
        table,
        Text(""),
        Align.center(Text("Press Enter to return...", style="dim"))
    )

    console.print(Align.center(Panel(content, border_style="green"), vertical="middle"))
    input()
