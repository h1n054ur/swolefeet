# services/phone_config.py

from services.api import twilio_request
from config.settings import ACCOUNT_SID
from utils.ui import print_success, print_error


def update_phone_number(sid, updates: dict):
    """
    Update a Twilio phone number with given fields.
    :param sid: The phone number SID.
    :param updates: Dictionary of field names and values to update.
    :return: bool - True if successful, False otherwise.
    """
    if not updates:
        print_error("No update fields provided.")
        return False

    endpoint = f"Accounts/{ACCOUNT_SID}/IncomingPhoneNumbers/{sid}.json"
    response = twilio_request("POST", endpoint, data=updates)

    if response and response.status_code == 200:
        print_success("✅ Number updated successfully.")
        return True
    else:
        print_error(f"❌ Update failed. Status code: {response.status_code if response else 'N/A'}")
        return False
