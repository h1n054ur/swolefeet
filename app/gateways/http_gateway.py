import logging
from typing import Dict, Optional
import requests
from requests.exceptions import RequestException

from .config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN

logger = logging.getLogger(__name__)

class HTTPGateway:
    BASE_URL = "https://api.twilio.com/2010-04-01"
    
    def __init__(self):
        self._session = requests.Session()
        self._session.auth = (TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        self._session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json"
        })

    def search_batch(self, country: str, type_: str, 
                    capabilities: Optional[Dict] = None,
                    page_size: int = 50,
                    page_token: Optional[str] = None) -> Dict:
        """
        Search for available phone numbers using raw HTTP requests.
        Supports pagination and capability filtering.
        """
        try:
            url = f"{self.BASE_URL}/Accounts/{TWILIO_ACCOUNT_SID}/AvailablePhoneNumbers/{country}/{type_}.json"
            
            params = {
                "PageSize": page_size
            }
            
            # Add capabilities filtering
            if capabilities:
                if capabilities.get("voice"):
                    params["VoiceEnabled"] = "true"
                if capabilities.get("sms"):
                    params["SmsEnabled"] = "true"
                if capabilities.get("mms"):
                    params["MmsEnabled"] = "true"
            
            # Add pagination token if provided
            if page_token:
                params["PageToken"] = page_token

            response = self._session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            logger.debug(f"Retrieved {len(data.get('available_phone_numbers', []))} numbers")
            
            return {
                "numbers": data.get("available_phone_numbers", []),
                "next_page_url": data.get("next_page_url"),
                "uri": data.get("uri")
            }

        except RequestException as e:
            logger.error(f"HTTP request failed during number search: {e}")
            raise

    def __del__(self):
        """Ensure proper cleanup of session."""
        if hasattr(self, '_session'):
            self._session.close()