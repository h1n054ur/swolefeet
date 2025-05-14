from twilio.rest import Client
from twilio_manager.shared.config import ACCOUNT_SID, AUTH_TOKEN

# Centralized Twilio client
twilio_client = Client(ACCOUNT_SID, AUTH_TOKEN)
