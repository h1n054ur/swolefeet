"""Service layer for phone number operations."""

from typing import Dict, List, Optional
import logging
from ..gateways.twilio_gateway import TwilioGateway
from ..gateways.http_gateway import HTTPGateway
from ..gateways.file_logger import FileLogger
from ..models.phone_number_model import NumberRecord

logger = logging.getLogger(__name__)

class NumberService:
    """Service for managing phone numbers."""

    def __init__(self, twilio_gateway: TwilioGateway,
                 http_gateway: HTTPGateway,
                 file_logger: Optional[FileLogger] = None):
        self.twilio_gateway = twilio_gateway
        self.http_gateway = http_gateway
        self.file_logger = file_logger

    async def search_available(self, country: str, type_: str,
                             capabilities: Optional[Dict] = None,
                             pattern: Optional[str] = None,
                             locality: Optional[Dict] = None,
                             limit: int = 50) -> List[NumberRecord]:
        """
        Search for available phone numbers with filtering.
        
        Args:
            country: Country code (e.g., 'US')
            type_: Number type (local/mobile/toll-free)
            capabilities: Required capabilities (voice/sms/mms)
            pattern: Number pattern to match
            locality: Location filters (city/state)
            limit: Maximum numbers to return
            
        Returns:
            List of available NumberRecord objects
        """
        try:
            # Build search filters
            filters = {}
            if pattern:
                filters["contains"] = pattern
            if locality:
                filters.update(locality)
            
            # Search using HTTP gateway for better pagination
            result = self.http_gateway.search_batch(
                country=country,
                type_=type_,
                capabilities=capabilities,
                page_size=limit
            )
            
            # Convert to NumberRecord objects
            numbers = []
            for num in result["numbers"]:
                numbers.append(NumberRecord(
                    phone_number=num["phone_number"],
                    country=country,
                    type=type_,
                    capabilities=list(capabilities.keys()) if capabilities else [],
                    region=num.get("region"),
                    locality=num.get("locality"),
                    rate_center=num.get("rate_center"),
                    latitude=num.get("latitude"),
                    longitude=num.get("longitude")
                ))
            
            # Log search
            if self.file_logger:
                self.file_logger.log_search(
                    country=country,
                    type_=type_,
                    capabilities=capabilities,
                    results_count=len(numbers)
                )
            
            return numbers
            
        except Exception as e:
            logger.error(f"Failed to search numbers: {e}")
            return []

    async def purchase_numbers(self, numbers: List[str]) -> Dict[str, str]:
        """
        Purchase multiple phone numbers.
        
        Args:
            numbers: List of phone numbers to purchase
            
        Returns:
            Dict mapping phone numbers to their SIDs or error messages
        """
        results = {}
        
        for number in numbers:
            try:
                sid = self.twilio_gateway.purchase_number(number)
                results[number] = sid
                
                if self.file_logger:
                    self.file_logger.log_operation(
                        operation="purchase",
                        number=number,
                        details={"sid": sid}
                    )
                    
            except Exception as e:
                logger.error(f"Failed to purchase {number}: {e}")
                results[number] = f"Error: {str(e)}"
                
                if self.file_logger:
                    self.file_logger.log_operation(
                        operation="purchase",
                        number=number,
                        status="failed",
                        details={"error": str(e)}
                    )
        
        return results

    def list_active_numbers(self, filters: Optional[Dict] = None) -> List[NumberRecord]:
        """
        List all active phone numbers with optional filtering.
        
        Args:
            filters: Optional filters for the query
            
        Returns:
            List of active NumberRecord objects
        """
        try:
            return self.twilio_gateway.list_numbers(filters)
        except Exception as e:
            logger.error(f"Failed to list active numbers: {e}")
            return []

    def release_number(self, sid: str) -> bool:
        """
        Release a phone number.
        
        Args:
            sid: The Twilio SID of the number to release
            
        Returns:
            True if successful, False otherwise
        """
        try:
            result = self.twilio_gateway.release_number(sid)
            
            if self.file_logger:
                self.file_logger.log_operation(
                    operation="release",
                    number=sid,
                    status="success" if result else "failed"
                )
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to release number {sid}: {e}")
            
            if self.file_logger:
                self.file_logger.log_operation(
                    operation="release",
                    number=sid,
                    status="failed",
                    details={"error": str(e)}
                )
            
            return False

    def get_number_config(self, sid: str) -> Optional[Dict]:
        """
        Get configuration for a phone number.
        
        Args:
            sid: The Twilio SID of the number
            
        Returns:
            Dict with number configuration or None if failed
        """
        try:
            number = self.twilio_gateway.get_client().incoming_phone_numbers(sid).fetch()
            return {
                "voice_url": number.voice_url,
                "sms_url": number.sms_url,
                "status_callback": number.status_callback,
                "voice_method": number.voice_method,
                "sms_method": number.sms_method,
                "status_callback_method": number.status_callback_method
            }
        except Exception as e:
            logger.error(f"Failed to get config for {sid}: {e}")
            return None

    def update_number_config(self, sid: str, config: Dict) -> bool:
        """
        Update configuration for a phone number.
        
        Args:
            sid: The Twilio SID of the number
            config: New configuration parameters
            
        Returns:
            True if successful, False otherwise
        """
        try:
            result = self.twilio_gateway.update_number_config(sid, config)
            
            if self.file_logger:
                self.file_logger.log_operation(
                    operation="update_config",
                    number=sid,
                    status="success" if result else "failed",
                    details={"config": config}
                )
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to update config for {sid}: {e}")
            
            if self.file_logger:
                self.file_logger.log_operation(
                    operation="update_config",
                    number=sid,
                    status="failed",
                    details={
                        "config": config,
                        "error": str(e)
                    }
                )
            
            return False
