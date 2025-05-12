from twilio.rest import Client
from twilio_manager.shared.config import ACCOUNT_SID, AUTH_TOKEN

client = Client(ACCOUNT_SID, AUTH_TOKEN)

def fetch_account_info_api():
    try:
        account = client.api.accounts(ACCOUNT_SID).fetch()
        return {
            "sid": account.sid,
            "friendly_name": account.friendly_name,
            "status": account.status,
            "date_created": str(account.date_created),
            "owner_email": account.owner_email if hasattr(account, "owner_email") else "—"
        }
    except Exception as e:
        print(f"[service] Account info error: {e}")
        return {}

def fetch_subaccounts_api():
    try:
        subs = client.api.accounts.list()
        return [
            {
                "sid": acc.sid,
                "friendly_name": acc.friendly_name,
                "status": acc.status
            } for acc in subs if acc.sid != ACCOUNT_SID
        ]
    except Exception as e:
        print(f"[service] Subaccount list error: {e}")
        return []

def fetch_api_keys_api():
    try:
        keys = client.new_keys.list()
        return [
            {
                "sid": key.sid,
                "friendly_name": key.friendly_name
            } for key in keys
        ]
    except Exception as e:
        print(f"[service] API key list error: {e}")
        return []

def fetch_sip_trunks_api():
    try:
        trunks = client.trunking.v1.trunks.list()
        return [
            {
                "sid": trunk.sid,
                "friendly_name": trunk.friendly_name,
                "voice_region": trunk.voice_region
            } for trunk in trunks
        ]
    except Exception as e:
        print(f"[service] SIP trunk error: {e}")
        return []

def fetch_twiml_apps_api():
    try:
        apps = client.applications.list()
        return [
            {
                "sid": app.sid,
                "friendly_name": app.friendly_name,
                "voice_url": app.voice_url
            } for app in apps
        ]
    except Exception as e:
        print(f"[service] TwiML app error: {e}")
        return []
