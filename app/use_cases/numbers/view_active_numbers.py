"""Use case: ViewActiveNumbers."""

from app.services.number_service import NumberService
from app.models.phone_number_model import PhoneNumberModel

class ViewActiveNumbers:
    def __init__(self):
        self.service = NumberService()

    def execute(self):
        """Return a list of PhoneNumberModel for all active numbers."""
        raw_numbers = self.service.get_active_numbers()
        return [PhoneNumberModel(n.sid, n.phone_number, n.friendly_name, n.voice_url, n.sms_url) for n in raw_numbers]
