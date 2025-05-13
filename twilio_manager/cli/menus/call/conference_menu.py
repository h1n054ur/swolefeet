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
from twilio_manager.cli.commands.call_command import (
    list_conferences,
    join_conference,
    end_conference
)
from twilio_manager.cli.menus.call.select_caller_menu import SelectCallerMenu

class ConferenceMenu(BaseMenu):
    def show(self):
        """Display conference management menu."""
        while True:
            conferences = list_conferences()
            if not conferences:
                print_warning("No active conferences found.")
                prompt_choice("\nPress Enter to return", choices=[""], default="")
                return

            self._display_conferences(conferences)
            
            print_panel("Options:", style='highlight')
            console.print("1. Join a conference", style=STYLES['data'])
            console.print("2. End a conference", style=STYLES['data'])
            console.print("0. Return to menu", style=STYLES['data'])
            
            choice = prompt_choice("\nSelect an option", choices=["0", "1", "2"], default="0")
            
            if choice == "0":
                break
            elif choice == "1":
                self._handle_join_conference()
            elif choice == "2":
                self._handle_end_conference()

    def _display_conferences(self, conferences):
        """Display conferences in a table."""
        table = create_table(
            columns=["#", "SID", "Name", "Status", "Participants"],
            title="Active Conferences"
        )

        for idx, conf in enumerate(conferences, 1):
            table.add_row(
                str(idx),
                conf.get('sid', '—'),
                conf.get('friendly_name', '—'),
                conf.get('status', '—'),
                str(conf.get('participant_count', 0)),
                style=STYLES['data']
            )

        console.print(table)

    def _handle_join_conference(self):
        """Handle joining a conference."""
        conference_sid = prompt_choice(
            "\nEnter conference SID to join (0 to cancel)",
            choices=None,
            default="0"
        )

        if conference_sid == "0":
            print_warning("Conference join cancelled.")
            return

        # Get number to join with
        from_number = SelectCallerMenu().show()
        if not from_number:
            return

        success = join_conference(conference_sid, from_number)

        if success:
            print_success(f"Successfully joined conference {conference_sid}!")
        else:
            print_error(f"Failed to join conference {conference_sid}.")

        prompt_choice("\nPress Enter to return", choices=[""], default="")

    def _handle_end_conference(self):
        """Handle ending a conference."""
        conference_sid = prompt_choice(
            "\nEnter conference SID to end (0 to cancel)",
            choices=None,
            default="0"
        )

        if conference_sid == "0":
            print_warning("Conference end cancelled.")
            return

        if not confirm_action(
            f"Are you sure you want to end conference {conference_sid}? "
            "All participants will be disconnected.",
            style='error'
        ):
            print_warning("Conference end cancelled.")
            return

        success = end_conference(conference_sid)

        if success:
            print_success(f"Conference {conference_sid} ended successfully!")
        else:
            print_error(f"Failed to end conference {conference_sid}.")

        prompt_choice("\nPress Enter to return", choices=[""], default="")