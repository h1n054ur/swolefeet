from twilio_manager.cli.menus.base_menu import BaseMenu
from twilio_manager.cli.commands.call_command import handle_make_call_command
from twilio_manager.cli.commands.view_logs_command import handle_view_call_logs_command
# from cli.commands.recording_command import handle_manage_recordings  # Optional future
# from cli.commands.conference_command import handle_conference_calls  # Optional future

class VoiceMenu(BaseMenu):
    def __init__(self):
        super().__init__("📞 Voice Call Management", "Voice Menu")

    def _setup_options(self):
        self.add_option("1", "Make a Call", handle_make_call_command, "📞")
        self.add_option("2", "View Call Logs", handle_view_call_logs_command, "📄")
        # self.add_option("3", "Manage Recordings", handle_manage_recordings, "🎙")
        # self.add_option("4", "Conference Calls", handle_conference_calls, "👥")
        self.add_option("0", "Back", True, "🔙")

def show_voice_menu():
    menu = VoiceMenu()
    menu.show()
