from twilio.rest import Client
from twilio_manager.shared.config import ACCOUNT_SID, AUTH_TOKEN

client = Client(ACCOUNT_SID, AUTH_TOKEN)

def fetch_account_info_api() -> tuple[dict, str | None]:
    """Fetch account information from Twilio API.
    
    Returns:
        tuple[dict, str | None]: (account_info, error_message)
    """
    try:
        account = client.api.accounts(ACCOUNT_SID).fetch()
        info = {
            "sid": account.sid,
            "friendly_name": account.friendly_name,
            "status": account.status,
            "date_created": str(account.date_created),
            "owner_email": account.owner_email if hasattr(account, "owner_email") else "—"
        }
        return info, None
    except Exception as e:
        return {}, str(e)

def fetch_subaccounts_api() -> tuple[list, str | None]:
    """Fetch subaccounts from Twilio API.
    
    Returns:
        tuple[list, str | None]: (subaccounts_list, error_message)
    """
    try:
        subs = client.api.accounts.list()
        accounts = [
            {
                "sid": acc.sid,
                "friendly_name": acc.friendly_name,
                "status": acc.status
            } for acc in subs if acc.sid != ACCOUNT_SID
        ]
        return accounts, None
    except Exception as e:
        return [], str(e)

def fetch_api_keys_api() -> tuple[list, str | None]:
    """Fetch API keys from Twilio API.
    
    Returns:
        tuple[list, str | None]: (api_keys_list, error_message)
    """
    try:
        keys = client.new_keys.list()
        api_keys = [
            {
                "sid": key.sid,
                "friendly_name": key.friendly_name
            } for key in keys
        ]
        return api_keys, None
    except Exception as e:
        return [], str(e)

def fetch_sip_trunks_api() -> tuple[list, str | None]:
    """Fetch SIP trunks from Twilio API.
    
    Returns:
        tuple[list, str | None]: (sip_trunks_list, error_message)
    """
    try:
        trunks = client.trunking.v1.trunks.list()
        trunk_list = [
            {
                "sid": trunk.sid,
                "friendly_name": trunk.friendly_name,
                "voice_region": trunk.voice_region
            } for trunk in trunks
        ]
        return trunk_list, None
    except Exception as e:
        return [], str(e)

def fetch_twiml_apps_api() -> tuple[list, str | None]:
    """Fetch TwiML applications from Twilio API.
    
    Returns:
        tuple[list, str | None]: (twiml_apps_list, error_message)
    """
    try:
        apps = client.applications.list()
        app_list = [
            {
                "sid": app.sid,
                "friendly_name": app.friendly_name,
                "voice_url": app.voice_url
            } for app in apps
        ]
        return app_list, None
    except Exception as e:
        return [], str(e)
