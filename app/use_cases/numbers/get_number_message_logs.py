"""Use case: GetNumberMessageLogs."""

from app.services.number_service import NumberService

class GetNumberMessageLogs:
    def __init__(self, limit=10):
        self.service = NumberService()
        self.limit = limit

    def execute(self, phone_number):
        """Return recent message logs for a specific number."""
        return self.service.get_message_logs_for_number(phone_number, limit=self.limit)
