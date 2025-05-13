from twilio_manager.cli.menus.base_menu import BaseMenu, with_loading
from twilio_manager.cli.commands.call_command import handle_make_call_command
from twilio_manager.cli.commands.view_logs_command import handle_view_call_logs_command

class VoiceMenu(BaseMenu):
    def __init__(self):
        super().__init__("📞 Voice Call Management", "Voice Menu")
        
        # Add menu options
        self.add_option("1", "Make a Call", self.make_call, "voice")
        self.add_option("2", "View Call Logs", self.view_logs, "voice")
        self.add_back_option()

    @with_loading("Initiating call...")
    def make_call(self):
        handle_make_call_command()
        return True

    @with_loading("Loading call logs...")
    def view_logs(self):
        handle_view_call_logs_command()
        return True

def show_voice_menu():
    menu = VoiceMenu()
    menu.show()
