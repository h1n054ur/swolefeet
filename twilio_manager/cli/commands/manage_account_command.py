from twilio_manager.core.account import (
    get_account_info,
    list_subaccounts,
    list_api_keys,
    list_sip_trunks,
    list_twiml_apps
)
from twilio_manager.shared.ui.styling import (
    console,
    create_table,
    print_panel,
    print_success,
    print_error,
    print_warning,
    print_info,
    prompt_choice,
    STYLES
)

def handle_view_account_info():
    """Display account information and balance."""

    info = get_account_info()
    if not info:
        print_error("Failed to retrieve account information.")
    else:
        table = create_table(columns=["Field", "Value"], title="Account Info")
        for key, value in info.items():
            table.add_row(key, str(value), style=STYLES['data'])
        console.print(table)

    prompt_choice("\nPress Enter to return", choices=[""], default="")


def handle_subaccount_management():
    """Display list of subaccounts."""

    subs = list_subaccounts()
    if not subs:
        print_warning("No subaccounts found.")
    else:
        table = create_table(columns=["SID", "Name", "Status"], title="Subaccounts")
        for sub in subs:
            table.add_row(sub["sid"], sub["friendly_name"], sub["status"], style=STYLES['data'])
        console.print(table)

    prompt_choice("\nPress Enter to return", choices=[""], default="")


def handle_api_key_management():
    """Display list of API keys."""

    keys = list_api_keys()
    if not keys:
        print_warning("No API keys found.")
    else:
        table = create_table(columns=["SID", "Friendly Name"], title="API Keys")
        for key in keys:
            table.add_row(key["sid"], key["friendly_name"], style=STYLES['data'])
        console.print(table)

    prompt_choice("\nPress Enter to return", choices=[""], default="")


def handle_sip_trunk_menu():
    """Display list of SIP trunks."""

    trunks = list_sip_trunks()
    if not trunks:
        print_warning("No SIP trunks found.")
    else:
        table = create_table(columns=["SID", "Friendly Name", "Voice Region"], title="SIP Trunks")
        for trunk in trunks:
            table.add_row(trunk["sid"], trunk["friendly_name"], trunk.get("voice_region", "—"), style=STYLES['data'])
        console.print(table)

    prompt_choice("\nPress Enter to return", choices=[""], default="")


def handle_twiml_app_menu():
    """Display list of TwiML applications."""

    apps = list_twiml_apps()
    if not apps:
        print_warning("No TwiML applications found.")
    else:
        table = create_table(columns=["SID", "Name", "Voice URL"], title="TwiML Apps")
        for app in apps:
            table.add_row(app["sid"], app["friendly_name"], app.get("voice_url", "—"), style=STYLES['data'])
        console.print(table)

    prompt_choice("\nPress Enter to return", choices=[""], default="")
