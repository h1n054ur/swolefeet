import os
import json

SEEN_FILE = "seen_numbers.json"

def load_seen_numbers():
    """Load previously seen numbers from a temp JSON file."""
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "r", encoding="utf-8") as f:
            try:
                return set(json.load(f))
            except json.JSONDecodeError:
                return set()
    return set()

def save_seen_numbers(numbers):
    """Save a list or set of phone numbers to disk."""
    with open(SEEN_FILE, "w", encoding="utf-8") as f:
        json.dump(list(numbers), f)

def clear_temp_file():
    """Delete the seen number tracking file if it exists."""
    if os.path.exists(SEEN_FILE):
        os.remove(SEEN_FILE)
