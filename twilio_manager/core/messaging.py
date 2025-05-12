from twilio_manager.services.messaging_service import (
    send_message_api,
    fetch_message_logs_api,
    get_recent_contacts_api
)

def send_message(from_number, to_number, body):
    try:
        return send_message_api(from_number, to_number, body)
    except Exception as e:
        print(f"[core] Messaging error: {e}")
        return False

def get_message_logs():
    try:
        return fetch_message_logs_api()
    except Exception as e:
        print(f"[core] Message log fetch error: {e}")
        return []


def get_recent_contacts(limit=10):
    """Get a list of unique recent contacts."""
    try:
        return get_recent_contacts_api(limit)
    except Exception as e:
        print(f"[core] Recent contacts fetch error: {e}")
        return []
