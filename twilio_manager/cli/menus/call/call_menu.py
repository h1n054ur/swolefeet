from twilio_manager.cli.menus.base_menu import BaseMenu
from twilio_manager.cli.menus.call.select_caller_menu import SelectCallerMenu
from twilio_manager.cli.menus.call.select_recipient_menu import SelectRecipientMenu
from twilio_manager.cli.menus.call.select_voice_response_menu import SelectVoiceResponseMenu
from twilio_manager.cli.menus.call.call_confirmation_menu import CallConfirmationMenu

class CallMenu(BaseMenu):
    def show(self):
        """Display the main call menu and handle the call flow."""
        # Get caller number
        from_number = SelectCallerMenu().show()
        if not from_number:
            return

        # Get recipient number
        to_number = SelectRecipientMenu().show()
        if not to_number:
            return

        # Get voice URL
        voice_url = SelectVoiceResponseMenu().show()
        if not voice_url:
            return

        # Show confirmation and make call
        CallConfirmationMenu(from_number, to_number, voice_url).show()