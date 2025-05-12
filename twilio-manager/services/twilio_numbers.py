# services/twilio_numbers.py

from services.api import twilio_request
from config.settings import ACCOUNT_SID
from rich.prompt import Confirm
import shutil


def get_active_numbers():
    """Fetch all active incoming phone numbers."""
    endpoint = f"Accounts/{ACCOUNT_SID}/IncomingPhoneNumbers.json"
    params = {"PageSize": 1000}
    response = twilio_request("GET", endpoint, params=params)
    if response and response.status_code == 200:
        return response.json().get("incoming_phone_numbers", [])
    return []


def get_number_properties(sid):
    """Fetch detailed metadata for a specific phone number."""
    endpoint = f"Accounts/{ACCOUNT_SID}/IncomingPhoneNumbers/{sid}.json"
    response = twilio_request("GET", endpoint)
    if response and response.status_code == 200:
        return response.json()
    return None


def update_friendly_name(sid, new_name):
    """Update the friendly name for a given number."""
    endpoint = f"Accounts/{ACCOUNT_SID}/IncomingPhoneNumbers/{sid}.json"
    data = {"FriendlyName": new_name}
    response = twilio_request("POST", endpoint, data=data)
    return response.status_code == 200 if response else False


def release_number(sid):
    """Release a Twilio number from your account."""
    endpoint = f"Accounts/{ACCOUNT_SID}/IncomingPhoneNumbers/{sid}.json"
    response = twilio_request("DELETE", endpoint)
    return response.status_code == 204 if response else False


def confirm_purchase_prompt():
    """Prints a centered confirmation prompt for purchases."""
    width = shutil.get_terminal_size().columns
    prompt_text = "Are you sure you want to proceed with this purchase?"
    padding = (width - len(prompt_text)) // 2
    aligned_prompt = " " * max(padding, 0) + prompt_text
    return Confirm.ask(aligned_prompt)
