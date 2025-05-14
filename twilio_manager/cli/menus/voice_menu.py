from twilio_manager.cli.menus.base_menu import BaseMenu
from twilio_manager.shared.constants import MENU_TITLES
from twilio_manager.cli.commands.call_command import handle_make_call_command
from twilio_manager.cli.menus.view_call_logs_menu import ViewCallLogsMenu
# from cli.commands.recording_command import handle_manage_recordings  # Optional future
# from cli.commands.conference_command import handle_conference_calls  # Optional future

class VoiceMenu(BaseMenu):
    def show(self):
        """Display the voice call management menu."""
        title, emoji = MENU_TITLES["voice"]
        self.display(title, emoji, {
            "1": "📞 Make a Call",
            "2": "📄 View Call Logs",
            # "3": "🎙 Manage Recordings",
            # "4": "👥 Conference Calls",
            "0": "🔙 Back"
        })

    def handle_choice(self, choice):
        """Handle the user's menu choice.
        
        Args:
            choice (str): The user's selected option
        """
        if choice == "1":
            handle_make_call_command()
        elif choice == "2":
            ViewCallLogsMenu().show()
        # elif choice == "3":
        #     handle_manage_recordings()
        # elif choice == "4":
        #     handle_conference_calls()
