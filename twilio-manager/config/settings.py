# config/settings.py

import os
from dotenv import load_dotenv

# Load from .env file (if it exists)
load_dotenv()

# Required Twilio credentials
ACCOUNT_SID = os.getenv("ACCOUNT_SID")
API_KEY_SID = os.getenv("API_KEY_SID")
API_KEY_SECRET = os.getenv("API_KEY_SECRET")

missing = [key for key, val in {
    "ACCOUNT_SID": ACCOUNT_SID,
    "API_KEY_SID": API_KEY_SID,
    "API_KEY_SECRET": API_KEY_SECRET
}.items() if not val]

if missing:
    raise EnvironmentError(f"⚠️ Missing required Twilio credentials in .env file: {', '.join(missing)}")
