def handle_view_account_info():
    """Display account information and balance."""
    from twilio_manager.cli.menus.account.account_info_menu import AccountInfoMenu
    AccountInfoMenu().show()

def handle_subaccount_management():
    """Display list of subaccounts."""
    from twilio_manager.cli.menus.account.subaccount_menu import SubaccountMenu
    SubaccountMenu().show()

def handle_api_key_management():
    """Display list of API keys."""
    from twilio_manager.cli.menus.account.api_key_menu import ApiKeyMenu
    ApiKeyMenu().show()

def handle_sip_trunk_menu():
    """Display list of SIP trunks."""
    from twilio_manager.cli.menus.account.sip_trunk_menu import SipTrunkMenu
    SipTrunkMenu().show()

def handle_twiml_app_menu():
    """Display list of TwiML applications."""
    from twilio_manager.cli.menus.account.twiml_app_menu import TwimlAppMenu
    TwimlAppMenu().show()
