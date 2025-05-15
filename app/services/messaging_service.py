from typing import Optional, Dict, List
import logging
from ..gateways.twilio_gateway import TwilioGateway
from ..gateways.file_logger import FileLogger

logger = logging.getLogger(__name__)

class MessagingService:
    def __init__(self, twilio_gateway: TwilioGateway,
                 file_logger: Optional[FileLogger] = None):
        self.twilio_gateway = twilio_gateway
        self.file_logger = file_logger

    def send_sms(self, from_: str, to: str, body: str) -> Optional[str]:
        """
        Send an SMS message.
        Returns message SID if successful, None if failed.
        """
        try:
            message_sid = self.twilio_gateway.send_sms(from_, to, body)
            
            if self.file_logger:
                self.file_logger.log_operation(
                    operation="send_sms",
                    number=from_,
                    details={
                        "to": to,
                        "message_sid": message_sid,
                        "body_length": len(body)
                    }
                )
            
            return message_sid
            
        except Exception as e:
            logger.error(f"Failed to send SMS from {from_} to {to}: {e}")
            
            if self.file_logger:
                self.file_logger.log_operation(
                    operation="send_sms",
                    number=from_,
                    status="failed",
                    details={
                        "to": to,
                        "error": str(e)
                    }
                )
            
            return None

    def get_message_logs(self, number: Optional[str] = None,
                        page_token: Optional[str] = None) -> Dict:
        """
        Retrieve message logs with optional filtering by number.
        Supports pagination.
        """
        try:
            return self.twilio_gateway.list_logs(
                type_="messages",
                sid=number,
                page_token=page_token
            )
        except Exception as e:
            logger.error(f"Failed to retrieve message logs: {e}")
            return {
                "items": [],
                "next_page_token": None
            }
