from twilio_manager.core.messaging import get_message_logs
from twilio_manager.core.voice import get_call_logs
from twilio_manager.shared.ui.styling import (
    console,
    create_table,
    print_panel,
    print_success,
    print_error,
    print_warning,
    print_info,
    prompt_choice,
    STYLES
)

def format_message_log_entry(log):
    """Format a single message log entry.
    
    Args:
        log (dict): Message log entry
        
    Returns:
        list: Formatted row values
    """
    return [
        log.get("from", "—"),
        log.get("to", "—"),
        log.get("body", "")[:40] + "...",
        log.get("status", "—"),
        log.get("date_sent", "—")
    ]

def display_message_logs(logs):
    """Display message logs in a table.
    
    Args:
        logs (list): List of message log entries
    """
    table = create_table(
        columns=["From", "To", "Body", "Status", "Date"],
        title="Message Logs"
    )

    for log in logs:
        table.add_row(
            *format_message_log_entry(log),
            style=STYLES['data']
        )

    console.print(table)
    prompt_choice("\nPress Enter to return", choices=[""], default="")

def handle_view_message_logs_command():
    """Display message logs."""
    from twilio_manager.cli.menus.view_message_logs_menu import ViewMessageLogsMenu
    ViewMessageLogsMenu().show()


def handle_view_call_logs_command():
    """Display call logs."""


    logs = get_call_logs()

    if not logs:
        print_error("No call logs found.")
        prompt_choice("\nPress Enter to return", choices=[""], default="")
        return

    table = create_table(
        columns=["From", "To", "Status", "Duration", "Start Time"],
        title="Call Logs"
    )

    for log in logs:
        table.add_row(
            log.get("from", "—"),
            log.get("to", "—"),
            log.get("status", "—"),
            str(log.get("duration", "0")),
            log.get("start_time", "—"),
            style=STYLES['data']
        )

    console.print(table)
    prompt_choice("\nPress Enter to return", choices=[""], default="")
