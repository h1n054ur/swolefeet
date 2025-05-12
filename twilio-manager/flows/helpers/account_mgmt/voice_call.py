# flows/helpers/account_mgmt/voice_call.py

import time
from twilio.rest import Client
from config.settings import ACCOUNT_SID, API_KEY_SID, API_KEY_SECRET
from utils.ui import console, clear_screen
from rich.console import Group
from rich.text import Text
from rich.panel import Panel
from rich.align import Align
from rich.prompt import Prompt

client = Client(API_KEY_SID, API_KEY_SECRET, ACCOUNT_SID)

def handle_outbound_call():
    clear_screen()
    
    try:
        from_number = Prompt.ask("Enter your Twilio phone number (in E.164 format, e.g. +1234567890)")
        to_number = Prompt.ask("Enter the destination number (in E.164 format)")
        twiml_url = Prompt.ask("Enter the TwiML URL to handle the call", default="http://demo.twilio.com/docs/voice.xml")

        call = client.calls.create(
            twiml=None,
            to=to_number,
            from_=from_number,
            url=twiml_url
        )

        final_states = {"completed", "failed", "no-answer", "busy", "canceled"}
        current_status = call.status

        while True:
            clear_screen()
            content = Group(
                Text("📞 Outbound Call Triggered", style="bold cyan", justify="center"),
                Text(f"Call SID: {call.sid}", style="white"),
                Text(f"To: {to_number}", style="white"),
                Text(f"From: {from_number}", style="white"),
                Text(f"Current Status: {current_status}", style="bold yellow"),
                Text(""),
                Text("🔄 Monitoring call status...", style="dim white", justify="center")
            )
            panel = Panel(content, border_style="green", padding=(1, 2))
            console.print(Align.center(panel, vertical="middle"))

            if current_status in final_states:
                break

            time.sleep(3)
            updated_call = client.calls(call.sid).fetch()
            new_status = updated_call.status
            if new_status != current_status:
                current_status = new_status

        # Show final result inside the panel
        clear_screen()
        final_content = Group(
            Text("📞 Outbound Call Completed", style="bold cyan", justify="center"),
            Text(f"Call SID: {call.sid}", style="white"),
            Text(f"To: {to_number}", style="white"),
            Text(f"From: {from_number}", style="white"),
            Text(f"Final Status: {current_status}", style="bold green"),
            Text(""),
            Text("✅ Call flow completed. Press Enter to return...", style="white", justify="center")
        )
        final_panel = Panel(final_content, border_style="green", padding=(1, 2))
        console.print(Align.center(final_panel, vertical="middle"))

    except Exception as e:
        console.print(f"[red]Error placing outbound call: {e}[/red]")

    console.input()
