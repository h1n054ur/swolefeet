from twilio_manager.cli.menus.base_menu import BaseMenu
from twilio_manager.shared.ui.styling import (
    console,
    create_table,
    print_warning,
    prompt_choice,
    STYLES
)
from twilio_manager.core.account import list_twiml_apps

class TwimlAppMenu(BaseMenu):
    def show(self):
        """Display list of TwiML applications."""
        apps = list_twiml_apps()
        if not apps:
            print_warning("No TwiML applications found.")
        else:
            table = create_table(
                columns=["SID", "Name", "Voice URL"],
                title="TwiML Apps"
            )
            for app in apps:
                table.add_row(
                    app["sid"],
                    app["friendly_name"],
                    app.get("voice_url", "—"),
                    style=STYLES['data']
                )
            console.print(table)

        prompt_choice("\nPress Enter to return", choices=[""], default="")