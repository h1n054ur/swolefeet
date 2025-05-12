from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.panel import Panel

from twilio_manager.core.messaging import get_message_logs
from twilio_manager.core.voice import get_call_logs

console = Console()

def handle_view_message_logs_command():
    console.clear()
    console.print(Panel.fit("[bold cyan]📄 Message Logs[/bold cyan]"))

    logs = get_message_logs()

    if not logs:
        console.print("[red]No message logs found.[/red]")
        Prompt.ask("\nPress Enter to return")
        return

    table = Table(title="Message Logs", show_lines=True)
    table.add_column("From", style="cyan")
    table.add_column("To", style="green")
    table.add_column("Body", style="white")
    table.add_column("Status", style="magenta")
    table.add_column("Date", style="dim")

    for log in logs:
        table.add_row(
            log.get("from", "—"),
            log.get("to", "—"),
            log.get("body", "")[:40] + "...",
            log.get("status", "—"),
            log.get("date_sent", "—")
        )

    console.print(table)
    Prompt.ask("\nPress Enter to return")


def handle_view_call_logs_command():
    console.clear()
    console.print(Panel.fit("[bold cyan]📄 Call Logs[/bold cyan]"))

    logs = get_call_logs()

    if not logs:
        console.print("[red]No call logs found.[/red]")
        Prompt.ask("\nPress Enter to return")
        return

    table = Table(title="Call Logs", show_lines=True)
    table.add_column("From", style="cyan")
    table.add_column("To", style="green")
    table.add_column("Status", style="magenta")
    table.add_column("Duration", justify="right")
    table.add_column("Start Time", style="dim")

    for log in logs:
        table.add_row(
            log.get("from", "—"),
            log.get("to", "—"),
            log.get("status", "—"),
            str(log.get("duration", "0")),
            log.get("start_time", "—")
        )

    console.print(table)
    Prompt.ask("\nPress Enter to return")
