# flows/helpers/account_mgmt/voice_conference.py

from utils.ui import console, clear_screen
from rich.console import Group
from rich.text import Text
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.align import Align

def handle_conference_calls():
    clear_screen()

    console.print("[bold cyan]👥 Host a Conference Call[/bold cyan]\n")

    try:
        room_name = Prompt.ask("Enter a name for your conference room (letters/numbers only)").strip()

        if not room_name.isalnum():
            console.print("[red]❌ Room name must be alphanumeric.[/red]")
            console.input("Press Enter to return...")
            return

        voice_url = generate_conference_twiml_url(room_name)

        content = Group(
            Text(f"✅ Conference Room Created: {room_name}", style="green"),
            Text(""),
            Text("You can assign this URL to a Twilio number or use it in outbound calls."),
            Text(""),
            Text(f"[bold]TwiML URL:[/bold] {voice_url}", style="cyan"),
            Text(""),
            Text("🔗 When multiple people call this URL, they will join the same room."),
        )

        panel = Panel(content, border_style="green", padding=(1, 2))
        console.print(Align.center(panel, vertical="middle"))

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

    console.input("\nPress Enter to return...")

def generate_conference_twiml_url(room_name: str) -> str:
    import urllib.parse
    twiml = f"""
<Response>
    <Say>Joining conference room {room_name}</Say>
    <Dial>
        <Conference>{room_name}</Conference>
    </Dial>
</Response>
    """.strip()

    # Encode TwiML to be used in a public service like Twimlets Echo or your custom endpoint
    encoded_twiml = urllib.parse.quote(twiml)
    return f"https://twimlets.com/echo?Twiml={encoded_twiml}"
