# flows/helpers/account_mgmt/voice_ivr.py

from utils.ui import console, clear_screen
from rich.console import Group
from rich.text import Text
from rich.panel import Panel
from rich.prompt import Prompt
from rich.align import Align
import urllib.parse

def handle_ivr_menu():
    clear_screen()
    console.print("[bold cyan]🤖 Interactive Voice Response (IVR)[/bold cyan]\n")

    try:
        sales_number = Prompt.ask("Enter the phone number for Sales (e.g., +1234567890)")
        support_number = Prompt.ask("Enter the phone number for Support (e.g., +1234567890)")

        twiml = f"""
<Response>
    <Gather numDigits="1" action="/process_gather" method="POST">
        <Say>Welcome to the company hotline.</Say>
        <Say>Press 1 for Sales. Press 2 for Support.</Say>
    </Gather>
    <Redirect>/process_gather</Redirect>
</Response>
""".strip()

        process_twiml = f"""
<Response>
    <Say>Connecting you now</Say>
    <Dial>
        <Number>{sales_number}</Number>
    </Dial>
</Response>
""".strip()

        alt_process_twiml = f"""
<Response>
    <Say>Connecting you now</Say>
    <Dial>
        <Number>{support_number}</Number>
    </Dial>
</Response>
""".strip()

        gather_twiml_url = "https://twimlets.com/echo?Twiml=" + urllib.parse.quote(twiml)
        sales_twiml_url = "https://twimlets.com/echo?Twiml=" + urllib.parse.quote(process_twiml)
        support_twiml_url = "https://twimlets.com/echo?Twiml=" + urllib.parse.quote(alt_process_twiml)

        content = Group(
            Text("✅ IVR Setup Complete", style="green"),
            Text(""),
            Text("[bold]Main IVR Menu URL:[/bold]"),
            Text(gather_twiml_url, style="cyan"),
            Text(""),
            Text("[bold]Use these in your app logic or assign manually:[/bold]"),
            Text(f"Option 1 → {sales_twiml_url}", style="white"),
            Text(f"Option 2 → {support_twiml_url}", style="white"),
            Text(""),
            Text("Note: You'll need to handle /process_gather manually if not using static TwiML.")
        )

        panel = Panel(content, border_style="green", padding=(1, 2))
        console.print(Align.center(panel, vertical="middle"))

    except Exception as e:
        console.print(f"[red]Error setting up IVR: {e}[/red]")

    console.input("\nPress Enter to return...")
