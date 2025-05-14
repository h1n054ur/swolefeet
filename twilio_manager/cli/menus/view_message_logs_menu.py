from twilio_manager.cli.menus.base_menu import BaseMenu
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
from twilio_manager.cli.commands.view_logs_command import (
    get_message_logs_list,
    format_message_log_entry
)

class ViewMessageLogsMenu(BaseMenu):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.page_size = 10
        self.current_page = 1
        self.total_pages = 1
        self.formatted_logs = []

    def show(self):
        """Display message logs with pagination."""
        # Clear screen and show title
        console.clear()
        print_panel("Message Logs", style='highlight')

        # Get logs
        logs, error = get_message_logs_list()
        if error:
            self.print_error(f"Failed to fetch message logs: {error}")
            self.pause_and_return()
            return
        
        if not logs:
            self.print_warning("No message logs found.")
            self.pause_and_return()
            return

        # Format logs
        self.formatted_logs = []
        skipped = 0
        for log in logs:
            if isinstance(log, dict):  # Ensure log is a dictionary
                self.formatted_logs.append(format_message_log_entry(log))
            else:
                skipped += 1
                continue

        if skipped > 0:
            self.print_warning(f"Skipped {skipped} malformed log entries")

        if not self.formatted_logs:
            self.print_warning("No valid message logs to display.")
            self.pause_and_return()
            return

        # Initialize pagination
        self.current_page = 1
        self.total_pages = (len(self.formatted_logs) + self.page_size - 1) // self.page_size

        # Show first page
        self._show_current_page()

    def _show_current_page(self):
        """Display the current page of logs."""
        # Calculate page range
        start_idx = (self.current_page - 1) * self.page_size
        end_idx = min(start_idx + self.page_size, len(self.formatted_logs))
        page_logs = self.formatted_logs[start_idx:end_idx]

        # Show title
        print_panel(f"Message Logs (Page {self.current_page}/{self.total_pages})", style='highlight')

        # Create and display table
        table = create_table(
            columns=["From", "To", "Body", "Status", "Date"],
            title=None  # Remove title since we're showing it in panel
        )

        for log in page_logs:
            table.add_row(
                log['from'],
                log['to'],
                log['body'],
                log['status'],
                log['date_sent'],
                style=STYLES['data']
            )

        console.print(table)
        console.print("")  # Add spacing

        # Show navigation options
        options = {"0": "Return to menu"}
        if self.total_pages > 1:
            if self.current_page > 1:
                options["P"] = "Previous page"
            if self.current_page < self.total_pages:
                options["N"] = "Next page"

        # Show options without using display() to avoid clearing screen
        print_panel("Navigation Options:", style='highlight')
        for key, value in options.items():
            console.print(f"{key}. {value}", style=STYLES['data'])
        console.print("")

        # Get user choice
        choice = prompt_choice(
            "Select an option",
            choices=list(options.keys()),
            default="0"
        )

        # Handle the choice
        self.handle_choice(choice)

    def handle_choice(self, choice):
        """Handle navigation choice."""
        choice = choice.upper()
        if choice == "0":
            return  # Return to parent menu
        elif choice == "P" and self.current_page > 1:
            self.current_page -= 1
            self._show_current_page()
        elif choice == "N" and self.current_page < self.total_pages:
            self.current_page += 1
            self._show_current_page()