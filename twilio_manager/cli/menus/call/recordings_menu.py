from twilio_manager.cli.menus.base_menu import BaseMenu
from twilio_manager.shared.ui.styling import (
    console,
    create_table,
    print_panel,
    print_success,
    print_error,
    print_warning,
    prompt_choice,
    confirm_action,
    STYLES
)
from twilio_manager.cli.commands.call_command import get_recordings, delete_recording

class RecordingsMenu(BaseMenu):
    def show(self):
        """Display recordings management menu."""
        while True:
            recordings = get_recordings()
            if not recordings:
                print_warning("No recordings found.")
                prompt_choice("\nPress Enter to return", choices=[""], default="")
                return

            self._display_recordings(recordings)
            
            print_panel("Options:", style='highlight')
            console.print("1. Delete a recording", style=STYLES['data'])
            console.print("0. Return to menu", style=STYLES['data'])
            
            choice = prompt_choice("\nSelect an option", choices=["0", "1"], default="0")
            
            if choice == "0":
                break
            elif choice == "1":
                self._handle_delete_recording()

    def _display_recordings(self, recordings):
        """Display recordings in a table."""
        table = create_table(
            columns=["#", "SID", "Call SID", "Duration", "Date"],
            title="Call Recordings"
        )

        for idx, recording in enumerate(recordings, 1):
            table.add_row(
                str(idx),
                recording.get('sid', '—'),
                recording.get('call_sid', '—'),
                str(recording.get('duration', '0')) + "s",
                recording.get('date_created', '—'),
                style=STYLES['data']
            )

        console.print(table)

    def _handle_delete_recording(self):
        """Handle recording deletion."""
        recording_sid = prompt_choice(
            "\nEnter recording SID to delete (0 to cancel)",
            choices=None,
            default="0"
        )

        if recording_sid == "0":
            print_warning("Deletion cancelled.")
            return

        if not confirm_action(
            f"Are you sure you want to delete recording {recording_sid}? "
            "This action cannot be undone.",
            style='error'
        ):
            print_warning("Deletion cancelled.")
            return

        success = delete_recording(recording_sid)

        if success:
            print_success(f"Recording {recording_sid} deleted successfully!")
        else:
            print_error(f"Failed to delete recording {recording_sid}.")

        prompt_choice("\nPress Enter to return", choices=[""], default="")