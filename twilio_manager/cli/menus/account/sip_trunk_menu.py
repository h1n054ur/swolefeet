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
    def __init__(self, parent=None):
        super().__init__(parent)
        self.sip_trunks = None

    def show(self):
        """Display list of SIP trunks."""
        self.sip_trunks = list_sip_trunks()
        if not self.sip_trunks:
            self.print_warning("No SIP trunks found.")
            self.pause_and_return()
            return

        self._display_sip_trunks()
        options = {"0": "Return to menu"}
        self.display(
            title="SIP Trunks",
            emoji="📞",
            options=options
        )

    def _display_sip_trunks(self):
        """Display SIP trunks in a table."""
        table = create_table(
            columns=["SID", "Friendly Name", "Voice Region"],
            title="SIP Trunks"
        )
        for trunk in self.sip_trunks:
            table.add_row(
                trunk["sid"],
                trunk["friendly_name"],
                trunk.get("voice_region", "—"),
                style=STYLES['data']
            )
        console.print(table)

    def handle_choice(self, choice):
        """Handle menu selection."""
        self.return_to_parent()