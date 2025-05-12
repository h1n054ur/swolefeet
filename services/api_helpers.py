import requests
from requests.auth import HTTPBasicAuth
from services.api import twilio_request
from config.settings import ACCOUNT_SID, API_KEY_SID, API_KEY_SECRET

auth = HTTPBasicAuth(API_KEY_SID, API_KEY_SECRET)


def get_sip_trunks():
    """Fetches a list of SIP trunks using the correct API endpoint."""
    url = "https://trunking.twilio.com/v1/Trunks"
    try:
        response = requests.get(url, auth=auth)
        if response.ok:
            return response.json().get("trunks", [])
        else:
            print(f"❌ GET {url} failed with status {response.status_code}:")
            print(response.text)
    except Exception as e:
        print(f"❌ Error fetching SIP trunks: {e}")
    return []


def get_twiml_apps():
    """Fetches a list of TwiML applications."""
    endpoint = f"Accounts/{ACCOUNT_SID}/Applications.json"
    response = twilio_request("GET", endpoint)
    if response and response.ok:
        return response.json().get("applications", [])
    return []
