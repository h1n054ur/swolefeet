"""Use case: MakeCall."""

from app.services.voice_service import VoiceService

class MakeCall:
    def __init__(self):
        self.service = VoiceService()

    def execute(self, from_num, to_num, twiml_url):
        """Place a voice call and return the call object."""
        return self.service.make_call(from_num, to_num, twiml_url)
