"""Service class for Voice operations."""

from app.gateways.twilio_gateway import get_twilio_client

class VoiceService:

    def __init__(self):

        self.client = get_twilio_client()



    def make_call(self, from_num, to_num, twiml_url):

        """Initiate a voice call."""

        return self.client.calls.create(from_=from_num, to=to_num, url=twiml_url)



    def get_logs(self, limit=10):

        """Retrieve recent voice call logs."""

        return self.client.calls.list(limit=limit)

