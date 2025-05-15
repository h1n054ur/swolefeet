"""Use case: GetMessageLogs."""

from app.services.messaging_service import MessagingService

class GetMessageLogs:
    def __init__(self, limit=10):
        self.service = MessagingService()
        self.limit = limit

    def execute(self):
        """Retrieve recent message logs."""
        return self.service.get_logs(limit=self.limit)
