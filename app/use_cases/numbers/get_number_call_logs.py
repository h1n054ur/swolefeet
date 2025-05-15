"""Use case: GetNumberCallLogs."""

from app.services.number_service import NumberService

class GetNumberCallLogs:
    def __init__(self, limit=10):
        self.service = NumberService()
        self.limit = limit

    def execute(self, phone_number):
        """Return recent call logs for a specific number."""
        return self.service.get_call_logs_for_number(phone_number, limit=self.limit)
