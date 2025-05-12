from twilio_manager.services.messaging_service import (
    send_message_api,
    fetch_message_logs_api
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
