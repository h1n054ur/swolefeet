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

class RecordingsMenu(BaseMenu):
    def show(self):
        """Display the recordings management menu."""
        options = {
            "1": "View recordings",
            "2": "Delete a recording",
            "0": "Return to previous menu"
        }
        self.display("Call Recordings", "🎙️", options)

    def handle_choice(self, choice):
        """Handle the user's menu choice."""
        from twilio_manager.cli.commands.call_command import (
            get_recordings,
            delete_recording,
            display_recordings,
            get_recording_sid
        )

        if choice == "1":
            # View recordings
            recordings = get_recordings()
            if not recordings:
                print_warning("No recordings found.")
                prompt_choice("\nPress Enter to return", choices=[""], default="")
                return

            display_recordings(recordings)

        elif choice == "2":
            # Delete a recording
            recordings = get_recordings()
            if not recordings:
                print_warning("No recordings found.")
                prompt_choice("\nPress Enter to return", choices=[""], default="")
                return

            # Display recordings and get SID
            display_recordings(recordings)
            recording_sid = get_recording_sid()
            if not recording_sid:
                return

            # Delete the recording
            delete_recording(recording_sid)