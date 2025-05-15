from typing import Optional
import logging
from ..gateways.twilio_gateway import TwilioGateway
from ..gateways.file_logger import FileLogger

logger = logging.getLogger(__name__)

class VoiceService:
    def __init__(self, twilio_gateway: TwilioGateway,
                 file_logger: Optional[FileLogger] = None):
        self.twilio_gateway = twilio_gateway
        self.file_logger = file_logger

    def make_call(self, from_: str, to: str) -> Optional[str]:
        """
        Initiate a call between two numbers.
        Returns call SID if successful, None if failed.
        """
        try:
            call_sid = self.twilio_gateway.make_call(from_, to)
            
            if self.file_logger:
                self.file_logger.log_operation(
                    operation="make_call",
                    number=from_,
                    details={
                        "to": to,
                        "call_sid": call_sid
                    }
                )
            
            return call_sid
            
        except Exception as e:
            logger.error(f"Failed to initiate call from {from_} to {to}: {e}")
            
            if self.file_logger:
                self.file_logger.log_operation(
                    operation="make_call",
                    number=from_,
                    status="failed",
                    details={
                        "to": to,
                        "error": str(e)
                    }
                )
            
            return None
