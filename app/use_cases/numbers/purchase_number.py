"""Use case: PurchaseNumber."""

from app.gateways.twilio_gateway import get_twilio_client

class PurchaseNumber:
    def __init__(self):
        self.client = get_twilio_client()

    def execute(self, phone_number, voice_url=None, sms_url=None):
        try:
            result = self.client.incoming_phone_numbers.create(
                phone_number=phone_number,
                voice_url=voice_url,
                sms_url=sms_url
            )
            return f"✅ Purchased: {result.phone_number} (SID: {result.sid})"
        except Exception as e:
            return f"❌ Purchase failed: {e}"
