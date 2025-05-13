from twilio_manager.cli.menus.base_menu import BaseMenu
from twilio_manager.cli.commands.call_command import handle_make_call_command
from twilio_manager.cli.commands.view_logs_command import handle_view_call_logs_command
# from cli.commands.recording_command import handle_manage_recordings  # Optional future
# from cli.commands.conference_command import handle_conference_calls  # Optional future

class VoiceMenu(BaseMenu):
    def get_title(self):
        return "📞 Voice Call Management"

    def get_menu_name(self):
        return "Voice Menu"

    def get_options(self):
        return [
            ("1", "Make a Call", "📞"),
            ("2", "View Call Logs", "📄"),
            # ("3", "Manage Recordings", "🎙"),  # Optional future
            # ("4", "Conference Calls", "👥"),  # Optional future
            ("0", "Back", "🔙")
        ]

    def handle_choice(self, choice):
        if choice == "1":
            handle_make_call_command()
        elif choice == "2":
            handle_view_call_logs_command()
        # elif choice == "3":
        #     handle_manage_recordings()
        # elif choice == "4":
        #     handle_conference_calls()
        elif choice == "0":
            return True
        return False

def show_voice_menu():
    VoiceMenu().show()
