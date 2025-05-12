# services/api.py

import requests
from requests.auth import HTTPBasicAuth
from config.settings import API_KEY_SID, API_KEY_SECRET
from utils.ui import print_error

auth = HTTPBasicAuth(API_KEY_SID, API_KEY_SECRET)
BASE_URL = "https://api.twilio.com/2010-04-01/"


def twilio_request(method, endpoint, params=None, data=None):
    """
    Generic Twilio API request handler.

    Args:
        method (str): HTTP method (GET, POST, DELETE).
        endpoint (str): Endpoint path after BASE_URL.
        params (dict, optional): URL query parameters.
        data (dict, optional): Form-encoded POST data.

    Returns:
        Response object if successful or failed (check .ok), else None on exception.
    """
    if not endpoint:
        print_error("Empty endpoint provided to twilio_request()")
        return None

    url = BASE_URL + endpoint

    try:
        response = requests.request(
            method=method.upper(),
            url=url,
            auth=auth,
            params=params,
            data=data
        )

        if not response.ok:
            print_error(
                f"{method.upper()} {url} failed with status {response.status_code}:\n{response.text}"
            )

        return response

    except requests.RequestException as e:
        print_error(f"❌ Network error while contacting Twilio: {e}")
        return None
