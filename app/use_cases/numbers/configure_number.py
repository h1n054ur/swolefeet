"""Use case: ConfigureNumber."""

from app.services.number_service import NumberService

class ConfigureNumber:
    def __init__(self):
        self.service = NumberService()

    def execute(self, sid, sms_url=None, voice_url=None):
        """Update the SMS and Voice URLs for a number."""
        return self.service.configure_number(sid, sms_url=sms_url, voice_url=voice_url)
