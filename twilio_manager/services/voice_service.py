from twilio.rest import Client
from twilio_manager.shared.config import ACCOUNT_SID, AUTH_TOKEN

client = Client(ACCOUNT_SID, AUTH_TOKEN)

def make_call_api(from_number, to_number, voice_url):
    try:
        call = client.calls.create(
            to=to_number,
            from_=from_number,
            url=voice_url
        )
        return bool(call and call.sid)
    except Exception as e:
        print(f"[service] Call error: {e}")
        return False

def fetch_call_logs_api(limit=20):
    try:
        calls = client.calls.list(limit=limit)
        return [
            {
                "from": c.from_,
                "to": c.to,
                "status": c.status,
                "duration": c.duration,
                "start_time": str(c.start_time)
            } for c in calls
        ]
    except Exception as e:
        print(f"[service] Call log error: {e}")
        return []
