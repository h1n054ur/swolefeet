import json
import os

STORAGE_PATH = os.path.join(os.path.expanduser("~"), ".twilio_cli_cache.json")

def save_to_cache(key, data):
    cache = load_cache()
    cache[key] = data
    with open(STORAGE_PATH, "w") as f:
        json.dump(cache, f, indent=2)

def load_from_cache(key, default=None):
    cache = load_cache()
    return cache.get(key, default)

def load_cache():
    if not os.path.exists(STORAGE_PATH):
        return {}
    try:
        with open(STORAGE_PATH, "r") as f:
            return json.load(f)
    except Exception:
        return {}
