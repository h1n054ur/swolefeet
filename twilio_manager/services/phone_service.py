# File: twilio_manager/services/phone_service.py

import time
import requests
from typing import Dict, List, Set, Tuple, Optional
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from twilio_manager.shared.config import ACCOUNT_SID, AUTH_TOKEN
from urllib.parse import urlparse, parse_qs

# Singleton instance
_phone_service = None

def get_phone_service():
    global _phone_service
    if _phone_service is None:
        _phone_service = PhoneService()
    return _phone_service

# Exposed API functions
def search_available_numbers_api(*args, **kwargs):
    return get_phone_service()._search_available_numbers_api(*args, **kwargs)

def purchase_number_api(phone_number):
    return get_phone_service().purchase_number(phone_number)

def configure_number_api(sid_or_number, friendly_name=None, voice_url=None, sms_url=None):
    return get_phone_service().configure_number(sid_or_number, friendly_name, voice_url, sms_url)

def release_number_api(sid_or_number):
    return get_phone_service().release_number(sid_or_number)

def get_active_numbers_api():
    return get_phone_service().get_active_numbers()


class PhoneService:
    def __init__(self):
        self.client = Client(ACCOUNT_SID, AUTH_TOKEN)

    # Price map for different number types and countries
    PRICE_MAP = {
        ("US", "local"): 1.15,
        ("US", "tollfree"): 2.15,
        ("US", "mobile"): 1.15,
        ("GB", "local"): 1.15,
        ("GB", "mobile"): 1.15,
        ("GB", "tollfree"): 2.15,
        ("AU", "local"): 3.00,
        ("AU", "mobile"): 6.50,
        ("AU", "tollfree"): 16.00,
        ("CA", "local"): 1.15,
        ("CA", "tollfree"): 2.15,
    }

    # Supported countries and number types
    SUPPORTED_COUNTRIES = {
        "US": ["local", "tollfree", "mobile"],
        "GB": ["local", "tollfree", "mobile"],
        "CA": ["local", "tollfree"],
        "AU": ["local", "tollfree", "mobile"]
    }

    def _format_phone_number_dict(self, number_dict: Dict, country: str, number_type: str) -> Optional[Dict]:
        """Format a phone number dictionary from the REST API response."""
        try:
            caps = number_dict.get("capabilities", {})
            if isinstance(caps, (list, tuple)):
                caps_dict = {
                    "voice": "voice" in caps,
                    "sms": "sms" in caps,
                    "mms": "mms" in caps
                }
            else:
                caps_dict = {
                    "voice": caps.get("voice", False),
                    "sms": caps.get("sms", False),
                    "mms": caps.get("mms", False)
                }

            # Determine monthly rate
            try:
                monthly_rate = float(number_dict.get("monthly_rate", 0))
                if monthly_rate == 0:
                    monthly_rate = self.PRICE_MAP.get((country, number_type), 1.15)
            except (ValueError, TypeError):
                monthly_rate = self.PRICE_MAP.get((country, number_type), 1.15)

            return {
                "phoneNumber": number_dict.get("phone_number", "—"),
                "friendlyName": number_dict.get("friendly_name") or number_dict.get("phone_number", "—"),
                "region": number_dict.get("locality") or number_dict.get("region") or "—",
                "capabilities": caps_dict,
                "monthlyPrice": monthly_rate
            }
        except Exception:
            return None

    def _format_phone_number(self, number, country: str, number_type: str) -> Optional[Dict]:
        """Format a phone number object into our standard dict format."""
        try:
            caps = getattr(number, "capabilities", {})
            if isinstance(caps, (list, tuple)):
                caps_dict = {
                    "voice": "voice" in caps,
                    "sms": "sms" in caps,
                    "mms": "mms" in caps
                }
            else:
                caps_dict = {
                    "voice": caps.get("voice", False),
                    "sms": caps.get("sms", False),
                    "mms": caps.get("mms", False)
                }

            try:
                monthly_rate = float(getattr(number, "monthly_rate", 0) or 0)
                if monthly_rate == 0:
                    monthly_rate = self.PRICE_MAP.get((country, number_type), 1.15)
            except (ValueError, TypeError):
                monthly_rate = self.PRICE_MAP.get((country, number_type), 1.15)

            return {
                "phoneNumber": getattr(number, "phone_number", "—"),
                "friendlyName": getattr(number, "friendly_name", "") or getattr(number, "phone_number", "—"),
                "region": getattr(number, "locality", "") or getattr(number, "region", "") or "—",
                "capabilities": caps_dict,
                "monthlyPrice": monthly_rate
            }
        except Exception:
            return None

    def search_numbers(self, country_code: str, number_type: str, capabilities: List[str], pattern: str = "") -> List[Dict]:
        """Simple wrapper for CLI use."""
        results, _ = self._search_available_numbers_api(country_code, number_type, capabilities, pattern)
        return results

    def _search_available_numbers_api(
        self,
        country: str,
        number_type: str,
        capabilities: List[str],
        contains: str = "",
        progress_callback=None
    ) -> Tuple[List[Dict], str]:
        """
        Search for available phone numbers with pagination, trying AreaCode first
        for 3-digit US patterns, then falling back to Contains if that yields no results.
        """
        from twilio_manager.shared.utils.logger import get_logger
        logger = get_logger(__name__)

        country = country.upper()
        nt = number_type.lower()
        if country not in self.SUPPORTED_COUNTRIES:
            return [], f"Unsupported country code: {country}"
        if nt not in self.SUPPORTED_COUNTRIES[country]:
            return [], f"Number type '{nt}' not supported for country {country}"

        try:
            # Determine endpoint path
            type_map = {"local": "Local", "tollfree": "TollFree", "mobile": "Mobile"}
            endpoint = type_map.get(nt)
            if not endpoint:
                return [], "Invalid number type specified"

            base_url = (
                f"https://api.twilio.com/2010-04-01/Accounts/{ACCOUNT_SID}"
                f"/AvailablePhoneNumbers/{country}/{endpoint}.json"
            )

            # Build capability params
            params: Dict[str, str] = {}
            if capabilities:
                caps = [cap.upper().strip() for cap in capabilities]
                capability_map = {
                    "SMS": "SmsEnabled",
                    "VOICE": "VoiceEnabled",
                    "MMS": "MmsEnabled",
                    "MESSAGING": "SmsEnabled",
                    "CALL": "VoiceEnabled",
                    "TEXT": "SmsEnabled",
                }
                for cap in caps:
                    if cap in capability_map:
                        params[capability_map[cap]] = "true"

            # Handle 3-digit US patterns with fallback
            if contains := contains.strip():
                if country == "US" and contains.isdigit() and len(contains) == 3:
                    # First, try as AreaCode
                    test_params = params.copy()
                    test_params["AreaCode"] = contains
                    try:
                        test_resp = requests.get(
                            base_url,
                            auth=(ACCOUNT_SID, AUTH_TOKEN),
                            params=test_params,
                            timeout=10
                        )
                        test_resp.raise_for_status()
                        if test_resp.json().get("available_phone_numbers"):
                            params = test_params
                        else:
                            params["Contains"] = contains
                    except Exception as e:
                        logger.debug(f"AreaCode test failed ({contains}): {e}")
                        params["Contains"] = contains
                else:
                    # Non-US or non-3-digit → always Contains
                    params["Contains"] = contains

            logger.debug(f"Final search parameters: {params}")

            # Pagination loop
            results: List[Dict] = []
            seen_numbers: Set[str] = set()
            consecutive_no_unique = 0
            retry_count = 0
            max_retries = 3

            while len(results) < 500 and consecutive_no_unique < 2:
                try:
                    logger.debug(f"Requesting {base_url} with {params}")
                    resp = requests.get(
                        base_url,
                        auth=(ACCOUNT_SID, AUTH_TOKEN),
                        params=params,
                        timeout=30
                    )
                    logger.debug(f"Status {resp.status_code}: {resp.text[:200]}...")
                    resp.raise_for_status()
                    data = resp.json()
                    available = data.get("available_phone_numbers", [])

                    new_unique = 0
                    for entry in available:
                        pn = entry.get("phone_number")
                        if not pn or pn in seen_numbers:
                            continue
                        seen_numbers.add(pn)
                        formatted = self._format_phone_number_dict(entry, country, nt)
                        if formatted:
                            results.append(formatted)
                            new_unique += 1
                        if len(results) >= 500:
                            break

                    if progress_callback:
                        progress_callback(len(results))

                    consecutive_no_unique = consecutive_no_unique + 1 if new_unique == 0 else 0
                    time.sleep(1)

                except requests.exceptions.RequestException as e:
                    retry_count += 1
                    if retry_count >= max_retries:
                        return results, f"Error after {max_retries} retries: {e}"
                    # Back off on rate limit
                    if getattr(e.response, "status_code", None) == 429:
                        time.sleep(2**retry_count)
                    else:
                        time.sleep(1)
                    continue

            # Final status
            if len(results) >= 500:
                status = "Found maximum number of results (500)"
            elif consecutive_no_unique >= 2:
                status = "Search completed (no more results available)"
            else:
                status = "Search completed successfully"

            return results, status

        except Exception as e:
            return [], f"Unexpected error: {e}"

    def purchase_number(self, phone_number: str) -> bool:
        """Purchase a phone number."""
        try:
            num = self.client.incoming_phone_numbers.create(phone_number=phone_number)
            return bool(num and num.sid)
        except TwilioRestException:
            return False

    def configure_number(
        self,
        sid_or_number: str,
        friendly_name: Optional[str] = None,
        voice_url: Optional[str] = None,
        sms_url: Optional[str] = None
    ) -> bool:
        """Configure a phone number’s settings."""
        try:
            for num in self.client.incoming_phone_numbers.list():
                if sid_or_number in (num.sid, num.phone_number):
                    update_kwargs = {}
                    if friendly_name:
                        update_kwargs["friendly_name"] = friendly_name
                    if voice_url:
                        update_kwargs["voice_url"] = voice_url
                    if sms_url:
                        update_kwargs["sms_url"] = sms_url
                    updated = self.client.incoming_phone_numbers(num.sid).update(**update_kwargs)
                    return bool(updated)
            return False
        except TwilioRestException:
            return False

    def release_number(self, sid_or_number: str) -> bool:
        """Release a phone number."""
        try:
            for num in self.client.incoming_phone_numbers.list():
                if sid_or_number in (num.sid, num.phone_number):
                    return bool(self.client.incoming_phone_numbers(num.sid).delete())
            return False
        except TwilioRestException:
            return False

    def get_active_numbers(self) -> Tuple[List[Dict], Optional[str]]:
        """Get all active phone numbers from the account."""
        try:
            nums = self.client.incoming_phone_numbers.list()
            formatted = [
                {
                    "sid": n.sid,
                    "phoneNumber": n.phone_number,
                    "friendlyName": n.friendly_name or n.phone_number,
                    "capabilities": {
                        "voice": n.capabilities.get("voice", False),
                        "sms": n.capabilities.get("sms", False),
                        "mms": n.capabilities.get("mms", False)
                    },
                    "voiceUrl": n.voice_url,
                    "smsUrl": n.sms_url
                }
                for n in nums
            ]
            return formatted, None
        except TwilioRestException:
            return [], "Error fetching active numbers"
