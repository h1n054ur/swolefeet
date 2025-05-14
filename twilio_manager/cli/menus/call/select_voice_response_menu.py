from twilio_manager.cli.menus.base_menu import BaseMenu
from twilio_manager.shared.ui.styling import (
    print_panel,
    prompt_choice
)

class SelectVoiceResponseMenu(BaseMenu):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_url = None
        self.state = 'main'  # main, custom

    def show(self):
        """Display menu to select voice response URL."""
        self.state = 'main'
        options = {
            "1": "Use default greeting",
            "2": "Custom TwiML URL"
        }
        
        self.display(
            title="Select Voice Response",
            emoji="🔊",
            options=options
        )
        
        return self.selected_url

    def handle_choice(self, choice):
        """Handle the user's menu selection."""
        if self.state == 'main':
            if choice == "1":
                self.selected_url = "https://handler.twilio.com/twiml/default-greeting"
                self.print_success("Using default greeting")
                self.pause_and_return()
            elif choice == "2":
                self.state = 'custom'
                self.handle_custom_url()

    def handle_custom_url(self):
        """Handle custom TwiML URL entry."""
        url = prompt_choice("Enter TwiML URL", choices=None)
        if url:
            self.selected_url = url
            self.print_success(f"Using custom URL: {url}")
        else:
            self.print_warning("No URL entered")
        self.pause_and_return()