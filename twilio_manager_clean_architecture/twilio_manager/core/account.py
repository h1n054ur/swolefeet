from twilio_manager.services.account_service import (
    fetch_account_info_api,
    fetch_subaccounts_api,
    fetch_api_keys_api,
    fetch_sip_trunks_api,
    fetch_twiml_apps_api
)

def get_account_info():
    try:
        return fetch_account_info_api()
    except Exception as e:
        print(f"[core] Account info error: {e}")
        return {}

def list_subaccounts():
    try:
        return fetch_subaccounts_api()
    except Exception as e:
        print(f"[core] Subaccount list error: {e}")
        return []

def list_api_keys():
    try:
        return fetch_api_keys_api()
    except Exception as e:
        print(f"[core] API key list error: {e}")
        return []

def list_sip_trunks():
    try:
        return fetch_sip_trunks_api()
    except Exception as e:
        print(f"[core] SIP trunk error: {e}")
        return []

def list_twiml_apps():
    try:
        return fetch_twiml_apps_api()
    except Exception as e:
        print(f"[core] TwiML app error: {e}")
        return []
