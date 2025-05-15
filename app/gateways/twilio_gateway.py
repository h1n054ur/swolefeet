"""Twilio SDK wrapper for basic client access."""

from twilio.rest import Client
from app.gateways import config

def get_twilio_client():
    return Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)


import requests
from app.gateways import config

def search_available_numbers(country, number_type, params):
    url = f"https://api.twilio.com/2010-04-01/Accounts/{config.TWILIO_ACCOUNT_SID}/AvailablePhoneNumbers/{country}/{number_type}.json"
    response = requests.get(url, auth=(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN), params=params)
    response.raise_for_status()
    return response.json().get("available_phone_numbers", [])
