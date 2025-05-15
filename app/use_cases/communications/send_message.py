"""Use case: SendMessage."""

from app.services.messaging_service import MessagingService

class SendMessage:
    def __init__(self):
        self.service = MessagingService()

    def execute(self, from_num, to_num, body):
        """Send an SMS and return the message object."""
        return self.service.send_message(from_num, to_num, body)
