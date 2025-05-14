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

class CallMenu(BaseMenu):
    def show(self):
        """Display the voice call menu."""
        options = {
            "1": "Make a voice call",
            "0": "Return to previous menu"
        }
        self.display("Voice Call", "📞", options)

    def handle_choice(self, choice):
        """Handle the user's menu choice."""
        if choice == "1":
            from twilio_manager.cli.commands.call_command import (
                collect_call_inputs,
                initiate_call
            )
            
            # Get call inputs
            inputs = collect_call_inputs()
            if not inputs:
                return

            # Place the call
            initiate_call(
                inputs['from_number'],
                inputs['to_number'],
                inputs['voice_url']
            )