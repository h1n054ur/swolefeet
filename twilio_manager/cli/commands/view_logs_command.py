from rich.table import Table
from twilio_manager.core.messaging import get_message_logs
from twilio_manager.core.voice import get_call_logs
from twilio_manager.shared.ui.styling import (
    console,
    clear_screen,
    print_header,
    print_panel,
    prompt_choice
)

def handle_view_message_logs_command():
    """Display message logs."""
    clear_screen()
    print_header("Message Logs", "📄")

    logs = get_message_logs()

    if not logs:
        print_panel("[red]No message logs found.[/red]")
        prompt_choice("\nPress Enter to return", choices=[""], default="")
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
    prompt_choice("\nPress Enter to return", choices=[""], default="")


def handle_view_call_logs_command():
    """Display call logs."""
    clear_screen()
    print_header("Call Logs", "📄")

    logs = get_call_logs()

    if not logs:
        print_panel("[red]No call logs found.[/red]")
        prompt_choice("\nPress Enter to return", choices=[""], default="")
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
    prompt_choice("\nPress Enter to return", choices=[""], default="")
