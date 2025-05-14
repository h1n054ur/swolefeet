from twilio_manager.cli.menus.base_menu import BaseMenu
from twilio_manager.shared.ui.styling import (
    console,
    create_table,
    print_warning,
    prompt_choice,
    STYLES
)
from twilio_manager.core.account import list_sip_trunks

class SipTrunkMenu(BaseMenu):
    def show(self):
        """Display list of SIP trunks."""
        trunks = list_sip_trunks()
        if not trunks:
            print_warning("No SIP trunks found.")
        else:
            table = create_table(
                columns=["SID", "Friendly Name", "Voice Region"],
                title="SIP Trunks"
            )
            for trunk in trunks:
                table.add_row(
                    trunk["sid"],
                    trunk["friendly_name"],
                    trunk.get("voice_region", "—"),
                    style=STYLES['data']
                )
            console.print(table)

        prompt_choice("\nPress Enter to return", choices=[""], default="")