# utils/common.py

import platform
import time
from colorama import init as colorama_init
from utils.ui import console, print_error


def setup_cross_platform():
    """Initialize terminal settings for Windows, and give a user tip."""
    if platform.system() == "Windows":
        colorama_init(autoreset=True)
        console.print(
            "[bold green]💡 Tip:[/] For best experience, use [cyan]Windows Terminal[/cyan] "
            "with [italic]Cascadia Code[/italic] or [italic]Consolas[/italic] font.\n"
        )


def get_validated_choice(prompt_text, options):
    """
    Prompt user until they enter a valid option from a list.
    :param prompt_text: Input message
    :param options: List of accepted values
    """
    while True:
        choice = console.input(f"{prompt_text} ").strip().lower()
        if choice in options:
            return choice
        print_error(f"Invalid choice. Choose from: {', '.join(options)}.")


def get_validated_int(prompt_text, min_val, max_val):
    """
    Prompt user for an integer between min and max.
    """
    while True:
        try:
            value = int(console.input(f"{prompt_text} ").strip())
            if min_val <= value <= max_val:
                return value
            raise ValueError
        except ValueError:
            print_error(f"Enter a number between {min_val} and {max_val}.")


def wait_with_dots(message, duration=2):
    """
    Print a message and show dots while waiting.
    """
    console.print(f"{message}", end="", style="cyan")
    for _ in range(duration * 2):
        time.sleep(0.5)
        console.print(".", end="")
    console.print()


def is_windows():
    """Check if running on Windows."""
    return platform.system().lower() == "windows"
