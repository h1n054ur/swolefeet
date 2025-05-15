"""Service class for Messaging operations."""

from app.gateways.twilio_gateway import get_twilio_client

class MessagingService:

    def __init__(self):

        self.client = get_twilio_client()



    def send_message(self, from_num, to_num, body):

        """Send an SMS message."""

        return self.client.messages.create(from_=from_num, to=to_num, body=body)



    def get_logs(self, limit=10):

        """Retrieve recent SMS messages."""

        return self.client.messages.list(limit=limit)

