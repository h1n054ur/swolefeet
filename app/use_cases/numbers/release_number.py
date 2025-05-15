"""Use case: ReleaseNumber."""

from app.services.number_service import NumberService

class ReleaseNumber:
    def __init__(self):
        self.service = NumberService()

    def execute(self, sid):
        """Release the specified phone number."""
        return self.service.release_number(sid)
