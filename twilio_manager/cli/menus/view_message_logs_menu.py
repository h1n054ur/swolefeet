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
    def show(self):
        """Display message logs with pagination."""
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
        formatted_logs = []
        for log in logs:
            if isinstance(log, dict):  # Ensure log is a dictionary
                formatted_logs.append(format_message_log_entry(log))
            else:
                self.print_warning(f"Skipping malformed log entry: {log}")
                continue

        if not formatted_logs:
            self.print_warning("No valid message logs to display.")
            self.pause_and_return()
            return

        # Initialize pagination
        self.page_size = 10
        self.current_page = 1
        self.total_pages = (len(formatted_logs) + self.page_size - 1) // self.page_size
        self.formatted_logs = formatted_logs

        # Show first page
        self._show_current_page()

    def _show_current_page(self):
        """Display the current page of logs."""
        # Calculate page range
        start_idx = (self.current_page - 1) * self.page_size
        end_idx = min(start_idx + self.page_size, len(self.formatted_logs))
        page_logs = self.formatted_logs[start_idx:end_idx]

        # Create and display table
        table = create_table(
            columns=["From", "To", "Body", "Status", "Date"],
            title=f"Message Logs (Page {self.current_page}/{self.total_pages})"
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

        console.print("\n")
        console.print(table)

        # Show navigation options
        options = {"0": "Return to menu"}
        if self.total_pages > 1:
            if self.current_page > 1:
                options["P"] = "Previous page"
            if self.current_page < self.total_pages:
                options["N"] = "Next page"

        self.display(
            title="Message Logs Navigation",
            emoji="📜",
            options=options
        )

    def handle_choice(self, choice):
        """Handle navigation choice."""
        choice = choice.upper()
        if choice == "P" and self.current_page > 1:
            self.current_page -= 1
            self._show_current_page()
        elif choice == "N" and self.current_page < self.total_pages:
            self.current_page += 1
            self._show_current_page()
        else:
            self.return_to_parent()