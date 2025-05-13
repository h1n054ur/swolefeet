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

class SendMessageMenu(BaseMenu):
    def show(self):
        """Display the send message menu."""
        options = {
            "1": "Send a new message",
            "0": "Return to previous menu"
        }
        self.display("Send Message", "📱", options)

    def handle_choice(self, choice):
        """Handle the user's menu choice."""
        if choice == "1":
            from twilio_manager.cli.commands.send_message_command import (
                collect_message_inputs,
                validate_recipient_number,
                send_message_with_confirmation
            )
            
            # Get message inputs
            inputs = collect_message_inputs()
            if not inputs:
                return

            # Validate recipient
            if not validate_recipient_number(inputs['to_number']):
                print_error("Invalid recipient number format.")
                return

            # Send message with confirmation
            send_message_with_confirmation(
                inputs['from_number'],
                inputs['to_number'],
                inputs['body']
            )