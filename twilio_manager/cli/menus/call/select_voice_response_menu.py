from twilio_manager.cli.menus.base_menu import BaseMenu
from twilio_manager.shared.ui.styling import (
    print_panel,
    prompt_choice
)

class SelectVoiceResponseMenu(BaseMenu):
    def show(self):
        """Display menu to select voice response URL."""
        print_panel("Select voice response:", style='highlight')
        url_choice = prompt_choice(
            "Choose an option:\n1. Use default greeting\n2. Custom TwiML URL",
            choices=["1", "2"],
            default="1"
        )
        
        if url_choice == "1":
            return "https://handler.twilio.com/twiml/default-greeting"
        
        return prompt_choice("Enter TwiML URL", choices=None)