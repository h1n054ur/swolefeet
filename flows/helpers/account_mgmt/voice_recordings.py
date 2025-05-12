# flows/helpers/account_mgmt/voice_recordings.py

import webbrowser
from twilio.rest import Client
from config.settings import ACCOUNT_SID, API_KEY_SID, API_KEY_SECRET
from utils.ui import console, clear_screen
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.align import Align

client = Client(API_KEY_SID, API_KEY_SECRET, ACCOUNT_SID)

def handle_call_recordings():
    clear_screen()
    console.print("[bold cyan]📼 Call Recordings[/bold cyan]")

    try:
        recordings = client.recordings.list(limit=10)

        if not recordings:
            console.print("[yellow]No recordings found.[/yellow]")
            console.input("Press Enter to return...")
            return

        table = Table(title="Recent Recordings", header_style="bold green")
        table.add_column("Index", style="cyan", justify="right")
        table.add_column("SID", style="magenta", overflow="fold")
        table.add_column("Duration (s)", style="white")
        table.add_column("Date Created", style="white")

        sid_to_url = {}
        for i, recording in enumerate(recordings, 1):
            url = f"https://api.twilio.com{recording.uri.replace('.json', '.mp3')}"
            sid_to_url[str(i)] = url
            table.add_row(str(i), recording.sid, recording.duration or "0", str(recording.date_created.date()))

        console.print(table)

        if Confirm.ask("Would you like to open a recording in the browser?"):
            index = Prompt.ask("Enter the index number", choices=sid_to_url.keys())
            webbrowser.open(sid_to_url[index])
            console.print("[green]✅ Opened in browser.[/green]")

    except Exception as e:
        console.print(f"[red]Error fetching recordings: {e}[/red]")

    console.input("Press Enter to return...")
