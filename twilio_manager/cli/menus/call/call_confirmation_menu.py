from twilio_manager.cli.menus.base_menu import BaseMenu
from twilio_manager.shared.ui.styling import (
    console,
    print_panel,
    print_success,
    print_error,
    print_warning,
    prompt_choice,
    confirm_action,
    STYLES
)
from twilio_manager.core.voice import make_call

class CallConfirmationMenu(BaseMenu):
    def __init__(self, parent=None, from_number=None, to_number=None, voice_url=None):
        """Initialize the call confirmation menu.
        
        Args:
            parent (BaseMenu, optional): Parent menu
            from_number (str): The caller's phone number
            to_number (str): The recipient's phone number
            voice_url (str): The voice URL for the call
        """
        super().__init__(parent)
        self.from_number = from_number
        self.to_number = to_number
        self.voice_url = voice_url
        self.success = False

    def show(self):
        """Display call confirmation menu."""
        # Show call details
        print_panel("Review call details:", style='highlight')
        console.print("From:", style=STYLES['dim'])
        console.print(self.from_number, style=STYLES['success'])
        console.print("\nTo:", style=STYLES['dim'])
        console.print(self.to_number, style=STYLES['info'])
        console.print("\nVoice URL:", style=STYLES['dim'])
        console.print(self.voice_url, style=STYLES['warning'])

        # Display menu options
        self.display("Call Confirmation", "📞", {
            "1": "Place Call",
            "0": "Cancel"
        })

    def handle_choice(self, choice):
        """Handle call confirmation choice.
        
        Args:
            choice (str): The user's selected option
        """
        if choice != "1":
            self.print_warning("Call cancelled.")
            self.pause_and_return()
            return

        if not confirm_action("\nPlace this call?"):
            self.print_warning("Call cancelled.")
            self.pause_and_return()
            return

        success = make_call(self.from_number, self.to_number, self.voice_url)
        self.success = success

        if success:
            self.print_success("Call initiated successfully!")
        else:
            self.print_error("Failed to place the call.")

        self.pause_and_return()