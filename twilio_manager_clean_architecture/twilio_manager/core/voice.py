from twilio_manager.services.voice_service import (
    make_call_api,
    fetch_call_logs_api
)

def make_call(from_number, to_number, voice_url):
    try:
        return make_call_api(from_number, to_number, voice_url)
    except Exception as e:
        print(f"[core] Call error: {e}")
        return False

def get_call_logs():
    try:
        return fetch_call_logs_api()
    except Exception as e:
        print(f"[core] Call log fetch error: {e}")
        return []
