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
    def __init__(self, from_number, to_number, voice_url):
        super().__init__()
        self.from_number = from_number
        self.to_number = to_number
        self.voice_url = voice_url

    def show(self):
        """Display call confirmation screen and initiate call if confirmed."""
        # Show call details and confirm
        print_panel("Review call details:", style='highlight')
        console.print("From:", style=STYLES['dim'])
        console.print(self.from_number, style=STYLES['success'])
        console.print("\nTo:", style=STYLES['dim'])
        console.print(self.to_number, style=STYLES['info'])
        console.print("\nVoice URL:", style=STYLES['dim'])
        console.print(self.voice_url, style=STYLES['warning'])

        if not confirm_action("\nPlace this call?"):
            print_warning("Call cancelled.")
            return False

        success = make_call(self.from_number, self.to_number, self.voice_url)

        if success:
            print_success("Call initiated successfully!")
        else:
            print_error("Failed to place the call.")

        prompt_choice("\nPress Enter to return", choices=[""], default="")
        return success