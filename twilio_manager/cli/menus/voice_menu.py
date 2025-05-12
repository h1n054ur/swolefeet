from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from twilio_manager.cli.commands.call_command import handle_make_call_command
from twilio_manager.cli.commands.view_logs_command import handle_view_call_logs_command
# from cli.commands.recording_command import handle_manage_recordings  # Optional future
# from cli.commands.conference_command import handle_conference_calls  # Optional future

console = Console()

def show_voice_menu():
    while True:
        console.clear()
        console.print(Panel.fit("[bold cyan]📞 Voice Call Management[/bold cyan]", title="Voice Menu"))

        console.print("[bold magenta]1.[/bold magenta] 📞 Make a Call")
        console.print("[bold magenta]2.[/bold magenta] 📄 View Call Logs")
        # console.print("[bold magenta]3.[/bold magenta] 🎙 Manage Recordings")
        # console.print("[bold magenta]4.[/bold magenta] 👥 Conference Calls")
        console.print("[bold magenta]0.[/bold magenta] 🔙 Back\n")

        choice = Prompt.ask("Choose an option", choices=["1", "2", "0"], default="0")

        if choice == "1":
            handle_make_call_command()
        elif choice == "2":
            handle_view_call_logs_command()
        # elif choice == "3":
        #     handle_manage_recordings()
        # elif choice == "4":
        #     handle_conference_calls()
        elif choice == "0":
            break
