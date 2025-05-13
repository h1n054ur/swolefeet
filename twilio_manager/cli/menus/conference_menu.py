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

class ConferenceMenu(BaseMenu):
    def show(self):
        """Display the conference management menu."""
        options = {
            "1": "View active conferences",
            "2": "Join a conference",
            "3": "End a conference",
            "0": "Return to previous menu"
        }
        self.display("Conference Calls", "👥", options)

    def handle_choice(self, choice):
        """Handle the user's menu choice."""
        from twilio_manager.cli.commands.call_command import (
            list_conferences,
            join_conference,
            end_conference,
            display_conferences,
            get_conference_sid
        )

        if choice == "1":
            # View conferences
            conferences = list_conferences()
            if not conferences:
                print_warning("No active conferences found.")
                prompt_choice("\nPress Enter to return", choices=[""], default="")
                return

            display_conferences(conferences)

        elif choice == "2":
            # Join conference
            conferences = list_conferences()
            if not conferences:
                print_warning("No active conferences found.")
                prompt_choice("\nPress Enter to return", choices=[""], default="")
                return

            # Display conferences and get SID
            display_conferences(conferences)
            conference_sid = get_conference_sid("join")
            if not conference_sid:
                return

            # Join the conference
            join_conference(conference_sid)

        elif choice == "3":
            # End conference
            conferences = list_conferences()
            if not conferences:
                print_warning("No active conferences found.")
                prompt_choice("\nPress Enter to return", choices=[""], default="")
                return

            # Display conferences and get SID
            display_conferences(conferences)
            conference_sid = get_conference_sid("end")
            if not conference_sid:
                return

            # End the conference
            end_conference(conference_sid)