from twilio_manager.services.account_service import (
    fetch_account_info_api,
    fetch_subaccounts_api,
    fetch_api_keys_api,
    fetch_sip_trunks_api,
    fetch_twiml_apps_api
)

def get_account_info() -> tuple[dict, str | None]:
    """Get account information.
    
    Returns:
        tuple[dict, str | None]: (account_info, error_message)
    """
    try:
        info = fetch_account_info_api()
        return info, None
    except Exception as e:
        return {}, str(e)

def list_subaccounts() -> tuple[list, str | None]:
    """List subaccounts.
    
    Returns:
        tuple[list, str | None]: (subaccounts_list, error_message)
    """
    try:
        accounts = fetch_subaccounts_api()
        return accounts, None
    except Exception as e:
        return [], str(e)

def list_api_keys() -> tuple[list, str | None]:
    """List API keys.
    
    Returns:
        tuple[list, str | None]: (api_keys_list, error_message)
    """
    try:
        keys = fetch_api_keys_api()
        return keys, None
    except Exception as e:
        return [], str(e)

def list_sip_trunks() -> tuple[list, str | None]:
    """List SIP trunks.
    
    Returns:
        tuple[list, str | None]: (sip_trunks_list, error_message)
    """
    try:
        trunks = fetch_sip_trunks_api()
        return trunks, None
    except Exception as e:
        return [], str(e)

def list_twiml_apps() -> tuple[list, str | None]:
    """List TwiML applications.
    
    Returns:
        tuple[list, str | None]: (twiml_apps_list, error_message)
    """
    try:
        apps = fetch_twiml_apps_api()
        return apps, None
    except Exception as e:
        return [], str(e)
