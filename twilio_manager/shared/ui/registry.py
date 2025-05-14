"""Menu registry for dynamic menu loading and testing."""

from twilio_manager.cli.menus.main_menu import MainMenu
from twilio_manager.cli.menus.phone_menu import PhoneMenu
from twilio_manager.cli.menus.messaging_menu import MessagingMenu
from twilio_manager.cli.menus.voice_menu import VoiceMenu
from twilio_manager.cli.menus.account_menu import AccountMenu
from twilio_manager.cli.menus.advanced_menu import AdvancedMenu
from twilio_manager.cli.menus.search.search_menu import SearchMenu
from twilio_manager.cli.menus.search.search_parameters_menu import SearchParametersMenu
from twilio_manager.cli.menus.search.search_results_menu import SearchResultsMenu
from twilio_manager.cli.menus.purchase_menu import PurchaseMenu
from twilio_manager.cli.menus.configure_menu import ConfigureMenu
from twilio_manager.cli.menus.release_menu import ReleaseMenu
from twilio_manager.cli.menus.send_message_menu import SendMessageMenu
from twilio_manager.cli.menus.view_message_logs_menu import ViewMessageLogsMenu
from twilio_manager.cli.menus.delete_message_menu import DeleteMessageMenu
from twilio_manager.cli.menus.call.call_menu import CallMenu
from twilio_manager.cli.menus.call.call_confirmation_menu import CallConfirmationMenu
from twilio_manager.cli.menus.call.select_caller_menu import SelectCallerMenu
from twilio_manager.cli.menus.call.select_recipient_menu import SelectRecipientMenu
from twilio_manager.cli.menus.call.select_voice_response_menu import SelectVoiceResponseMenu
from twilio_manager.cli.menus.call.conference_menu import ConferenceMenu
from twilio_manager.cli.menus.call.recordings_menu import RecordingsMenu
from twilio_manager.cli.menus.account.account_info_menu import AccountInfoMenu
from twilio_manager.cli.menus.account.api_key_menu import ApiKeyMenu
from twilio_manager.cli.menus.account.sip_trunk_menu import SipTrunkMenu
from twilio_manager.cli.menus.account.subaccount_menu import SubaccountMenu
from twilio_manager.cli.menus.account.twiml_app_menu import TwimlAppMenu

# Menu registry for dynamic loading
menu_registry = {
    # Main menus
    "main": MainMenu,
    "phone": PhoneMenu,
    "messaging": MessagingMenu,
    "voice": VoiceMenu,
    "account": AccountMenu,
    "advanced": AdvancedMenu,
    
    # Phone number menus
    "search": SearchMenu,
    "search_parameters": SearchParametersMenu,
    "search_results": SearchResultsMenu,
    "purchase": PurchaseMenu,
    "configure": ConfigureMenu,
    "release": ReleaseMenu,
    
    # Messaging menus
    "send_message": SendMessageMenu,
    "view_messages": ViewMessageLogsMenu,
    "delete_message": DeleteMessageMenu,
    
    # Voice menus
    "call": CallMenu,
    "call_confirm": CallConfirmationMenu,
    "select_caller": SelectCallerMenu,
    "select_recipient": SelectRecipientMenu,
    "select_voice_response": SelectVoiceResponseMenu,
    "conference": ConferenceMenu,
    "recordings": RecordingsMenu,
    
    # Account menus
    "account_info": AccountInfoMenu,
    "api_keys": ApiKeyMenu,
    "sip_trunks": SipTrunkMenu,
    "subaccounts": SubaccountMenu,
    "twiml_apps": TwimlAppMenu
}

def get_menu(menu_id: str, parent=None):
    """Get a menu instance by ID.
    
    Args:
        menu_id (str): The menu ID from the registry
        parent (BaseMenu, optional): Parent menu to return to
        
    Returns:
        BaseMenu: The menu instance
        
    Raises:
        KeyError: If menu_id is not found in registry
    """
    if menu_id not in menu_registry:
        raise KeyError(f"Menu '{menu_id}' not found in registry")
    return menu_registry[menu_id](parent=parent)

def show_menu(menu_id: str, parent=None):
    """Show a menu by ID.
    
    Args:
        menu_id (str): The menu ID from the registry
        parent (BaseMenu, optional): Parent menu to return to
        
    Raises:
        KeyError: If menu_id is not found in registry
    """
    menu = get_menu(menu_id, parent)
    menu.show()