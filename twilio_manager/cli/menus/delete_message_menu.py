from twilio_manager.cli.menus.base_menu import BaseMenu
from twilio_manager.shared.ui.styling import (
    console,
    print_panel,
    print_success,
    print_error,
    print_warning,
    print_info,
    prompt_choice,
    STYLES
)

class DeleteMessageMenu(BaseMenu):
    def show(self):
        """Display the delete message menu."""
        options = {
            "1": "Delete a message",
            "0": "Return to previous menu"
        }
        self.display("Delete Message", "🗑️", options)

    def handle_choice(self, choice):
        """Handle the user's menu choice."""
        if choice == "1":
            from twilio_manager.cli.commands.send_message_command import (
                get_message_sid,
                confirm_deletion_prompt,
                delete_message_by_sid
            )
            
            # Get message SID
            message_sid = get_message_sid()
            if not message_sid:
                self.print_warning("No message SID provided.")
                self.pause_and_return()
                return

            # Confirm deletion
            if not confirm_deletion_prompt(message_sid):
                self.print_warning("Deletion cancelled.")
                self.pause_and_return()
                return

            # Execute deletion
            success = delete_message_by_sid(message_sid)
            if success:
                self.print_success(f"Message {message_sid} deleted successfully!")
            else:
                self.print_error(f"Failed to delete message {message_sid}")
            self.pause_and_return()