"""Use case: GetCallLogs."""

from app.services.voice_service import VoiceService

class GetCallLogs:
    def __init__(self, limit=10):
        self.service = VoiceService()
        self.limit = limit

    def execute(self):
        """Retrieve recent call logs."""
        return self.service.get_logs(limit=self.limit)
