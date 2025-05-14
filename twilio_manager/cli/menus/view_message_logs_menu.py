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
        logs = get_message_logs_list()
        if not logs:
            print_error("No message logs found.")
            prompt_choice("\nPress Enter to return", choices=[""], default="")
            return

        # Format logs
        formatted_logs = [format_message_log_entry(log) for log in logs]

        # Display logs with pagination
        page_size = 10
        current_page = 1
        total_pages = (len(formatted_logs) + page_size - 1) // page_size

        while True:
            # Calculate page range
            start_idx = (current_page - 1) * page_size
            end_idx = min(start_idx + page_size, len(formatted_logs))
            page_logs = formatted_logs[start_idx:end_idx]

            # Create and display table
            table = create_table(
                columns=["From", "To", "Body", "Status", "Date"],
                title=f"Message Logs (Page {current_page}/{total_pages})"
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
            print_panel("Options:", style='highlight')
            console.print("0. Return to menu", style=STYLES['data'])
            if total_pages > 1:
                if current_page > 1:
                    console.print("P/p. Previous page", style=STYLES['data'])
                if current_page < total_pages:
                    console.print("N/n. Next page", style=STYLES['data'])

            # Get user choice
            choices = ["0"]
            if total_pages > 1:
                if current_page > 1:
                    choices.extend(["P", "p"])
                if current_page < total_pages:
                    choices.extend(["N", "n"])

            choice = prompt_choice(
                "Select an option",
                choices=choices,
                default="0"
            )

            if choice == "0":
                break
            elif choice.upper() == "P" and current_page > 1:
                current_page -= 1
            elif choice.upper() == "N" and current_page < total_pages:
                current_page += 1