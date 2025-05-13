from twilio_manager.cli.menus.account_submenus import (
    AccountInfoMenu,
    SubaccountMenu,
    ApiKeyMenu,
    SipTrunkMenu,
    TwimlAppMenu
)

def handle_view_account_info():
    AccountInfoMenu().show()

def handle_subaccount_management():
    SubaccountMenu().show()

def handle_api_key_management():
    ApiKeyMenu().show()

def handle_sip_trunk_menu():
    SipTrunkMenu().show()

def handle_twiml_app_menu():
    TwimlAppMenu().show()
