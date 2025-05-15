from typing import Optional, Dict, List
import logging
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

from ..models.phone_number_model import NumberRecord
from .config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN

logger = logging.getLogger(__name__)

class TwilioGateway:
    def __init__(self):
        self._client: Optional[Client] = None

    def get_client(self) -> Client:
        if not self._client:
            self._client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        return self._client

    def list_numbers(self, filters: Optional[Dict] = None) -> List[NumberRecord]:
        """List active phone numbers with optional filtering."""
        try:
            numbers = self.get_client().incoming_phone_numbers.list(**filters or {})
            return [
                NumberRecord(
                    number=n.phone_number,
                    city=n.locality,
                    state=n.region,
                    type="local" if n.address_requirements == "local" else "toll-free",
                    price=float(n.voice_rate)
                ) for n in numbers
            ]
        except TwilioRestException as e:
            logger.error(f"Failed to list numbers: {e}")
            raise

    def purchase_number(self, phone_number: str) -> Optional[str]:
        """Purchase a phone number, returns SID if successful."""
        try:
            number = self.get_client().incoming_phone_numbers.create(
                phone_number=phone_number
            )
            logger.info(f"Successfully purchased number: {phone_number}")
            return number.sid
        except TwilioRestException as e:
            logger.error(f"Failed to purchase number {phone_number}: {e}")
            raise

    def release_number(self, sid: str) -> bool:
        """Release a phone number by SID."""
        try:
            self.get_client().incoming_phone_numbers(sid).delete()
            logger.info(f"Successfully released number with SID: {sid}")
            return True
        except TwilioRestException as e:
            logger.error(f"Failed to release number {sid}: {e}")
            raise

    def update_number_config(self, sid: str, config: Dict) -> bool:
        """Update phone number configuration."""
        try:
            self.get_client().incoming_phone_numbers(sid).update(**config)
            logger.info(f"Successfully updated config for number {sid}")
            return True
        except TwilioRestException as e:
            logger.error(f"Failed to update number config {sid}: {e}")
            raise

    def make_call(self, from_: str, to: str) -> str:
        """Initiate a call, returns call SID."""
        try:
            call = self.get_client().calls.create(
                to=to,
                from_=from_,
                url="http://demo.twilio.com/docs/voice.xml"  # Default TwiML
            )
            logger.info(f"Successfully initiated call from {from_} to {to}")
            return call.sid
        except TwilioRestException as e:
            logger.error(f"Failed to make call from {from_} to {to}: {e}")
            raise

    def send_sms(self, from_: str, to: str, body: str) -> str:
        """Send SMS message, returns message SID."""
        try:
            message = self.get_client().messages.create(
                to=to,
                from_=from_,
                body=body
            )
            logger.info(f"Successfully sent SMS from {from_} to {to}")
            return message.sid
        except TwilioRestException as e:
            logger.error(f"Failed to send SMS from {from_} to {to}: {e}")
            raise

    def list_logs(self, type_: str, sid: Optional[str] = None, 
                 page_token: Optional[str] = None) -> Dict:
        """List logs by type (calls/messages) with optional filtering."""
        try:
            client = self.get_client()
            resource = client.calls if type_ == "calls" else client.messages
            
            filters = {"page_size": 20}
            if sid:
                filters["sid"] = sid
            if page_token:
                filters["page_token"] = page_token

            logs = resource.list(**filters)
            return {
                "items": list(logs),
                "next_page_token": logs.next_page_url
            }
        except TwilioRestException as e:
            logger.error(f"Failed to list {type_} logs: {e}")
            raise